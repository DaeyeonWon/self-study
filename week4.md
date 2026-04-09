---
layout: default
title: 4주차. Embedding Models & Representation Learning for Retrieval
---

# 4주차: Embedding Models & Representation Learning for Retrieval
> 데이터를 벡터로 변환하는 임베딩 모델의 선택과 평가

임베딩 모델은 텍스트의 의미를 고차원 실수 벡터로 변환합니다. 이 벡터 공간에서 의미적으로 유사한 텍스트는 가까운 거리에 위치하게 됩니다. 임베딩 모델의 선택은 RAG 시스템의 검색 품질과 직결됩니다.

---

## 1. Dense vs Sparse 임베딩

### 이론 설명

**Sparse (희소 벡터):** BM25, TF-IDF 기반. 어휘 사전 크기만큼의 차원을 가지며 대부분 0으로 채워짐. 정확한 키워드 매칭이 강점.

**Dense (밀집 벡터):** 신경망 기반. 고정된 차원(예: 1536)으로 의미를 압축. "자동차"와 "차량"처럼 다른 단어라도 유사한 의미면 높은 유사도.

### PDF 원본 자료

<img src="assets/images_new/Fig_4_2_page_60.png" width="600">

*Fig 4.2: Dense 임베딩 공간에서 텍스트의 의미적 군집화 시각화 — 유사한 개념들이 공간적으로 근접 배치됨 (PDF p.60)*

### 예시

```
Sparse (BM25):
  "사과"  → [0, 0, 1, 0, 0, ...] (5만 차원 중 '사과' 위치만 1)
  "배"    → [0, 0, 0, 1, 0, ...] (완전히 다른 위치 → 유사도 0)

Dense (임베딩):
  "사과"  → [0.23, -0.81, 0.45, ...]  (1536 차원 밀집 벡터)
  "배"    → [0.19, -0.76, 0.41, ...]  (유사한 값 → 코사인 유사도 높음)
  → 과일 개념으로 유사하게 인식
```

---

## 2. 모델 선택 기준: MTEB 벤치마크 활용

### 이론 설명

**MTEB (Massive Text Embedding Benchmark)**: 56개의 데이터셋, 8개 태스크 카테고리에 걸쳐 임베딩 모델 성능을 종합 평가하는 표준 벤치마크.

**주요 선택 기준:**
1. **MTEB 점수**: 전반적 성능 지표 (높을수록 우수)
2. **벡터 차원**: 768 / 1024 / 1536 차원 → 높을수록 성능↑, 저장 비용↑
3. **최대 토큰 수**: 512~8192 토큰
4. **다국어 지원**: 한국어 포함 여부
5. **API 비용 vs 로컬 구동**: 클라우드 API vs 자체 서버 배포

### PDF 원본 자료

<img src="assets/images_new/Table_4_3_page_83.png" width="600">

*Table 4.3: 주요 임베딩 모델 성능 및 비용 비교표 (PDF p.83)*

---

## 3. Multi-Vector 임베딩: ColBERT

### 이론 설명

기존 Dense 임베딩은 문서 전체를 단 **하나의 벡터**로 압축합니다. 이 과정에서 세부 정보가 손실됩니다. ColBERT는 각 토큰마다 개별 벡터를 생성하고, **쿼리의 각 토큰과 문서의 각 토큰 간의 최대 유사도(MaxSim)를 합산**하여 점수를 계산합니다.

### 관련 논문

**📄 ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT (Khattab & Zaharia, Stanford, 2020)**
- 기존 BERT 기반 Cross-Encoder 대비 100배 빠른 검색 속도 달성
- MS MARCO 데이터셋에서 Dense Retrieval보다 최대 5% 높은 MRR@10
- **핵심 아이디어**: 쿼리와 문서를 따로 인코딩하되(Bi-Encoder), 최종 점수 계산은 토큰 수준에서 수행(Late Interaction)

### 아키텍처 다이어그램

<br>
<img src="assets/images_new/mermaid_w4_0.png" width="80%" style="margin: 10px 0; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); background-color: white; padding: 10px;">
<br>

---

## 4. Matryoshka Representation Learning (MRL)

### 이론 설명

러시아 전통 인형 마트료시카처럼, 고차원 벡터의 앞부분만 잘라내도 성능이 크게 유지되도록 **다차원 동시 훈련**하는 기법입니다. 1536차원의 벡터에서 앞 256차원만 사용해도 전체 차원 성능의 약 90%를 유지합니다.

### 관련 논문

**📄 Matryoshka Representation Learning (Kusupati et al., Google Research, 2022)**
- OpenAI `text-embedding-3-large` / `text-embedding-3-small` 모델에 채택된 핵심 기법
- 벡터 차원을 1/6로 줄여도 성능 손실 10% 미만 달성
- **실무 가치**: 벡터 DB 스토리지 비용을 최대 80% 절감하면서 검색 성능 유지 가능

---

## 5. NVIDIA 10-K 사례 연구 워크플로우 (PDF p.69-77)

### 이론 설명

다양한 임베딩 모델의 실제 성능을 NVIDIA 연간 보고서(10-K) 데이터를 사용하여 비교하는 실증 평가 방법론입니다.

평가 지표:
- **Attribution**: 검색된 문서가 실제 답변 생성에 기여했는가
- **Adherence**: 생성된 답변이 검색 문서의 내용에 충실한가 (환각 없음)

---

## 💻 구현: 임베딩 모델 비교 및 활용

### 관련 프레임워크

| 라이브러리 | 특징 | 지원 모델 |
|-----------|------|----------|
| **sentence-transformers** | 오픈소스, 로컬 실행 | BGE, E5, MPNet 등 |
| **openai** | API, 최고 성능 | text-embedding-3-small/large |
| **cohere** | 다국어 특화 | embed-multilingual-v3 |
| **llama-index** | 다양한 임베딩 통합 | 거의 모든 모델 |

### 클라우드 서비스

| 서비스 | 모델 | 특징 |
|--------|------|------|
| **OpenAI API** | text-embedding-3-large (3072d) | 최고 성능, MRL 지원 |
| **Azure OpenAI** | text-embedding-ada-002 | 엔터프라이즈 SLA 보장 |
| **Cohere Embed** | embed-multilingual-v3 | 한국어 포함 100개 언어 |
| **AWS Bedrock** | Titan Embeddings, Cohere | 완전관리형 |
| **HuggingFace Inference API** | BGE-M3, E5-large | 오픈소스 모델 클라우드 호스팅 |

### 코드 샘플 1: OpenAI Embedding (API 기반)

```python
from openai import OpenAI
import numpy as np

client = OpenAI()

def get_openai_embedding(text: str, dimensions: int = 1536) -> list[float]:
    """
    OpenAI text-embedding-3-large를 사용한 임베딩 생성
    MRL 지원: dimensions 파라미터로 차원 조정 가능 (256 ~ 3072)
    """
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=text,
        dimensions=dimensions  # MRL: 작은 차원으로 비용 절감 가능
    )
    return response.data[0].embedding

# 코사인 유사도 계산
def cosine_similarity(vec1: list, vec2: list) -> float:
    v1, v2 = np.array(vec1), np.array(vec2)
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

# 의미 검색 테스트
query = "NVIDIA의 2023년 데이터센터 매출"
documents = [
    "NVIDIA 데이터센터 부문은 2023 회계연도에 약 150억 달러의 매출을 기록했습니다.",
    "오늘 서울의 날씨는 맑으며 최고 기온은 24도입니다.",
    "AMD의 MI300X GPU는 AI 학습 시장에서 NVIDIA A100과 경쟁합니다."
]

query_emb = get_openai_embedding(query)
doc_embs = [get_openai_embedding(doc) for doc in documents]

scores = [(doc, cosine_similarity(query_emb, emb))
          for doc, emb in zip(documents, doc_embs)]
scores.sort(key=lambda x: x[1], reverse=True)

print("의미 검색 결과 (유사도 순):")
for doc, score in scores:
    print(f"  [{score:.4f}] {doc[:50]}...")
```

### 코드 샘플 2: BGE-M3 로컬 임베딩 (오픈소스)

```python
from sentence_transformers import SentenceTransformer
import torch

# BAAI/BGE-M3: 다국어 + Dense + Sparse + Multi-Vector 지원
# MTEB 다국어 리더보드 상위권 모델
model = SentenceTransformer("BAAI/bge-m3", device="cuda" if torch.cuda.is_available() else "cpu")

# 한국어 / 영어 혼합 문서 인코딩
texts = [
    "RAG 시스템의 핵심은 정확한 문서 검색에 있습니다.",
    "The core of RAG systems lies in accurate document retrieval.",
    "今日の天気は晴れです。"  # 일본어
]

# normalize_embeddings=True: 코사인 유사도 최적화를 위해 L2 정규화
embeddings = model.encode(
    texts,
    normalize_embeddings=True,
    batch_size=32,
    show_progress_bar=True
)

print(f"임베딩 차원: {embeddings.shape}")  # (3, 1024)

# 한국어-영어 교차 언어 유사도 (다국어 모델 성능 테스트)
from sentence_transformers.util import cos_sim
score = cos_sim(embeddings[0], embeddings[1])
print(f"한-영 교차 유사도: {score.item():.4f}")  # 높으면 다국어 이해 우수
```

### 코드 샘플 3: 임베딩 모델 성능 비교 워크플로우

```python
"""
NVIDIA 10-K 스타일의 임베딩 모델 평가 워크플로우
Attribution(검색 기여도) 및 Adherence(팩트 충실도) 측정
"""
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.evaluation import load_evaluator

def evaluate_embedding_model(model_name: str, docs: list, qa_pairs: list) -> dict:
    """
    모델별 RAG 성능 평가
    qa_pairs: [(question, ground_truth_answer), ...]
    """
    # 임베딩 모델로 인덱스 구성
    if "openai" in model_name:
        embeddings = OpenAIEmbeddings(model=model_name)
    else:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        embeddings = HuggingFaceEmbeddings(model_name=model_name)

    vectorstore = FAISS.from_texts(docs, embedding=embeddings)

    # LLM-as-Judge 평가
    judge_llm = ChatOpenAI(model="gpt-4o", temperature=0)
    evaluator = load_evaluator("qa", llm=judge_llm)

    results = []
    for question, ground_truth in qa_pairs:
        # 검색
        retrieved = vectorstore.similarity_search(question, k=3)
        context = "\n".join([d.page_content for d in retrieved])

        # 생성
        answer = judge_llm.invoke(f"컨텍스트: {context}\n질문: {question}").content

        # 평가
        eval_result = evaluator.evaluate_strings(
            input=question, prediction=answer, reference=ground_truth
        )
        results.append(eval_result)

    accuracy = sum(1 for r in results if r["score"] == 1) / len(results)
    return {"model": model_name, "accuracy": accuracy}

# 모델 비교 실행
models = ["text-embedding-3-small", "text-embedding-3-large"]
# 실제 실행 시 qa_pairs와 docs를 NVIDIA 10-K 데이터로 교체
```

---

다음 주차 → [5주차: Vector Databases & Retrieval Architecture Design](week5.md)
