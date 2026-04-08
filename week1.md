---
layout: default
title: 1주차. RAG Fundamentals & System Challenges
---

# 1주차: RAG Fundamentals & System Challenges (RAG의 기초와 시스템적 과제)

RAG Master 스터디의 대장정에 오신 것을 환영합니다! 1주차 과정에서는 최근 자연어 처리(NLP)와 엔터프라이즈 AI 환경에서 폭발적인 반응을 불러일으키고 있는 **RAG (Retrieval-Augmented Generation, 검색 증강 생성)** 의 기본 개념과 등장 배경을 학술적, 실무적 관점에서 깊이 있게 다룹니다. 나아가 RAG 시스템을 구축할 때 직면하는 여러 가지 시스템 챌린지를 살펴봅니다.

---

## 1. LLM의 근본적 한계와 RAG의 탄생 배경

대규모 언어 모델(LLM)의 등장은 인간과 기계 간의 소통 방식을 송두리째 바꿔 놓았지만, 구조적으로 몇 가지 치명적인 결함을 내포하고 있습니다. RAG는 바로 이 결함들을 보완하기 위해 2020년 Facebook AI Research(현재 Meta AI) 연구원들에 의해 처음 학계에 공식적으로 제안되었습니다. 

### 1.1. 환각 현상 (Hallucination)
LLM은 사실을 데이터베이스처럼 '저장'하고 있는 것이 아니라, 방대한 텍스트의 확률 분포를 학습하여 "문맥상 다음에 올 가장 자연스러운 단어"를 통계적으로 예측하여 내뱉습니다. 그 결과, 지식이 부족한 상황에서도 오답을 정답처럼 지어내는 환각이 발생합니다.
> 🍔 **이해를 돕는 예시: 공부 안 한 수험생**
> 시험 공부를 전혀 하지 않은 학생이 백지를 내는 대신, 문제의 뉘앙스를 파악하여 그럴싸한 소설을 지어서 답안지 전체를 꽉 채워 제출하는 것과 같습니다. RAG는 이 학생(LLM)에게 시험 10분 전 관련된 '오픈북(검색된 외부 문서)'을 쥐어주는 역할을 합니다.

![Hallucination Issue](assets/images_new/Fig_1_1_page_7.png)
*Fig 1.1: 생성 모델이 범하는 환각(Hallucination)의 주요 유형들 (입력 충돌, 문맥 충돌, 사실 충돌).*

### 1.2. 모델의 지식 단절 (Knowledge Cut-off)
모델 학습은 엄청난 시간과 천문학적인 컴퓨팅 자원(GPU)을 소모합니다. 따라서 학습 시점이 지나고 나면 최신 세상의 정보(최신 법령 개정, 오늘의 날씨, 어제 발표된 애플의 신제품 등)를 전혀 인지하지 못합니다. 매일매일 변화하는 금융/의학 지식 환경에서는 이는 실무 활용을 불가능하게 합니다.

### 1.3. 프라이버시 및 데이터 보안 (Data Privacy)
기업의 사내 기밀문서나 고객의 개인정보를 LLM에 직접 학습시킬 경우, 그 보안 데이터가 모델 가중치 네트워크 내부에 잠복하게 됩니다. 다른 사용자가 교묘한 질문을 던졌을 때 이 정보가 무단으로 유출되는 보안 참사가 일어날 수 있습니다.

![Confidential Information issue](assets/images_new/Fig_1_2_page_8.png)
*Fig 1.2: 기존 언어 모델들이 내부의 기밀 데이터를 무단으로 유출할 수 있는 위험 모형.*

---

## 2. RAG (Retrieval-Augmented Generation) 아키텍처의 원리

RAG 모델은 단어 그대로 **'검색을 통해(Retrieval) 정보를 가져와, 이를 기반으로 증강된(Augmented) 답변을 생성(Generation)한다'**는 논리적 흐름을 갖추고 있습니다.

### 대표적인 RAG 파이프라인
1. **문서 섭취 및 인덱싱 (Ingestion & Indexing):** 기업의 모든 PDF, 워드, 데이터베이스 내 지식을 잘게 자르고(Chunking), 임베딩(Embedding) 모델을 통해 고차원의 숫자 벡터로 변환하여 벡터 DB에 안전하게 보관합니다.
2. **검색 체계 (Retrieval):** 사용자의 쿼리(질문)가 들어오면, 질문 역시 벡터로 치환한 뒤 사내 벡터 DB에서 코사인 유사도 연산을 통해 "가장 의미가 겹치는" 상위 5개의 핵심 문서를 쏙 뽑아옵니다.
3. **증강 생성 (Augmented Generation):** 검색된 문서 묶음(Context)과 원래의 질문(Query)을 LLM에게 프롬프트 형태로 합쳐서 전달합니다. "오직 이 문서를 근거지로 하여 답을 작성해"라는 지시를 덧붙여 LLM이 똑똑하게 내용을 정리하고 대답하도록 만듭니다.

![RAG Working Mechanism](assets/images_new/Fig_1_3_page_10.png)
*Fig 1.3: 일반적인 RAG 파이프라인 아키텍처. 쿼리 임베딩부터 벡터 탐색, 생성까지의 과정.*

---

## 3. RAG vs 파인튜닝 (Fine-Tuning) vs 프롬프트 엔지니어링

엔터프라이즈 AI 아키텍처를 그릴 때 가장 헷갈리는 이 3가지 접근법을 확실히 비교해 보겠습니다.

![Comparison Table](assets/images_new/Table_1_1_page_12.png)
*Table 1.1: RAG, 파인튜닝, 프롬프트 엔지니어링 비교.*

1. **프롬프트 엔지니어링 (Prompt Engineering):** 시스템 개선 없이 지시문만 정교하게 세팅합니다. (예: "너는 판사야. 엄격하게 대답해.")
2. **파인튜닝 (Fine-Tuning):** LLM 내부의 신경망 파라미터를 미세 조정하여 의사의 톤, 법률가의 어조 등 '도메인의 분위기(스타일)'를 입힙니다. 빈번하게 지식이 업데이트되는 환경에는 쥐약입니다.
3. **RAG:** "팩트 업데이트"와 "출처 표기(Citation)"에 특화된 유일한 방법입니다.

---

## 4. 실무 RAG 시스템 구축의 7대 챌린지 (System Challenges)

이론은 무척 뛰어나지만 실제 서비스에서는 RAG 파이프라인 각각의 터널에서 수많은 데이터 병목과 환각 오류가 연쇄적으로 발생합니다. 이 스터디에서 앞으로 매주 하나씩 부숴나갈 과제들입니다.

1. **Missing Content:** 벡터 DB 안에 사용자가 묻는 지식 자체가 없으면 RAG는 오작동합니다.
2. **Missed Top Ranked Documents:** 정답 문서는 존재하지만 임베딩 검색 엔진의 한계로 쓰레기 문서에 밀려나 LLM에게 전달되지 못합니다 (이 문제는 6주차 리랭커에서 배웁니다).
3. **Lost in the Middle (가운데에서 길 잃기):** 너무 많은 문서를 LLM에게 주면, 정답이 한가운데에 포진되었을 때 컴퓨터가 이를 망각/패스해버립니다.
4. **Incorrect Specificity & Wrong Format:** 지나치게 일반적인 답변을 하거나 요구한 시스템 포맷(JSON 등)을 어기는 포맷팅 파괴 오류입니다.

---

## 💡 연구 트렌드 및 관련 학술 아티클

> **[Paper Reference 1]** *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (Lewis et al., 2020)*
> RAG 메커니즘을 딥러닝과 자연어 처리 분야에 최초로 명명하고 제안한 Facebook(Meta) AI의 기념비적 논문입니다. 이 논문은 매개변수형 메모리(Parametric Memory)와 비매개변수형(Non-parametric) 외부 데이터베이스를 상호 융합하면 지식 집약적 질문에서 모델의 환각이 획기적으로 억제됨을 처음 수학적으로 증명했습니다. 

> **[Paper Reference 2]** *Lost in the Middle: How Language Models Use Long Contexts (Liu et al., 2023)*
> 이 연구 논문은 LLM이 문서의 처음과 끝 내용만 기억하고 '가운데' 있는 정보의 정확도를 심각하게 떨어뜨리는 U자형 성능 곡선(U-shaped performance)을 발견했습니다. RAG 시스템에서 단순히 글을 길게 때려 넣는 것이 해답이 아님을 경고하며 청킹 시스템의 중요성을 입증했습니다.

---

## 마무리하며

이번 1주차에서는 LLM의 본원적 한계를 넘기 위해 외부 확장 뇌(데이터베이스)를 장착하는 RAG 생태계의 거시적 안목을 배웠습니다. 다음 2주차 수업에서는 이 시스템의 종착역이자 출구를 담당하는 LLM 통제 기술, 즉 프롬프트 엔지니어링 메커니즘인 'Prompting Strategies for Hallucination Reduction' 분야를 대대적으로 해부해 보겠습니다.
