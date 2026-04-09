---
layout: default
title: 5주차. Vector Databases & Retrieval Architecture Design
---

# 5주차: Vector Databases & Retrieval Architecture Design (벡터 데이터베이스 인프라 구조학 및 거대 검색 아키텍처 설계)

지난 4주차를 통해 우리는 조각난 문서 파편들을 수학적 기하 의미를 함축한 '천문학적 고차원(1536차원) 숫자 배열(Dense Vector)'로 치환했습니다. 기업의 1억 개 문서가 모두 차원 공간에 뿌려졌습니다. 사용자가 질문할 때 이 수많은 별들 사이에서 0.1초 만에 최적의 정답 문서 점을 찾아내려면 어떻게 해야 할까요?
이를 위해 구축된 초고속 수색망 인프라의 하드코어 혁명, **벡터 데이터베이스(Vector Database)** 의 내부 코어 ANN 구동 원리와 엔터프라이즈 모노리틱 클러스터 아키텍처를 심층 해부합니다.

---

## 1. 기존 데이터베이스와의 궤를 달리 하는 벡터 DB

전통적 스칼라 관계형 RDB(MySQL 등)는 정직한 행(Row)과 열(Column) 격자형 스키마 아래, 데이터를 규격화시켜 수납합니다. `SELECT * FROM table WHERE item='사과'` 와 같은 1차원적인 스펠링 절대 일치 매칭은 빠르지만, "어딘가 슬프지만 끝엔 감동적인 청춘 소설 글귀 찾아줘" 식의 감성 지향적 유사도 질의는 원천적으로 불가능합니다.

이를 부수고 탄생한 **벡터 데이터베이스(Vector Database)** 는 데이터를 엑셀 테이블에 넣는 것이 아니라, 수천 차원 공간 허공에 찍힌 미아 별들로 띄워 군집 형태로 저장합니다. 

![Vector DB Architecture](assets/images_new/Fig_4_3_page_81.png)
*Fig 4.3: [Vector DB Comparison] Pinecone, Milvus, Weaviate, Qdrant 등 글로벌 메이저 벡터 DB들의 HNSW, IVF(PQ) 지원 성능표를 적나라하게 비교한 백서 차트.*

---

## 2. ANN (Approximate Nearest Neighbor): 초고도 유사도 탐색 엔진의 두뇌

우주 허공에 뿌려진 10억 개의 점들과 사용자의 질문 점 간의 거리를 일일이 코사인 연산(K-NN 전수 탐색)하면 서버가 다운됩니다.
이를 0.01초 만에 해결하는 알고리즘이 **근사치 탐색(ANN)** 엔진입니다.
탐색 1위 결과의 '완벽한 100% 무결점 매칭 정확도'를 0.1% 양보하는 대가로, 검색 속도를 수만 배 폭등시키는 우아한 알고리즘입니다.

![ANN Tree Strategy](assets/images_new/Fig_5_2_page_137.png)
*Fig 5.2: [Test for Retrieval Quality] 광염합성(Photosynthesis) 질의를 검색했을 때, 해당 문서들이 일방적으로 스펠링만 일치하는 것이 아니라 Relevancy(유사성), Preciseness(정밀도)를 모두 충족하는지를 평가하는 QA 검증 과정.*

---

## 🌟 벡터 데이터베이스 논문 아키텍처
아무리 모델의 벡터가 정교해도 0.01초 만에 디스크에서 꺼내오지 못하면 서비스는 파멸합니다. 이 불가능한 공간 연산 지연 한계(Latency bottleneck)를 돌파한 천재 수학자들의 학술적 발자취를 추적합니다.

### 📜 1. HNSW (Hierarchical Navigable Small World)
**[논문]** *Efficient and Robust Approximate Nearest Neighbor Search... (Malkov et al., 2018)*
* **해결 기술:** 세상 99%의 상업용 벡터 DB가 채용하는 궁극의 최강 탐색 노드 네트워크망. 스키장 슬로프처럼 여러 위상 층으로 단차(Hierarchical)를 설계합니다. 최상단에는 대표 바운더리 오메가 대장 점들만 있고, 밑으로 내려갈수록 촘촘한 개미 층이 나옵니다. 쿼리가 최상단에서 주변 대장들을 만나 폭넓은 궤적을 찾고, 즉시 엘리베이터를 타고 좁아진 하위 층으로 점프 수직 하강하여 극소 구역에서만 탐색을 완성합니다.
* **의의:** 기존 전수 계산 `O(N)`에서 시간 로직 비약 `O(log N)` 으로 급강하시킨 마일스톤 모델.

<div class="mermaid">
graph TD
    subgraph 최상단 층 L2
    L2_A(대장 문서 A) --- L2_B(대장 문서 B)
    Q((질문 낙하산)) -.->|가장 흡사한 B 방향| L2_B
    end
    subgraph 지상 층 L1
    L1_B(문서 B 하위) --- L1_C(문서 C)
    L2_B ==>|수직 하강| L1_B
    L1_B -.-> L1_C
    end
    subgraph 바닥 실검 전수 층 L0
    L0_C(말단 문서 C) --- L0_Target[[목표 타겟 D!]] --- L0_E
    L1_C ==>|초좁은 반경 도달| L0_C
    L0_C -.-> L0_Target
    end
</div>

### 📜 2. FAISS: 10억 단위 매머드급 병렬 특공대의 폭주
**[논문]** *Billion-scale similarity search with GPUs (Johnson et al., Meta Research, 2019)*
* **해결 기술:** HNSW가 CPU용이라면, 페이스북은 10억 스케일을 감당하기 위해 GPU 코어 수천 개를 방정식 연산에 때려박는 FAISS를 런칭했습니다. 특히 **IVF-ADC** 기법으로 우주 공간을 수만 개의 셀(격자 방)로 칼질해 찢고, 벡터 배열들을 **양자화 압축(Product Quantization, PQ)** 무지막지 타격 기술로 찌그러뜨려 RAM 캐시에 억지로 상주시켜 수십억 병렬 연산을 이룩했습니다.

### 📜 3. Milvus (클라우드 분산 샤딩 메커니즘)
**[아키텍처]** *Milvus: A Purpose-Built Vector Data Management System (Wang et al., SIGMOD 2021)*
* **해결 기술:** 검색 및 쿼리 파싱만 담당하는 가벼운 노드 컴퓨터(Compute Node)와, 실제 데이터 파편이 단단히 저장되는 노드(Storage Node / S3)를 원천적으로 이산시켰습니다 (마이크로서비스). 라이브 중인 서브 인프라 머신을 수평적 무한 복제 병렬화 시켜 무중단 무정지 확장이 가능한 고가용 엔터프라이즈 사옥 DB의 표준을 완성했습니다.

<div class="mermaid">
flowchart TD
    Proxy[Proxy 로드밸런싱 마스터] --> Compute1[연산 Node 1]
    Proxy --> Compute2[쿼리 라우터 Node N]
    Compute1 & Compute2 --> Storage[MinIO / S3 공용 분산 스토리지 샤딩 클러스터망]
</div>

### 📜 4. ScaNN: 양자화 오차의 구원
**[논문]** *Accelerating Large-Scale Inference with Anisotropic Vector Quantization (Guo et al., Google 2020)*
* **해결 기술:** FAISS의 PQ 양자화로 인해 발생하던 원본 데이터 손실에 의한 오답 에러를, '비등방성(Anisotropic) 연산'이라는 기법으로 방어해 냈습니다. 거리를 계산할 때 방향성에 필수적인 주요 인자는 절대 훼손하지 않고 노이즈 성분 위주로만 용량을 깎아내려 치는 수식을 도입하여 속도와 1위 정확도를 다 잡았습니다.

### 📜 5. DiskANN: 메모리 굴레를 박살 낸 짠돌이 혁신
**[논문]** *DiskANN: Fast Accurate Billion-point NN Search (Subramanya et al., Microsoft 2019)*
* **해결 기술:** RAM 카드에 벡터를 다 올리려면 지출 한계 비용이 박살납니다. MS는 값싸고 큰 하드디스크(SSD)와 비싸고 작은 RAM을 직조 융합한 **Vamana 그래프**를 고안해냈습니다. RAM엔 네비게이션 표지판 캐시 그래프만 두고, 무거운 수조 개의 팩트 배열은 SSD에 박아둬 쿼리가 네비게이션을 타고 목적지에 도착했을 때 한 번만 SSD 디스크 엑세스를 때리는 "메모리-디스크 병행 경제 탐색기"로 빅테크를 구원했습니다.

### 📜 기타 HNSW 기반 벡터 인프라 혁신 백서
6. **SPANN:** DiskANN을 이어받아 경계면 라우팅을 붙인 극한 하이브리드 인프라 연구.
7. **Pinecone 아키텍처:** 클라우드 서버리스(SaaS) 기반 관리 프리 상용 시스템, 유지보수 오버헤드를 0으로 날림.
8. **Qdrant / Weaviate 엔진:** Rust 언어로 코드를 저수준 작성해 C++을 이기는 스피드 확보 및 파괴적 Payload 기반 메타데이터 사전 필터링 구조 생태계 점령.

---



## 💻 [Implementation Frameworks] Pinecone Serverless 클라우드 구축
서버 관리 없이 인프라를 무한 확장할 수 있는 SaaS 기반 Pinecone 백엔드 구축 샘플입니다.
```python
from pinecone import Pinecone, ServerlessSpec

# 1. Pinecone Client 초기화
pc = Pinecone(api_key="유어-파인콘-api-키")

# 2. 1536 차원의 Vector DB Index (방) 생성
index_name = "rag-master-index"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536, # OpenAI 임베딩 차원
        metric="cosine", # 유사도 함수: 코사인
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

# 3. Vector 추가 및 유사도 검색
index = pc.Index(index_name)
# index.upsert(...) # 텐서 데이터 주입
```

## 마무리하며

이번 과정에서는 거대한 문서를 무지성 좌표계로 단순 비교하던 한계를 극복하고, HNSW와 같은 트리, GPU 괴물 FAISS 등 수색 탐색망 병목 트래픽 레이어를 극복하는 아키텍트 시스템들을 파헤쳤습니다. 
하지만! 엔진이 아무리 초고속으로 퍼올려준 1, 2위 검색 문단이더라도, 그 순위를 우리가 직관적으로 봤을 때 '진정으로 치명적이고 완벽한 정답 문서'라고 확신할 수 있을까요? 
코사인 탐색망의 천박한 한계를 부수고 AI 채점관을 앉혀 순위를 갈아엎어 버리는 등용문 필터링 구조! 6주 차 **Reranking Models & Hybrid Retrieval Techniques (압박 면접 리랭킹 모델과 융복합 투트랙 기술 체계)** 에서 최종 검색 튜닝의 마법을 엿보겠습니다!
