import streamlit as st
from lib import styles
from lib.checklist_ui import render_checklist
from lib.content_data import RISK_WARNINGS

styles.hero(
    "① 의료기관(병원·의원) 폐업 신고 및 환자 보호",
    "폐업은 보건소에 신고하는 행정 절차이지만, 그 이면에는 환자의 진료 연속성과 의료기록 보호라는 "
    "중대한 책임이 있습니다.",
    eyebrow="PHASE 1 · 의료기관 폐업",
)

styles.section_title("절차 개요")
st.markdown(
    """
    <div class="mediem-card">
    <p>폐업일(마지막 진료일)을 확정한 후에는 예약 환자, 치료 중인 환자, 입원 환자에 대한 체계적인 안내와
    이관 계획을 수립해야 합니다. 특히 만성질환자나 지속 치료가 필요한 환자의 경우 다른 의료기관으로의
    원활한 전원을 돕는 것이 의료인의 책무입니다.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

steps = [
    ("01", "폐업일 확정 및 내부 공지", "진료 종료일(마지막 진료일)을 명확히 정하고, 전 직원에게 일정과 역할을 안내합니다."),
    ("02", "환자 보호 조치", "예약/입원/치료 중인 환자 명단을 작성하고, 개별 안내(전화/문자) 및 게시판 공지를 병행합니다."),
    ("03", "진료기록 관리 체계 구축", "진료기록 보관 책임자를 지정하고, 폐업 이후에도 기록 발급·열람 요청에 대응할 수 있는 프로세스를 마련합니다."),
    ("04", "보건소 폐업 신고", "관할 보건소에 폐업신고서와 필요 첨부서류를 제출합니다. 지역별로 요구사항이 다를 수 있으니 사전 확인이 필요합니다."),
    ("05", "사후 행정 처리", "간판 및 옥외광고물 철거, 홈페이지·SNS 폐업 안내 게시, 의료폐기물 처리, 의약품 재고 정리 등을 완료합니다."),
]
for no, title, desc in steps:
    st.markdown(
        f"""
        <div class="mediem-card" style="display:flex;gap:14px;align-items:flex-start;">
            <span class="step-num" style="background:#1B3A5C;">{no}</span>
            <div>
                <div style="font-weight:700;color:#0F1B2D;font-size:14.3px;">{title}</div>
                <div style="color:#1C2733;font-size:13.2px;line-height:1.7;margin-top:2px;">{desc}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

styles.alert("danger", f"<b>⚠️ 리스크 포인트 —</b> {RISK_WARNINGS['records']}")

st.write("")
styles.section_title("현장 실무 체크리스트", "항목을 체크하면 자동으로 진행률에 반영되고, 마지막 리포트에도 포함됩니다.")
render_checklist("closure")

styles.footer()
