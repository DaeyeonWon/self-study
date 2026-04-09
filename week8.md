---
layout: default
title: 8주차. RAG Evaluation, Monitoring & Optimization
---

# 8주차: RAG Evaluation, Monitoring & Optimization
> 실전 배포를 위한 품질 평가 및 지속적 관찰 파이프라인

RAG 시스템을 구축했다고 끝이 아닙니다. **"이 시스템이 얼마나 정확한가?"를 정량적으로 증명**하고, 실운영 환경에서 지속적으로 품질을 모니터링하며 최적화하는 것이 엔지니어링의 마무리입니다.

---

## 1. 배포 전 테스트 시나리오

### 이론 설명

배포 전 다양한 극한 시나리오에서 시스템을 평가하여 약점을 사전에 발견해야 합니다.

### PDF 원본 자료

<img src="assets/images_new/Fig_5_1_page_136.png" width="600">

*Fig 5.1: RAG 평가 테스트 시나리오 전체 분류 체계 (PDF p.136)*

<img src="assets/images_new/Fig_5_2_page_137.png" width="600">
<img src="assets/images_new/Fig_5_3_page_137.png" width="600">

*Fig 5.2-5.3: 검색 품질(Relevance, Preciseness) 평가 시나리오 예시 (PDF p.137)*

**핵심 테스트 시나리오:**

**① 검색 품질 (Retrieval Quality)**
- **Relevance**: 검색된 문서가 질문과 주제적으로 관련 있는가
- **Preciseness**: 검색 결과에 불필요한 정보가 포함되어 있지 않은가

**② 신뢰성 테스트 (Reliability)**
- **Noise Robustness**: 관련 없는 문서를 의도적으로 포함시켜도 정확한 답변을 하는가
- **Negative Rejection**: DB에 답이 없을 때 "모른다"고 올바르게 거부하는가

**③ 보안·브랜드 안전성 (Safety)**
- **Privacy Breaches**: PII(개인 식별 정보) 노출 없이 응답하는가
- **Malicious Use**: 프롬프트 인젝션 공격에 저항하는가
- **Brand Safety**: 톤앤매너를 유지하며 유해 콘텐츠를 생성하지 않는가

### PDF 원본 자료

<img src="assets/images_new/Fig_5_4_page_138.png" width="600">
<img src="assets/images_new/Fig_5_5_page_139.png" width="600">
<img src="assets/images_new/Fig_5_6_page_140.png" width="600">
<img src="assets/images_new/Fig_5_7_page_141.png" width="600">
<img src="assets/images_new/Fig_5_8_page_142.png" width="600">
<img src="assets/images_new/Fig_5_9_page_142.png" width="600">
<img src="assets/images_new/Fig_5_10_page_143.png" width="600">
<img src="assets/images_new/Fig_5_11_page_143.png" width="600">
<img src="assets/images_new/Fig_5_12_page_144.png" width="600">
<img src="assets/images_new/Fig_5_13_page_144.png" width="600">
<img src="assets/images_new/Fig_5_14_page_145.png" width="600">
<img src="assets/images_new/Fig_5_15_page_146.png" width="600">
<img src="assets/images_new/Fig_5_16_page_147.png" width="600">
<img src="assets/images_new/Fig_5_17_page_147.png" width="600">
<img src="assets/images_new/Fig_5_18_page_148.png" width="600">
<img src="assets/images_new/Fig_5_19_page_149.png" width="600">
<img src="assets/images_new/Fig_5_20_page_150.png" width="600">
<img src="assets/images_new/Fig_5_21_page_150.png" width="600">
<img src="assets/images_new/Fig_5_22_page_151.png" width="600">

*Fig 5.4-5.22: 배포 전 전체 테스트 시나리오 — Noise Robustness/Negative Rejection/Privacy/Malicious Use/Toxicity 등 각 시나리오별 평가 기준 및 예시 (PDF p.138-151)*

---

## 2. 핵심 평가 지표와 RAGAS 프레임워크

### 이론 설명

**RAGAS(RAG Assessment)**: RAG 파이프라인을 자동으로 평가하는 오픈소스 프레임워크로, LLM-as-a-Judge 방식을 이용하여 다음 4가지 핵심 지표를 측정합니다.

| 지표 | 측정 대상 | 계산 방법 |
|------|---------|---------|
| **Faithfulness** | 답변이 컨텍스트에 근거하는가 (환각 없음) | 답변의 각 주장이 컨텍스트에 존재하는 비율 |
| **Answer Relevance** | 답변이 질문에 적절한가 | 역생성 질문과 원래 질문의 임베딩 유사도 |
| **Context Precision** | 검색된 컨텍스트 중 관련 있는 비율 | 관련 청크 수 / 전체 검색 청크 수 |
| **Context Recall** | 필요한 정보가 충분히 검색되었는가 | 정답 커버리지 측정 |

### 관련 논문

**📄 RAGAS: Automated Evaluation of Retrieval Augmented Generation (Es et al., 2023)**
- Human 평가와의 높은 상관관계(Spearman ρ=0.72) 입증
- LLM-as-a-Judge 방식으로 레이블 없이 자동 평가 가능
- Faithfulness 지표가 인간의 환각 감지와 가장 높은 일치도를 보임

**📄 ARES: An Automated Evaluation Framework for RAG Systems (Saad-Falcon et al., Stanford, 2023)**
- 소량의 레이블 데이터로 도메인 특화 평가 모델 학습
- RAGAS 대비 도메인 특화 태스크에서 더 높은 정확도

---

## 3. 모니터링 및 관측 가능성 (Observability)

### 이론 설명

실운영 환경에서는 **LLM 파이프라인의 각 단계를 실시간으로 추적**해야 합니다.

**핵심 모니터링 지표:**
- **Context Adherence**: 답변의 각 문장이 검색된 컨텍스트에 근거하는 비율
- **Completeness**: 사용자 질문의 모든 하위 요소에 답변했는가
- **Latency**: 각 파이프라인 단계별 처리 시간
- **Cost**: API 호출 비용 추적 (토큰 수 × 단가)
- **PII Detection**: 개인정보 노출 여부 실시간 감지

### PDF 원본 자료

<img src="assets/images_new/Fig_6_1_page_153.png" width="600">

*Fig 6.1: Galileo Observe — 실시간 리트리벌 체인 트레이스 대시보드, 각 컴포넌트 레이턴시와 비용 추적 화면 (PDF p.153)*

<img src="assets/images_new/Fig_6_2_page_158.png" width="600">
<img src="assets/images_new/Fig_6_3_page_159.png" width="600">
<img src="assets/images_new/Fig_6_4_page_159.png" width="600">
<img src="assets/images_new/Fig_6_5_page_160.png" width="600">
<img src="assets/images_new/Fig_6_6_page_160.png" width="600">
<img src="assets/images_new/Fig_6_7_page_161.png" width="600">
<img src="assets/images_new/Fig_6_8_page_161.png" width="600">
<img src="assets/images_new/Fig_6_9_page_162.png" width="600">

*Fig 6.2-6.9: 모니터링 대시보드 — Context Adherence, Completeness, PII 감지, 비용 추적 지표 화면들 (PDF p.158-162)*

---

## 4. 최적화 사례 연구 (PDF p.184-188)

### 이론 설명

실제 프로덕션 환경에서 측정된 최적화 결과를 통해 각 컴포넌트 튜닝의 효과를 검증합니다.

### PDF 원본 자료

<img src="assets/images_new/Fig_7_20_page_184.png" width="600">
<img src="assets/images_new/Fig_7_21_page_184.png" width="600">
<img src="assets/images_new/Fig_7_22_page_185.png" width="600">
<img src="assets/images_new/Fig_7_23_page_185.png" width="600">
<img src="assets/images_new/Fig_7_24_page_186.png" width="600">
<img src="assets/images_new/Fig_7_25_page_187.png" width="600">
<img src="assets/images_new/Fig_7_26_page_187.png" width="600">
<img src="assets/images_new/Fig_7_27_page_188.png" width="600">

*Fig 7.20-7.27: 컴포넌트별 최적화 전후 성능 비교 그래프 — 임베딩 모델 교체, Chunking 방식 변경, Top-K 튜닝 결과 (PDF p.184-188)*

**주요 최적화 결과:**

| 최적화 내용 | 효과 |
|------------|------|
| 임베딩 모델 교체 (ada-002 → text-embedding-3-large) | Adherence +15% |
| Fixed-size → Recursive Chunking 전환 | Context Recall +12% |
| Top-K 100 → 5 (리랭커 도입 후) | **비용 23% 절감, 레이턴시 22% 단축** |
| Binary Quantization 적용 | 스토리지 비용 60% 절감, 검색속도 25% 향상 |

---

## 💻 구현: RAGAS 자동 평가 + LangSmith 모니터링

### 관련 프레임워크

| 라이브러리 | 특징 |
|-----------|------|
| **RAGAS** | RAG 전용 자동 평가 프레임워크, LLM-as-Judge |
| **TruLens** | RAG 트리아드(Groundedness, Relevance) 평가 |
| **LangSmith** | LangChain 기반 파이프라인 트레이싱·모니터링 |
| **Phoenix (Arize)** | 오픈소스 LLM 관측 가능성 플랫폼 |
| **ARES** | 레이블 기반 도메인 특화 평가 |

### 클라우드 서비스

| 서비스 | 제공사 | 특징 |
|--------|--------|------|
| **Galileo** | Galileo AI | Context Adherence, PII 감지 실시간 대시보드 |
| **LangSmith** | LangChain | 파이프라인 트레이스, 프롬프트 버전 관리 |
| **Azure AI Studio** | Microsoft | 통합 평가 + 모니터링 |
| **CloudWatch + X-Ray** | AWS | 커스텀 LLM 메트릭 추적 |
| **Weights & Biases** | W&B | ML 실험 추적, LLM 평가 시각화 |

### 코드 샘플 1: RAGAS 자동 평가 파이프라인

```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from datasets import Dataset
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# 평가 데이터셋 구성
eval_data = {
    "question": [
        "삼성전자의 2023년 영업이익은 얼마인가?",
        "RAG에서 환각을 줄이는 프롬프팅 기법은?",
    ],
    "answer": [
        "삼성전자의 2023년 영업이익은 6.57조 원입니다.",  # 시스템 생성 답변
        "Chain of Note와 Chain of Verification이 효과적입니다.",
    ],
    "contexts": [
        # 검색된 컨텍스트 (리스트의 리스트 형식)
        ["삼성전자는 2023년 연간 영업이익 6.57조 원을 발표했습니다...",
         "2023년 반도체 부문 적자가 전체 실적에 영향을 미쳤습니다..."],
        ["Chain of Note는 각 문서에 읽기 노트를 작성하여...",
         "Chain of Verification은 초안을 생성 후 자기 검증을 수행합니다..."],
    ],
    "ground_truth": [
        "삼성전자 2023년 영업이익은 6.57조 원이다.",
        "CoN과 CoVe가 RAG 환각 줄이기에 사용된다.",
    ]
}

dataset = Dataset.from_dict(eval_data)

# 평가 실행 (GPT-4o를 Judge LLM으로 사용)
from ragas.llms import LangchainLLMWrapper
judge_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o", temperature=0))

results = evaluate(
    dataset=dataset,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
    llm=judge_llm,
    embeddings=OpenAIEmbeddings(),
)

# 결과 출력
df = results.to_pandas()
print(df[["question", "faithfulness", "answer_relevancy", "context_precision", "context_recall"]])
print(f"\n평균 Faithfulness: {df['faithfulness'].mean():.3f}")
print(f"평균 Answer Relevancy: {df['answer_relevancy'].mean():.3f}")
```

### 코드 샘플 2: LangSmith 트레이싱 통합

```python
import os
from langsmith import Client
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.tracers import LangChainTracer

# LangSmith 설정
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-langsmith-api-key"
os.environ["LANGCHAIN_PROJECT"] = "RAG-Master-Production"

# 이후 모든 LangChain 실행이 자동으로 LangSmith에 트레이싱됨
llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 정확한 정보를 제공하는 어시스턴트입니다."),
    ("human", "컨텍스트: {context}\n\n질문: {question}")
])

chain = prompt | llm

# 실행 시 트레이스 자동 기록
result = chain.invoke({
    "context": "RAG는 외부 DB를 검색하여 LLM 응답을 강화합니다.",
    "question": "RAG의 핵심 이점은?"
})
```

### 코드 샘플 3: 자동 최적화 - Top-K 튜닝 비용 분석

```python
"""
Top-K 파라미터 튜닝을 통한 비용 vs 품질 최적화
목표: 품질 유지하면서 토큰 비용 최소화
"""
from ragas import evaluate
from ragas.metrics import faithfulness, context_precision
from datasets import Dataset
import matplotlib.pyplot as plt

def run_rag_with_topk(questions: list, vectorstore, k: int) -> dict:
    """특정 Top-K 값으로 RAG 실행 및 평가"""
    from langchain_openai import ChatOpenAI
    
    llm = ChatOpenAI(model="gpt-4o-mini")
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    
    answers, contexts, total_tokens = [], [], 0
    
    for question in questions:
        docs = retriever.invoke(question)
        context = "\n".join([d.page_content for d in docs])
        
        response = llm.invoke(f"컨텍스트: {context}\n\n질문: {question}")
        answer = response.content
        
        answers.append(answer)
        contexts.append([d.page_content for d in docs])
        total_tokens += len(context.split()) + len(answer.split())  # 근사치
    
    # RAGAS 평가
    dataset = Dataset.from_dict({
        "question": questions,
        "answer": answers,
        "contexts": contexts,
    })
    scores = evaluate(dataset, metrics=[faithfulness, context_precision])
    
    return {
        "k": k,
        "faithfulness": scores["faithfulness"],
        "context_precision": scores["context_precision"],
        "estimated_tokens": total_tokens,
        "estimated_cost_usd": total_tokens * 0.00000015  # gpt-4o-mini 단가
    }

# Top-K 1, 3, 5, 10, 20 비교
questions = ["..."] * 10  # 테스트 질문 10개
k_values = [1, 3, 5, 10, 20]

results = []
for k in k_values:
    result = run_rag_with_topk(questions, vectorstore=None, k=k)  # vectorstore 실제 연결 필요
    results.append(result)
    print(f"K={k}: Faithfulness={result['faithfulness']:.3f}, "
          f"Cost=${result['estimated_cost_usd']:.4f}")

# 결론: Top-K=5 지점이 품질 대비 비용 최적점인 경우 많음
# 실험 결과 예시: K=100 대비 K=5에서 비용 23% 절감, 레이턴시 22% 단축, 품질 감소 < 2%
```

### 코드 샘플 4: Noise Robustness 테스트 자동화

```python
"""
노이즈 문서를 의도적으로 주입하여 시스템의 내성을 측정
"""
import random

def noise_robustness_test(qa_chain, qa_pairs: list, noise_ratio: float = 0.5) -> float:
    """
    qa_pairs: [(question, ground_truth), ...]
    noise_ratio: 노이즈 문서 비율 (0.5 = 50%가 관련 없는 문서)
    """
    noise_docs = [
        "오늘 날씨는 맑고 기온이 25도입니다.",
        "전국 맛집 TOP 100 리스트입니다.",
        "스포츠 경기 결과: 한국 vs 일본 2:1",
    ]
    
    correct = 0
    for question, ground_truth in qa_pairs:
        # 관련 문서와 노이즈 문서를 섞어서 주입
        related_docs = qa_chain.retriever.invoke(question)
        noise_count = int(len(related_docs) * noise_ratio)
        injected_docs = related_docs + random.sample(noise_docs, noise_count)
        random.shuffle(injected_docs)
        
        context = "\n".join([d if isinstance(d, str) else d.page_content
                             for d in injected_docs])
        
        answer = qa_chain.llm.invoke(
            f"컨텍스트:\n{context}\n\n질문: {question}\n"
            f"컨텍스트에 없는 내용은 '알 수 없음'이라고 답하세요."
        ).content
        
        # 간단한 키워드 매칭으로 정확도 측정 (실제로는 LLM-Judge 사용 권장)
        if any(word in answer for word in ground_truth.split()[:3]):
            correct += 1
    
    accuracy = correct / len(qa_pairs)
    print(f"노이즈 비율 {noise_ratio*100}%에서 정확도: {accuracy:.2%}")
    return accuracy

# 다양한 노이즈 비율로 테스트
for ratio in [0.0, 0.3, 0.5, 0.7]:
    noise_robustness_test(qa_chain=None, qa_pairs=[], noise_ratio=ratio)
```

---

## 마무리: RAG Master 8주 과정 완성

8주에 걸쳐 다음의 완전한 RAG 스택을 학습하였습니다:

1. **1주차**: LLM 한계 이해 → RAG 필요성 → 7가지 실패 지점
2. **2주차**: CoT, ThoT, CoN, CoVe로 환각을 제어하는 프롬프팅
3. **3주차**: 의미 기반 청킹, Proposition, RAPTOR로 문서를 지능적으로 분할
4. **4주차**: Dense/Sparse 임베딩, ColBERT, MRL로 텍스트를 벡터로 변환
5. **5주차**: HNSW, PQ, 엔터프라이즈 벡터 DB로 초고속 검색 인프라 구축
6. **6주차**: Cross-Encoder, Hybrid Search, HyDE로 검색 순위 최적화
7. **7주차**: Knowledge Graph로 Multi-hop 추론과 관계 기반 검색
8. **8주차**: RAGAS, LangSmith로 품질 자동 평가 및 지속적 최적화

이 파이프라인을 완전히 이해하고 구현할 수 있다면, 어떤 도메인에서도 엔터프라이즈급 RAG 시스템을 설계·배포할 수 있습니다.
