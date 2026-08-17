import streamlit as st
from lib import styles
from lib.calculations import financial_diagnosis, D
from lib.content_data import RISK_WARNINGS

styles.hero(
    "경로 진단: 해산·청산 vs 파산",
    "자산·부채·현금흐름 데이터를 입력하면 채무초과·영업불능 여부를 자동 판정하고 권장 경로를 제시합니다.",
    eyebrow="STEP 1 · 재무 진단",
)

styles.section_title("① 재무 현황 입력", "자산은 실제 처분(환가) 가능 금액 기준, 부채는 확정채무와 추정채무를 모두 포함하여 입력하세요.")

fin = st.session_state["financial_inputs"]

col1, col2 = st.columns(2)
with col1:
    st.markdown("**자산 · 부채**")
    total_assets = st.number_input(
        "총자산 (처분가능액 기준, 원)", min_value=0, step=1_000_000,
        value=int(fin.get("total_assets", 0)), format="%d",
    )
    total_liabilities = st.number_input(
        "총부채 (확정+추정, 원)", min_value=0, step=1_000_000,
        value=int(fin.get("total_liabilities", 0)), format="%d",
    )
with col2:
    st.markdown("**월간 현금흐름**")
    monthly_cash_in = st.number_input(
        "월 평균 현금유입 (진료수입 등, 원)", min_value=0, step=500_000,
        value=int(fin.get("monthly_cash_in", 0)), format="%d",
    )
    monthly_cash_out = st.number_input(
        "월 평균 현금유출 (인건비·임차료·재료비 등, 원)", min_value=0, step=500_000,
        value=int(fin.get("monthly_cash_out", 0)), format="%d",
    )

st.session_state["financial_inputs"] = {
    "total_assets": total_assets,
    "total_liabilities": total_liabilities,
    "monthly_cash_in": monthly_cash_in,
    "monthly_cash_out": monthly_cash_out,
}

result = financial_diagnosis(total_assets, total_liabilities, monthly_cash_in, monthly_cash_out)

st.write("")
styles.section_title("② 진단 결과")

k1, k2, k3, k4 = st.columns(4)
with k1:
    styles.kpi("순자산", f"{result['net_asset']:,.0f}원",
               "채무초과" if result["is_insolvent"] else "정상 범위",
               "#B0413E" if result["is_insolvent"] else "#2E6B4F")
with k2:
    styles.kpi("월 현금흐름 갭", f"{result['cash_gap']:,.0f}원",
               "영업불능 우려" if result["is_illiquid"] else "현금흐름 유지",
               "#B0413E" if result["is_illiquid"] else "#2E6B4F")
with k3:
    styles.kpi("채무초과 여부", "예" if result["is_insolvent"] else "아니오")
with k4:
    styles.kpi("영업불능 여부", "예" if result["is_illiquid"] else "아니오")

path_map = {
    "liquidation": ("해산·청산 경로 권장", "정상 청산이 가능한 재무 상태로 판단됩니다. '② 해산·청산 절차' 메뉴를 참고하세요.", "ok"),
    "bankruptcy": ("파산 경로 검토 필요", "채무초과이면서 영업불능 상태로, 파산 절차를 우선 검토해야 합니다. '③ 파산 절차' 메뉴를 참고하세요.", "danger"),
    "review": ("전문가 검토 필요 (경계 상태)", "채무초과 또는 영업불능 중 하나에만 해당하는 경계 상태입니다. 반드시 법률·회계 전문가와 사전 협의 후 경로를 확정하세요.", "warn"),
}
label, desc, kind = path_map[result["recommended_path"]]
styles.alert(kind, f"<b>시스템 권장 경로: {label}</b><br>{desc}")

st.write("")
styles.section_title("③ 최종 경로 확정", "시스템 권장 결과를 참고하여 컨설턴트/의사결정권자가 최종 경로를 선택하세요.")

path_options = {"liquidation": "해산·청산", "bankruptcy": "파산", None: "미확정(추가 검토 중)"}
current = st.session_state.get("selected_path")
selected = st.radio(
    "최종 선택 경로",
    options=["liquidation", "bankruptcy", None],
    format_func=lambda x: path_options[x],
    index=["liquidation", "bankruptcy", None].index(current) if current in ["liquidation", "bankruptcy", None] else 2,
    horizontal=True,
)
st.session_state["selected_path"] = selected

styles.alert("danger", f"<b>⚠️ 리스크 경고 —</b> {RISK_WARNINGS['liquidation_capital']}")

st.write("")
styles.section_title("④ 금지행위 자가진단", "이사회 결의 전, 아래 항목에 해당되는 사실이 있는지 반드시 자가점검하세요.")
flags = st.session_state["forbidden_flags"]
new_flags = {}
for label_key in flags:
    new_flags[label_key] = st.checkbox(label_key, value=flags.get(label_key, False))
st.session_state["forbidden_flags"] = new_flags

if any(new_flags.values()):
    styles.alert(
        "danger",
        "<b>🚨 해당 사항이 있습니다.</b> 위 항목 중 하나라도 해당된다면 즉시 법률 전문가와 상담하고, "
        "추가적인 유사 행위를 즉시 중단해야 합니다. 이는 이사·청산인·대표자의 민·형사상 책임으로 이어질 수 있습니다."
    )

styles.footer()
