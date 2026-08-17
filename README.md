# 병원 폐업·해산·파산 실무 가이드 PRO (Mediem)

의료재단(의료법인) 및 의료기관의 폐업·해산·청산·파산 절차를 관리하는 **유료 전용** Streamlit 컨설팅 도구입니다.

## 주요 기능
- 핵심개념·의사결정 트리·용어사전·FAQ (원 가이드북 콘텐츠 기반)
- 재무 데이터 기반 **채무초과·영업불능 자동 진단** 및 경로(해산·청산 vs 파산) 추천
- **간트 차트 기반 8~15개월 전체 로드맵** 시각화
- 5개 영역(폐업/해산청산/파산/인사노무/세무행정) **인터랙티브 체크리스트** + 진행률 KPI
- **퇴직금 추정 계산기** (근속기간·평균임금 기반)
- **7종 실무 문서 템플릿 자동 생성** (환자·직원·거래처 공지문, 이사회 결의서, 채권신고 공고문 등) — txt/HTML 다운로드
- **종합 리스크 스코어(게이지 차트)** — 체크리스트 이행률 + 재무 리스크 + 금지행위 자가진단 가중 산출
- **AI 종합진단** — Gemini API 연동 (모델 자동 폴백: `gemini-3.6-flash` → `gemini-3.5-flash-lite` → `gemini-2.5-flash` → `gemini-2.0-flash`)
- **최종 HTML 종합 리포트** 다운로드 (재무진단 + 체크리스트 + AI 진단 통합)
- 진행상황 **JSON 저장/불러오기** (별도 DB 없이 세션 간 이어서 작업)
- **유료 라이선스 키 게이트** (Streamlit Secrets 기반)

## 로컬 실행
```bash
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml   # 값 입력 후
streamlit run app.py
```

## Streamlit Community Cloud 배포
1. GitHub 저장소에 이 폴더 전체를 업로드합니다 (Web UI 드래그앤드롭 가능).
2. [share.streamlit.io](https://share.streamlit.io) 에서 New app → 저장소/브랜치/`app.py` 지정 후 Deploy.
3. **App settings → Secrets** 에 `.streamlit/secrets.toml.example` 내용을 참고하여
   `GEMINI_API_KEY`, `LICENSE_KEYS`(또는 `LICENSE_KEY_HASHES`)를 등록합니다.
4. 파일명은 모두 ASCII로 구성되어 있어 Windows/Cloud 환경 호환성 문제가 없습니다.

## 폴더 구조
```
app.py                     # 진입점: 라이선스 게이트 + st.navigation 구성
lib/
  styles.py                # 프리미엄 UI 테마 (네이비·골드)
  content_data.py          # 가이드북 본문 콘텐츠 (핵심개념/서류/템플릿/FAQ/용어)
  checklist_data.py        # 5개 체크리스트 마스터 데이터 + 로드맵 데이터
  checklist_ui.py          # 체크리스트 공통 렌더링 컴포넌트
  calculations.py          # 재무진단·퇴직금·리스크 스코어 계산 (Decimal 정밀 계산)
  gemini_client.py         # Gemini API 연동 (모델 폴백 체인)
  report_generator.py      # 최종 HTML 종합 리포트 생성기
  license_gate.py          # 유료 라이선스 인증
  state.py                 # 세션 상태 초기화 및 JSON 저장/불러오기
views/
  page_00_home.py ~ page_10_ai_report.py   # 11개 화면
.streamlit/
  config.toml               # 테마 설정
  secrets.toml.example       # Secrets 등록 가이드 (실제 키는 Cloud Secrets에만 저장)
```

## 라이선스 키 발급 방법 (운영자용)
`LICENSE_KEYS` 에 콤마로 구분된 평문 키를 등록하거나, 더 안전하게 관리하려면 아래처럼
SHA-256 해시를 생성해 `LICENSE_KEY_HASHES` 에 등록하세요.
```python
import hashlib
print(hashlib.sha256("발급할키".encode()).hexdigest())
```

## ⚠️ 유의사항
본 프로그램은 실무 참고용이며, 법률·세무·노무 자문을 대체하지 않습니다. 사안별 사실관계 및
관할기관(보건소·주무관청·법원·세무서)에 따라 절차·서류가 달라질 수 있으므로, 중요한 의사결정 전
반드시 변호사·회계사·노무사 등 전문가와 사전 협의하시기 바랍니다.
