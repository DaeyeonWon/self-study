---
layout: default
title: 3주차. Advanced Document Chunking & Context Engineering
---

# 3주차: Advanced Document Chunking & Context Engineering (고도화된 문서 분할과 토막 파이프라인의 극의)

아무리 훌륭한 프롬프트 통제기(Week 2)와 천문학적 벡터 인프라(Week 5)를 보유했다 하더라도, RAG 파이프라인의 **'입구'** 격인 데이터 수집단에서 문서가 쓰레기같이 토막 난다면 쓰레기가 들어가 쓰레기가 나오는(Garbage In, Garbage Out) 파멸을 면치 못합니다.

인간의 안구는 수천 페이지의 회계 장부를 보며 맥락을 자유자재로 이어 붙이지만, AI의 벡터 DB는 입력 문서를 작은 토막(Chunk) 단위로 가차 없이 난도질하여 고립된 단위 배열로 구겨 넣습니다. 이때 "이순신 장군은 명량 해전에서 / (뚝 끊김) / 13척의 배로 싸웠다" 와 같이 문맥 구조망의 허리가 잘려 절단되면, 이 조각을 찾아온 LLM은 주어가 누구인지 영구 상실하여 답변을 날조합니다. 이 끔찍한 맥락 파단(Context Fragmentation)의 저주를 원천 봉쇄하는 혁명적 기법 체계를 다룹니다.

---

## 1. 청킹(Chunking)의 파괴적 진화론: 단절에서 유기체로 

초창기 모델들은 단순히 500자 단위, 1000토큰 단위로 무자비하게 텍스트를 기계톱으로 썰어버리는 Naive Fixed-size Chunking을 지향했습니다. 하지만 현대 엔터프라이즈 환경은 이를 버리고 **의미 단위 생태계 분할(Semantic Split)** 로 이동했습니다.

![Advanced Chunking Techniques](assets/images_new/Fig_4_1_page_40.png)
*Fig 4.1: [어드밴스드 청킹 기법 (Advanced Chunking)] 특정 파서를 사용해 Chunk Size(50)와 Overlap(15) 설정을 튜닝하여, 문맥의 끄트머리 꼬리를 다음 청크의 앞머리에 교집합시켜 맥락 단절을 막는 오버랩 튜닝의 시각화 파이프.*

단순 글자 수 쪼개기를 넘어서, 문서의 HTML 태그나 Markdown 헤더의 논리 트리를 보존하는 구조 인식 분할(Structural Parsing)과 문서의 앞뒤를 참조하는 계층형 로직이 시장을 지배하기 시작합니다.

---

## 🌟 토막 단절의 맹점을 부수는 전설적 논문 및 SOTA 아키텍처 완전 해부

텍스트의 물리적 뼈대를 끊지 않고 유기체적 생명력을 보존하기 위해 등장한 학계와 업계의 최신 메타 방법론들을 깊이 들여다봅니다. 단순 PDF의 범주를 아득히 뛰어넘어 실제 인더스트리의 코어 인사이트를 돌출시킵니다.

### 📜 1. 의미 기반 쪼개기 시스템 (Semantic Chunking & Splitting)
**[핵심 아키텍처 / 프레임워크 패러다임]** *LlamaIndex Semantic Splitter Node Parser*
* **해설:** 문장 부호 제약 없이, 문장과 문장 사이의 '임베딩 거리(유사도)'를 미친 듯이 실시간으로 계산합니다. 만약 1번 문장과 2번 문장의 주제 텐서가 갑자기 급변하여 코사인 각도가 낮아진다면, "아, 여기서부터 단락 주제가 바뀌었군!" 이라고 AI 스스로 판단해 그 틈새를 가위로 잘라내는 지능형 자가 절단 기법입니다.
* 💡 **핵심 산업계 Insight:** 법률 문서나 긴 정책 매뉴얼에서 진가를 폭발시킵니다. "계약 파기 위약금 조항"과 "보증 기간 조항"이 물리적 글자 수의 제약 때문에 엉뚱하게 반반 갈라져 섞이는 재앙을 아예 100% 원천 봉쇄해버리는 의미론적 단락 분해의 바이블.

### 📜 2. 후기 청킹 패러다임 (Late Chunking의 대반란)
**[혁신 논문 모델]** *Late Chunking: Jina AI & BAAI Research 트렌드 (2024)*
* **해설:** 기존 멍청한 방식들은 "1. 텍스트를 토막낸다 -> 2. 임베딩 모델에 넣어 번호판(벡터)을 판다" 형식이다 보니, 토막이 잘리면 텍스트가 숲을 잃었습니다. Jina AI 등은 미친 역발상을 꾀합니다. **"1. 토막 내기 전에 아예 거대한 책 1권을 통째로 임베딩 모델 롱 컨텍스트에 밀어 넣어 전체 문단 간의 Attention(교차 의미망)을 다 계산시킨다 -> 2. 그 후 의미가 가득 충전된 상태에서 나중에 잘라낸다(Late Chunking)."**
* 💡 **핵심 산업계 Insight:** "사과"라는 청크 덩어리를 잘라낼 때, "이건 먹는 사과가 아니라 스티브잡스의 아까 그 사과야"라는 전 우주의 배경 맥락 지식을 영원히 품고 절단되게 하여 극도의 탐색 적중률 폭발을 가져오는 SOTA 트랙.

### 📜 3. Small-to-Big Retrieval (Parent-Child 문서 역추적 계층화)
**[아키텍처 로직]** *Auto-Merging Retriever & Parent Document Retreiver*
* **해설:** 벡터 데이터베이스에 저장할 때는 검색 레이더의 정밀 포착 효율을 극대화하기 위해 극도로 쪼그맣게 '명사형 1줄(Child)'로 잘게 부숴 저장합니다. 하지만 검색되어 LLM 프롬프트에 배달해줄 때는, 그 1줄이 원래 붙어있던 무식하게 거대한 '원본 부모 페이지 전체(Parent)'를 통째로 보쌈하듯 딸려 인입시켜 보내주는 2단계 스왑(SWAP) 아키텍처.
* 💡 **핵심 산업계 Insight:** "검색은 바늘구멍 조준경으로 예리하게 찾고 (정밀도 상승), 답변은 광활한 숲 배경 설명으로 풍성하게 먹인다 (문맥 단절 보존)" 는 가장 완벽하고 극악적인 엔터프라이즈 모순 해결 콤보 설계입니다. Elasticsearch 등과 결합할 때 최고의 포텐셜을 발휘합니다.

### 📜 4. RAPTOR: 거시의 세계를 압축 요약의 피라미드로 세우다 
**[논문]** *RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval (Sarthi et al., 스탠포드 2024)*
* **해설:** 앞선 1~2페이지 세부 토막 청킹의 한계는, "해리포터 1편~7편 전체를 통틀어 주인공의 사상적 성장을 1줄로 요약해봐" 와 같은 전 우주 통합형 쿼리(Global Query) 앞에서는 맥을 못 춘다는 것입니다. RAPTOR는 이런 멍청함을 부수기 위해 문서를 나무 계보로 짭니다. 밑바닥 청크(잎사귀)들을 끼리끼리 묶어 융합한 뒤 LLM으로 요약하고 상위 가지 청크로 통합 격상시키는 과정을 반복해 거대 최상단 서머리 노드 피라미드를 영구 적립합니다. 질문 스케일에 따라 검색하는 높이와 층계를 자동 판독 발동하는 시스템.
* 💡 **핵심 산업계 Insight:** 후에 7주차에 다룰 Graph RAG와 결합될 때 엄청난 광역 파급을 일으킵니다. 사내 데이터가 수십만 건의 법원 판례일 때, 파편화된 개별 문서를 뒤지는 걸 넘어 "최근 10년간 판결의 추세 요약 숲"이라는 새로운 요약 단서를 기계 스스로 추출 창조해 가지고 있는 권능을 제공합니다.

---

## 💻 [Implementation Frameworks] LlamaIndex 기반 Advanced Chunking & Hierarchical Parse
단순히 글자 수로 쪼개지 않고, Small-to-big 로직을 접목하거나 문장의 의미로 계층화하는 고도화된 파서는 **LlamaIndex** 생태계에서 가장 우아하고 아름답게 통제 구축됩니다.

```python
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SemanticSplitterNodeParser, HierarchicalNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding

# 1. 원시 문서 로드 
documents = SimpleDirectoryReader("./data/enterprise_docs").load_data()

# 2. Semantic Splitter (의미 단위 자율 컷팅 분할기) 초기화
embed_model = OpenAIEmbedding()
semantic_splitter = SemanticSplitterNodeParser(
    buffer_size=1, 
    breakpoint_percentile_threshold=95, 
    embed_model=embed_model
)

# 3. 혹은, Small2Big Retrieval을 돕는 부모-자식 다단계 계층 파서망 가동
hierarchical_splitter = HierarchicalNodeParser.from_defaults(
    chunk_sizes=[2048, 512, 128] # 거대 부모 -> 자식 -> 말단 손자 단계로 피라미드 노드 폭격 생성
)

# 4. 문서를 지능형 노드(청크) 로직으로 치환 연산 변환
nodes = hierarchical_splitter.get_nodes_from_documents(documents)
print(f"문맥 분절을 완벽 방어하며 쪼갠 생태계 청크 계보수 총량: {len(nodes)}개 파편")
```

---

## 마무리하며 지성의 조각화 마스터

이번 3주 차 과정에서는 방대한 엔터프라이즈의 무질서 텍스트 덩어리를 LLM의 입 천장에 맞게 정교한 횟감으로 썰어내는 기술인 **문서 청킹 구조론의 SOTA 방법론 (Semantic, Late Chunking, RAPTOR, Small2Big)** 전반을 지독하게 도해했습니다. 아무리 큰 문서라도 잘게 부수면 무너지는 한계를 보완하여 문맥 핏줄을 부모-자식 관계로 잇는 위대한 인사이트들을 흡수했습니다.
다음 4주 차 대서사시에서는, 이렇게 정교하게 잘라낸 언어 데이터 조각들을 수학적 공간의 무중력 허공 X-Y-Z 행렬 자성 텐서 숫자 배열로 치환 변형해버리는 마법의 통역 신경망, **Embedding Models & Representation Learning (밀집 벡터 표현학 파이프라인의 진수)** 으로 깊이 잠수하여 우주의 속을 관찰 격파 들어가보겠습니다! 돌격!
