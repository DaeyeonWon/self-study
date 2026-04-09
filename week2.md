---
layout: default
title: 2주차. Prompting Strategies for Hallucination Reduction
---

# 2주차: Prompting Strategies for Hallucination Reduction (검색 문맥을 활용한 답변 정확도 혁신 고급 기법)

아무리 RAG를 통해 고품질의 팩트 문서를 5장 찾아서 LLM에게 쥐여주더라도, LLM이 문서를 대강 요약하다가 엉뚱한 결론으로 점프해버리면 말짱 도루묵입니다. 
이번 2주 차에서는 검색 시스템(Retriever)의 영역을 넘어 LLM 스스로 자신의 대답을 멱살 잡고 검열하게 만드는 **초고도화 프롬프트 추론 기술(Prompt Engineering Strategies)** 리스트를 전부 까발립니다. 단순 기능을 넘어 **전문가급 세미나의 근원이 되는 핵심 논문(Paper)** 베이스라인 패러다임들을 해부합니다.

---

## 1. 선형적 추론의 기본기: Chain of Thought (CoT)

단순히 "정답은 무엇인가?"라고 묻는 Zero-Shot의 한계를 돌파하기 위해 "Let's think step by step"이라는 지시를 추가하여 모델이 단계별 사고 과정을 거쳐 논리적 결론에 도달하도록 유도하는 기초 방어망입니다 [cite: 135].

* 🔬 **[Paper Reference]:** *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models (Wei et al., Google Brain, 2022)*
* **논문 인사이트:** 단순 지시를 내리면 복잡한 다단계 논리를 건너뛰고 오답을 내지만, 중간 사고 체인을 프롬프트 텍스트상에 강제로 남기게 하면 연산 로직이 끊어지지 않고 이어져 수학 및 추론 능력이 비약적으로 상승함을 세계 최초로 전 수학적으로 증명한 전설적 논문입니다.

---

## 2. 복잡한 난제를 파괴하는 혼돈 해석: Thread of Thought (ThoT)

혼란스럽고 복잡한 문맥에서 중요한 정보를 선별하기 위해 문맥을 나누어 요약하고 분석함[cite: 151, 156].

* 🔬 **[Paper Reference]:** *Thread of Thought Unraveling Chaotic Contexts (Zheng et al., 2023)*
* **논문 인사이트:** RAG로 긁어온 데이터는 100% 정제된 텍스트가 아닙니다. 표, 텍스트, 광고가 뒤섞인 혼돈의 문단 더미입니다. 이 논문은 LLM에게 "거대 문맥을 통째로 요약하지 말고, 관련된 정보의 가닥(Thread)을 하나하나 핀셋으로 뽑아내 분석한 후 합쳐라"고 지시하여, 노이즈가 가득한 문맥 속에서도 극강의 정보 추출력을 보여주는 패러다임을 제안합니다.

<br>
<img src="assets/images_new/mermaid_w2_0.png" width="80%" style="margin: 10px 0; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); background-color: white; padding: 10px;">
<br>

---

## 3. 읽기 노트 수동 작성: Chain of Note (CoN)

검색된 각 문서에 대해 '읽기 노트'를 작성하여 정보의 관련성과 답변 가능 여부를 사전 평가[cite: 186, 199].

* 🔬 **[Paper Reference]:** *Chain-of-Note: Enhancing Robustness in Retrieval-Augmented Language Models (Yu et al., Tencent AI, 2023)*
* **논문 인사이트:** LLM에게 바로 답변을 강요하지 않고, 모든 문서마다 `[Note: 이 문서는 질문의 핵심과 일치함 / 일치하지 않음]`을 먼저 스스로 평가 작성하게 만듭니다. 이렇게 하면 아예 쓸데없는 문서를 들고 거짓말을 치는(환각) 리스크를 완전히 박살 냅니다.

---

## 4. 자기 성찰 검열 엔진: Chain of Verification (CoVe)

초기 답변 생성 → 검증 질문 생성 → 재검색 및 검증 → 최종 수정 답변 생성의 4단계 프로세스 [cite: 235-239].

* 🔬 **[Paper Reference]:** *Chain-of-Verification Reduces Hallucination in Large Language Models (Dhuliawala et al., Meta AI, 2023)*
* **논문 인사이트:** 기계 스스로가 '판사'가 됩니다. 자기가 내놓은 답을 보고, "이게 사실이 맞나?"를 묻는 단답형 퀴즈를 5개 스폰폰해서 다시 문서와 대조합니다. 틀렸으면 스스로 수정된 답안을 도출해내는 극도의 자기 검열망 보우 시스템.

<br>
<img src="assets/images_new/mermaid_w2_1.png" width="80%" style="margin: 10px 0; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); background-color: white; padding: 10px;">
<br>

---

## 5. 심리적/전문적 자극 기법 극대화 효과

* **EmotionPrompt:** "커리어에 중요하다"와 같은 감정적 문구 추가 시 성능 향상[cite: 245, 258].
* **ExpertPrompting:** 모델에 특정 분야 전문가의 정체성을 부여하여 상세한 답변 유도[cite: 272, 280].

* 🔬 **[Paper Reference]:** *Large Language Models Understand and Can be Enhanced by Emotional Stimuli (Li et al., Microsoft, 2023)*
* **논문 인사이트:** 거대 신경망조차 인간의 '감정적 긴급도'에 반응하여 어텐션 가중치를 집중시킨다는 기이한 현상 증명. "이건 내 목숨과 연결되어 있어"라는 문장 하나만으로 코딩/추론 능력이 평균 10% 이상 수직 상승하는 어텐션 집중 효과가 실무 백엔드에 즉각 도입 중입니다.

<br>
<div style="display:flex; flex-wrap:wrap; margin-top:10px; margin-bottom:20px;">
<img src="assets/images_new/Fig_3_1_page_21.png" width="30%" style="margin:5px; border-radius:8px; box-shadow:0 4px 6px rgba(0,0,0,0.1);">
<img src="assets/images_new/Fig_3_2_page_23.png" width="30%" style="margin:5px; border-radius:8px; box-shadow:0 4px 6px rgba(0,0,0,0.1);">
<img src="assets/images_new/Fig_3_4_page_27.png" width="30%" style="margin:5px; border-radius:8px; box-shadow:0 4px 6px rgba(0,0,0,0.1);">
<img src="assets/images_new/Fig_3_5_page_30.png" width="30%" style="margin:5px; border-radius:8px; box-shadow:0 4px 6px rgba(0,0,0,0.1);">
<img src="assets/images_new/Fig_3_6_page_32.png" width="30%" style="margin:5px; border-radius:8px; box-shadow:0 4px 6px rgba(0,0,0,0.1);">
<img src="assets/images_new/Fig_3_7_page_33.png" width="30%" style="margin:5px; border-radius:8px; box-shadow:0 4px 6px rgba(0,0,0,0.1);">
<img src="assets/images_new/Fig_3_8_page_35.png" width="30%" style="margin:5px; border-radius:8px; box-shadow:0 4px 6px rgba(0,0,0,0.1);">
<img src="assets/images_new/Fig_3_9_page_36.png" width="30%" style="margin:5px; border-radius:8px; box-shadow:0 4px 6px rgba(0,0,0,0.1);">
<img src="assets/images_new/Fig_3_10_page_38.png" width="30%" style="margin:5px; border-radius:8px; box-shadow:0 4px 6px rgba(0,0,0,0.1);">
</div>
