# Toss AI Platform Data Assistant Mini Project

## Project Goal

AI Hub 금융분야 고객상담 데이터를 활용해 AI 안전성 모델 학습 데이터 업무와 연결되는 역량을 보여주는 미니 프로젝트입니다. 원문 상담 텍스트는 외부 반출하지 않고, 공개 가능한 라벨 필드와 집계 통계만 사용했습니다.

## Dataset Scope

- 데이터 출처: AI Hub 금융분야 고객상담 데이터
- 데이터 구성: Training/Validation, 원천데이터/라벨링데이터
- 도메인: 은행(bk), 보험(ins), 증권(sec)
- 분석 대상: 라벨링 JSON의 메타데이터 및 QA 라벨 필드
- 제외 대상: 상담 원문, 질문/답변 본문, 생성 출력문

## Key Findings

- 전체 zip 파일 수: 88개
- 전체 JSON 파일 수: 155,262개
- 원천 JSON: 65,262개
- 라벨링 JSON: 90,000개
- 라벨링 데이터 도메인 분포:
  - 은행: 45,000개
  - 보험: 27,000개
  - 증권: 18,000개
- 주요 라벨 필드:
  - `consulting_category`
  - `consulting_topic`
  - `task_category`
  - `consulting_situation`
  - `qa_topic`
  - `consulting_purpose`
  - `core_financial_terms`

## Toss JD Connection

이 프로젝트는 토스 AI Platform팀 Data Assistant 업무 중 다음 역량과 연결됩니다.

- 한국어 금융 상담 문장의 맥락을 구조화하는 능력
- 라벨 기준을 일관되게 적용하고 점검하는 능력
- 라이브 트래픽 오탐 발굴에 필요한 유형별 분포 확인 관점
- SQL을 활용한 라벨 분포, 누락, 중복, 이상치 점검 능력
- 개인정보 및 금융 보안 맥락을 고려한 데이터 취급 태도

## Deliverables

- `risk_labeling_guideline.md`: 개인정보/유해성 위험도 3단계 분류 기준
- `sql/quality_checks.sql`: 라벨 품질 점검용 SQL 쿼리
- `scripts/build_safe_summary.py`: 원문 제외 집계 통계 생성 스크립트
- `outputs/`: 스크립트 실행 결과 저장 위치

## Resume Summary

AI Hub 금융 고객상담 데이터의 원천/라벨링 JSON 구조를 분석하고, 은행·보험·증권 도메인별 상담 유형, 업무 상황, 핵심 금융 용어 라벨 분포를 점검했습니다. 원문 텍스트를 외부 반출하지 않는 조건에서 라벨 필드 기반 통계만 산출했으며, SQL 품질 점검 관점으로 누락·중복·분포 편향을 확인하는 미니 프로젝트를 수행했습니다.

## Interview Pitch

욕설이나 유해성 데이터 라벨링을 직접 수행한 경험은 아직 없지만, 금융 고객상담 텍스트 데이터를 기준화해서 분석한 경험이 있습니다. 이 데이터는 상담 주제, 업무 상황, 핵심 금융 용어처럼 맥락 판단이 필요한 라벨 필드를 포함하고 있어, 한국어 상담 문장을 일관된 기준으로 구조화하는 연습이 되었습니다. 또한 원문 반출 제한을 지키면서 라벨 통계만 분리해 분석했기 때문에, 개인정보와 보안이 중요한 토스 AI 안전성 데이터 업무에도 책임감 있게 적응할 수 있다고 생각합니다.
