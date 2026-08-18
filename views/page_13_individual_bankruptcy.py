import streamlit as st
from lib import styles
from lib.checklist_ui import render_checklist
from lib.content_data import INDIVIDUAL_BANKRUPTCY_DOCS, RISK_WARNINGS
from lib.checklist_data import FORBIDDEN_ACTS_INDIVIDUAL

styles.hero(
    "개인파산·면책 절차 (개인 병의원 원장)",
    "소득이나 재산이 거의 없어 변제가 사실상 불가능한 경우, 법원에 파산을 신청하고 "
    "면책을 받아 채무에서 벗어나는 절차입니다.",
    eyebrow="개인 병의원 트랙 · 개인파산·면책",
)

stages = [
    ("사전 준비", "재산목록·채무목록을 전수 조사하고, 최근 2년 이내 재산 처분·증여·변제 내역을 정리합니다. 면책불허가 사유 해당여부를 자가점검합니다."),
    ("법원 신청", "관할 법원에 파산 및 면책 신청서를 함께 제출합니다(통상 동시 신청). 채권자 목록, 재산목록, 진술서를 첨부합니다."),
    ("파산 선고", "법원이 파산을 선고합니다. 재산이 거의 없으면 관재인 선임 없이 '동시폐지'로 간소하게 진행될 수 있습니다."),
    ("채권자집회·심문", "필요 시 채권자집회 및 법원 심문이 진행됩니다. 성실하게 자료를 제출하고 질의에 응답합니다."),
    ("면책 결정", "법원이 면책 여부를 심사하여 결정합니다. 면책이 확정되면 비면책채권을 제외한 나머지 채무에서 벗어납니다."),
]
styles.section_title("절차 5단계")
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
styles.section_title("개인파산·면책 필수 서류 패키지")
doc_cols = st.columns(2)
for i, (doc, note) in enumerate(INDIVIDUAL_BANKRUPTCY_DOCS):
    with doc_cols[i % 2]:
        note_html = f"<div style='color:#6B7685;font-size:12px;margin-top:2px;'>{note}</div>" if note else ""
        st.markdown(
            f"""<div class="mediem-card" style="padding:12px 16px;">
            📄 <b style="color:#0F1B2D;font-size:13.3px;">{doc}</b>{note_html}
            </div>""",
            unsafe_allow_html=True,
        )

st.write("")
forbidden_html = "".join([f"<li>{act}</li>" for act in FORBIDDEN_ACTS_INDIVIDUAL])
styles.alert(
    "danger",
    f"<b>🚨 면책불허가·부인권 리스크 —</b> {RISK_WARNINGS['individual_forbidden']}"
    f"<ul style='margin-top:8px;'>{forbidden_html}</ul>",
)

styles.alert(
    "warn",
    "<b>비면책채권 유의 —</b> 면책이 확정되어도 세금, 벌금·과태료, 고의적 불법행위로 인한 손해배상 등 "
    "일부 채무는 면책 대상에서 제외됩니다. 채무 목록 작성 시 어떤 채무가 비면책채권에 해당하는지 "
    "전문가와 함께 사전에 확인하세요.",
)

st.write("")
styles.section_title("개인파산·면책 실행 체크리스트")
render_checklist("individual_bankruptcy")

styles.footer()
