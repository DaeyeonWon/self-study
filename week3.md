---
layout: default
title: 3주차. Advanced Document Chunking & Context Engineering
---

# 3주차: Advanced Document Chunking & Context Engineering
> 검색 성능의 기초가 되는 텍스트 분할 최적화 전략

청킹(Chunking)은 RAG 파이프라인의 가장 기초적이면서도 가장 과소평가되는 단계입니다. 청크의 크기와 방식은 **검색 품질, 저장 비용, 쿼리 지연 시간, 환각 발생 여부에 직접적으로 영향**을 미칩니다.

---

## 1. 청킹의 영향력 개요

### 이론 설명

텍스트 분할은 다음 4가지 요인 모두에 영향을 미칩니다:
- **검색 품질**: 너무 크면 노이즈 포함, 너무 작으면 문맥 단절
- **스토리지 비용**: 청크 수 × 임베딩 차원 = 저장 용량
- **쿼리 지연**: 검색되는 청크 수와 토큰 합산량에 비례
- **환각 여부**: 문맥이 잘린 청크는 LLM의 판단 오류를 유발

### PDF 원본 자료

<img src="assets/images_new/Fig_4_1_page_40.png" width="600">

*Fig 4.1: 청킹 파라미터(Chunk Size 50, Overlap 15) 설정에 따른 문서 분할 시각화 — 색상 구분으로 오버랩 구간 확인 가능 (PDF p.41)*

### 청킹 전략 선택 기준 3요소 (PDF p.42-44)

1. **문서 구조**: 코드/테이블/일반 텍스트에 따라 최적 전략이 다름
2. **임베딩 모델의 토큰 한계**: text-embedding-3 기준 최대 8,191 토큰
3. **질문 유형**: 단답형 팩트 QA vs. 통합 요약 쿼리에 따라 청크 크기 최적화

---

## 2. Recursive Character Splitter

### 이론 설명

계층적 구분자를 순차적으로 시도하여 문맥을 최대한 보존하면서 분할합니다. 분할 우선순위: `\n\n` → `\n` → `.` → `!?` → ` ` → `""`.

### 관련 논문 / 레퍼런스

**📄 LangChain RecursiveCharacterTextSplitter (공식 구현체)**
- 실제 프로덕션 환경에서 가장 널리 채택되는 베이스라인 청킹 방식
- 문단 → 줄 → 문장 → 단어 순의 계층적 우선순위로 자연어 단위를 최대한 보존

---

## 3. Semantic Splitting (의미 기반 분할)

### 이론 설명

임베딩 모델을 활용하여 인접한 문장 간 코사인 유사도를 측정하고, **주제가 전환되는 지점(유사도 급감 지점)**에서 자동 분할합니다.

### 관련 논문

**📄 Semantic Chunking for RAG (Greg Kamradt, 2024)**
- 단순 글자 수 기반 청킹 대비 검색 F1 점수 12% 향상 보고
- Breakpoint Threshold(일반적으로 95th percentile)를 초과하는 지점을 분할 기준으로 설정
- **단점**: 임베딩 호출 비용이 추가로 발생, 짧은 문서에서는 오히려 과분할 위험

---

## 4. Document Specific Splitting (구조 인식 분할)

### 이론 설명

HTML 태그, Markdown 헤더, PDF 레이아웃 등 **문서의 구조적 메타데이터를 인식하여 논리 단위로 분할**합니다. 표(Table)나 코드 블록이 중간에 잘리는 것을 방지합니다.

### 관련 논문 / 도구

**📄 Unstructured.io / LlamaParse (2024)**
- PDF, PPT, Excel 등 비정형 문서에서 표·이미지·헤더를 구조적으로 추출
- 표(Table)를 Markdown 형식으로 변환하여 청킹 시 셀 단위 정보 보존
- **Impact**: 재무보고서, 법률 문서 처리 시 검색 정확도 20~30% 향상 사례 보고

---

## 5. LLM 기반 Propositions 청킹 (원자적 사실 분해)

### 이론 설명

LLM을 파서로 활용하여 텍스트를 **독립적이고 원자적인 사실 명제(Atomic Proposition)** 단위로 분해합니다. 각 청크가 하나의 완결된 팩트를 담도록 강제하여 검색 명중률을 극대화합니다.

### 예시

```
[원본 텍스트]
"이순신 장군은 1545년에 태어났으며, 1598년 노량해전에서 전사했고 거북선을 개발했습니다."

[Proposition 청킹 결과]
1. "이순신 장군은 1545년에 태어났다."
2. "이순신 장군은 1598년 노량해전에서 전사했다."
3. "이순신 장군은 거북선을 개발했다."
```

### 관련 논문

**📄 Dense X Retrieval: What Retrieval Granularity Should We Use? (Chen et al., University of Waterloo, 2023)**
- Proposition 단위 청킹이 문단/문장 단위 대비 검색 Recall을 20% 이상 개선
- 하나의 청크에 여러 팩트가 혼재될 경우 관련 없는 팩트가 검색 노이즈로 작용함을 실증

---

## 6. 청킹 효과 측정 지표 (PDF p.57-58)

### 이론 설명

두 가지 핵심 지표로 청킹 전략의 효과를 정량 평가합니다:

- **Chunk Attribution**: "이 청크가 실제 최종 답변 생성에 기여했는가?" — 기여하지 않은 청크는 노이즈
- **Chunk Utilization**: "검색된 청크의 텍스트 중 실제로 참조된 비율" — 낮으면 청크가 너무 큼

### 아키텍처 다이어그램

<br>
<img src="assets/images_new/mermaid_w3_0.png" width="80%" style="margin: 10px 0; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); background-color: white; padding: 10px;">
<br>

---

## 💻 구현: LangChain + LlamaIndex 청킹 실습

### 관련 프레임워크 및 라이브러리

| # | 프레임워크 / 라이브러리 | 특징 | 추천 청킹 방식 |
|---|-----------|------|------------|
| 1 | **LangChain TextSplitters** | RecursiveCharacter, Token, Markdown 등 10종+ 스플리터 내장 | 일반 텍스트, 범용 |
| 2 | **LlamaIndex NodeParsers** | SemanticSplitter, HierarchicalNodeParser, SentenceWindow | 의미 기반·계층형 |
| 3 | **Unstructured.io** | PDF·Table·Image 구조 인식 오픈소스 파서 | 비정형 문서 (표, 양식) |
| 4 | **LlamaParse** | 고품질 PDF 파서 API, 복잡한 레이아웃 처리 | 복잡한 PDF (재무제표) |
| 5 | **DoclingParser (IBM)** | 오픈소스 문서 이해 엔진, 표·수식·이미지 추출 | 학술 논문, 기술 문서 |
| 6 | **PyMuPDF (fitz)** | 빠른 PDF 텍스트/이미지 추출, 레이아웃 보존 | 대용량 PDF 처리 |
| 7 | **pdfplumber** | 표(Table) 추출에 특화된 Python 라이브러리 | PDF 내 표 데이터 |
| 8 | **Marker (VikParuchuri)** | PDF → Markdown 고품질 변환, OCR 내장 | PDF를 Markdown으로 변환 |
| 9 | **Chonkie** | 경량 청킹 전용 라이브러리, 다양한 전략 지원 | 빠른 청킹 실험 |
| 10 | **Textsplitter (jina-ai)** | 의미적 유사도 기반 적응형 분할 | 다국어 의미 기반 |
| 11 | **Surya (VikParuchuri)** | 다국어 OCR + 레이아웃 분석, 90개 언어 | 스캔 문서, 이미지 PDF |
| 12 | **Camelot** | PDF 표 추출 전용, Lattice/Stream 두 가지 방식 | 정형 표 데이터 추출 |

### 클라우드 서비스

| 서비스 | 제공사 | 특징 |
|--------|--------|------|
| **Azure AI Document Intelligence** | Microsoft | OCR + 구조 인식, 표/양식 추출 |
| **Amazon Textract** | AWS | PDF/이미지 텍스트·표·서식 추출 |
| **Google Document AI** | Google | ML 기반 비정형 문서 파싱 |

### 코드 샘플 1: RecursiveCharacterTextSplitter (기본)

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

# 문서 로드
loader = PyPDFLoader("company_report.pdf")
documents = loader.load()

# Recursive 분할: 문단 > 줄 > 문장 순으로 우선순위 보존
splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", ".", "!", "?", " ", ""],
    chunk_size=512,      # 512 토큰 이하
    chunk_overlap=64,    # 64 토큰 오버랩으로 문맥 연결
    length_function=len,
    add_start_index=True  # 원본 문서 내 위치 메타데이터 추가
)
chunks = splitter.split_documents(documents)

print(f"총 청크 수: {len(chunks)}")
print(f"청크 샘플:\n{chunks[0].page_content[:200]}")
print(f"메타데이터: {chunks[0].metadata}")
```

### 코드 샘플 2: LlamaIndex Semantic Splitter (의미 기반)

```python
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding

# 문서 로드
documents = SimpleDirectoryReader("./data/").load_data()

# 의미 기반 분할기 초기화
embed_model = OpenAIEmbedding(model="text-embedding-3-small")
splitter = SemanticSplitterNodeParser(
    buffer_size=1,                       # 인접 1개 문장씩 비교
    breakpoint_percentile_threshold=95,  # 유사도 상위 5% 변화 지점에서 분할
    embed_model=embed_model,
)

nodes = splitter.get_nodes_from_documents(documents)
print(f"의미 기반 청크 수: {len(nodes)}")

# Chunk Attribution 평가: 각 노드의 실제 답변 기여도 측정
for i, node in enumerate(nodes[:3]):
    print(f"\n[청크 {i}] 길이: {len(node.text)} 글자")
    print(f"텍스트 앞부분: {node.text[:100]}...")
```

### 코드 샘플 3: Proposition 기반 LLM 청킹

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

proposition_prompt = PromptTemplate(
    input_variables=["text"],
    template="""다음 텍스트를 독립적이고 원자적인 사실 명제들로 분해하십시오.
각 명제는:
1. 그 자체로 완결된 의미를 가져야 합니다
2. 다른 명제를 참조하지 않아도 이해 가능해야 합니다
3. 하나의 핵심 사실만 담아야 합니다

텍스트:
{text}

명제 목록 (번호 매겨서 출력):"""
)

def chunk_to_propositions(text: str) -> list[str]:
    """텍스트를 원자적 명제 단위로 분해"""
    chain = proposition_prompt | llm
    result = chain.invoke({"text": text})
    
    # 번호 제거하고 명제 리스트 추출
    lines = result.content.strip().split("\n")
    propositions = [
        line.lstrip("0123456789. ").strip()
        for line in lines
        if line.strip() and line[0].isdigit()
    ]
    return propositions

# 테스트
sample_text = """
삼성전자는 1969년에 설립되었으며 대한민국에 본사를 두고 있습니다. 
2024년 기준 글로벌 반도체 시장 점유율 1위를 기록하였고, 
갤럭시 스마트폰 시리즈로 전 세계 22개국에서 판매량 1위를 차지했습니다.
"""

props = chunk_to_propositions(sample_text)
for i, prop in enumerate(props, 1):
    print(f"{i}. {prop}")
```

---

다음 주차 → [4주차: Embedding Models & Representation Learning](week4.md)
