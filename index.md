---
layout: default
title: RAG Master — 엔터프라이즈급 RAG 시스템 구축 마스터 클래스
---

# 🧠 RAG Master 스터디 포털
**엔터프라이즈급 RAG 시스템 구축 마스터 클래스**

> 이 스터디 자료는 현업 AI 엔지니어 및 리서처를 위한 **전문가급 세미나 교안**입니다.  
> LLM의 한계 극복부터 프로덕션 배포·최적화까지, RAG의 전체 스택을 이론·논문·구현 코드로 다룹니다.

---

## 📚 전체 커리큘럼 구성

각 주차는 다음 구조로 작성되었습니다:  
**이론 설명 → PDF 원본 자료 → 관련 SOTA 논문 → 아키텍처 다이어그램 → 구현 프레임워크/클라우드/코드 샘플**

---

### [1주차: RAG Fundamentals & System Challenges](week1.md)
**LLM의 한계 극복을 위한 RAG의 도입과 실무적 난제**

| 항목 | 내용 |
|------|------|
| 🎯 핵심 문제 | LLM의 환각(Hallucination), 지식 컷오프, 보안·편향 문제 |
| 🏗 핵심 개념 | RAG 아키텍처 (Retrieve → Augment → Generate) |
| ⚖️ 기술 비교 | RAG vs Fine-tuning vs Prompt Engineering |
| ⚠️ 실패 지점 | RAG 구축 시 발생하는 7가지 주요 실패 시나리오 |
| 📄 핵심 논문 | Lewis et al. (Meta AI, 2020) — RAG 원조 논문 |
| 💻 구현 | LangChain 기반 기초 RAG 파이프라인 + 환각 방지 프롬프트 |

---

### [2주차: Prompting Strategies for Hallucination Reduction](week2.md)
**검색된 문맥을 활용해 답변의 정확도를 높이는 고급 프롬프트 기술**

| 항목 | 내용 |
|------|------|
| 🔗 Chain of Thought | 단계별 추론 강제로 복잡한 추론 정확도 향상 |
| 🧵 Thread of Thought | 혼란스러운 컨텍스트를 가닥별로 분리 분석 |
| 📝 Chain of Note | 각 문서에 읽기 노트 작성 → 관련성 사전 평가 |
| ✅ Chain of Verification | 초안 → 검증 질문 생성 → 재검토 → 최종 답변 |
| 💡 EmotionPrompt / ExpertPrompting | 감정·전문가 자극 기법으로 성능 8~15% 향상 |
| 📄 핵심 논문 | Wei et al. (Google Brain), Dhuliawala et al. (Meta AI), Li et al. (Microsoft) |
| 💻 구현 | DSPy 오토 최적화 + CoN & CoVe 결합 파이프라인 |

---

### [3주차: Advanced Document Chunking & Context Engineering](week3.md)
**검색 성능의 기초가 되는 텍스트 분할 최적화 전략**

| 항목 | 내용 |
|------|------|
| 📏 영향력 | 청킹 방식은 검색 품질·비용·지연·환각 모두에 직결 |
| 🔄 Recursive Character Splitter | 계층적 구분자 우선순위로 문맥 보존 분할 |
| 🧠 Semantic Splitting | 임베딩 유사도 기반 주제 전환 지점 자동 감지 분할 |
| 🏗 Document Specific Splitting | 표·코드·헤더 구조를 인식하는 비정형 문서 파싱 |
| ⚛️ LLM Propositions 청킹 | 원자 사실 단위로 분해하여 검색 명중률 극대화 |
| 📊 측정 지표 | Chunk Attribution (기여도), Chunk Utilization (효율성) |
| 📄 핵심 논문 | Chen et al. (Dense X Retrieval), Sarthi et al. (RAPTOR, Stanford) |
| 💻 구현 | LangChain + LlamaIndex Semantic Splitter + LLM Proposition 청킹 코드 |

---

### [4주차: Embedding Models & Representation Learning](week4.md)
**데이터를 벡터로 변환하는 임베딩 모델의 선택과 평가**

| 항목 | 내용 |
|------|------|
| 📡 Dense vs Sparse | 키워드 매칭(BM25)과 의미 기반 검색(Dense)의 차이 |
| 🎯 MTEB 벤치마크 | 56개 데이터셋 기반 모델 선택 기준 (차원, 비용, 언어) |
| 🔬 ColBERT | 토큰별 다중 벡터 + Late Interaction으로 초정밀 검색 |
| 🪆 Matryoshka (MRL) | 차원 축소해도 성능 유지 — 스토리지 최대 80% 절감 |
| 📊 평가 워크플로우 | NVIDIA 10-K 사례 연구: Attribution vs Adherence 측정 |
| 📄 핵심 논문 | Khattab et al. (ColBERT, Stanford 2020), Kusupati et al. (MRL, Google 2022) |
| 💻 구현 | OpenAI MRL 임베딩 + BGE-M3 로컬 + 모델 성능 비교 코드 |

---

### [5주차: Vector Databases & Retrieval Architecture Design](week5.md)
**엔터프라이즈급 데이터 저장소 선정 및 시스템 설계**

| 항목 | 내용 |
|------|------|
| 🗄 DB 선택 | FAISS / Milvus / Qdrant / Pinecone 비교 분석 |
| 🔒 엔터프라이즈 기능 | SOC-2, SSO, RBAC, Rate Limiting 필수 체크리스트 |
| ⚡ HNSW 인덱스 | 그래프 계층 구조로 O(log n) 근사 검색 — 속도 수천 배 향상 |
| 💰 비용 절감 | Binary Quantization (32배 압축), DiskANN (RAM 90% 절감) |
| 🏛 전체 아키텍처 | 인증 → 가드레일 → 쿼리 리라이터 → 검색 → LLM 통합 설계 |
| 📄 핵심 논문 | Malkov et al. (HNSW, 2016), Jayaram et al. (DiskANN, Microsoft 2019) |
| 💻 구현 | FAISS HNSW 인덱스 + Pinecone RBAC 메타데이터 필터링 코드 |

---

### [6주차: Reranking Models and Hybrid Retrieval Techniques](week6.md)
**검색 결과의 순위 재조정을 통한 답변 품질 혁신**

| 항목 | 내용 |
|------|------|
| 🎖 리랭커 역할 | 초기 검색 Top-100에서 최적 Top-5를 정밀 선별 |
| ⚔️ Cross-Encoder | 쿼리+문서 통합 인코딩으로 양방향 어텐션 — 정확도 극대화 |
| 🤖 LLM Reranking | Pointwise / Listwise / Pairwise 3가지 방식 |
| 🔀 Hybrid Search | BM25 + Dense 결합, RRF(Reciprocal Rank Fusion)로 통합 |
| 🎭 HyDE | 가상 답변 문서를 먼저 생성 후 임베딩 → 검색 정확도 향상 |
| 📐 NDCG 측정 | 검색 순위 품질의 정량 평가 지표 |
| 📄 핵심 논문 | Reimers et al. (Sentence-BERT), Qin et al. (Pairwise LLM Ranking), Gao et al. (HyDE) |
| 💻 구현 | BGE Cross-Encoder + EnsembleRetriever(Hybrid) + HyDE 코드 |

---

### [7주차: Knowledge Graph RAG & Graph-based Retrieval Systems](week7.md)
**정형/비정형 지식을 연결하는 그래프 기반 RAG**

| 항목 | 내용 |
|------|------|
| 🕸 GraphRAG 필요성 | 벡터 검색으로는 불가능한 Multi-hop 관계 추론 해결 |
| 🏷 엔티티 추출 | NER로 인물·조직·장소·개념 노드 자동 식별 |
| 🔗 관계 매핑 | 트리플(Subject-Predicate-Object)로 지식 그래프 구축 |
| 🚶 Graph Traversal | BFS/DFS로 연쇄 관계를 따라 Multi-hop 추론 |
| 🌐 Microsoft GraphRAG | 커뮤니티 감지 + 계층적 요약으로 글로벌 쿼리 처리 |
| 🔄 Vector + Graph 하이브리드 | Dense 검색 → 그래프 순회 결합 아키텍처 |
| 📄 핵심 논문 | Edge et al. (Microsoft GraphRAG 2024), Cabot & Navigli (REBEL) |
| 💻 구현 | LLM 트리플 추출 + Neo4j Cypher QA Chain + LlamaIndex KG Index |

---

### [8주차: RAG Evaluation, Monitoring & Optimization](week8.md)
**실전 배포를 위한 품질 평가 및 지속적 관찰 파이프라인**

| 항목 | 내용 |
|------|------|
| 🧪 배포 전 테스트 | Noise Robustness, Negative Rejection, Privacy Breaches 시나리오 |
| 🛡 보안·브랜드 검증 | PII 감지, Malicious Use 차단, Toxicity 필터 |
| 📊 RAGAS 지표 | Faithfulness, Answer Relevancy, Context Precision/Recall |
| 🔭 모니터링 | Galileo Observe 실시간 추적 — 레이턴시·비용·품질 대시보드 |
| ⚙️ 최적화 결과 | Top-K 튜닝으로 **비용 23% 절감, 레이턴시 22% 단축** 실증 |
| 📄 핵심 논문 | Es et al. (RAGAS 2023), Saad-Falcon et al. (ARES, Stanford 2023) |
| 💻 구현 | RAGAS 자동 평가 + LangSmith 트레이싱 + Noise Robustness 테스트 코드 |

---

## 🗺 전체 RAG 파이프라인 흐름

```
사용자 질문 입력
      │
      ▼
[1주차] LLM 한계 이해 → RAG 필요성 확인
      │
      ▼
[2주차] 프롬프트 엔지니어링 (CoT, CoN, CoVe, ThoT)
      │
      ▼
[3주차] 문서 청킹 (Recursive / Semantic / Proposition)
      │
      ▼
[4주차] 임베딩 변환 (Dense / ColBERT / MRL)
      │
      ▼
[5주차] 벡터 DB 저장 및 검색 (HNSW / Pinecone / FAISS)
      │
      ▼
[6주차] 리랭킹 + 하이브리드 검색 (Cross-Encoder / HyDE / Hybrid)
      │
      ▼
[7주차] Knowledge Graph Multi-hop 추론 (Neo4j / GraphRAG)
      │
      ▼
[8주차] 품질 평가·모니터링·최적화 (RAGAS / LangSmith / Galileo)
      │
      ▼
  최종 답변 생성 (환각 없음, 출처 명시, 비용 최적)
```

---

## 📎 참고 리소스

| 자료 | 링크 |
|------|------|
| 공식 가이드라인 | [guidelines.md](guidelines.md) |
| GitHub 저장소 | [DaeyeonWon/self-study](https://github.com/DaeyeonWon/self-study) |
| 원본 참고 문서 | RAG Guide.pdf (Galileo AI) |
