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

## 💡 연구 트렌드 및 관련 학술 아티클

> **[Paper Reference 1]** *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models (Wei et al., 2022)*
> 구글 브레인 연구원들이 발표한 역사적 논문으로, 모델에게 모범 답안의 '추론 단계(중간 사슬)'를 제공하는 것만으로 산술 및 상식 추론 논리력이 획기적으로 도약함을 입증했습니다. CoT는 현재 프롬프트 엔지니어링의 교과서적인 스탠다드입니다.

> **[Paper Reference 2]** *Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection (Asai et al., 2023 - 2024)*
> 일반적인 프롬프트를 넘어서 RAG 모델이 스스로 답변을 생성해 놓고, 자신의 답변이 주어진 문맥과 일치하는지, 문맥에 충실한지 비판(Critique)하고, 부족하다면 다시 한 번 DB를 재검색하도록 유도하는 "자가 반성 및 순환 로직"을 최초로 구현한 첨단 논문입니다. 현재 최고 수준의 환각 감소 기법으로 주목받고 있습니다.

---

## 마무리하며

오늘은 언어 모델의 폭주를 막는 프롬프팅 통제술에 대해 탐구했습니다. 하지만 LLM에게 문장을 효율적으로 읽히기 위해서는 문장 덩어리(Context) 자체의 사이즈가 모델의 위장에 부담이 가지 않도록 가공되어야만 합니다. 3주차에는 무자비하게 긴 텍스트를 영리하게 칼질하는 예술, **Advanced Document Chunking & Context Engineering** 에 대해 본격적으로 파헤쳐 보겠습니다.
