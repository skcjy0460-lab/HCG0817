import streamlit as st
from lib import styles
from lib.checklist_ui import render_checklist
from lib.content_data import LIQUIDATION_DOCS, RISK_WARNINGS

styles.hero(
    "② 의료재단 해산·청산 절차",
    "채무를 모두 정리할 수 있는 재무 상태에서 선택하는 정상 종료 경로입니다. "
    "이사회의 해산 결의로 시작하여 청산종결 등기에 이르기까지 체계적인 절차를 거쳐야 합니다.",
    eyebrow="PHASE 3-A · 해산·청산",
)

stages = [
    ("이사회 해산 결의", "해산 사유와 재무 수치를 명확히 기재한 결의서를 작성하고, 청산인을 선임합니다. 청산인의 권한 범위와 책임을 명시해야 합니다."),
    ("주무관청 허가 신청", "관할 시·도에 해산 허가(또는 승인) 신청서를 제출합니다. 최근 3개년 재무제표, 자산·부채 현황, 청산 계획서 등을 첨부합니다."),
    ("채권자 보호 절차", "채권자에게 일정 기간(통상 2개월) 내에 채권을 신고하도록 공고합니다. 공고는 관보 및 일간신문에 2회 이상 게재하는 것이 일반적입니다."),
    ("자산 환가 및 채무 변제", "자산을 시가로 처분하고(감정평가 등 공정성 확보), 법정 우선순위에 따라 채무를 변제합니다. 임금·세금 등 우선채권을 먼저 처리해야 합니다."),
    ("청산종결 및 등기", "잔여재산은 정관에 따라 귀속 처리하고, 청산종결 등기를 거쳐 법인을 말소합니다. 세무상 폐업 신고도 병행합니다."),
]
styles.section_title("절차 5단계")
for i, (title, desc) in enumerate(stages, 1):
    st.markdown(
        f"""
        <div class="mediem-card gold-edge">
            <h4>{i}. {title}</h4>
            <p>{desc}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")
styles.section_title("해산·청산 필수 서류 패키지")
doc_cols = st.columns(2)
for i, (doc, note) in enumerate(LIQUIDATION_DOCS):
    with doc_cols[i % 2]:
        note_html = f"<div style='color:#6B7685;font-size:12px;margin-top:2px;'>{note}</div>" if note else ""
        st.markdown(
            f"""<div class="mediem-card" style="padding:12px 16px;">
            📄 <b style="color:#0F1B2D;font-size:13.3px;">{doc}</b>{note_html}
            </div>""",
            unsafe_allow_html=True,
        )

styles.alert("danger", f"<b>⚠️ 자본잠식 상태 주의 —</b> {RISK_WARNINGS['liquidation_capital']}")

st.write("")
styles.section_title("해산·청산 실행 체크리스트")
render_checklist("liquidation")

styles.footer()
