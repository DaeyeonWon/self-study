---
layout: default
title: 3주차. Advanced Document Chunking & Context Engineering
---

# 3주차: Advanced Document Chunking & Context Engineering (고급 문서 청킹, 구문 분석과 문맥 결찰 엔지니어링 생태계)

RAG의 강력함은 방대한 양의 사내 사일로(Silo) 데이터를 LLM과 융합하는 데이터 독점력에 있습니다. 하지만 수십만 페이지짜리 법률 위키피디아, 반도체 제품 스펙 매뉴얼, 사규집을 통째로 LLM의 '컨텍스트 윈도우(Context Window)' 식도에 우겨 던져버리면 모델 신경망이 터져 다운되거나 기절하는 정보 소화 불량 증세(OOM 에러)에 빠집니다.

이를 방지하기 위해 문서를 작고 일관된 '가장 완벽한 의미'를 가진 데이터 논리적 조각 덩어리(Chunk) 단위로 파내어 저장하는 **문서 청킹(Document Chunking) 파서(Parser) 기법**과, 이렇게 산산조각 흩뿌려진 파편들이 자신의 출처 정체성을 잃지 않게 강력한 메타데이터 닻을 묶어주는 **문맥 엔지니어링(Context Engineering)** 기술 생태계의 모든 학술적 코어를 이번 주차에 아주 매우 깊숙이 살펴봅니다.

---

## 1. 전처리 과정의 심장마비: 왜 청킹(Chunking)이 RAG 성능 병목의 대법관인가?

모든 LLM은 처리할 수 있는 최대 토큰 입력 뇌용량 한계(Token Limits)를 구조적으로 가지고 있습니다. 백만 토큰 제한(Gemini 1.5 Pro) 등 어거지로 한계치를 늘려 무력 극복하더라도, 너무 많은 더미 정보(Noise context)가 함께 섞여 들어오면 정작 알짜배기 백금 보석 정보가 문서 텍스트 한가운데에 끼어 있을 때 이를 바보처럼 못 찾고 잃어버리는 'Lost in the Middle' 오류를 필연적으로 범하게 됩니다.

또한, 수만 자의 긴 문장을 통째로 하나의 데이터 포인트로 임베딩(Vector Transformation)하여 우주 좌표 하나 구석에 몰아 압축시켜 버리면, 그 안에서 언급된 수십 가지의 다양한 세부 기술 스펙과 감정 정보들이 전부 짬뽕되어 평균 회귀해버립니다(Average-out 희석 문제). 결국 뭉퉁그려진 희미한 노이즈 회색 좌표가 형성되어 정밀 스나이퍼 타겟 검색은 매칭 스코어가 떨어져 영원히 실패하게 됩니다.

> 🍔 **이해를 돕는 직관 예시: 거대 도서관 수박 깍둑썰기**
> 집채만 한 거대한 수박(수천 페이지 제품 매뉴얼 문서)을 믹서기 입구 병목(LLM 프롬프트)에 한 번에 통째로 들이밀어 넣을 수는 없습니다. 먹기 좋은 스푼 크기로 깍둑썰기를 해야만 부드럽게 유입됩니다. 하지만 수박을 아무렇게나 톱으로 무지성 난도질해서 껍질과 씨앗만 들어가는 최악의 파편 조각이 우연히 생긴다면? 모델은 그걸 읽다 퉤 뱉어버리고 엉뚱한 대답을 합니다. 의미의 달콤한 결이 칼날에 끊어지지 않고, 가장 조화로운 맛의 과육 단위(문단 문맥 등)로 아름답게 절단하는 수학적 예술 기술이 바로 스마트 청킹입니다.

![Chunking Concept Analysis](assets/images_new/Fig_4_1_page_40.png)
*Fig 4.1: [어드밴스드 청킹 기법 (Advanced Chunking)] 특정 Character Splitter를 사용해 Chunk Size(50)와 Overlap(15) 설정을 적용, 하나의 문단을 핑크, 블루, 옐로우 색상으로 자연스럽게 교차 분리한 청크 구조의 실례.*

---


![Chain of Thought](assets/images_new/Fig_3_1_page_21.png)
*Fig 3.1: [Chain of Thought Prompting] 테니스 공과 사과 계산 과정을 통해 산술 단계(Step 1, 2, 3)를 하나씩 강제 명시하게 하여, 모델이 단순 결론(오답 27)이 아니라 정답(9)을 찾도록 유도.*

![Chain of Note](assets/images_new/Fig_3_4_page_27.png)
*Fig 3.4: [Chain of Note Framework] 문서를 읽고 이것이 정답을 도출하기에 Relevant(관련유)인지 Irrelevant(무능)인지 AI가 먼저 평가 필터링하는 파이프라인.*

## 2. 청킹 아키텍처의 3대 진화 단계 패러다임

#
![Chain of Thought](assets/images_new/Fig_3_1_page_21.png)
*Fig 3.1: [Chain of Thought Prompting] 테니스 공과 사과 계산 과정을 통해 산술 단계(Step 1, 2, 3)를 하나씩 강제 명시하게 하여, 모델이 단순 결론(오답 27)이 아니라 정답(9)을 찾도록 유도.*

![Chain of Note](assets/images_new/Fig_3_4_page_27.png)
*Fig 3.4: [Chain of Note Framework] 문서를 읽고 이것이 정답을 도출하기에 Relevant(관련유)인지 Irrelevant(무능)인지 AI가 먼저 평가 필터링하는 파이프라인.*

## 2.1 Character/Token-based Chunking (단순 고정 길이 무지성 분할)
초창기 랭체인(Langchain)의 디폴트로 채택된 가장 원시적이고 C코딩으로 구현이 극히 쉬운 코어 기법입니다. 문맥과 인간의 언어를 아예 무시하고, 기계어 바이트 수 500자(문자) 단위, 혹은 트랜스포머 토큰 400개 단위로 무조건 톱날로 자르듯 텍스트를 절단합니다.
* **치명적 단점:** 인간의 한 문장이나 혹은 중요한 핵심 전문 용어(예: "인공지능")가 "인공", "지능" 두 청크 경계선 사이에서 우연히 절단되어(Truncation) 양쪽 조각에 나뉘어 버리는 대참사가 빈번해 앞뒤 텍스트 간 숨은 의미의 연결고리가 하찮게 끊어지고 RAG 검색 능력이 반토막 폭락합니다.

#
![Chain of Thought](assets/images_new/Fig_3_1_page_21.png)
*Fig 3.1: [Chain of Thought Prompting] 테니스 공과 사과 계산 과정을 통해 산술 단계(Step 1, 2, 3)를 하나씩 강제 명시하게 하여, 모델이 단순 결론(오답 27)이 아니라 정답(9)을 찾도록 유도.*

![Chain of Note](assets/images_new/Fig_3_4_page_27.png)
*Fig 3.4: [Chain of Note Framework] 문서를 읽고 이것이 정답을 도출하기에 Relevant(관련유)인지 Irrelevant(무능)인지 AI가 먼저 평가 필터링하는 파이프라인.*

## 2.2 Overlapping Sliding Window Chunking (오버랩 꼬리 물기 겹침)
무지성 고정 길이 자르기의 문맥 훼손 절단마를 그나마 봉합 완화하기 위해, 이전 청크의 맨 끝 단어들 50개(Overlap length) 버퍼를 다음 새로 시작하는 두 번째 청크의 맨 앞머리에 복사-중복으로 포함시켜 엮어 저장하는 방식입니다. 슬라이딩 윈도우 스캔 방식처럼 바느질하듯 엮습니다.

> 🔗 **이해를 돕는 예시: 풍경 파노라마 사진 바느질 촬영**
> 스마트폰 카메라로 산 정상에서 파노라마 풍경을 넓게 쭉 이어서 찍을 때, 다음 장면 사진이 어긋나 잘리지 않게 큰 도화지처럼 부드럽게 소프트 연계되도록 가장자리 전경을 의도적으로 살짝 겹치게 구도를 잡고 합성합니다. 오버랩 역시 잘린 의미의 이음새 역할을 하며 붕괴 안전망 역할을 훌륭히 수행합니다.

#
![Chain of Thought](assets/images_new/Fig_3_1_page_21.png)
*Fig 3.1: [Chain of Thought Prompting] 테니스 공과 사과 계산 과정을 통해 산술 단계(Step 1, 2, 3)를 하나씩 강제 명시하게 하여, 모델이 단순 결론(오답 27)이 아니라 정답(9)을 찾도록 유도.*

![Chain of Note](assets/images_new/Fig_3_4_page_27.png)
*Fig 3.4: [Chain of Note Framework] 문서를 읽고 이것이 정답을 도출하기에 Relevant(관련유)인지 Irrelevant(무능)인지 AI가 먼저 평가 필터링하는 파이프라인.*

## 2.3 Semantic Chunking & Structural Parser Extraction (의미 기반 형태 구조적 광학 청킹)
더 이상 단어나 글자 수를 세지 않는 고급 지능 단계입니다. NLP 언어 모델 구조 분석기나 머신러닝 파서(Parser)를 가동하여, 문장의 끝 마침표(`.`), 엔터 줄바꿈 기호, 혹은 인간이 쓴 문서의 HTML 헤더 태그(`<h1>`, `<h2>`)나 마크다운 구조 챕터를 광학적으로 지능 인지합니다. 이를 기반으로 철저하게 '하나의 테마 단락' 단위로 청크 볼륨을 고무줄처럼 축소/확장하며 유동성 있게 쪼갭니다. 테이블(표) 셀 안의 데이터는 가로세로를 묶어 인지하여 하나의 절대 쪼개지지 않는 캡슐 지식 단위 덩어리로 무적 유지해킵니다.

![Table Parsing in Chunking](assets/images_new/Fig_4_1_15_page_102.png)
*Fig 4.1: [어드밴스드 청킹 기법 (Advanced Chunking)] 특정 Character Splitter를 사용해 Chunk Size(50)와 Overlap(15) 설정을 적용, 하나의 문단을 핑크, 블루, 옐로우 색상으로 자연스럽게 교차 분리한 청크 구조의 실례.*

---

## 3. 문맥 엔지니어링 (Context Enrichment): 파편화된 조각들에 생명 줄 불어넣기

산산이 조각난 수십만 개의 문서 토막 파편들은 자신이 원래 '어느 1권의 위대한 책이나 법전'에서 비롯되었는지 그 거시적 시대 배경 정체성을 철저히 잃어버리는 일종의 고립된 '구조적 기억상실증'을 경험합니다. 이를 심혈관처럼 복원해 주는 것이 문맥 주입 엔지니어링입니다.

1. **메타데이터 꼬리표 부착 (Metadata Tagging Tracking):** 
   쪼개진 각 파편 청크 데이터 공간에 이 데이터가 "어느 계약서 문서 파일에서 가져왔는지(File ID)", "원문 작성 일자는 과거 언제인지", "어느 소제목 3장 파트 소속인지" 등의 메타데이터 Key-Value 꼬리표 태그를 벡터 DB의 속성망에 매핑 결찰합니다. 추후 RAG 검색 때 "2023년도 계약서 문서안에서만 찾아" 처럼 2차원 필터를 걸 수 있게 하는 무시무시한 강력 필터 무기가 됩니다.
2. **요약 압축 부착 기법 (Summary-Augmented / Parent-Child Chunking Tree):** 
   각 작은 미시 파편(자식 노드)들을 저장하기 직전에, 해당 문서 혹은 상위 챕터 전체의 포괄적 요약본(부모 노드)을 미리 가벼운 소형 LLM을 통해 짤막하게 추출 전처리 생성한 뒤, 작은 파편들 텍스트들 맨 맨 앞에 헤리포터 도장처럼 헤더로 강력하게 찍어 함께 전부 다 덧붙여줍니다. 이제 파편화된 조각 한 줌만 찾아 들여다봐도 전체 숲의 웅장한 맥락과 주인공 이름을 손쉽게 가늠할 수 있어 임베딩 엔진의 타격 검색 품질이 수십 배 폭증합니다!

> 🗂️ **매우 직관적 예시: 조선왕조실록 서적 낱장으로 찢어 빈 박스에 담기**
> 10만 권의 실록 백과사전들을 무자비하게 폭격해 찢어 박스에 담을 때, 그냥 누런 빈 종이만 두면 이 페이지가 무슨 왕 내용인지조차 절대 모릅니다. 매 낱장 종이 상단마다 의무적으로 주홍 글씨 포스트잇으로 `[조선 세종대왕 전집 - 제 3장 24p 집현전 사건]` 라고 백그라운드 라벨링(Metadata)을 달고 `[전체 요약: 한글 창제 당시 훈민정음 반포 과정에 대한 서사 내용]`을 요약해 압핀으로 써붙이는 치밀한 보강 아카이빙 작업이 일어납니다.

---

## 🌟 구조적 텍스트 청킹(Chunking)의 역사를 뒤집은 12대 최전선 아키텍처 논문
단순히 텍스트를 칼로 써는 방식을 넘어, 문맥을 입체적으로 3D 유지하고 정보의 거대한 연속성 파편화를 보존하기 위한 글로벌 천재 연구진들의 첨단 데이터 구조 공학 아키텍처 트리 모델 생태계들을 샅샅이 해부 전개 소개합니다.

### 📜 1. RAPTOR: 문서를 거대한 피라미드 나무 트리로 압축 요약하며 추상화하다
**[논문]** *RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval (Sarthi et al., 스탠포드 대학교, 2024)*
* **연구 배경:** "이 책의 결말 특정 주인공이 죽었어 살았어?" 같은 미시 돋보기 쿼리 서치는 일반 RAG로 풀립니다. 하지만 "이 동화책 책 100권 시리즈 전체에서 관통하는 궁극적 작가의 철학과 우주관 테마는 대략적으로 무엇인가?"와 같은 글로벌 거시 통합 통계 질문엔 RAG가 철저히 맹인처럼 박살났습니다. (숲을 융합해 보지 못하고 그냥 맨 앞 나뭇잎 조각 한두 개만 툭 뜯어와 검색하기 때문).
* **해결 기술 (Architecture):** 
  긴 문서를 짧은 말단 단말 청크(Leaf nodes) 조각들로 전부 쪼갠 뒤 거기서 멈추지 않습니다! RAPTOR 시스템이 인접한 이웃 청크들을 클러스터링으로 그룹 묶어, 하위 청크들을 아우르고 요약하는 더 큰 상위 부모 요약 청크 블럭을 상단에 생성(LLM Abstractive Summarization)합니다. 이를 나무구조 피라미드(Tree) 계층처럼 재귀적(Recursive)으로 계속 위로 쌓아 올려, 최종적 최상단 꼭대기엔 책 전체 내용을 포괄하는 거대한 슈퍼 카테고리 루트 요약 노드 청크까지 형성시킵니다.
* **의의:** 구체적 미시 팩트 검증은 제일 하위 계층 잎사귀 청크 영역에서 캐치 타격하고, 포괄적 통합 테마 질문은 제일 꼭대기의 부모 요약 청크에서 짚어내는, 즉 현미경(Local)과 거대 망원경(Global)의 초초광역 시야를 동시에 완벽히 만족 커버시키는 트리 구축 RAG 아키텍처의 찬란한 대지평을 마침내 기적적으로 실현했습니다.

<div class="mermaid">
graph BT
    L1[원본 말단 문단 A 청크] --> P1(1차 요약 노드 M1)
    L2[원본 말단 문단 B 청크] --> P1
    L3[원본 말단 문단 C 청크] --> P2(1차 요약 노드 M2)
    L4[원본 말단 문단 D 청크] --> P2
    P1 --> Root{최종 전 우주 통합 요약 루트 청크 탑단}
    P2 --> Root
    style Root fill:#f9d0c4,stroke:#e83e8c,stroke-width:2px
    style P1 fill:#d1ecf1,stroke:#17a2b8,stroke-width:2px
    style P2 fill:#d1ecf1,stroke:#17a2b8,stroke-width:2px
</div>

### 📜 2. Late Chunking: 먼저 온전히 뇌에 다 담고, 그 다음 뒤늦게 가위로 잘라라
**[최신 트렌드/백서]** *Late Chunking: Contextual Embeddings in Jina AI (Jina AI Research, 2024)*
* **연구 배경:** 일반적인 고전 랭체인 시대 RAG는 무조건 먼저 글 단락을 100조각으로 부수고 쪼갠(Early Chunk) 뒤, 그 잘려나간 파편 조각 단위별로 각각 임베딩 모델에 넣고 좌표점(Vector)을 부여했습니다. 이 과정에서 파편 앞뒤를 이어주던 핵심 명사가 잘려나가면서 문맥 이탈의 정보 누수 왜곡이 엄청나게 스며들었습니다.
* **해결 기술 (Architecture):**
  획기적으로 프로세스 연산 순서를 리버스 역전시킵니다! 문서 수십 쪽 분량 전체를 절대 쪼개지 않고 단박에 한 번 트랜스포머 장문 임베딩 모델(8K Token support 모델급) 궤도에 통채로 먹여 아주 깊이 투사(Encoding)시켜 버립니다. 그러면 문서 전체의 앞단락과 뒷단락 결론이 서로 그물 교차망처럼 맥락을 비비며 참조한(Global Attention Mechanism) 강력한 통맥락 토큰 텐서 배열들이 뇌세포 속에 형성됩니다. 바로 그 직후! 임베딩이 끝난 아주 깊은 장기 텐서 상태의 뇌 내부 공간 배열 구조 속에서, 이제서야 기계 수학적으로 단락 분절점 꼬리표를 찾아 뒤늦게 툭툭 떼어내 잘라서 조각(Late cut) 내어 벡터 DB에 담아 보관 분리합니다.
* **의의:** 결과론적으로 DB에 담긴 청크 덩어리 자체 외형은 500자 짧은 조각일지라도, 그 안의 매트릭스 DNA 숫자(벡터 배열)에는 이미 원본 책 전체의 거시적 맥락 은유 냄새와 앞 문맥 결론이 짙게 내포되어 응축 스며들어있게 되는 기적적인 컨텍스트 유지 효과가 발생합니다! 모델 검색 미아 방지율 최고의 신성입니다.

<div class="mermaid">
flowchart LR
    subgraph 고전적 무지성 방식 (Early Chunking)
    Doc1[전체 논문 문서] --> C1[가위로 쪼개기 조각 1] & C2[조각 2]
    C1 --> V1[(맥락 파괴된 짧은 벡터)]
    C2 --> V2[(가운데가 단절된 벡터)]
    end
    
    subgraph Late Chunking 극한의 혁신
    Doc2[전체 완전무결 문서 통채로] --> Embed_Model[Long-Context 통 임베딩 모델]
    Embed_Model --> Tensor[Global Attention 거대 맥락 텐서 배열 망상구조]
    Tensor --> TV1[(전체 숲의 맥락이 포함된 고밀도 벡터 청크 조각 1)] & TV2[(고밀도 청크 2)]
    end
    
    style Doc2 fill:#fff3cd,stroke:#ffc107
    style Embed_Model fill:#d4edda,stroke:#28a745
</div>

### 📜 3. Contextual Retrieval (문맥 기반 능동 검색 덧붙이기)
**[혁신 리포트]** *Introducing Contextual Retrieval (Anthropic Research, 2024)*
* **연구 배경:** 앞서 "메타데이터 부착"을 수동으로 배워봤지만, 파일명 정도 다는 가벼운 수준에서는 쪼개진 문구의 근원적 지시어 모호함이 완벽히 해결되지 않습니다. (예: "그 회사의 재무 성과가 작년 폭망했다"라는 청크에서 '그 회사'가 애플인지 삼성전자 소속 파편인지 모델은 절대 모름)
* **해결 기술:** 본문 책 전체 내용을 뼈대로 서버에 유지한 채, 별도의 백그라운드 LLM(Claude 등)이 각각 잘려진 수만 개의 짧은 청크 파편들을 보며 프롬프트로 질의 명령합니다. **"이 조각 글이 원본 메인 문서 전체 역사에서 구체적으로 누구의 어떤 사건 의미(Context)를 대변하고 있는지 완전 분석 추론해서 그 힌트를 서론 짧은 문장 헤더로 청크 앞에 억지로 생성해 붙여놔!"** 
* **의의:** 청크 앞에 "이 조각은 애플의 2023년 하반기 아이폰15 관련 재무 성과 부서 스펙에 대한 문단임" 이라는 컨텍스트 앵커 요약줄이 영구 강제 주입 결찰됩니다. 잃어버린 대명사 주어가 완벽 리커버리 복원되어 RAG의 타겟 코사인 매칭 확률이 기하급수적으로 폭증합니다.

### 📜 4. Dense X Retrieval (Proposition-based Chunking 명제 중심 분해 모델링)
**[논문]** *Dense X Retrieval: What Retrieval Granularity Should We Use? (Chen et al., 2023)*
* **연구 배경:** 보통 인간은 청킹을 '문장 단위(Sentence)' 단위나 '문단 길이 단위(Paragraph)'로 자릅니다. 하지만 한 긴 문장 안에는 사실 두세 가지의 상충하는 정보 "A는 사과를 샀으나, B는 배를 부셨다"가 공존하여 벡터 공간을 엉망으로 섞습니다.
* **해결 기술:** 텍스트를 문장 길이 단위로 자르는 패러다임을 타파하고, 문장 내부의 논리적 사실 뼈대인 최하위 입자 **명제(Proposition: 참/거짓을 판별 가능한 가장 팩트 지향적인 최소 단위 정보 주장구)** 레벨 단위로 문서를 극단적 분해 해체하여 각 명제 단위별로 벡터를 인덱싱 처리해 저장합니다. 검색 효율과 노이즈 차단에서 역대급 극상의 1순위 정제 정밀 성능 타겟력을 보여줍니다.

### 📜 5. DocQA & LayoutParser (다중 구조적 광학 문서 파싱 스키마 엔진)
**[논문/기술]** *LayoutParser: A Unified Toolkit for Deep Learning Based Document Image Analysis (Shen et al., 2021) / Unstructured.io Library*
* **해결 기술:** 기업의 문서는 순수 줄글 텍스트 txt가 아닙니다. 표, PPT 차트, 머릿말, 다단 2단 구조 PDF 혼합체가 극악의 형태로 더미를 이룹니다. 이 이미지급 PDF 파일들을 컴퓨터 비전 Object Detection (YOLO 기반 등) 모델 레이아웃 파서 라이브러리로 투과시켜 스캔합니다. 즉시 기계가 "아! 이 왼쪽 블록 덩어리는 이미지 캡션이고, 중앙 덩어리 상자는 핵심 데이터 테이블 표로 인식해 파괴하지 말고 보존해야지 캡슐화!" 하고 시각적 구조(Visual Semantic Layout) 뼈대 자체를 분석 유지하며 잘라내 데이터 무결성 파괴를 막아내는 OCR의 진화 체계 파서론입니다.

### 📜 6. TextTiling: NLP 분야의 파티션 역사를 연 위대한 고전
**[논문]** *TextTiling: Segmenting Text into Multi-paragraph Subtopic Passages (Hearst, 1997)*
* **의의:** 비록 30년이 지났으나 오늘날 Semantic Chunking이 탄생할 수 있었던 위대한 NLP 자연어 처리 기초 분할 알고리즘 논문입니다. 단어의 토큰 벡터가 확연히 주변과 달라지는 코사인 오차(Valley) 골짜기를 지능적으로 탐지하여, 주제 테마가 전환되는 블록 경계선을 자동으로 예리하게 감지해 칼질 컷하는 서브토픽 논리 수학 분할법의 조상급 바이블 모형.

### 📜 7. PARENT (테이블 표 데이터를 위한 표상 모델 변환)
**[논문]** *Handling Divergent Reference Texts when Evaluating Table-to-Text... (Dhingra et al., 2019)*
* **해결 기술:** 엑셀 표(Row/Column 구조) 데이터를 청킹해 일반 줄글 문장 문서 벡터 더미로 섞을 경우 속성이 어긋나 엉망이 됩니다. PARENT와 Table-to-Text 아키텍처는 이 격자형 숫자 테이블 좌표 구조 표들을 LLM을 이용해 자연스러운 "2021년도 삼성 스마트폰 수익은 100조입니다" 라는 인간의 문장 해설형 문구로 강제 번역 변환 시켜 치환해낸 뒤 청킹하는 표-텍스트 호환 기술의 정형적 교두보를 마련했습니다.

### 📜 8. Longformer Sliding Window: 장문 처리를 위한 근접 윈도우 한계 돌파
**[논문]** *Longformer: The Long-Document Transformer (Beltagy et al., 2020)*
* **의의:** 청킹의 오버랩(Sliding Window) 철학을 아예 트랜스포머의 어텐션 기어 신경망 내부 하드코어로 가져가 이식한 모델. 문서를 무제한 길이로 늘이기 위해 전부를 비교하는 풀 어텐션을 포기하고, 내 앞뒤 이웃 토큰 200개 반경만 슬라이딩 윈도우로 무빙 탐색하며 집중 연산하여 만 장의 문서 처리도 병목 없이 가동시키며 토큰 랭스 확장의 역사에 한 획을 그었습니다.

---



## 💻 [Implementation Frameworks] LlamaIndex 고급 청킹 파이프라인
단순히 글자 수로 쪼개지 않고, 의미 단위로 잘라내는 고급 파서는 **LlamaIndex**에서 가장 강력하게 지원합니다.
```python
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding

# 1. 문서 로드 
documents = SimpleDirectoryReader("./data").load_data()

# 2. Semantic Splitter (의미 기반 분할기) 초기화
embed_model = OpenAIEmbedding()
splitter = SemanticSplitterNodeParser(
    buffer_size=1, breakpoint_percentile_threshold=95, embed_model=embed_model
)

# 3. 문서를 노드(청크)로 변환
nodes = splitter.get_nodes_from_documents(documents)
print(f"의미 단위로 분리된 총 청크 개수: {len(nodes)}")
```

## 마무리하며

이번 3주차에는 무지막지한 더미의 기업 문서 텍스트 파편들을 컴퓨터 엔진이 정보 소화장애 붕괴를 일으키지 않고 한땀한땀 입체적으로 살려 이식할 수 있도록 지혈해 막아내는 S-급 최상 라인의 광학 파서들과 지능형 의미론적 트리(RAPTOR 등) 아키텍처 청킹, 그리고 문맥의 생명줄 메타 태그 주입 기법의 학술적 토대를 모두 폭파시키듯 파해 마스터했습니다.

이제 조리될 데이터 칼질 안료 덩어리 지식들은 모두 준비되었습니다. 
다음 4주 차에서는 이렇게 예술적으로 잘려진 이 알파벳 자연어 덩어리 살점들을 전혀 차원이 다른 우주인, 기계만이 온전히 이해할 수 있는 좌표 체계(수만 차원 숫자 배열)로 마법 연금술 텔레포트를 시전하는 핵심 코어 인코딩 동력, **Embedding Models & Representation Learning (대규모 임베딩 모델 인코더와 토큰 교차 분절)** 의 진수를 담은 트랜스포머들의 내부 연산에 대해 학습해 보겠습니다.
