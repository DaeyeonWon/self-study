# [세미나 자료] 엔터프라이즈급 RAG 시스템 구축 마스터 클래스

## **1주차: RAG Fundamentals & System Challenges**
**주요 내용: LLM의 한계 극복을 위한 RAG의 도입과 실무적 난제**
* **LLM의 이해와 한계 (PDF p.5-8)**
    * 작동 원리: 방대한 데이터로 훈련된 '스마트 자동완성 봇'으로서 시퀀스 내 요소 간 문맥 관계를 학습함[cite: 5, 20].
    * 주요 PITFALLS:
        * 환각 (Hallucinations): 사실과 다르지만 그럴싸한 답변 생성[cite: 31].
        * 지식 컷오프: 모델 학습 시점 이후의 최신 정보 접근 불가[cite: 42].
        * 보안 및 편향: 개인정보 유출 위험 및 학습 데이터의 편향 증폭[cite: 43].
* **RAG (Retrieval Augmented Generation)란? (PDF p.9-11)**
    * 정의: 외부 데이터베이스에서 관련 정보를 검색하여 LLM의 응답을 강화하는 아키텍처[cite: 51].
    * 이점: 정보의 최신성 유지, 답변의 출처 제공, 도메인 특화 지식 활용 가능[cite: 52].
* **RAG vs. Fine-tuning vs. Prompt Engineering (PDF p.12)**
    * RAG: 동적 데이터에 최적이며 환각 최소화에 가장 효과적임[cite: 77].
    * Fine-tuning: 모델을 특정 작업/스타일에 맞게 조정할 때 유리하지만 데이터 업데이트가 어려움[cite: 75].
* **RAG 구축의 7가지 주요 실패 지점 (PDF p.14-19)**
    * 내용 누락(Missing Content), 순위권 밖 문서(Missed Top Ranked), 문맥 통합 제한(Consolidation Strategy Limitations) 등 실무적 고충 분석 [cite: 101-123].

## **2주차: Prompting Strategies for Hallucination Reduction**
**주요 내용: 검색된 문맥을 활용해 답변의 정확도를 높이는 고급 프롬프트 기술**
* **Chain of Thought (CoT) (PDF p.21)**
    * 모델이 단계별 사고 과정을 거쳐 논리적 결론에 도달하도록 유도[cite: 135].
* **Thread of Thought (ThoT) (PDF p.22-23)**
    * 혼란스럽고 복잡한 문맥에서 중요한 정보를 선별하기 위해 문맥을 나누어 요약하고 분석함[cite: 151, 156].
* **Chain of Note (CoN) (PDF p.26-29)**
    * 검색된 각 문서에 대해 '읽기 노트'를 작성하여 정보의 관련성과 답변 가능 여부를 사전 평가[cite: 186, 199].
* **Chain of Verification (CoVe) (PDF p.30-31)**
    * 초기 답변 생성 → 검증 질문 생성 → 재검색 및 검증 → 최종 수정 답변 생성의 4단계 프로세스 [cite: 235-239].
* **심리적/전문적 자극 기법 (PDF p.32-37)**
    * EmotionPrompt: "커리어에 중요하다"와 같은 감정적 문구 추가 시 성능 향상[cite: 245, 258].
    * ExpertPrompting: 모델에 특정 분야 전문가의 정체성을 부여하여 상세한 답변 유도[cite: 272, 280].

## **3주차: Advanced Document Chunking & Context Engineering**
**주요 내용: 검색 성능의 기초가 되는 텍스트 분할 최적화 전략**
* **청킹(Chunking)의 영향력 (PDF p.41)**
    * 검색 품질, 저장 비용, 쿼리 지연 시간 및 환각 발생 여부에 직접적 영향을 미침 [cite: 316-322].
* **청킹 전략 선택 기준 (PDF p.42-44)**
    * 텍스트 구조(코드, 테이블, 일반 텍스트), 임베딩 모델의 토큰 제한, 질문의 유형에 따라 결정 [cite: 326-337].
* **고급 청킹 기법 (PDF p.46-54)**
    * Recursive Character Splitter: 계층적 구분자를 통한 문맥 보존[cite: 366].
    * Semantic Splitting: 임베딩을 이용해 문장 간 유사도를 측정하여 주제별 분할 [cite: 423-425].
    * Document Specific Splitting: 표(Table) 구조 인식을 포함한 비정형 데이터 파싱[cite: 457, 474].
* **LLM 기반 청킹: Propositions (PDF p.55)**
    * 텍스트를 독립적이고 원자적인 사실 단위(Atomic expressions)로 나누어 검색 정밀도 극대화 [cite: 480-481].
* **청킹 효과 측정 (PDF p.57-58)**
    * Chunk Attribution: 실제 응답 생성에 해당 청크가 기여했는가[cite: 502].
    * Chunk Utilization: 청크 내 텍스트 중 실제 사용된 비율[cite: 510].

## **4주차: Embedding Models & Representation Learning for Retrieval**
**주요 내용: 데이터를 벡터로 변환하는 임베딩 모델의 선택과 평가**
* **임베딩의 개념 (PDF p.60-61)**
    * 고차원 시맨틱 공간에서 텍스트 간의 관계를 캡처하는 밀집 벡터(Dense vectors)[cite: 530].
* **모델 선택 기준 (PDF p.62-64)**
    * 벡터 차원, MTEB(Massive Text Embedding Benchmark) 점수, 언어 지원 및 비용 분석 [cite: 548-561].
* **임베딩 모델의 유형 (PDF p.65-68)**
    * Sparse vs Dense: 키워드 기반 매칭과 의미 중심 매칭의 차이[cite: 568, 571].
    * Multi-Vector (ColBERT): 후기 상호작용(Late Interaction)을 통한 정밀 검색[cite: 575].
    * Matryoshka Representation Learning (MRL): 가변 차원 임베딩을 통한 효율적 검색[cite: 582].
* **성능 측정 워크플로우 (PDF p.69-77)**
    * NVIDIA 10-K 사례 연구를 통한 모델별 Attribution 및 Adherence 비교 실습 [cite: 618, 726-727].

## **5주차: Vector Databases & Retrieval Architecture Design**
* **벡터 데이터베이스 선택 (PDF p.81-84)**
    * 오픈소스(Milvus, FAISS) vs 상용(Pinecone) 서비스 비교 [cite: 838, 895-896].
    * 엔터프라이즈 기능: SOC-2 준수, SSO 통합, Rate Limits, RBAC 관리 [cite: 908-913].
* **성능 최적화 기술 (PDF p.86-92)**
    * 인덱스: Exact(Flat) vs Approximate(HNSW) 검색 [cite: 931-932].
    * 필터링: Pre-filtering과 Post-filtering의 전략적 활용 [cite: 933-935].
    * 비용 절감: Disk Index 및 Binary Quantization 활용[cite: 963, 965].
* **RAG 전체 아키텍처 설계 (PDF p.117-120)**
    * 사용자 인증, 입력 가드레일, 쿼리 리라이터, 지식 베이스 관리의 유기적 통합 [cite: 1098-1100].

## **6주차: Reranking Models and Hybrid Retrieval Techniques**
* **리랭커(Reranker)의 역할 (PDF p.94-96)**
    * 초기 검색 결과(Top-K)의 순위를 재조정하여 가장 관련성 높은 문서를 상단 배치 [cite: 994-995].
* **리랭커의 유형 (PDF p.99-101)**
    * Cross-Encoders: 쿼리와 문서를 동시에 연산하여 매우 높은 정밀도 제공 [cite: 1043-1044].
    * LLM 기반 Reranking: Pointwise, Listwise, Pairwise 방식 분석 [cite: 1081-1083].
* **하이브리드 및 고급 검색 패턴 (PDF p.127-130)**
    * Hybrid Search: Dense(시맨틱)와 Sparse(키워드) 검색의 결합[cite: 1109].
    * HyDE (Hypothetical Document Embeddings): 가상의 답변 문서를 생성하여 검색 정확도 개선[cite: 1109].
    * Recursive Retrieval: 작은 청크로 검색하고 연결된 큰 문맥을 반환하는 기법[cite: 1111].

## **7주차: Knowledge Graph RAG & Graph-based Retrieval Systems**
* **GraphRAG의 필요성**
    * 단순 벡터 유사도는 문서 간의 복합적인 관계(Entity Relationship) 파악에 한계가 있음.
    * PDF 관련 근거: 9페이지의 '구조화된 소스(Tables, Graphs)' 언급 및 124페이지의 '메타데이터 추출' 기반 기술[cite: 53, 1105].
* **핵심 구성 요소**
    * 엔티티 추출 (Entity Extraction), 관계 매핑 (Relation Mapping), Graph Traversal.
* **엔터프라이즈 활용**
    * 글로벌 데이터 요약 및 복잡한 관계 추론 질문 해결.

## **8주차: RAG Evaluation, Monitoring & Optimization**
* **배포 전 테스트 시나리오 (PDF p.136-150)**
    * 검색 품질(Relevance, Preciseness) 및 신뢰성(Noise Robustness, Negative Rejection) 테스트 [cite: 1117-1120].
    * 보안성(Privacy Breaches, Malicious Use) 및 브랜드 보호(Tone, Toxicity) 검증 [cite: 1123-1130].
* **모니터링 및 관측 가능성 (PDF p.153-157)**
    * Galileo Observe: 실시간 모니터링, 비용 추적 및 가드레일 지표 관리[cite: 1134].
    * 핵심 지표: Context Adherence(정밀도), Completeness(재현율), PII 노출 여부 등 [cite: 1137-1138].
* **최적화 사례 연구 (PDF p.184-188)**
    * 임베딩 모델 교체 및 Recursive Chunking 도입을 통한 Adherence 향상 분석[cite: 1165, 1168].
    * Top-K 튜닝: 검색 문서 수 조정을 통해 비용 23% 감소, 지연 시간 22% 단축 달성[cite: 1169].

**[참고] 실습 과제 리스트**
* 46페이지: Character Splitter 구현 실습 [cite: 362]
* 75페이지: 임베딩 모델 성능 비교 워크플로우 실습 [cite: 716]
* 85페이지: 벡터 DB 엔터프라이즈 기능 설정 실습 [cite: 915]
* 106페이지: NDCG를 활용한 리랭커 성능 계산 실습 [cite: 1087]
