---
layout: page_with_mermaid
title: 6주차. Reranking Models and Hybrid Retrieval Techniques
---

# 6주차: Reranking Models and Hybrid Retrieval (쌍끌이 투트랙 검색과 무결점 면접 채점 통치 리랭킹 망)

5주 차에서 우리는 어마무시한 속도로 수백 장의 유사 후보 청크들을 뽑아내는 고속도로 벡터 검색 톨게이트 엔진을 서버에 건설했습니다. 그러나 기업 비즈니스 생산 라인 전장에서는 Vector의 코사인 유사성 하나에만 단일 극의존했다간 파멸의 벽돌 버그를 마주합니다. 

유저가 극단적으로 지엽적인 스펠링 부품 번호가 박힌 질문("NVIDIA A100 Tensor Core의 4분기 적자폭")을 던질 때, 단순 어감(Dense) 벡터 AI 엔진만 돌리면 '적자'나 '분기'의 둥그런 문맥에 취해 정작 A100이란 결정적 키워드 부품 팩트는 날려 먹고 멍청한 서치를 배출합니다.
따라서, 과거 구식 타자형 스펠링 위주 검색(Sparse) 밧줄과, 우주 차원 심층 뜻 검색(Dense) 밧줄을 동시에 양방향 폭발로 던져 잡아채는 융합 사냥망 **(Hybrid Retrieval)** 패러다임. 그리고 이렇게 잡어 찌꺼기가 뒤섞여 건져진 허접한 Top-100 탑 무리들을 최악의 면접관 앞에 소환시켜 1등부터 줄세워 등수를 폭력적으로 갈아 마시는 **(Reranking Models)** 아키텍처 세계관의 지평을 활짝 찢어발기겠습니다!

---

## 1. 1차 포획의 품질 혁명: 하이브리드 및 고급 단서 수색 패턴 (PDF p.127-130)
<div style="display:flex; flex-wrap:wrap; margin-top:10px; margin-bottom:20px;">
<img src="assets/images_new/Table_1_1_page_12.png" width="30%" style="margin:5px; border-radius:8px; box-shadow:0 4px 6px rgba(0,0,0,0.1);">
</div>

<img src="assets/images_new/Fig_4_4_page_94.png" width="600">
*Fig 4.4: [Reranking Pipeline (PDF p.94)] 검색된 초기 후보군을 다시 중간에서 가로채고 재평가하여 LLM에 최종 주입하는 아키텍처 다이어그램.*

* **Hybrid Search 융합 교배망:** "태양은 크다" 와 "태양 광선 방출 사이즈" 의 스펠링 불일치를 극복하려다 Dense의 매력에 빠진 나머지 스펠링을 너무 잊은 현 사태를 구원합니다. Dense(시맨틱) 서치로 100위 랭킹, Sparse(BM25/TF-IDF) 키워드 100위 랭킹을 각각 산출한 뒤 Alpha 조합 상수(Weight) 비례 비율 연산으로 더하여 쌍방의 아킬레스건을 철벽 방어 보우합니다.
* **HyDE (Hypothetical Document Embeddings):** 천재적인 역발상 구조! 멍청한 사용자의 3음절 짧은 쿼리 질문 자체를 인코딩 변환 시키지 않습니다. 사용자 쿼리를 받아 먼저 판타지 가상의 그럴싸한 정답본 소설 텍스트 문서 가짜 본판을 LLM에게 생성하라고 시킨 뒤, 그 가짜 5줄짜리 동화책 답변을 벡터 우주로 임베딩 투척 서치 매칭합니다! 퀄리티가 무섭게 치솟습니다.
* **Recursive Retrieval (소형 점 탐색 + 대형 보쌈 반환):** 바늘만 한 크기(문단 1줄) 청크 덩어리로 잘게 벡터 DB에 분해 보관하여 레이더 탐색 정밀도는 극한으로 올리고, 그 문단이 캐치되었을 땐 답변 생성 LLM에게 "문단 1줄의 소속 애비인 부서장(해당 페이지 HTML 테이블 전체 + 앞뒤 거대 부모 페이지 통짜 문맥)" 통 덩어리로 문맥 교체 반환 환불해주는 무사 보존 스왑(Small2Big 구조) 서치.

---

## 2. 면접 채점 통제관 : 리랭커(Reranker) 아키텍처 로직 (PDF p.94-101)
<div style="display:flex; flex-wrap:wrap; margin-top:10px; margin-bottom:20px;">
<img src="assets/images_new/Table_4_4_page_97.png" width="30%" style="margin:5px; border-radius:8px; box-shadow:0 4px 6px rgba(0,0,0,0.1);">
</div>

하지만 하이브리드 투트랙으로 뽑혀 올라온 50개의 결과 더미는 사실 퀄리티가 개판입니다. 서로 자기들 1위를 다투며 뒤엉켜있어, 이대로 50개를 전부 LLM 팝업 컨텍스트로 구겨 넣었다간 토큰 폭주 마비 결제로 사장님이 기절할 것입니다. 최정예 해병 탑 K 문서만 5개 추려내 도출해야 합니다!

* **역할 (Role of Top-K Reranking):** 초기 깡통 벡터 비교로 추출된 50여 장 후보들의 1위부터 50위까지를 갈기갈기 찢고 무효화한 뒤, 가장 유저 쿼리에 소름 끼치게 응답 가능한 직격타 논리 정답 문서를 정수리 1위 자리에 우그려 강제 승격시켜 랭킹 박아 리스폰 재조정 배치시키는 중간 관문 미들웨어 스캐너. 

### 🎯 3가지 교차 리랭커 유형 파이프라인 무덤
1. **Cross-Encoders:** 과거 검색 엔진이 쿼리 백터와 문서 백터 각자 찐따같이 분리해 코사인 각도를 쟀다면, 크로스오버 형은 쿼리랑 문서를 한 문장 버스에 바짝 결박 결합해서 1000레이어 Attention 가중치 교차 파라미터가 단어의 앞과 뒤, 뜻과 철학을 1:1로 피 토하게 맞장 면접 배틀 비교 검수해버립니다. (정확도 악랄하게 우수, 랙 메모리 타임 심함)
2. **LLM 기반 분류 Reranking 시스템:** 비싼 파인튜닝 모델 없이 그냥 싸구려 오픈 LLM에게 지시를 내립니다.
   * **Pointwise:** 문서 1개씩 던져주고 "이거 1에서 10점 만점 중에 몇 점 짜리냐?" 개별 채점 배김.
   * **Listwise:** 문서 리스트 10개를 한 번에 보여주고 "1순위부터 10순위까지 순서 등수 나래비 매겨봐".
   * **Pairwise:** A문서와 B문서를 양방에 붙여 "이 듀얼에서 누가 더 정답 스웩에 가깝나?" 승자독식 결판 지어 연승제 토너먼트를 돌림.

---

## 💻 [Implementation Frameworks] 크로스인코더(Cross-Encoder) NDCG 리랭커 성능 검증
단순 검색 50위 밖으로 유실 소실 추락했던 핵심 정답 보물 덱 문서를 다시 어텐션 1등 면접관 로직을 투입해 순위를 역전 돌파 승격시키는 크로스 인코더 튠업입니다 (PDF p.106 NDCG 리랭커 성능 계산 실습 연계 과제).

```python
from sentence_transformers import CrossEncoder

# 1. BAAI 오픈 글로벌 압박 면접관 로컬 머신 등판 로딩 (HuggingFace 포탈 등재 1위계)
rerank_scorer_model = CrossEncoder("BAAI/bge-reranker-v2-m3")

# 2. 질문과 벡터DB망에서 하이브리드로 대충 발체된 원시 4가지 문서 배열 덱 
query = "최근 클라우드 보안 환경 아키텍처 중, Rate Limits와 SOC-2를 결합한 최고 보호망은?"
retrieved_docs = [
    "A 문단: 오늘 구글 클라우데 서버 연동 아키텍처가 버그가 발생했다.",
    "B 문단: 과거 로비 금융 비자금 조성 아키텍처 보안 장부 구조는 다음과 같습니다...",
    "C 문단: 하이브리드 Dense 서치는 정확합니다.",
    "D 문단: 완전 관리형 상용 DB인 파인콘 등은 SOC-2 통과 보안 및 초당 Rate Limits 통제 API로 아키텍처를 압록 도배합니다."
]

# 3. 크로스 인코더 압박 면접 연산 (Query + Doc 쌍을 통합 스쿼트 어텐션 타격 맵핑 크로스 융합)
raw_matrix_scores = rerank_model.predict([[query, doc] for doc in retrieved_docs])

# 4. 점수 출력 및 쌍 결합 내림차순 랭크 등수 대변혁 뒤집어엎기
doc_score_pairs = list(zip(retrieved_docs, raw_matrix_scores))
doc_score_pairs.sort(key=lambda x: x[1], reverse=True) # 점수 폭등순 정렬 스탠스

print("--- [면접관 최종 타격 NDCG 예측 탑 티어 랭킹] ---")
for idx, (doc, score) in enumerate(doc_score_pairs, 1):
    print(f"압도적 {idx}위 랭킹 | 어텐션 확률 스코어: {score:+.3f} | 통과된 문서 도출부: {doc[:30]}...")
# *결과: 깡통 벡터 단어 빈도 때문에 뒤에 쳐박혀 있던 완전 정답(D 문단)이 소름끼치게 1등으로 수직 복권 격상 스왑됨.
```

## 마무리하며 지식 추론망의 1% 결여 
이번 6주 차 지옥 훈련 전당에서는 유치원급의 단일 검색을 가차 없이 파기하고, 하이브리드 쌍끌이 사냥 지형을 뚫고 지나가 최종 선상에 오른 100명을 가장 잔혹무도한 논문 교차 평가 인공지능관(Cross-Encoder Reranker)과 LLM-Pairwise 배틀 토너먼트로 도척 분리 재정비 배열 서열 랭크 배치시키는! 100% 미친듯이 정교한 정답 필터 타겟팅망 최전선 무기들을 습득 흡수했습니다!

그러나... "작년 우리 회사를 무담보 대출로 퇴사한 직원 A와, 그와 친했던 부서장 B가 작당 동맹 모의하여 연쇄 로비 빼돌린 외부 거래처 C 문서의 결론은?" 처럼 수십 개의 문서 점선을 연결하는 연쇄 추론(Multi-Hop Reasoning) 추적의 그물망 호핑 쿼리 어택이 난도질해 폭주하면, 텍스트를 따로따로 파편화시킨 이 거대 검색 엔진 구조는 인과관계 파악 로직이 없이 모조리 마비되고 아수라장으로 병렬 파단 붕괴하고 맙니다!
이 연쇄 폭발적 혈연 인과율 망각 단절 사태 절망감을 완전 통달 전지구 사슬망 네트워크로 구원 도출 부수어 버리는 최신 지식 파이프 스택의 결정판 그 자체! **Knowledge Graph RAG & GNN Graph-based Retrieval Systems (표 구조 데이터 융합 지능 거미줄 그래프 노드 통치망 구축)** 파트로 대망의 폭등 7주 차 여정 침투 킥오프를 강타 돌격! 날리겠습니다! 전진 격파!!
