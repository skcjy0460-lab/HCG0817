import streamlit as st
from lib import styles
from lib.checklist_ui import render_checklist
from lib.content_data import BANKRUPTCY_DOCS, BANKRUPTCY_TIMELINE, RISK_WARNINGS
from lib.checklist_data import FORBIDDEN_ACTS

styles.hero(
    "③ 의료재단 파산 절차",
    "채무초과나 영업불능 등으로 정상적인 청산이 곤란할 때 법원의 관리 하에 법인을 종료하는 절차입니다. "
    "파산 선고 이후 자산의 관리·처분 권한은 관재인에게 이전됩니다.",
    eyebrow="PHASE 3-B · 파산",
)

stages = [
    ("사전 정리", "채무초과 또는 영업불능 상태를 입증할 자료를 확정합니다. 자산 목록, 부채 목록, 채권자 명부를 정확히 작성합니다."),
    ("이사회 파산 결의", "파산 신청을 의결하고, 신청 사유와 재무 수치를 명확히 기재합니다. 대표권자 지정도 필요합니다."),
    ("파산 신청서 제출", "관할 법원에 파산신청서와 첨부서류(재무제표, 자산·부채 목록, 채권자 명부, 이사회 회의록 등)를 제출합니다."),
    ("파산 선고", "법원이 파산 선고를 하면 자산 관리·처분 권한이 관재인에게 이전됩니다. 이후 모든 거래는 관재인의 승인이 필요합니다."),
    ("관재인 업무 진행", "관재인이 자산을 환가(매각)하고, 부당행위 조사를 실시하며, 채권자의 채권 신고를 받아 검증합니다."),
    ("배당 및 종결", "법정 우선순위에 따라 채권자에게 배당하고, 절차가 종결되면 법인이 말소됩니다."),
]
styles.section_title("절차 6단계")
for i, (title, desc) in enumerate(stages, 1):
    st.markdown(
        f"""
        <div class="mediem-card" style="border-left:4px solid #B0413E;">
            <h4>{i}. {title}</h4>
            <p>{desc}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")
styles.section_title("파산 신청 필수 서류 패키지")
doc_cols = st.columns(2)
for i, (doc, note) in enumerate(BANKRUPTCY_DOCS):
    with doc_cols[i % 2]:
        note_html = f"<div style='color:#6B7685;font-size:12px;margin-top:2px;'>{note}</div>" if note else ""
        st.markdown(
            f"""<div class="mediem-card" style="padding:12px 16px;">
            📄 <b style="color:#0F1B2D;font-size:13.3px;">{doc}</b>{note_html}
            </div>""",
            unsafe_allow_html=True,
        )

st.write("")
styles.section_title("예상 일정")
for t in BANKRUPTCY_TIMELINE:
    st.markdown(
        f"""<div class="mediem-card" style="display:flex;gap:16px;align-items:center;">
        <span class="badge badge-danger" style="min-width:96px;text-align:center;">{t['period']}</span>
        <span style="color:#1C2733;font-size:13.5px;">{t['desc']}</span>
        </div>""",
        unsafe_allow_html=True,
    )

st.write("")
forbidden_html = "".join([f"<li>{act}</li>" for act in FORBIDDEN_ACTS])
styles.alert(
    "danger",
    f"<b>🚨 절대 금지 행위 (중대 리스크) —</b> {RISK_WARNINGS['bankruptcy_forbidden']}"
    f"<ul style='margin-top:8px;'>{forbidden_html}</ul>",
)

st.write("")
styles.section_title("파산 절차 실행 체크리스트")
render_checklist("bankruptcy")

styles.footer()
