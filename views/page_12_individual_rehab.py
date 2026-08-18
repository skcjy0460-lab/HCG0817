import streamlit as st
from lib import styles
from lib.checklist_ui import render_checklist
from lib.content_data import INDIVIDUAL_REHAB_DOCS, RISK_WARNINGS

styles.hero(
    "개인회생 절차 (개인 병의원 원장)",
    "안정적 소득이 있는 원장이 3~5년간 가용소득을 변제에 투입하고, 계획을 성실히 이행하면 "
    "나머지 채무를 면책받는 절차입니다.",
    eyebrow="개인 병의원 트랙 · 개인회생",
)

stages = [
    ("사전 준비", "채무 목록과 재산목록을 전수 조사하고, 최근 소득 자료(종합소득세 신고서 등)를 준비합니다. 변제계획안 초안을 작성합니다."),
    ("법원 신청", "관할 법원(회생법원/지방법원)에 개인회생 신청서와 채권자 목록, 재산목록, 수입지출목록을 제출합니다."),
    ("회생위원 면담", "회생위원이 신청 서류를 검토하고 보정을 요구할 수 있습니다. 소득·재산 관련 자료를 성실히 제출합니다."),
    ("변제계획인가", "법원이 변제계획을 인가하면, 인가일로부터 3~5년간 매월 정해진 금액을 변제합니다."),
    ("면책 결정", "변제계획을 성실히 이행하고 완료하면 법원이 나머지 채무에 대해 면책 결정을 내립니다."),
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
styles.section_title("개인회생 필수 서류 패키지")
doc_cols = st.columns(2)
for i, (doc, note) in enumerate(INDIVIDUAL_REHAB_DOCS):
    with doc_cols[i % 2]:
        note_html = f"<div style='color:#6B7685;font-size:12px;margin-top:2px;'>{note}</div>" if note else ""
        st.markdown(
            f"""<div class="mediem-card" style="padding:12px 16px;">
            📄 <b style="color:#0F1B2D;font-size:13.3px;">{doc}</b>{note_html}
            </div>""",
            unsafe_allow_html=True,
        )

styles.alert("danger", f"<b>⚠️ 재산 신고 유의사항 —</b> {RISK_WARNINGS['individual_asset_disclosure']}")

st.write("")
styles.section_title("개인회생 실행 체크리스트")
render_checklist("individual_rehab")

styles.footer()
