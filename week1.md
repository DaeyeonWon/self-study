---
layout: page_with_mermaid
title: 1주차. RAG Fundamentals & System Challenges
---

# 1주차: RAG Fundamentals & System Challenges (LLM의 한계 극복을 위한 RAG의 도입과 실무적 난제)

인공지능의 시대가 도래하며 LLM(대형 언어 모델)은 세상을 바꿀 마법 지팡이처럼 여겨졌습니다. 하지만 곧 기업들은 LLM을 실무 B2B 프로덕션 환경에 투입하며 끔찍한 병목 현상과 재앙적인 오류들을 마주하게 됩니다.
이번 1주차 과정에서는 LLM이 본질적으로 지니고 있는 치명적 한계점(Pitfalls)들을 낱낱이 파헤치고, 이를 방어하기 위한 최상위 설계 아키텍처인 **RAG(Retrieval-Augmented Generation)** 의 근본 원리와 실패 지점 7가지를 심층 해부합니다. 

단순한 개념 소개를 넘어, 기업이 직면하는 보안 유출과 파이프라인 붕괴 현상의 인사이트를 다룹니다.

---

## 1. LLM의 이해와 근본적 한계 (The Pitfalls)

### 스마트 자동완성 봇의 구조적 맹점
LLM은 내부적으로 세상의 진리를 판독하는 스카이넷이 아닙니다. 방대한 텍스트 시퀀스 내에서 요소 간의 문맥 확률을 학습하여 다음에 올 단어를 예측하는 '스마트 자동완성 봇(Smart Autocomplete Bot)'에 불과합니다. 이 구조적 특성 때문에 필연적으로 3대 한계점이 발생합니다.

<img src="assets/images_new/Fig_1_1_page_7.png" width="600">
*Fig 1.1: [LLM의 환각(Hallucinations) 사례 (PDF p.7)] 단순 오답이 아닌, 사실과 다르지만 문맥상 그럴싸한 거짓말을 날조하는 치명적 환각 아키텍처 예시.*

<img src="assets/images_new/Fig_1_2_page_8.png" width="600">
*Fig 1.2: [보안 및 프라이버시 침해 (PDF p.8)] 학습 데이터에 섞여 있던 글로벌 개인 신용카드 번호, 사내 기밀문서 등의 민감한 정보가 여과 없이 노출되는 현상.*

* **주요 PITFALLS 심층 팩트체크:**
    * **환각 (Hallucinations):** 학습 데이터 구멍을 메우기 위해 그럴싸한 거짓 소설을 지어냅니다. 이는 B2B 계약서 작성이나 의료 진단 도메인에서 기업을 즉결 파산시킬 수 있는 리스크입니다.
    * **지식 컷오프 (Knowledge Cut-off):** 2023년까지 학습된 모델은 2024년의 최신 법률 개정안을 절대로 알 방법이 없습니다. 
    * **보안 및 편향성 (Privacy & Bias):** 학습된 데이터의 치충증, 혹은 해커의 프롬프트 인젝션 방어에 속수무책으로 뚫립니다.

---

## 2. RAG (Retrieval Augmented Generation)란?

이를 해결하기 위해 인공지능이 대답하기 전, 사내 데이터베이스라는 확장된 '도서관'에 파견을 보내는 아키텍처가 등장했습니다.

<img src="assets/images_new/Fig_1_3_page_10.png" width="600">
*Fig 1.3: [RAG 기본 아키텍처 메커니즘 (PDF p.10)] 유저 질문 -> 외부 위키 DB 검색 -> 컨텍스트와 질문을 병합하여 LLM에 프롬프트 주입 -> 안전한 답변 생성 구조.*

* **정의:** 외부 신뢰할 수 있는 데이터베이스에서 관련 정보(문단)를 실시간 검색하여, LLM의 응답 프롬프트를 증강(Augment)하는 백엔드 아키텍처.
* **압도적 이점:** 
  1. 정보의 실시간 최신성 유지 (새로운 사규가 갱신되어도 재학습 불필요)
  2. 고객에게 '답변의 출처(Citation)' 제시 가능 (환각 억제)
  3. 보안이 철저한 도메인 특화 사내 지식(ERP) 활용 가능.

---

## 3. 타 기술과의 대결: RAG vs. Fine-tuning vs. Prompt Engineering

<img src="assets/images_new/Table_1_1_page_12.png" width="600">
*Table 1.1: [RAG, Fine-Tuning, Prompt Engineering 간의 스펙 비교 (PDF p.12)] 어느 상황에서 어떤 무기를 채택해야 하는가에 대한 결정 테이블.*

* 💡 **핵심 산업계 Insight:** 
    * **RAG:** 동적(Dynamic)으로 매일매일 데이터가 변하는 지식 기반 환경에서 팩트 오류를 100% 방지할 수 있는 최고 효율 엔진.
    * **Fine-Tuning:** 모델에게 새로운 회사 말투나 특정 제이슨(JSON) 출력 폼팩터 행동 양식을 이식할 때 유리하지만, 내일 사실이 바뀌면 다시 1억을 들여 파인튜닝해야 하는 재앙이 존재. 

---

## 4. 실전! RAG 구축의 7가지 주요 실패 지점 (Pain points)

튜토리얼 수준에서는 완벽하던 RAG가 실무 서버에서는 왜 터질까요?

<img src="assets/images_new/Table_2_1_page_15.png" width="600">
<img src="assets/images_new/Table_2_2_page_15.png" width="600">
*Table 2.1 & 2.2: [RAG 파이프라인의 7대 치명적 실패 지점 (PDF p.15)] 시스템이 붕괴하는 원인망.*

1. **내용 누락 (Missing Content):** 근본적으로 데이터베이스에 답을 할 정보 파일 자체가 안 들어있는 경우.
2. **순위권 밖 문서 (Missed Top Ranked):** 정답 파일이 존재하나, 서치 시스템이 바보여서 100위 밖으로 밀어내 LLM이 읽지도 못한 경우.
3. **문맥 통합 제한 (Consolidation Strategy Limitations):** 찾기는 5개의 문단을 잘 찾았으나, 이를 프롬프트에 구겨 넣을 때 문맥이 잘리거나 LLM 수용 한계를 초과해 박살 나는 고충.
4. (이 외 환각 생성, 잘못된 포맷 지시 등 총 7대 실패 사례와 그 원인을 깊이 고찰합니다.)

---

## 💻 [Implementation Frameworks] LangChain 기반 기초 RAG 방어망 파이프라인

단순히 글을 읽는 것을 넘어, 가장 대중적으로 활용되는 프레임워크인 **LangChain**을 통해 위 RAG의 뼈대를 어떻게 가동하는지 5줄 코드로 보여드립니다.

```python
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# 1. 외부 지식 문서 로드 및 청킹 (Missing Content 방지)
loader = PyPDFLoader("data/RAG_Guide.pdf")
pages = loader.load_and_split()

# 2. 임베딩 및 Vector DB 저장 (Missed Top Ranked 방어형 모델 채택 필요)
vectorstore = Chroma.from_documents(pages, embedding=OpenAIEmbeddings())

# 3. 질의응답 Retriever 체인 생성 (지식 통합)
qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(), retriever=vectorstore.as_retriever())
print(qa_chain.run("LLM의 주요 3가지 한계점이 무엇인가요?"))
```

## 마무리하며 지식 팽창의 첫걸음
이번 1주 차 과정에서는 스마트한 LLM의 필연적 저주인 맹목적 환각을 제어하고 프라이버시를 지키는 RAG의 설계 당위성을 파헤쳤습니다. 이제 이 거대한 개념을 장착했으니, 다음 2주 차 **"Prompting Strategies for Hallucination Reduction"** 에서는 검색된 문서를 LLM에게 던져줄 때, 어떻게 윽박지르고 세뇌해야 환각을 0%에 수렴시킬 수 있는지 최상위 프롬프트 주작 기법들을 대해부하겠습니다!
