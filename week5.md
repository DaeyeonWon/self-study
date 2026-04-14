---
layout: default
title: 5주차. Vector Databases & Retrieval Architecture Design
---

# 5주차: Vector Databases & Retrieval Architecture Design
> 엔터프라이즈급 데이터 저장소 선정 및 시스템 설계

벡터 DB는 임베딩으로 변환된 수백만~수십억 개의 벡터를 저장하고 초고속으로 유사도 검색을 수행하는 특화 데이터베이스입니다. 올바른 DB 선택과 아키텍처 설계는 검색 속도·비용·보안 모두에 영향을 미칩니다.

---

## 1. 벡터 데이터베이스 선택: 오픈소스 vs 상용

### 이론 설명

벡터 DB를 선택할 때는 성능 지표뿐 아니라 운영 방식, 보안 요건, 확장성을 종합적으로 고려해야 합니다.

### PDF 원본 자료

<img src="assets/images_new/Fig_4_3_page_81.png" width="600">

*Fig 4.3: 주요 벡터 데이터베이스 기능 및 성능 비교 차트 (PDF p.81)*

<img src="assets/images_new/Table_4_3_page_83.png" width="600">

*Table 4.3: Pinecone, Milvus, Weaviate, Qdrant 등 벡터 DB 상세 비교표 (PDF p.83)*

### 주요 벡터 DB 비교

| DB | 유형 | 인덱스 | 특징 | 최적 상황 |
|----|------|--------|------|----------|
| **FAISS** | 오픈소스 | IVF, HNSW, PQ | Facebook AI 개발, 초고속 | 연구/소규모, 인메모리 |
| **Milvus / Zilliz** | 오픈소스/클라우드 | HNSW, IVF | 분산 아키텍처, 대규모 | 대규모 온프레미스 |
| **Qdrant** | 오픈소스/클라우드 | HNSW | 고급 필터링, 페이로드 필터 | 필터링 중요 시나리오 |
| **Weaviate** | 오픈소스/클라우드 | HNSW | 멀티모달, 그래프 지원 | 복합 데이터 타입 |
| **Pinecone** | 완전 관리형 SaaS | 독자 인덱스 | 인프라 관리 0, 엔터프라이즈 | 빠른 배포, 관리 최소화 |
| **Chroma** | 오픈소스 | HNSW | 개발자 친화적 API | 프로토타이핑 |

---

## 2. 엔터프라이즈 필수 기능

### 이론 설명

B2B 운영 환경에서는 단순 검색 성능 외에 보안·거버넌스 기능이 핵심 선택 기준입니다.

**필수 엔터프라이즈 체크리스트:**
- **SOC-2 Type II 인증**: 데이터 보안 감사 준수
- **SSO(Single Sign-On) 통합**: SAML/OIDC 기반 중앙 인증
- **RBAC(Role-Based Access Control)**: 부서별 벡터 접근 권한 분리
- **Rate Limiting**: 비정상 접근 트래픽 차단
- **VPC Peering / Private Endpoints**: 인터넷 비노출 연결

---

## 3. 인덱스 종류와 성능 최적화

### 이론 설명

**Exact (Flat) Index**: 모든 벡터 전수 비교. 100% 정확, 데이터 수에 비례하는 O(n) 시간 복잡도.

**HNSW (Hierarchical Navigable Small World)**: 그래프 계층 구조로 근사 검색. O(log n) 복잡도.

### 관련 논문

**📄 Efficient and Robust Approximate Nearest Neighbor Search Using HNSW (Malkov & Yashunin, 2016)**
- HNSW는 현재 99%의 상용 벡터 DB의 디폴트 인덱스
- 검색 속도는 Flat 대비 수천 배 빠르고, Recall@10 기준 95% 이상 유지
- **핵심 구조**: 상위 계층(고속도로)에서 대략적 방향을 잡고, 하위 계층(골목길)에서 정밀 탐색

**📄 Product Quantization for Nearest Neighbor Search (Jégou et al., INRIA, 2011)**
- 벡터를 sub-vector로 분할하고 각각을 양자화하여 저장 공간 기하급수적 감소
- 1536차원 float32 벡터(6KB) → 32바이트로 압축 (187:1 압축비)
- IVF(Inverted File Index)와 결합되어 FAISS의 IVF-PQ 방식으로 대규모 시스템에 채택

### 아키텍처 다이어그램

<br>
<img src="assets/images_new/mermaid_w5_0.png" width="80%" style="margin: 10px 0; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); background-color: white; padding: 10px;">
<br>

---

## 4. 필터링 전략: Pre vs Post-filtering

### 이론 설명

메타데이터 필터(날짜, 카테고리 등)와 벡터 검색을 결합할 때 순서가 성능에 큰 영향을 미칩니다.

- **Pre-filtering**: 먼저 메타데이터로 후보 축소 → 축소된 집합에서 벡터 검색. **정밀도 높음, 재현율 위험**
- **Post-filtering**: 벡터 검색으로 Top-K 추출 → 메타데이터 필터 적용. **재현율 높음, Top-K 손실 위험**

---

## 5. 비용 절감: Binary Quantization & Disk Index

### 이론 설명

**Binary Quantization**: float32(32비트) 벡터를 단 1비트(0 또는 1)로 압축. 저장 공간 32배 절감. 검색 속도 25배 향상. 정확도는 약 5% 감소.

**Disk-based Index (DiskANN)**: RAM 대신 SSD를 활용하여 수십억 벡터를 저장. RAM 비용 90% 이상 절감.

### 관련 논문

**📄 DiskANN: Fast Accurate Billion-point Nearest Neighbor Search on a Single Node (Jayaram et al., Microsoft Research, 2019)**
- 단일 서버로 10억 벡터의 ANN 검색을 1ms 미만 레이턴시로 달성
- 비용 효율: Azure 기준 동일 성능 대비 클러스터 서버 비용 60% 절감

---

## 6. 전체 RAG 아키텍처 설계 (PDF p.117-120)

### 이론 설명

실제 프로덕션 RAG 시스템은 단순히 벡터 DB 쿼리를 넘어 여러 컴포넌트의 유기적 통합이 필요합니다.

**핵심 컴포넌트:**
1. **사용자 인증 (Auth)**: SSO/RBAC 기반 접근 제어
2. **입력 가드레일 (Input Guardrails)**: 프롬프트 인젝션, 유해 콘텐츠 필터
3. **쿼리 리라이터 (Query Rewriter)**: 대화 히스토리 기반 질문 정교화
4. **하이브리드 검색**: Dense + Sparse 복합 검색
5. **리랭커**: 검색 결과 품질 재정렬
6. **출력 가드레일 (Output Guardrails)**: PII 마스킹, 톤 검증

### PDF 원본 자료

<img src="assets/images_new/Fig_4_4_page_94.png" width="600">

*Fig 4.4: 전체 엔터프라이즈 RAG 아키텍처 구성 요소 플로우 다이어그램 (PDF p.94)*

<img src="assets/images_new/Fig_4_5_page_116.png" width="600">

*Fig 4.5: 쿼리 처리 파이프라인 단계별 구성 (PDF p.116)*

---

## 💻 구현: 벡터 DB 실습

### 관련 프레임워크 및 라이브러리

| # | 라이브러리 / 서비스 | 특징 |
|---|-----------|------|
| 1 | **FAISS (Meta AI)** | CPU/GPU 지원, IVF·HNSW·PQ 인덱스, 연구용 표준 |
| 2 | **Qdrant** | Rust 기반 고성능, 고급 필터링(payload filter), REST/gRPC |
| 3 | **Milvus / Zilliz** | 분산 아키텍처, 수십억 벡터 스케일, GPU 인덱스 |
| 4 | **Pinecone** | 완전 관리형 SaaS, 엔터프라이즈 SLA, Serverless |
| 5 | **Weaviate** | 멀티모달 지원, GraphQL API, 모듈형 벡터라이저 |
| 6 | **Chroma** | 개발자 친화적 API, 인메모리/영속 전환 용이 |
| 7 | **pgvector** | PostgreSQL 확장, 기존 RDB 인프라 활용 |
| 8 | **LanceDB** | 서버리스, 디스크 기반, Lance 컬럼나 포맷 |
| 9 | **Vespa (Yahoo)** | 하이브리드 검색(벡터+BM25+필터) 네이티브 결합 |
| 10 | **Marqo** | 멀티모달(텍스트·이미지) 통합 벡터 검색 엔진 |
| 11 | **Vald (Yahoo Japan)** | 분산 ANN 검색, 대규모 실시간 업데이트 특화 |
| 12 | **Redis Vector Search** | Redis Stack 기반, 캐시+벡터 검색 통합, 저지연 |
| 13 | **Turbopuffer** | 서버리스, 저비용 벡터 스토리지, 필터링 최적화 |

### 클라우드 서비스

| 서비스 | 벡터 규모 | 특징 |
|--------|---------|------|
| **Pinecone Serverless** | 무제한 (종량제) | 관리 0, 엔터프라이즈 SLA |
| **Azure AI Search** | 수십억 건 | OpenAI 네이티브 통합 |
| **Amazon OpenSearch** | 페타바이트급 | 기존 ES 인프라 활용 |
| **Google Vertex AI Matching Engine** | 수십억 건 | ScaNN 기반 초고속 |
| **Weaviate Cloud** | 클러스터 자동 확장 | 멀티모달 지원 |

### 코드 샘플 1: FAISS 인덱스 구축 및 검색

```python
import faiss
import numpy as np
from openai import OpenAI

client = OpenAI()

def get_embedding(text: str) -> np.ndarray:
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=text,
        dimensions=1536
    )
    return np.array(response.data[0].embedding, dtype=np.float32)

# 문서 임베딩 생성
documents = [
    "파이썬은 간결한 문법을 가진 프로그래밍 언어입니다.",
    "머신러닝은 데이터에서 패턴을 학습하는 AI 분야입니다.",
    "RAG는 LLM의 지식 한계를 외부 검색으로 보완합니다.",
    "오늘 저녁 메뉴는 삼겹살 어떨까요?",
]

doc_embeddings = np.array([get_embedding(doc) for doc in documents])

# HNSW 인덱스 구성 (M=16: 각 노드당 16개 연결)
dimension = 1536
index = faiss.IndexHNSWFlat(dimension, 16)
index.hnsw.efConstruction = 200  # 구축 시 정확도 (높을수록 느리나 정확)
index.add(doc_embeddings)

# 검색
query = "LLM의 환각 문제를 해결하는 방법은?"
query_emb = np.array([get_embedding(query)])

index.hnsw.efSearch = 50  # 검색 시 정확도 설정
distances, indices = index.search(query_emb, k=2)  # Top-2 검색

print("검색 결과:")
for dist, idx in zip(distances[0], indices[0]):
    print(f"  유사도: {1 - dist:.4f} | 문서: {documents[idx]}")
```

### 코드 샘플 2: Pinecone Serverless 엔터프라이즈 구축

```python
import os
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
openai_client = OpenAI()

# 인덱스 생성 (없으면 신규 생성)
index_name = "enterprise-rag-v1"
if index_name not in [idx.name for idx in pc.list_indexes()]:
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index(index_name)

# 벡터 업서트 (문서 + 메타데이터 함께 저장)
def upsert_documents(documents: list[dict]):
    """
    documents: [{"id": str, "text": str, "metadata": dict}, ...]
    """
    vectors = []
    for doc in documents:
        emb = openai_client.embeddings.create(
            model="text-embedding-3-large",
            input=doc["text"],
            dimensions=1536
        ).data[0].embedding

        vectors.append({
            "id": doc["id"],
            "values": emb,
            "metadata": {
                **doc["metadata"],
                "text": doc["text"]  # 검색 후 텍스트 복원용
            }
        })

    # 배치 단위로 업서트 (Pinecone 최대 100개/배치)
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        index.upsert(vectors=vectors[i:i+batch_size])

# RBAC: 메타데이터 필터로 부서별 접근 제어
def search_with_rbac(query: str, user_dept: str, top_k: int = 5) -> list:
    """부서별 접근 권한 필터링을 적용한 검색"""
    query_emb = openai_client.embeddings.create(
        model="text-embedding-3-large",
        input=query,
        dimensions=1536
    ).data[0].embedding

    results = index.query(
        vector=query_emb,
        top_k=top_k,
        filter={
            "$or": [
                {"access_level": {"$eq": "public"}},
                {"department": {"$eq": user_dept}}  # 본인 부서 문서만 접근
            ]
        },
        include_metadata=True
    )

    return [
        {
            "text": match.metadata["text"],
            "score": match.score,
            "source": match.metadata.get("source", "unknown")
        }
        for match in results.matches
    ]

# 사용 예시
search_results = search_with_rbac(
    query="2024년 마케팅 전략은?",
    user_dept="marketing"
)
```

---

다음 주차 → [6주차: Reranking Models and Hybrid Retrieval](week6.md)
