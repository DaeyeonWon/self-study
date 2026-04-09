# RAG Master 세미나 자료 작성 지침 (ALL WEEKS)

## 목적
이 자료는 현업 엔지니어링 및 AI 리서처를 대상으로 한 **전문가급 세미나 자료**입니다.
각 주차의 토픽은 아래의 엄격한 구조에 따라, 단 하나의 섹션도 누락 없이 작성되어야 합니다.

---

## ✅ 각 주차별 필수 작성 구조 (ALL REQUIRED)

### 1. 개요 (Overview)
- 이 주차가 전체 RAG 파이프라인에서 어떤 역할을 하는가
- 앞/뒷 주차와의 연결 관계

---

### 2. 핵심 이론 섹션들 (1개 섹션이상, 각 토픽별로 반복)

각 이론 섹션은 아래 구조를 **모두** 포함해야 합니다:

#### 2-1. 이론 설명
- 개념 정의, 원리, 수식/직관적 설명 포함
- 왜 이게 필요한가? 이전 방식의 한계는?

#### 2-2. PDF 원본 자료 이미지 (⚠️필수)
- 해당 토픽에 관련된 PDF의 Figure/Table 이미지를 반드시 삽입
- 포맷: `<img src="assets/images_new/Fig_X_X_page_XX.png" width="600">`
- 캡션: `*Fig X.X: [설명 (PDF p.XX)]*`

#### 2-3. 예시 (예: 수학 문제 풀기, 비유 등)
- 추상적 개념을 직관적으로 이해하도록 쉬운 예시 포함

#### 2-4. 관련 논문 레퍼런스 (⚠️필수, 있는 경우)
- 논문명, 저자, 소속, 연도
- 논문의 핵심 아이디어 / 무엇을 해결했는가
- 논문의 주요 결과 / 성능 향상 수치
- 왜 이 논문이 중요한지 (Impact)

#### 2-5. 논문 아키텍처 다이어그램 (⚠️필수, 해당되는 경우)
- 논문의 핵심 아키텍처를 직접 Mermaid 다이어그램으로 재현
- 각 컴포넌트와 데이터 흐름 표현
- 형식:
```
![diagram](assets/images_new/mermaid_wX_Y.png)
```
(render_mermaid.py 실행 후 자동으로 이미지로 변환됨)

---

### 3. 💻 구현 (Implementation) 섹션 (⚠️필수)

관련 이론 설명이 끝난 뒤 반드시 구현 섹션이 이어져야 합니다.

#### 3-1. 관련 프레임워크 / 라이브러리 소개
- 해당 기법을 구현할 수 있는 오픈소스 프레임워크 목록 (예: LangChain, LlamaIndex, DSPy 등)
- 각 프레임워크의 장/단점, 적합한 상황 설명

#### 3-2. 클라우드 서비스 (해당되는 경우)
- AWS, Azure, GCP, 또는 전문 AI 클라우드 서비스(Pinecone, Cohere, OpenAI 등) 소개
- 각 서비스의 주요 기능, 과금 모델, 적합한 아키텍처

#### 3-3. 코드 샘플 (⚠️필수)
- 실제로 실행 가능한 Python 코드 블록
- 주요 변수와 로직에 한글 주석 포함
- 1개 이상의 완성된 end-to-end 흐름 예시

---

## 📋 주차별 핵심 토픽 목록

### 1주차: RAG Fundamentals & System Challenges (PDF p.5-19)
- LLM의 이해와 한계 (환각, 지식 컷오프, 보안 편향)
- RAG 정의 및 이점
- RAG vs. Fine-tuning vs. Prompt Engineering (Table 비교)
- RAG 구축의 7가지 주요 실패 지점

### 2주차: Prompting Strategies for Hallucination Reduction (PDF p.21-38)
- Chain of Thought (CoT)
- Thread of Thought (ThoT)
- Chain of Note (CoN)
- Chain of Verification (CoVe)
- EmotionPrompt / ExpertPrompting

### 3주차: Advanced Document Chunking & Context Engineering (PDF p.40-58)
- 청킹의 영향력 개요
- 청킹 전략 선택 기준
- Recursive Character Splitter
- Semantic Splitting
- Document Specific Splitting (Table 파싱 포함)
- LLM 기반 Propositions 청킹
- Chunk Attribution / Utilization 측정

### 4주차: Embedding Models & Representation Learning (PDF p.60-77)
- Dense vs Sparse 임베딩 개념
- 모델 선택 기준 (MTEB, 차원, 비용)
- Sparse vs Dense 비교
- Multi-Vector (ColBERT)
- Matryoshka Representation Learning (MRL)
- NVIDIA 10-K 사례 연구 워크플로우

### 5주차: Vector Databases & Retrieval Architecture (PDF p.81-120)
- 벡터 DB 선택 기준 (오픈소스 vs 상용)
- 엔터프라이즈 기능 (SOC-2, SSO, RBAC)
- 인덱스 종류 (Exact vs HNSW)
- 필터링 전략 (Pre/Post-filtering)
- 비용 절감 기법 (Binary Quantization, Disk Index)
- 전체 RAG 아키텍처 설계 (쿼리 리라이터, 가드레일 등)

### 6주차: Reranking Models and Hybrid Retrieval (PDF p.94-130)
- 리랭커의 역할
- Cross-Encoders
- LLM 기반 Reranking (Pointwise, Listwise, Pairwise)
- Hybrid Search (Dense + Sparse)
- HyDE (Hypothetical Document Embeddings)
- Recursive Retrieval
- NDCG 성능 측정

### 7주차: Knowledge Graph RAG (GraphRAG, 최신 논문 기반)
- GraphRAG 필요성
- 엔티티 추출 (Entity Extraction)
- 관계 매핑 (Relation Mapping / Triplets)
- Graph Traversal
- Microsoft GraphRAG 논문
- Vector + Graph 하이브리드 활용

### 8주차: RAG Evaluation, Monitoring & Optimization (PDF p.136-188)
- 배포 전 테스트 시나리오 (Relevance, Noise Robustness, Negative Rejection)
- 보안/브랜드 보호 검증 (Privacy, Toxicity)
- Galileo Observe 모니터링
- Context Adherence / Completeness 지표
- 최적화 사례 연구 (임베딩 교체, Top-K 튜닝 →  비용 23% ↓, 지연 22% ↓)

---

## ⚠️ 금지 사항
- PDF 내용이 없어도 대략적인 텍스트 설명만으로 섹션을 때우는 행위 금지
- 논문 없는 섹션에서 논문이 있는 척 하는 행위 금지
- 이미지를 생략하거나, 이미지 경로가 없는데 있는 척 하는 행위 금지
- 코드 샘플을 빈 껍데기(# placeholder)로만 채우는 행위 금지
- `10X Massive Deep Dive`, `돌격!`, `박살!` 등의 편집성 문구를 본문에 삽입하는 행위 금지

---

## 📂 이미지 파일 목록 (assets/images_new/)
아래 파일들이 현재 존재하며 각 주차에 반드시 활용:
- Fig_1_1~1_3 (p.7,8,10): LLM 한계, RAG 아키텍처
- Table_1_1 (p.12): RAG vs Fine-tuning 비교표
- Table_2_1~2_2 (p.15): 7가지 실패 지점
- Fig_3_1~3_10 (p.21~38): CoT, ThoT, CoN, CoVe, EmotionPrompt 등
- Fig_4_1~4_5 (p.40~116): Chunking, Embedding, Vector DB, Reranker
- Table_4_3~4_4 (p.83,97): Vector DB 비교표, Reranker 비교표
- Fig_5_1~5_22 (p.136~151): RAG 평가 시나리오
- Fig_6_1~6_17 (p.153~166): Galileo 모니터링, 최적화
- Table_6_1~6_3 (p.156~157): 지표 테이블
- Fig_7_1~7_30 (p.169~189): 최적화 케이스 스터디
