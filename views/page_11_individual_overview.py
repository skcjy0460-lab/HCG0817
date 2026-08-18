import streamlit as st
from lib import styles
from lib.calculations import individual_path_diagnosis
from lib.content_data import (
    INDIVIDUAL_CORE_CONCEPTS, INDIVIDUAL_DECISION_STEPS, RISK_WARNINGS,
)
from lib.checklist_data import FORBIDDEN_ACTS_INDIVIDUAL

styles.hero(
    "개인 병의원(원장 개인 명의) 폐업·채무정리 개요",
    "의료법인이 아닌 개인사업자로 운영하는 병·의원은 '법인 해산'이 아니라 "
    "폐업신고 + 원장 개인의 개인회생/개인파산 절차로 채무 문제를 정리합니다.",
    eyebrow="개인 병의원 트랙 · STEP 1",
)

styles.alert(
    "warn",
    "<b>먼저 확인하세요 —</b> 의료기관(병원 건물·진료) 폐업 절차 자체는 법인이든 개인이든 동일합니다. "
    "사이드바의 <b>'① 의료기관 폐업'</b> 체크리스트를 함께 이용하시고, 이 트랙에서는 "
    "<b>원장 개인의 채무 정리(개인회생/개인파산)</b>에 집중합니다.",
)

styles.section_title("핵심 개념")
cols = st.columns(3)
for col, concept in zip(cols, INDIVIDUAL_CORE_CONCEPTS):
    with col:
        bullets_html = "".join([f"<li>{b}</li>" for b in concept["bullets"]])
        st.markdown(
            f"""
            <div class="mediem-card gold-edge" style="min-height:250px;">
                <h4>{concept['icon']} {concept['title']}</h4>
                <p>{concept['desc']}</p>
                <ul style="margin-top:10px;padding-left:18px;color:#1C2733;font-size:13.3px;line-height:1.85;">
                    {bullets_html}
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")
styles.section_title("경로 선택 의사결정 흐름", "개인회생 vs 개인파산: 4단계로 판단합니다.")
for step in INDIVIDUAL_DECISION_STEPS:
    st.markdown(
        f"""
        <div class="mediem-card" style="display:flex;align-items:flex-start;">
            <span class="step-num">{step['step']}</span>
            <div>
                <div style="font-weight:700;color:#0F1B2D;font-size:14.5px;margin-bottom:3px;">{step['title']}</div>
                <div style="color:#1C2733;font-size:13.3px;line-height:1.7;">{step['desc']}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")
styles.section_title("① 재무·소득 현황 입력", "원장 개인 명의의 재산·채무·소득을 입력하면 개인회생/개인파산 경로를 참고 진단합니다.")

ind = st.session_state["individual_inputs"]
c1, c2 = st.columns(2)
with c1:
    st.markdown("**재산 · 채무 (원장 개인 명의)**")
    total_assets = st.number_input(
        "총재산(부동산·차량·예금·보험해약환급금 등, 원)", min_value=0, step=1_000_000,
        value=int(ind.get("total_assets", 0)), format="%d",
    )
    total_debt = st.number_input(
        "총채무(사업용+개인용 포함, 원)", min_value=0, step=1_000_000,
        value=int(ind.get("total_debt", 0)), format="%d",
    )
with c2:
    st.markdown("**월 소득 · 생계비**")
    monthly_income = st.number_input(
        "월 소득(봉직의 근무 등 폐업 이후 예상 소득, 원)", min_value=0, step=100_000,
        value=int(ind.get("monthly_income", 0)), format="%d",
    )
    monthly_living_cost = st.number_input(
        "월 최저 생계비(법원 기준 인정 생계비, 원)", min_value=0, step=100_000,
        value=int(ind.get("monthly_living_cost", 0)), format="%d",
    )
has_stable_income = st.checkbox(
    "폐업 이후에도 안정적 소득(봉직의 근무 등)을 유지할 수 있다",
    value=bool(ind.get("has_stable_income", True)),
)

st.session_state["individual_inputs"] = {
    "total_assets": total_assets, "total_debt": total_debt,
    "monthly_income": monthly_income, "monthly_living_cost": monthly_living_cost,
    "has_stable_income": has_stable_income,
}

result = individual_path_diagnosis(total_assets, total_debt, monthly_income, monthly_living_cost, has_stable_income)

st.write("")
styles.section_title("② 진단 결과")
k1, k2, k3, k4 = st.columns(4)
with k1:
    styles.kpi("월 가용소득", f"{result['monthly_available']:,.0f}원",
               "변제 재원" , "#2E6B4F" if result["monthly_available"] > 0 else "#B0413E")
with k2:
    styles.kpi("청산가치(추정 처분재산)", f"{result['liquidation_value']:,.0f}원")
with k3:
    styles.kpi("60개월 변제총액(추정)", f"{result['est_rehab_total_60']:,.0f}원")
with k4:
    styles.kpi("청산가치 보장 원칙", "충족" if result["meets_liquidation_value"] else "미충족", "",
               "#2E6B4F" if result["meets_liquidation_value"] else "#B0413E")

path_map = {
    "individual_rehab": ("개인회생 경로 권장", "안정적 소득과 청산가치 보장 조건을 충족할 가능성이 높습니다. '개인회생 절차' 메뉴를 참고하세요.", "ok"),
    "individual_bankruptcy": ("개인파산·면책 경로 검토 필요", "소득이 불안정하거나 가용소득이 없어 변제계획 이행이 어려울 것으로 보입니다. '개인파산·면책 절차' 메뉴를 참고하세요.", "danger"),
    "review": ("전문가 검토 필요 (경계 상태)", "재산 규모 대비 변제 여력이 애매한 경계 상태입니다. 반드시 법률 전문가(변호사·법무사)와 사전 상담 후 경로를 확정하세요.", "warn"),
}
label, desc, kind = path_map[result["recommended_path"]]
styles.alert(kind, f"<b>시스템 참고 진단: {label}</b><br>{desc}")

st.write("")
styles.section_title("③ 최종 경로 확정")
path_options = {"individual_rehab": "개인회생", "individual_bankruptcy": "개인파산·면책", None: "미확정(추가 검토 중)"}
current = st.session_state.get("selected_path")
selected = st.radio(
    "최종 선택 경로",
    options=["individual_rehab", "individual_bankruptcy", None],
    format_func=lambda x: path_options[x],
    index=["individual_rehab", "individual_bankruptcy", None].index(current) if current in path_options else 2,
    horizontal=True,
)
st.session_state["selected_path"] = selected

styles.alert("danger", f"<b>⚠️ 리스크 경고 —</b> {RISK_WARNINGS['individual_asset_disclosure']}")

st.write("")
styles.section_title("④ 금지행위 자가진단")
forbidden_html = "".join([f"<li>{act}</li>" for act in FORBIDDEN_ACTS_INDIVIDUAL])
styles.alert("danger", f"<b>🚨 주의해야 할 행위 —</b> {RISK_WARNINGS['individual_forbidden']}<ul style='margin-top:8px;'>{forbidden_html}</ul>")

styles.footer()
