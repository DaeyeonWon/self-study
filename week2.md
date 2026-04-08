---
layout: default
title: 2주차. Prompting Strategies for Hallucination Reduction
---

# 2주차: Prompting Strategies for Hallucination Reduction (환각을 줄이기 위한 프롬프팅 전략)

지난 1주차에서는 RAG의 기본 뼈대를 배웠습니다. 하지만 검색이 아무리 성공적으로 수백 개의 정확한 문서를 가져왔다 한들, 이를 넘겨받아 '말을 만들어내는' LLM 모델이 폭주하여 엉뚱한 거짓말(Hallucination)을 덧붙인다면 RAG 시스템의 신뢰도는 무너집니다.

이번 2주 차에서는 문맥(Context)을 LLM에게 어떻게 들이밀고, 어떤 제약조건(Constraints)의 족쇄를 걸어야만 AI가 판사처럼 건조하고 맹목적으로 팩트에만 기반해 대답하게 만들 수 있는지, **프롬프팅 전략(Prompting Strategies)** 의 극의를 파헤칩니다.

---

## 1. 프롬프팅(Prompting)의 근본적인 목적

일반적인 대화형 챗봇 환경에서 사용자는 LLM에게 자유로운 창작(Creative writing)을 유도합니다. 하지만 RAG 환경의 프롬프팅은 이와 정반대인 **'제한적 사고 강제(Grounding)'** 가 목적입니다.

* **환각의 3대 유형 방어:**
  1) 주어진 Context와 상반된 소설을 쓰는 것 (Context-Conflicting)
  2) Context에 전혀 없는 내용을 자신이 학습한 기존 상식에서 가져오는 것 (Input-Conflicting)
  3) 과학적/논리적 수치를 스스로 조작하는 것 (Fact-Conflicting)

> 🛑 **이해를 돕는 예시: 법원 안의 변호사**
> 변호사가 재판정에서 판사에게 "이 피고인은 살인범입니다. 그냥 제 촉이 그렇습니다"라고 대답할 수 없습니다. "제공된 형법 제250조 서류 3페이지에 근거하여..." 라고만 대답하게 입을 막아야 합니다. RAG 프롬포트는 바로 이 강력한 법적 '증거 채택 동의서'와 같습니다.

---

## 2. Advanced Prompting Techniques (진보된 프롬프팅 구조론)

단순 지시에 그치지 않고, AI의 추론 논리 과정 자체를 업그레이드하는 최신 프롬프팅 기법들을 살펴봅니다.

![Chain of Thought Analysis](assets/images_new/Fig_3_1_page_21.png)
*Fig 3.1: 단순 프롬프팅과 Chain of Thought (CoT) 프롬프팅 추론 방식 비교.*

### 2.1 Zero-shot vs. Few-shot Prompting
* **제로샷(Zero-shot) 프롬프팅:**
  명령만 단도직입적으로 내리는 것입니다. "문서를 요약해라."
* **퓨샷(Few-shot) 프롬프팅:**
  명령 전에, **모범 답안 예시(Examples)** 를 2~3개 보여주어 출력 형태와 논조를 백락시키는 방식입니다. RAG에서 JSON 형태로 답을 반환받고 싶거나 톤앤매너를 지키게 할 때 압도적인 성능 개선을 보입니다.

### 2.2 Chain-of-Thought (CoT, 생각의 사슬)
질문이 복잡할 때 (예: 두 문서를 융합하여 결론을 내릴 때) 매우 효과적입니다. 프롬프트에 **"단계별로 차근차근 생각해 보자 (Let's think step-by-step)"** 라는 문구 하나만 삽입해도, 모델은 즉답을 멈추고 1번 단계, 2번 단계를 텍스트로 풀어내며 자신의 글에 스스로 피드백을 받아 정답률이 비약적으로 오릅니다.
> 🔗 **이해를 돕는 예시: 수학 연습장**
> 초등학생에게 암산으로 답을 내라고 하면 틀리지만, 연습장을 주고 "수식의 과정을 번호 매겨 적고 답을 적출해라" 라고 하면 정답 확률이 치솟는 것과 같은 이치입니다.

### 2.3 Thread of Thought (ThoT) & Tree of Thoughts (ToT)
단순한 1차원적 사슬(Chain)을 넘어, "만약 A 방향으로 가면 어떻게 될까? B 방향으로 가면?" 처럼 사고의 나무(Tree)나 스레드(Thread)를 평행하게 뻗으며 다학제적으로 검증문을 작성한 후 최적의 답안을 선택하는 프롬프팅 기법입니다.

![Thread of Thought](assets/images_new/Fig_3_2_page_23.png)
*Fig 3.2: 여러 갈래의 사고를 생성하고 최적을 골라내는 Thread of Thought 기법 과정.*

---

## 3. 구조적 출력 (Structured Output) 강제와 겸손한 거절 (Graceful Fallback)

RAG 환경은 외부 소프트웨어 API 서버와 연동되므로 줄글 서술형 답변보다 **정해진 JSON/XML 포맷** 만을 내보내야 합니다.
또한, 제공된 검색 문서들에 정답에 대한 힌트가 단 한 줄도 없을 때, 컴퓨터가 아는 체를 하지 못하도록 **"해당 문서에 답변이 명시되어 있지 않다면, 절대 추론하지 말고 '알 수 없음' 이라고 반환하라"** 고 쐐기를 박아야 합니다.

![Emotion Prompting](assets/images_new/Fig_3_7_page_33.png)
*Fig 3.7: 프롬프트에 감정적, 긴급성 압박을 주어 집중도를 올리는 Emotion Prompting 예시.*

---

## 🌟 [Deep Dive] 환각 통제 및 검증 로직 강화를 이끈 글로벌 학술 논문

모델이 소설을 쓰지 않게 막고, 스스로 답변을 고도화하게 만드는 '프롬프팅 심화 인지 마법'의 정수가 담긴 연구들을 살펴봅니다. 각 논문의 아키텍처 다이어그램을 이해하면 프롬프팅의 수준을 예술의 경지로 끌어올릴 수 있습니다.

### 📜 1. 생각의 사슬: LLM에 논리 추론력을 부여하다
**[논문명]** *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models (Wei et al., Google Brain, 2022)*
* **연구 배경:** LLM은 연산이나 로직 문제가 주어지면 과정 없이 다이렉트로 답만 맞히려 들다 보니 오답률이 엄청났습니다.
* **해결 기술 (Architecture):** 
  질문을 주고 대답을 강제하기 전, 프롬프트 예시에 "풀이 과정(중간 생각의 사슬 단계)" 문장을 서술해 줍니다. 이렇게 하자 모델이 답변을 낼 때 스스로 텍스트로 생각을 정리해가며 논리를 맞춰갑니다.
* **의의:** 프롬프트에 `Let's think step by step`이라는 코드 한 줄만 넣어도 신경망의 복잡한 추론 능력이 비약적으로 도약한다는 미친듯한 마술을 입증했으며, 현대 AI 사고 과정의 교과서적인 스탠다드가 되었습니다.

<div class="mermaid">
graph TD
    A[사용자 질문: A는 사과 2개, B는 배 3개...] --> B{기존 방식: 즉각 답변}
    B -->|단답 출력| C[오답 도출 우려]
    A --> D{CoT 방식: 단계적 풀이 활성화}
    D --> E[단계 1: A의 총량 확인]
    E --> F[단계 2: B의 총량 더하기]
    F --> G[단계 3: 수량 차감 후 검토]
    G --> H[정답 도출 확정]
    style D fill:#d4edda,stroke:#28a745,stroke-width:2px
    style G fill:#d4edda,stroke:#28a745,stroke-width:2px
</div>

### 📜 2. ReAct: 생각(Reasoning)하고 행동(Acting)하라
**[논문명]** *ReAct: Synergizing Reasoning and Acting in Language Models (Yao et al., 프린스턴, 2022)*
* **연구 배경:** 모델이 아무리 혼자 생각을 잘해도(CoT), 바깥 세상의 실존하는 데이터를 직접 찾아보는 '행동'을 섞지 못하면 지식에 갇히게 됩니다.
* **해결 기술 (Architecture):**
  모델의 뇌 구조 프롬프트를 **Thought(생각) -> Action(검색이나 API 호출 등) -> Observation(관찰 및 결과 반환)** 의 무한 반복 루프로 설계했습니다. 모델이 "나는 이 부분의 사실 관계를 정확히 모른다"라고 판단하면 즉시 멈추고 Action(지식 DB 검색)을 실행하여 결과를 Observe(관찰)한 뒤, 다음 Thought를 이어갑니다.
* **의의:** 기존 RAG가 사용자의 입력을 받아 무조건 한 번 1회성으로 검색하고 대답하는 것을 넘어, AI 에이전트(Agent)가 스스로 필요한 문서를 다단 검색하고 탐구하며 환각을 부숴버리는 시대를 열었습니다.

<div class="mermaid">
stateDiagram-v2
    [*] --> Thought: 질문 접수 및 전략 구상
    Thought --> Action: "사내 DB에서 연차 규정 검색 실행"
    Action --> Observation: DB 검색 결과(연차 15일) 반환됨
    Observation --> Thought: "찾은 문서를 보니 내 지식과 다르군. 다시 가공해보자"
    Thought --> Output: 정답 산출 완료
</div>

### 📜 3. Self-RAG: 자가 성찰 및 자체 검열 시스템
**[논문명]** *Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection (Asai et al., 워싱턴 대학, 2023 - 2024)*
* **연구 배경:** 검색된 문서가 쓸모 없거나, 생성된 대답이 엉터리일 때 이를 외부 센서가 아닌 모델 자신이 직접 지적하고 퇴짜를 놓을 수 있을까?
* **해결 기술 (Architecture):** 
  이 연구에서는 RAG 모델이 스스로 특별한 '비판 토큰(Critique tokens, 예: `[Relevant]`, `[Fully supported]`, `[Contradiction]`)을 무자비하게 찍어내며 자기 자신을 감시합니다.
  1) 검색이 필요한가 판단(`[Retrieve]`)
  2) 검색된 문서들이 정답 도출에 관련된 쓸모있는 문서인가 평가(`[Relevant/Irrelevant]`)
  3) 본인이 방금 지껄여서 만든 정답이 문서 내용만을 준수했는가 혹시 창작했는가 반성(`[Supported / No support]`)
* **의의:** 환각을 잡아내는 경찰관을 프롬프트 내부에 토큰 형태로 내장 박아버려 자가 치유(Self-Healing)를 달성한 현존 최고 수준의 오픈소스 프롬프팅 최적화 기법입니다.

<div class="mermaid">
sequenceDiagram
    participant User
    participant LM as Self-RAG Model
    participant DB as Vector Search
    User->>LM: 질문: "A회사의 작년 매출은?"
    LM->>LM: [Retrieve=Yes] 필요성 인지
    LM->>DB: 쿼리 실행
    DB-->>LM: 문서 세트 리턴
    LM->>LM: 문서 평가: "이 문서들은 매출 내용이군 [Is_relevant]"
    LM->>LM: 가답안 생성
    LM->>LM: 교차 검증: "내 대답이 문서 한계 내에 있는가? [Supported]"
    LM-->>User: 비판적 검토가 끝난 완벽한 정답 출력
</div>

### 📜 4. 다층적 사고의 나무 (Tree of Thoughts)
**[논문명]** *Tree of Thoughts: Deliberate Problem Solving with Large Language Models (Yao et al., 2023)*
* **연구 배경:** 한 길로만 논리(사슬)를 잇다 중간에 실수하면 결과적으로 엉뚱한 결론에 도달하는 CoT의 선형적 한계점.
* **해결 기술 (Architecture):**
  체스나 바둑의 수읽기처럼, "방법 A로 시작했을 때의 전개", "방법 B로 시작했을 때의 파생 경로"를 나무(Tree) 가지처럼 여러 방향으로 넓게 뻗으며 대안을 탐색(Search)합니다. 각 경로 전진 후마다 스스로 중간 평가 점수를 매겨, 가망이 없는 나뭇가지는 잘라버리고 확률이 높은 노드로 백트래킹(Backtracking)하여 올라갑니다.
* **의의:** 오류 우회 능력과 난제 타파 능력에서 혁신의 정점을 찍은 프롬프팅 기법입니다.

---

## 마무리하며

오늘은 언어 모델의 폭주를 막는 프롬프팅 통제술과 학계의 무궁무진한 모델 자가 치유 테크닉에 대해 탐구했습니다. 하지만 LLM에게 문장을 효율적으로 읽히기 위해서는 문장 덩어리(Context) 자체의 사이즈가 모델의 위장에 부담이 가지 않도록 가공되어야만 합니다. 3주차에는 무자비하게 긴 텍스트를 영리하게 칼질하는 예술, **Advanced Document Chunking & Context Engineering** 에 대해 본격적으로 파헤쳐 보겠습니다.
