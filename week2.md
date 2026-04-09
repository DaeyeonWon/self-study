---
layout: page_with_mermaid
title: 2주차. Prompting Strategies for Hallucination Reduction
---

# 2주차: Prompting Strategies for Hallucination Reduction (검색 문맥을 활용한 답변 정확도 혁신 고급 기법)

아무리 RAG를 통해 고품질의 팩트 문서를 5장 찾아서 LLM에게 쥐여주더라도, LLM이 문서를 대강 요약하다가 엉뚱한 결론으로 점프해버리면 말짱 도루묵입니다. 
이번 2주차에서는 검색 시스템(Retriever)의 영역을 넘어 LLM 스스로 자신의 대답을 멱살 잡고 검열하게 만드는 **초고도화 프롬프트 추론 기술(Prompt Engineering Strategies)** 리스트를 전부 까발립니다. 단순한 Chain of Thought를 넘어, 실전에서 극악무도한 환각율을 틀어막는 Thread of Thought부터 CoN, CoVe에 이르는 학계 최고의 병기들을 장착하십시오.

---

## 1. 선형적 추론의 기본기: Chain of Thought (CoT)

<img src="assets/images_new/Fig_3_1_page_21.png" width="600">
*Fig 3.1: [Chain of Thought (PDF p.21)] 테니스 공과 사과 산술 과정을 강요하여 중간 계산 과정을 노출하게 만들기.*

단순히 "정답은 무엇인가?"라고 묻는 Zero-Shot의 한계를 돌파하기 위해 "Let's think step by step"이라는 지시를 추가하여 모델이 단계별 사고 과정을 거쳐 논리적 결론에 도달하도록 유도하는 기초 방어망입니다.

---

## 2. 복잡한 난제를 파괴하는 혼돈 해석: Thread of Thought (ThoT)

<img src="assets/images_new/Fig_3_2_page_23.png" width="600">
*Fig 3.2: [Thread of Thought 프레임워크 성능 비교 (PDF p.22-23)] 기존 프롬프트를 썼을 때 놓쳤던 정보를 ThoT가 어떻게 파편별로 분리 취득하는가를 보여주는 로직 차트.*

* 💡 **핵심 산업계 Insight:** RAG가 던져주는 문맥 덩어리는 하나의 깔끔한 동화책이 아닙니다. 이 문서 저 문서 잡다하게 긁혀온 극도의 **혼란스럽고 복잡한 문맥 노이즈(Chaotic Context)** 입니다. Thread of Thought는 LLM에게 "문서 통째로 읽고 퉁쳐서 말하지 말고, 문맥을 가닥(Thread) 단위로 하나씩 쪼개서 개별적으로 분석해 평가한 후 합쳐라"고 지시하여 지엽적 정보가 묻히는 정보 손실을 원천 차단합니다.

---

## 3. 읽기 노트 수동 작성: Chain of Note (CoN)

<img src="assets/images_new/Fig_3_4_page_27.png" width="600">
*Fig 3.4: [Chain of Note 메커니즘 (PDF p.26-29)] Retrieved 문서에 대해 즉각 대답하지 않고 요약 평가본을 선 도출함.*

* 💡 **핵심 기능:** 모델에게 검색된 문서 A, B, C를 줄 때, "답 찾아내"라고 하지 않고 "문서 A 요약 노트 적어. 질문에 답변 가능한지 평가결과도 적어"라고 지시합니다. 관련 없는 문서를 억지로 참조하여 답변을 꾸며내는 환각을 막고, 문서가 죄다 쓰레기일 경우 "정답을 도출할 문서가 없습니다" 라고 당당히 말할 수 있는 노이즈 내성(Noise Robustness)의 정점입니다.

---

## 4. 자기 성찰 검열 엔진: Chain of Verification (CoVe)

<img src="assets/images_new/Fig_3_5_page_30.png" width="600">
*Fig 3.5: [Chain of Verification(CoVe) 파이프라인 구조 (PDF p.30-31)] 답변 도출 후 스스로에게 재심문 하는 4단계 루프 시스템.*

AI 스스로 판사가 되어 본인의 대답을 재검열합니다:
1. **초기 답변 생성 (Draft Response)**
2. **검증 질문 계획 (Plan Verifications):** 자신의 대답 속 팩트를 확인하기 위해 스스로에게 검증용 후속 단답형 퀴즈들을 출제함.
3. **검증 질문 실행 (Execute Verifications):** 다시 문서들을 재검색(혹은 독자 추론)하여 검증 리포트 완성.
4. **최종 답변 생성 (Generate Final Verified Response):** 검증 시 틀렸던 팩트를 들어내며 수정 본판 배포.

---

## 5. 심리적/전문적 자극 기법 극대화 효과

단순 연산 명령을 넘어 거대 신경망은 인간 언어의 '미묘한 긴장감'에도 퍼포먼스 텐션을 올립니다.

<img src="assets/images_new/Fig_3_6_page_32.png" width="600">
<img src="assets/images_new/Fig_3_9_page_36.png" width="600">
*Fig 3.6 & 3.9: [EmotionPrompt 및 ExpertPrompting 적용 사례 차트 (PDF p.32-37)]*
<div style="display:flex; flex-wrap:wrap; margin-top:10px; margin-bottom:20px;">
<img src="assets/images_new/Fig_3_7_page_33.png" width="30%" style="margin:5px; border-radius:8px; box-shadow:0 4px 6px rgba(0,0,0,0.1);"><img src="assets/images_new/Fig_3_8_page_35.png" width="30%" style="margin:5px; border-radius:8px; box-shadow:0 4px 6px rgba(0,0,0,0.1);">
</div>

* **EmotionPrompt:** "이 답변은 내 커리어에 অত্যন্ত 중요하다(This is very important to my career)", "잘 대답하면 팁을 주겠다" 같은 감정적 부담 문구를 프롬프트에 추가하면 신기하게도 연산 집요성이 10% 이상 뛰어오르는 인간다운 어텐션 스파크 현상.
* **ExpertPrompting:** "해당 분야의 최고 권위자로서", "수석 보안 엔지니어의 관점에서" 라고 정체성(Persona) 페달을 밟아주면, 하위 계층 데이터를 배제하고 권위 있는 전문 용어와 구조 깊은 포맷의 상세 답변을 무조건 유도해냅니다.

---

## 💻 [Implementation Frameworks] DSPy를 활용한 오토 프롬프트 최적화
단순히 프롬프트를 텍스트로 치는 시대는 끝났습니다. 스탠포드의 **DSPy**는 프롬프트를 파이토치 신경망처럼 튜닝합니다.
```python
import dspy

# 1. 언어 모델 설정 
turbo = dspy.OpenAI(model="gpt-4o-mini")
dspy.settings.configure(lm=turbo)

# 2. 추론 모듈 (Signature) 선언
class BasicQA(dspy.Signature):
    """주어진 질문에 대해 해당 분야의 전문가로서(ExpertPrompting) 커리어의 사활을 걸고(EmotionPrompting) 사실에 입각하여 디테일하게 답변합니다."""
    question = dspy.InputField(desc="사용자의 질문")
    # 답변 생성 전 CoN, ThoT 로직을 반영한 중간 프로세서 가동 목적
    note = dspy.OutputField(desc="문서를 읽고 작성한 검증용 읽기 노트")  
    answer = dspy.OutputField(desc="가장 논리적이고 정답률 100%의 답변")

# 3. ChainOfThought 적용 (DSPy 내장 엔진으로 중간 경로 추적 활성)
cot_qa = dspy.ChainOfThought(BasicQA)
response = cot_qa(question="환각(Hallucination)을 줄이는 최신 프롬프팅 다단계 전략 3개를 서술해줘.")

print(response.reasoning) # 중간 추론 및 검증(CoVe) 도출 과정 자동 출력
print(response.answer)
```

## 마무리하며 통치의 족쇄
이번 2주 차에서는 감정적 자극(Emotion Prompt)부터 쓰레기 문맥 가닥 치기(Thread of Thought), 스스로 자백하는 4단계 검증(Chain of Verification)까지 LLM이 거짓말을 할 일말의 싹을 잘라버리는 추론 감금 메커니즘을 터득했습니다.
하지만 아무리 훌륭한 판사 프롬프트라도, 주어진 문서 덩어리 자체가 너무 크고 쓰레기 더미라면 필연적으로 과식(Out Of Context) 붕괴가 일어납니다. 다음 3주 차 대서사시 **"Advanced Document Chunking & Context Engineering"** 에서는 문서의 살과 뼈를 가장 예리한 가위로 잘라버리는 토막 내기 파서 분절 기술의 정점 파이프라인으로 뛰어들겠습니다!
