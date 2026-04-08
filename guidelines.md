# RAG 스터디 자료 작성 지침 (Guidelines)

이 지침은 "RAG Master" 과정의 1주차부터 8주차까지의 세미나 자료를 작성할 때 반드시 준수해야 하는 규칙을 정리한 것입니다.

## 1. 기본 원칙
- **이론 중심**: 특정 솔루션(예: 특정 회사의 상용 서비스, 특정 벤더의 데이터베이스 등)에 대한 내용은 최대한 배제하고 개념과 이론 중심으로 설명합니다.
- **초보자 친화적 & 예시 필수**: 처음 해당 이론을 접하는 사람도 완전히 이해할 수 있도록 아주 친절하고 상세하게 설명합니다. **(중요) 모든 개념 설명 뒤에는 항상 "간단하고 이해하기 쉬운 명시적인 예시(예: 일상 생활의 비유 등)"를 추가합니다.**
- **자기완결성**: 해당 문서만 읽어도 해당 주차의 토픽을 완벽히 이해할 수 있도록 풍부한 내용을 담습니다.

## 2. 콘텐츠 구성
- **PDF 참고**: `RAG Guide.pdf`의 내용을 기본 토대로 활용합니다. PDF에 포함된 그림이나 표의 주요 내용을 활용하거나 설명에 포함합니다. (텍스트로 표를 재구성하거나, 시각 자료는 Mermaid 다이어그램 등으로 재현합니다).
- **최신 내용 보충 (웹 검색)**: PDF 내용 외에도 필요하다면 인터넷 검색을 통해 최신의 이론, 기법, 이미지를 찾아 내용을 보충합니다.
- **출처 명시**: 인터넷에서 참고한 새로운 내용이나 이론에 대해서는 반드시 하단이나 해당 부분에 출처(링크 등)를 명시합니다.

## 3. 웹페이지(마크다운) 형식
- GitHub Pages에서 잘 보이도록 Markdown(`*.md`) 형식으로 작성합니다.
- 각 주차별로 개별 파일(예: `week1.md`, `week2.md`...)을 생성하고, 파일 시작 부분에 제목과 목차를 분명히 명시합니다.
- 가독성을 높이기 위해 적절한 헤딩(`##`, `###`), 글머리 기호(`-`), 강조(`**`), 코드 블록 등을 활용합니다.

## 4. 주차별 작성 토픽
1주차: RAG Fundamentals & System Challenges
2주차: Prompting Strategies for Hallucination Reduction
3주차: Advanced Document Chunking & Context Engineering
4주차: Embedding Models & Representation Learning for Retrieval
5주차: Vector Databases & Retrieval Architecture Design
6주차: Reranking Models and Hybrid Retrieval Techniques
7주차: Knowledge Graph RAG & Graph-based Retrieval Systems
8주차: RAG Evaluation, Monitoring & Optimization

---
*참고: 작성을 진행할 때는 매 단계 이 지침을 상기하여 누락되는 조건이 없도록 합니다.*
