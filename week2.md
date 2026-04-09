---
layout: default
title: 2주차. Prompting Strategies for Hallucination Reduction
---

# 2주차: Prompting Strategies for Hallucination Reduction (환각 통제 모형과 진보된 프롬프팅 전략의 해부)

지난 1주차에서는 RAG의 기본 뼈대와 15대 기초-한계 돌파 논문들을 배웠습니다. 하지만 검색이 아무리 성공하여 완벽하게 정련된 정답 문서를 수백 개 가져왔다 한들, 이를 넘겨받아 '실제 문장으로 창작해 내는' 출력기인 LLM 모델이 프롬프트 무대 위에서 자기 잘난 맛에 폭주하여 엉뚱한 거짓말(Hallucination)을 덧붙인다면 전체 RAG 파이프라인의 보안/신뢰도는 영구히 파멸하고 맙니다.

이번 2주 차에서는 가져온 문맥(Context)을 대다수 LLM의 어텐션 블록에 어떻게 주입하고, 어떤 숨막히는 제약조건(Constraints Constraint)의 암호 족쇄를 시스템 프롬프트(System Prompt)에 걸어주어야만 AI 모델이 감정을 배제한 차가운 판사처럼 맹목적으로 제공된 "팩트(Fact)"에만 기반해 조립을 해대는지, **프롬프팅 전략(Prompting Strategies)** 의 극의와 15개의 뇌과학적 SOTA 통제 논문들을 파헤칩니다.

---

## 1. 프롬프팅(Prompting)의 근본적인 엔터프라이즈 목적

대중적인 B2C ChatGPT 챗봇 환경에서 사용자는 LLM에게 자유로운 소설 창작이나 시 쓰기(Creative & Unconstrained writing)를 유도합니다. 하지만 기업형 RAG 환경의 프롬프팅은 이와 철저하게 180도 정반대인 **'제한적 사고 강제(Grounding)를 통한 통제 억압'** 이 유일무이한 최정상 과제 목적입니다.

* **환각의 방어를 위한 프롬프트 핵심 규칙 (Rules of Grounding):**
  1. **Strict Context Adherence (문맥 엄수):** "네가 아무리 사실을 잘 알고 있더라도, 내가 아래에 제시한 이 문서 쪼가리에 답이 안 적혀 있으면 고집 부리지 말고 모른다고 답해라."
  2. **Citation Injection (출처 및 각주 강제):** "모든 단답 추론 뒤에는 반드시 [문서 1-B 파트] 같은 형태로 형식을 갖춰 증거 출처 조항을 꼬리표로 묶어라."
  3. **Tonal Boundary (페르소나 제약):** "인간인 척 감정적인 대화형 수식어(예: 좋은 하루입니다!)를 전부 생략하고 기계적인 결론 정보만 JSON 통신 형태로 리턴해라."

> 🛑 **이해를 돕는 강력한 예시: 밀실 재판정의 냉혹한 검사**
> 피고가 명백한 살인범이라는 확신과 촉이 아무리 든다 하더라도, 검사가 판사(User)에게 "제 직감으로 얘는 진범입니다"라고 대답하면 재판은 파탄납니다. 무조건 "국립과학수사연구원의 문서 14페이지 혈흔 보고서에 의거하여..." 형식으로만 말하도록 검사의 언행 자체를 억압 통제하는 것이 바로 RAG 프롬프트 엔지니어링의 본질입니다.

---

## 2. Advanced Prompting Techniques (진보된 다단계 추론 프롬프팅 구조론)

단순 "요약해라"라는 천박한 1차원 지시에 그치지 않고, AI의 추론 논리 뇌파 회로 과정 자체를 단계별로 업그레이드하는 최신 프롬프팅 기법의 원리를 살펴봅니다.

![Chain of Thought Analysis](assets/images_new/Fig_3_1_page_21.png)
*Fig 3.1: 단순 다이렉트 프롬프팅과 Chain of Thought (CoT, 생각의 사슬) 프롬프팅 간의 논리 전개 추론 방식의 비교 모식도.*

### 2.1 제로샷 (Zero-shot) & 퓨샷 (Few-shot) 프롬프팅 메커니즘
* **제로샷(Zero-shot) 프롬프팅:**
  사전 예시 없이 지시문 하나만 던져 뇌 구조가 백지인 상태에서 모델의 기본 본능에 의존해 출력을 짜내는 방식입니다. RAG 환경에서는 출력 형식이 제멋대로 튀거나 정보 누락이 많아 실패율이 높습니다.
* **퓨샷(Few-shot) 컨텍스트 주입 프롬프팅:**
  명령 전에, 사용자가 직접 수작업으로 타이핑한 **"질문 - 가짜 제공문서 - 완벽한 모범 요약 답안 예시(Examples)"** 세트를 프롬프트 최상단에 2~3세트 보여주어 인-컨텍스트 러닝(In-context Learning)을 시켜버리는 방식입니다. 이 방식은 LLM에게 백 마디 설명보다 압도적으로 강한 포맷팅 준수율(톤앤매너, 말투, 출력 형식)과 성능 개선을 보장합니다.

### 2.2 구조적 출력 (Structured Output & Format Forcing)
기업 RAG 환경은 채팅창이 끝이 아닙니다. 이 답변을 파싱(Parsing)해 사내 UI 앱 화면이나 데이터베이스에 또 밀어 넣어야 하므로 줄글 서술로는 시스템 에러가 발생합니다.
따라서 무조건 `{ "Answer": "...", "Confidence": 95, "Citation": "Doc-A" }` 와 같은 정해진 JSON 포맷만을 내보내게 강제하는 **포맷팅 인젝션 기법**이 들어갑니다.

![Thread of Thought](assets/images_new/Fig_3_2_page_23.png)
*Fig 3.2: 여러 갈래의 사고를 생성하고 최적을 골라내는 Thread of Thought 기법 과정.*

---

## 🌟 프롬프트 모형의 지성을 파멸적으로 끌어올린 15대 프론티어 논문 완벽 해부
LLM이 단순히 앵무새를 넘어 스스로 내면에서 생각하고 검열하며, 자신의 논리의 헛점을 바로잡게 만드는 '인지 제어 마법'의 정수가 담긴 연구들을 집중 조명합니다.

### 📜 1. 생각의 사슬 (Chain of Thought): AI 사고력 봉인의 해제
**[논문]** *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models (Wei et al., Google Brain, 2022)*
* **연구 배경:** LLM은 연산이나 로직 문제가 주어지면 과정 없이 다이렉트로 결괏값만 툭 뱉으려다 오답을 내는 심각한 버그 구멍을 가지고 있었습니다.
* **해결 기술 (Architecture):** 
  Few-shot 예제 프롬프트의 답안 부분에 정답만 달아놓는 대신, 풀이 과정(중간 생각의 사슬 과정 문장)을 인간처럼 서술해 두었습니다. 이제 프롬프트를 받은 모델이 새로운 문제를 풀 때 즉답을 하지 않고, "단계별로 생각해보자"며 텍스트로 과정을 쭉 떠들며 논리를 끼워 맞춘 뒤 자체적으로 깨달음을 얻고 정답률을 올립니다.
* **의의:** `Let's think step by step` 이라는 마법의 주문이 신경망 내부의 암묵적 지식을 어떻게 폭발적으로 일깨우는지 증명한 최고 권위 논문.

<div class="mermaid">
flowchart TD
    Q[Q: 매장 주차장에 차가 5대, 버스가 2대. 총 바퀴 갯수는?] --> Base[Standard Prompt]
    Base --> Wrong[A: 음... 총 바퀴는 14개야. (오답)]
    
    Q --> CoT[CoT Prompt: "단계별로 하나씩 풀이해 가자"]
    CoT --> S1[A: 1단계: 차는 5대고 각각 바퀴 4개니 5x4=20.]
    S1 --> S2[2단계: 버스는 2대고 바퀴 6개 잡으면 2x6=12.]
    S2 --> S3[3단계: 총합 20+12 = 32개.]
    S3 --> Right[최종 정답은 32개. (정답!)]
    
    style Right fill:#d4edda,stroke:#28a745,stroke-width:2px
    style Wrong fill:#f8d7da,stroke:#dc3545,stroke-width:2px
</div>

### 📜 2. ReAct: 에이전트의 탄생 (생각하고 행동하라)
**[논문]** *ReAct: Synergizing Reasoning and Acting in Language Models (Yao et al., Princeton, 2022)*
* **연구 배경:** 혼자 CoT로 백날 방구석에서 짱구를 굴려봤자 최신 팩트는 검색을 못하면 소용이 없습니다.
* **해결 기술 (Architecture):**
  프롬프트를 **Thought(생각) -> Action(검색 엔진 호출 등 행동) -> Observation(검색 결과 관찰)** 의 루아(Lua) 스크립트 형태의 에이전트 루프 구조로 짜버렸습니다. 모델은 "나는 이 부분의 사실 관계를 정확히 모른다"라고 Thought 판단하면 멈춰서 Action(위키피디아 검색 API 호출)을 던져 결과를 받아 읽고, 다시 다음 추론 Thought를 이어가는 탐정 같은 능동형 무한 루프를 돕니다.
* **의의:** 외부 RAG 서치 함수를 모델 스스로가 자율적으로 실행하고 검증하며 통신하게 만든 최초의 도약 발판. 에이전트 생태계의 알파이자 오메가입니다.

<div class="mermaid">
stateDiagram-v2
    [*] --> Thought_1: Thought 1. 사용자가 2024년 대선 승율 묻네. 내 지식엔 없는 데이터다.
    Thought_1 --> Action_1: Action 1. [Search_API: "2024 Election Polls"] 실행!
    Action_1 --> Observation_1: Obs 1. (API 리턴값: A후보 51%, B후보 48%)
    Observation_1 --> Thought_2: Thought 2. 아하, 관찰 결과 A 후보가 우세하군. 다른 매체도 교차 검증하자.
    Thought_2 --> Action_2: Action 2. [Search_API: "2024 CNN Election News"]
    Action_2 --> Observation_2: Obs 2. (API 리턴값: A후보 박빙 리드)
    Observation_2 --> Final_Action: Action 3. [Final_Answer: "두 매체를 바탕으로 A후보 박빙 우세입니다."]
</div>

### 📜 3. Self-RAG: 기계의 양심 고백, 비판 토큰(Critique Token) 자가 치유 망
**[논문]** *Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection (Asai et al., 2023)*
* **연구 배경:** 검색 엔진이 간혹 헛소리 문서를 가져오거나, 생성된 출력물이 정답인양 헛소리할 때, 멍청한 다른 모형들은 그걸 필터 없이 그대로 내보내 대형 사고를 친다. 이걸 모델 스스로 지적하고 반려(Reject) 때릴 수 있을까?
* **해결 기술:** 모델 내부에 특별한 감시 경찰 토큰들(`[Retrieve]`, `[Relevant]`, `[Supported]`)을 뿜어내게 파인튜닝했습니다.
  1. 사용자 질문을 보고 자기가 `[Retrieve=Yes]` 토큰을 내뱉으면 그때만 검색 작동.
  2. 검색 문서가 오면 그 문서가 쓰레기인지 아닌지 `[Relevant / Irrelevant]` 토큰으로 자가 평가.
  3. 마지막 답변을 작성한 후, 자기 대답이 지문에서 가져온 게 맞는지 날조했는지 점검하는 `[Supported / Contradiction]` 토큰을 내뱉으며 불량이 뜨면 말을 철회하고 다시 재생성 구조.

<div class="mermaid">
sequenceDiagram
    participant LLM as Self-RAG Generation Model
    participant DB as Vector Search Module
    LLM->>LLM: Q: "뉴턴의 3법칙은?" -> [Retrieve=Yes] 필요성 감지
    LLM->>DB: 자체적 검색 발동
    DB-->>LLM: 문서 세트 리턴 (뉴턴 운동, 사과 이야기 등)
    LLM->>LLM: 문서 필터링: "사과 얘기 문서 [Irrelevant], 운동법칙 문서 [Relevant]"
    LLM->>LLM: 답변 임시 초안 생산 (작용-반작용)
    LLM->>LLM: 자가 교차 성찰: "내 대답이 저 Relevant 문서에 기반했나? [Fully_Supported]"
    LLM-->>User: 검증 완료된 무조건적 신뢰 답변 출력
</div>

### 📜 4. ToT (Tree of Thoughts): 사고의 가지를 뻗다 탈락시키기
**[논문]** *Tree of Thoughts: Deliberate Problem Solving with Large Language Models (Yao et al., 2023)*
* **해결 기술:** CoT처럼 일직선(선형)으로 한 길만 쭉 파다 중간에 계산 실수하면 끝장나는 한계를 타파. 체스 수읽기처럼 "만약 A방향 논리를 펼치면?", "B 논리로 풀면?" 의 여러 갈래 나뭇가지(Tree) 대안을 전부 뻗으며 탐색합니다. 중간중간 가지마다 이 논리 전개가 살아남을지 가망 없는지 휴리스틱 점수를 스스로 매겨(Value Heuristic), 점수가 낮은 가지치기는 자비 없이 자르고 유망한 가지의 줄기로 회귀(Backtrack)하여 집중합니다. 범용 복잡 로직 연산, 복잡한 교환 퍼즐 문제 최적화.

### 📜 5. GoT (Graph of Thoughts): 네트워크로 뒤엉킨 초현실적 사고망 구축
**[논문]** *Graph of Thoughts: Solving Elaborate Problems with Large Language Models (Besta et al., 논문 2023)*
* **해결 기술:** Tree 구조조차 단점(가지끼리 정보 교환 단절)이 있음을 지적하며, 다발의 사고 추론 노드(점)들이 상호 간선(Edge)으로 얽혀서 "내 논리 A 덩어리와 네 논리 B 덩어리를 융합해보자(Synergize)"라며 결론 정보를 서로 머지(Merge)하거나 거부하는 무수한 다변적 네트워크 논리망 추리 엔진 프롬프트를 창조했습니다. 문서 통합 요약 시 소름 돋는 강점을 보입니다.

### 📜 6. AoT (Algorithm of Thoughts)
**[논문]** *Algorithm of Thoughts: Enhancing Exploration of Ideas in Large Language Models (Sel et al., 2023)*
* **해결 기술:** ToT의 단점인 LLM 연속 재호출(토큰 낭비)을 잡기 위해, 기존 딥 서치(DFS)나 넓이 탐색(BFS) 알고리즘 로직 패턴을 인간이 프롬프트 코드 구조 원문으로 심어주어 단 한 번의 LLM 프롬프트 생성 사이클 안에서 로컬 연산 트리 순회가 무리 없이 일어나도록 하는 코스트 최적화 트랙 기술.

### 📜 7. ToG (Think-on-Graph): 진짜 지식 그래프 위를 뛰어놀다
**[논문]** *Think-on-Graph: Deep and Responsible Reasoning of Large Language Model with Knowledge Graph (Sun et al., 2023)*
* **해결 기술:** 외부의 그래프 노드 DB 체계 안을 LLM이 직접 더듬거리며 한 칸, 두 칸 간선(Edge-Hop)을 무수히 뛰어넘어가며 자기 생각과 지식 그래프 상의 실시간 탐색 경로를 맞춰가며 추렴하는 다단계 RAG의 혁신 프론티어입니다. (추후 7주차에서 본질로 배웁니다!)

### 📜 8. CoVe (Chain of Verification): 본인이 한 말 자기가 다시 되묻기
**[논문]** *Chain-of-Verification Reduces Hallucination in Large Language Models (Dhuliawala et al., Meta 2023)*
* **해결 기술:** 모델이 초안 대답을 뽑아내면 곧장 사용자에게 주지 않습니다. 이 초안 안에 있는 수많은 명제(팩트 뼈대)들을 잘게 찢어서 스스로 각각의 사실확인용 질문들(Verification Questions: "아까 내가 뉴욕시장 임기가 5년이라 대답했지? 진짜 5년인가?")을 10개 만들어 냅니다! 그리고는 10개 질문을 병렬 독립적으로 다시 자기 엔진에 던져 검증하고, 만약 오답이 도출되면 초안을 철회 수정하고 내보내는 지독한 교차 확인 수직 검열 모형입니다. 환각 타파에 어마어마한 전과를 입증했습니다.

### 📜 9. Step-Back Prompting: 나무를 보지 말고 숲을 보라
**[논문]** *Take a Step Back: Evoking Reasoning via Abstraction in Large Language Models (Zheng et al., Google 2023)*
* **해결 기술:** 디테일하고 지독히 어려운 사용자 질문("1977년 스팍이 발명한 A장치의 x-ray 배터리 성분은 뭐지?")에 매몰되어 멘붕이 온 모델을 위해, 아예 반 발짝 뒤로 강제로 스텝백 추상화시켜 큰 범주의 형이상학적 원리 질문("배터리 화학 물리 성질의 원리는 무엇이지?")을 우선 도출하게 합니다. 그 대원리를 기초 토대로 하여 다시 세부 퍼즐을 풀게 되먹이는 엄청난 인간적 영감 도출 구조입니다.

### 📜 10. Reflexion: 오답의 고통을 언어 텐서로 기억하는 자기반성망
**[논문]** *Reflexion: Language Agents with Verbal Reinforcement Learning (Shinn et al., 2023)*
* **해결 기술:** 강화학습 환경에서 모델(에이전트)이 코드를 짜거나 대답해서 에러가 터지고 폭망(실패)했을 때, 숫자 값의 패널티 로그를 주는 대신 모델 스스로 "내가 방금 이래저래 생각해서 망했으니, 다음부턴 저 메서드는 피해야지" 하고 통절한 '반성문 자연어 일기 텍스트'를 작성해 자기 메모리 뇌 영역에 누적 저장시켜 다신 같은 실수를 안 하도록 만드는(Verbal Reinforcement) 획기적인 로직입니다. 

### 📜 11. Self-Refine: 쉴 새 없는 원고 지우고 쓰기 수정의 예술
**[논문]** *Self-Refine: Iterative Refinement with Self-Feedback (Madaan et al., 2023)*
* **해결 기술:** LLM이 초안 글을 던지면, 멈추지 않고 스스로 프롬프트에게 "이 글의 단점 피드백을 내놔"하고 피드백을 생산, 그 피드백을 읽고 2차 원고 산출, 3차 원고 산출 무한 이터레이션을 돌며 문장 다이아몬드를 깎아내는 장인 기법 메커니즘. 코딩 작성과 작문 과제에서 SOTA를 갱신합니다.

### 📜 12. Emotional Prompting: 모델에게 감성과 압박 주기
**[논문]** *Large Language Models Understand and Can be Enhanced by Emotional Stimuli (Li et al., 2023)*
* **해결 기술:** 단순히 프롬프트 말미에 "이 일은 내 커리어의 목숨이 달린 막중한 과제야. 네가 틀리면 내 인생이 위험해! 제발 집중해서 반드시 정답만 찾아라!" 라는 인간적이고 극단적인 감정-압박성 심리 언어(Emotional Stimuli)를 강하게 퍼부어 넣었을 뿐인데도, 놀랍게도 어텐션 집중도가 폭발해 성능 지표가 무려 10% 이상 뛰어오르는 LLM의 특이하고 오묘한 구조적 맹점을 발견한 연구입니다. 

### 📜 13. System 2 Attention (S2A): 쓰레기를 아예 눈에서 차단하기
**[논문]** *System 2 Attention (is something you might need too) (Weston et al., Meta 2023)*
* **해결 기술:** 프롬프트에 사용자가 "사실은 이러쿵저러쿵 편견(Bias)이 있는데, 정답 뭐냐?"하고 찌꺼기 헛소리 편견 정보(Opinionated noise)를 섞어오면 대다수 LLM이 그 편견 쓰레기에 전염돼 환각을 냅니다. S2A 기법은 모델을 2기통으로 돌려서, 통통이 1번 모델이 "사용자 말 중 편견 제거하고 딱 클린한 팩트 지문만 다시 써줘" 한 뒤에 세척된 객관적 지문만 메인 모델에 넣어 어텐션의 오염을 영구 방어하는 강력한 위생 세탁술입니다.

### 📜 14. Prompt2Model: 프롬프트를 작은 로컬 모델로 아예 증류시켜 버리기
**[논문]** *Prompt2Model: Generating Deployable Models from Natural Language Instructions (Viswanathan et al., 2023)*
* **해결 기술:** 거대 API 토큰 프롬프트 비용을 아끼기 위해, 훈련된 특정 프롬프트 과제를 소형 경량 모델링(Small Model) 코드로 파인튜닝 로직화해서 뽑아내어 로컬 온프레미스 기업망 안에 배포할 수 있는 신선한 파이프라인.

### 📜 15. DExperts (Decoding-time Experts): 전문가 모델 무임승차 제어기
**[논문]** *DExperts: Decoding-Time Controlled Text Generation with Experts and Anti-Experts (Liu et al., 2021)*
* **해결 기술:** 모델이 나쁜 말(Toxic)이나 환각을 내뿜으려는 벡터 확률 방향성을 포착하면, 옆에 숨겨둔 "나쁜 말 전용 안티-엑스퍼트 모델"과 "착한 말 전문가 모델" 연산 로직을 출력단(Decoding) 배럴 모서리에 동시 끼워넣어 나쁜 확률 벡터는 상쇄시켜버리고 착한 벡터만 증폭시켜 안전하고 독성 없는 신성한 정답만 깔때기로 골라 도출하는 튜닝 프리 억제 기술입니다.

---



## 💻 [Implementation Frameworks] DSPy를 활용한 프롬프트 자동 최적화
단순히 프롬프트를 텍스트로 치는 시대는 끝났습니다. 스탠포드의 **DSPy**는 프롬프트를 파이토치 신경망처럼 튜닝합니다.
```python
import dspy

# 1. 언어 모델 설정 
turbo = dspy.OpenAI(model="gpt-3.5-turbo")
dspy.settings.configure(lm=turbo)

# 2. 추론 모듈 (Signature) 선언
class BasicQA(dspy.Signature):
    """주어진 질문에 대해 사실에 입각하여 답변합니다."""
    question = dspy.InputField(desc="사용자의 질문")
    answer = dspy.OutputField(desc="가장 논리적인 답변")

# 3. ChainOfThought 적용
cot_qa = dspy.ChainOfThought(BasicQA)
response = cot_qa(question="환각(Hallucination)을 줄이는 가장 좋은 전략은?")
print(response.reasoning) # 중간 추론 과정 자동 출력
print(response.answer)
```

## 마무리하며

오늘은 언어 모델이 제멋대로 날뛰는 폭주를 막는 프롬프팅 통제술과, 학계의 무궁무진한 모델 자가 치유 에이전트(LLM Agents) 반성 테크닉에 대해 15편의 엄청난 학술 전당의 역사와 해부도를 낱낱이 파고들며 탐구했습니다. 
하지만 이 아무리 위대한 LLM들도 그들의 위장(Context Window)에 효율적으로 문장을 밀어 넣기 위해서는 그 먹이감인 '긴 문서 원본 데이터 덩어리' 자체가 거친 돌출 부위 없이 정보 밀집 포만감을 주도록 정교하게 가공되어야만 합니다. 
3주차에는 무자비하게 길고 복잡한 실무 위키 문서를 영리하게 칼질하고 마분지 분류하는 조각술의 대예술의 마경, **Advanced Document Chunking & Context Engineering (고급 문서 청킹과 메타데이터 주입 문맥 엔지니어링 생태계)** 에 대해 본격적으로 파헤쳐 보겠습니다.
