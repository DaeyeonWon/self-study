---
layout: default
title: 6주차. Reranking Models and Hybrid Retrieval Techniques
---

# 6주차: Reranking Models and Hybrid Retrieval Techniques
> 검색 결과의 순위 재조정을 통한 답변 품질 혁신

벡터 검색만으로는 충분하지 않습니다. 코사인 유사도 기반의 초기 검색(Bi-Encoder)은 속도를 위해 정확도를 일부 희생합니다. Reranking은 초기 검색의 Top-K 결과를 **훨씬 정교한 모델로 재평가하여 순위를 재조정**하는 2단계 검색 아키텍처입니다.

---

## 1. 리랭커의 역할과 필요성

### 이론 설명

**초기 검색(1st Stage)**: 빠른 Bi-Encoder → 수백만 문서 중 Top-100 후보 선별 (밀리초 단위)  
**리랭킹(2nd Stage)**: 정밀한 Cross-Encoder → Top-100 중 최적 Top-5 선별 (초 단위)

리랭커는 쿼리와 문서를 **함께 인식**하여 양방향 어텐션을 수행하므로, Bi-Encoder 대비 훨씬 정확한 관련성 점수를 산출합니다.

### PDF 원본 자료

<img src="assets/images_new/Fig_4_4_page_94.png" width="600">

*Fig 4.4: 리랭킹 파이프라인 — 초기 검색(Top-K)과 Cross-Encoder 리랭킹의 2단계 아키텍처 (PDF p.94)*

<img src="assets/images_new/Table_4_4_page_97.png" width="600">

*Table 4.4: 다양한 리랭커 모델 성능 비교표 (PDF p.97)*

---

## 2. Cross-Encoder 리랭커

### 이론 설명

Cross-Encoder는 쿼리와 문서를 하나의 시퀀스로 연결하여 트랜스포머에 입력합니다. 결과적으로 모든 토큰 간 어텐션이 가능해져 **관련성 판단 정확도가 극적으로 향상**됩니다.

**Bi-Encoder vs Cross-Encoder:**
```
Bi-Encoder: 
  encode(query) → q_vec
  encode(document) → d_vec
  score = cosine(q_vec, d_vec)  ← 각각 독립 인코딩

Cross-Encoder:
  encode([query] + [SEP] + [document]) → score
  ← 쿼리와 문서가 상호 참조하며 통합 인코딩
```

### 관련 논문

**📄 Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks (Reimers & Gurevych, 2019)**
- Bi-Encoder 구조로 BERT를 문장 임베딩에 최적화한 핵심 논문
- Cross-Encoder가 Bi-Encoder 대비 MNLI/STS 벤치마크에서 평균 3~5% 정확도 우위임을 실증

**📄 MS-MARCO Passage Ranking with Cross-Encoders (Nogueira & Cho, 2019)**
- Cross-Encoder를 리랭킹에 적용하여 MRR@10을 30% 이상 향상
- 2-Stage 파이프라인(BM25 검색 → BERT 리랭킹)의 효과를 최초 체계적으로 증명

### 아키텍처 다이어그램

<br>
<img src="assets/images_new/mermaid_w6_0.png" width="80%" style="margin: 10px 0; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); background-color: white; padding: 10px;">
<br>

---

## 3. LLM 기반 Reranking

### 이론 설명

전문 리랭커 모델 없이 일반 LLM을 관련성 평가 판사로 활용하는 방법입니다.

**3가지 방식:**
- **Pointwise**: 각 문서를 독립적으로 0~10점 채점
- **Listwise**: 전체 문서 목록을 한 번에 주고 순위 결정 요청
- **Pairwise**: 두 문서씩 비교하여 어떤 것이 더 관련 있는지 판단 (토너먼트식)

### 관련 논문

**📄 Large Language Models are Effective Text Rankers with Pairwise Ranking Prompting (Qin et al., 2023)**
- GPT-4의 Pairwise 방식이 전문 리랭커 모델(monoT5)과 동등하거나 우수한 성능
- **한계**: LLM 호출 비용과 레이턴시가 높음 → Top-20 이내 후보에만 적용 권장

### PDF 원본 자료

<img src="assets/images_new/Table_6_1_page_156.png" width="600">

*Table 6.1: Pointwise / Listwise / Pairwise 리랭킹 방식 성능 및 비용 비교표 (PDF p.156)*

<img src="assets/images_new/Table_6_2_page_157.png" width="600">

*Table 6.2: 리랭킹 모델별 NDCG 성능 측정 결과 (PDF p.157)*

<img src="assets/images_new/Table_6_3_page_157.png" width="600">

*Table 6.3: 리랭킹 신뢰도 및 레이턴시 종합 분석 (PDF p.157)*

---

## 4. Hybrid Search: Dense + Sparse 결합

### 이론 설명

Dense(의미 검색)와 Sparse(키워드 검색)는 각각 다른 강점을 가집니다. 두 결과를 **RRF(Reciprocal Rank Fusion)** 또는 **가중 평균**으로 통합하면 각각의 약점을 보완할 수 있습니다.

**RRF 공식:**
```
RRF_score(d) = Σ 1 / (k + rank_i(d))
여기서 k=60 (상수), rank_i(d)는 i번째 검색 시스템에서 문서 d의 순위
```

### 관련 논문

**📄 Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods (Cormack et al., 2009)**
- 여러 랭킹 시스템을 단순 RRF로 결합하면 개별 최고 시스템보다 성능 향상
- 복잡한 학습 없이 구현 가능한 ensemble 기법

---

## 5. HyDE (Hypothetical Document Embeddings)

### 이론 설명

짧은 키워드나 모호한 쿼리는 벡터 검색에 불리합니다. HyDE는 **LLM을 사용하여 가상의 답변 문서를 먼저 생성**하고, 이 가상 문서를 쿼리 대신 임베딩하여 검색합니다.

### 관련 논문

**📄 Precise Zero-Shot Dense Retrieval without Relevance Labels (Gao et al., 2022)**
- HyDE가 BM25와 유사하거나 더 우수한 Zero-Shot 검색 성능 달성
- 쿼리가 짧거나 추상적일 때 특히 효과적
- **단점**: LLM 호출 추가로 레이턴시 50~200ms 증가

---

## 6. Recursive Retrieval (반복 검색)

### 이론 설명

Small2Big 패턴: 세밀한 청크로 검색하고, 발견된 청크의 **부모 문서(큰 컨텍스트)**를 LLM에 제공하는 방식입니다.

**흐름:**
1. 작은 청크(128 token)로 정밀 검색
2. 발견된 청크의 부모 노드(512 token) 또는 전체 페이지를 실제 컨텍스트로 반환
3. LLM에는 풍부한 컨텍스트를 제공하면서, 검색 정밀도도 유지

---

## 💻 구현: 리랭킹 파이프라인 실습

### 관련 프레임워크 및 라이브러리

| # | 라이브러리 / 서비스 | 특징 |
|---|-----------|------|
| 1 | **sentence-transformers CrossEncoder** | 가장 간편한 Cross-Encoder API, 다양한 사전학습 모델 |
| 2 | **Cohere Rerank API** | 클라우드 리랭킹, 한국어 포함 100개 언어 지원 |
| 3 | **FlashRank** | 경량 로컬 리랭커, ONNX 기반, 지연 최소화 |
| 4 | **RankGPT** | GPT-4 기반 Listwise/Pairwise 리랭킹 구현체 |
| 5 | **FlagEmbedding BGE-Reranker** | BAAI 공식 리랭커, bge-reranker-v2-m3 (다국어) |
| 6 | **Jina Reranker** | 8192 토큰, 다국어, API+로컬 모두 가능 |
| 7 | **rank_bm25** | 순수 Python BM25 구현, Sparse 검색 베이스라인 |
| 8 | **LangChain EnsembleRetriever** | BM25+Dense 하이브리드 RRF 결합 내장 |
| 9 | **ColBERT (Stanford)** | 토큰 레벨 Late Interaction, 초정밀 검색+리랭킹 |
| 10 | **RAGatouille** | ColBERTv2 래퍼, 간편한 fine-tuning 및 검색 API |
| 11 | **LiteLLM** | 여러 LLM 프로바이더 통합 인터페이스, LLM 리랭킹용 |
| 12 | **Voyager Reranker (Voyage AI)** | 코드·법률 도메인별 특화 리랭킹 모델 |
| 13 | **Infinity (michaelfeil)** | 임베딩+리랭킹 통합 추론 서버, 배치 최적화 |

### 클라우드 서비스

| 서비스 | 제공사 | 특징 |
|--------|--------|------|
| **Cohere Rerank** | Cohere | command-r-plus 기반, 100개 언어 |
| **Azure AI Search Semantic Ranker** | Microsoft | BERT 기반 의미 재랭킹 내장 |
| **Amazon Kendra** | AWS | 완전 관리형 의미 검색 및 리랭킹 |
| **Jina Reranker API** | Jina AI | 8192 토큰, 다국어 지원 |

### 코드 샘플 1: BGE Cross-Encoder 리랭킹

```python
from sentence_transformers import CrossEncoder
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Cross-Encoder 로드 (BAAI/bge-reranker-v2-m3: 다국어 지원, MTEB 1위권)
reranker = CrossEncoder("BAAI/bge-reranker-v2-m3", max_length=512)

def two_stage_retrieval(query: str, vectorstore, top_k_retrieve=20, top_k_final=5):
    """
    2단계 검색: Dense 검색(1단계) → Cross-Encoder 리랭킹(2단계)
    """
    # 1단계: Dense 검색으로 Top-20 후보 수집
    candidates = vectorstore.similarity_search(query, k=top_k_retrieve)
    
    # 2단계: Cross-Encoder 리랭킹
    pairs = [(query, doc.page_content) for doc in candidates]
    scores = reranker.predict(pairs)
    
    # 점수 기준 내림차순 정렬
    ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
    
    print(f"리랭킹 전 Top-3:")
    for i, doc in enumerate(candidates[:3]):
        print(f"  {i+1}. {doc.page_content[:60]}...")
    
    print(f"\n리랭킹 후 Top-3:")
    for i, (doc, score) in enumerate(ranked[:3]):
        print(f"  {i+1}. [{score:.3f}] {doc.page_content[:60]}...")
    
    return [doc for doc, _ in ranked[:top_k_final]]
```

### 코드 샘플 2: Hybrid Search (BM25 + Dense) with RRF

```python
from langchain_community.retrievers import BM25Retriever
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.retrievers import EnsembleRetriever

# 문서 준비
texts = [
    "NVIDIA A100 GPU는 80GB HBM2e 메모리를 탑재합니다.",
    "대규모 언어 모델 학습에는 고성능 GPU 클러스터가 필요합니다.",
    "오늘 날씨가 맑고 기온이 상쾌합니다.",
    "GPT-4는 OpenAI가 개발한 대형 언어 모델입니다.",
]
from langchain_core.documents import Document
documents = [Document(page_content=t) for t in texts]

# BM25 검색기 (Sparse)
bm25_retriever = BM25Retriever.from_documents(documents, k=4)

# Dense 검색기
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(documents, embeddings)
dense_retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# Hybrid: RRF 방식으로 두 검색 결과 통합 (weights: 가중치 [BM25, Dense])
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, dense_retriever],
    weights=[0.3, 0.7]  # Dense에 더 높은 가중치
)

results = ensemble_retriever.invoke("NVIDIA GPU 메모리 용량은?")
print("Hybrid 검색 결과:")
for r in results:
    print(f"  - {r.page_content}")
```

### 코드 샘플 3: HyDE 구현

```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
embeddings = OpenAIEmbeddings()

hyde_prompt = PromptTemplate(
    input_variables=["question"],
    template="""다음 질문에 대한 가상의 전문적인 답변 문서를 2~3문장으로 작성하십시오.
실제 사실이 아니어도 됩니다. 검색에 활용될 예시 답변입니다.

질문: {question}
가상 답변 문서:"""
)

def hyde_search(query: str, vectorstore, k: int = 5):
    """HyDE: 가상 문서 생성 후 임베딩하여 검색"""
    # 1. 가상 답변 문서 생성
    hyde_chain = hyde_prompt | llm
    hypothetical_doc = hyde_chain.invoke({"question": query}).content
    print(f"생성된 가상 문서: {hypothetical_doc[:100]}...")
    
    # 2. 가상 문서를 임베딩하여 검색 (원래 쿼리 대신)
    results = vectorstore.similarity_search(hypothetical_doc, k=k)
    return results

# NDCG 성능 측정 예시
def calculate_ndcg(ranked_docs: list, relevant_docs: set, k: int = 5) -> float:
    """NDCG@K 계산"""
    import math
    dcg = 0.0
    for i, doc in enumerate(ranked_docs[:k], 1):
        if doc.page_content in relevant_docs:
            dcg += 1.0 / math.log2(i + 1)
    
    # IDCG: 이상적인 DCG (모든 관련 문서가 상위에 있을 때)
    ideal_hits = min(len(relevant_docs), k)
    idcg = sum(1.0 / math.log2(i + 1) for i in range(1, ideal_hits + 1))
    
    return dcg / idcg if idcg > 0 else 0.0
```

---

다음 주차 → [7주차: Knowledge Graph RAG & Graph-based Retrieval Systems](week7.md)
