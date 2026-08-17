import streamlit as st
from datetime import date
import pandas as pd
from lib import styles
from lib.checklist_ui import render_checklist
from lib.calculations import calc_service_period, calc_severance_pay, D
from lib.content_data import RISK_WARNINGS

styles.hero(
    "④ 인사·노무 정리: 임금·퇴직금·권고사직 유의사항",
    "임금과 퇴직금은 법적으로 최우선 변제 대상이며, 처리 방식에 따라 노동청 진정, 민사소송, "
    "형사고발로 이어질 수 있습니다.",
    eyebrow="PHASE 4 · 인사·노무",
)

st.markdown(
    """
    <div class="mediem-card">
    <p>퇴직 절차는 권고사직, 합의퇴직, 정리해고 등 유형에 따라 법적 요건과 절차가 다릅니다. 특히 정리해고는
    엄격한 요건(긴박한 경영상 필요성, 해고 회피 노력, 공정한 선정 기준, 노조·근로자 협의)을 충족해야 하며,
    요건 미비 시 부당해고로 판정될 수 있습니다.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

styles.alert("danger", f"<b>⚠️ 실무 팁: 체불 방지가 최우선 —</b> {RISK_WARNINGS['wage']}")

st.write("")
styles.section_title(
    "퇴직금 추정 계산기",
    "근속기간과 평균월급여를 입력하면 참고용 퇴직금을 추정합니다. (근로자퇴직급여보장법 기준 근사 산정치 — 실무에서는 최근 3개월 실지급 총액 기준 정밀 산정 필요)",
)

with st.form("hr_add_form", clear_on_submit=True):
    fc1, fc2, fc3, fc4 = st.columns([1.3, 1, 1, 1])
    with fc1:
        emp_name = st.text_input("직원명(또는 사번)", placeholder="예: 홍길동 / EMP-013")
    with fc2:
        hire_date = st.date_input("입사일", value=date(2020, 1, 1), min_value=date(1980, 1, 1))
    with fc3:
        end_date = st.date_input("퇴직(예정)일", value=date.today())
    with fc4:
        avg_wage = st.number_input("최근 3개월 평균 월급여(원)", min_value=0, step=100_000, value=3_000_000)
    add_submitted = st.form_submit_button("+ 계산 후 명단에 추가", use_container_width=True)

if add_submitted and emp_name:
    total_days, (y, m, d) = calc_service_period(hire_date, end_date)
    severance = calc_severance_pay(avg_wage, total_days)
    st.session_state["hr_rows"].append({
        "직원명": emp_name,
        "입사일": str(hire_date),
        "퇴직(예정)일": str(end_date),
        "근속기간": f"{y}년 {m}개월 {d}일",
        "근속일수": total_days,
        "평균월급여": avg_wage,
        "추정퇴직금": float(severance),
    })
    st.success(f"{emp_name} 님 추가 완료 — 추정 퇴직금 {severance:,.0f}원")

rows = st.session_state.get("hr_rows", [])
if rows:
    df = pd.DataFrame(rows)
    st.dataframe(
        df.style.format({"평균월급여": "{:,.0f}원", "추정퇴직금": "{:,.0f}원"}),
        use_container_width=True, hide_index=True,
    )
    total_severance = sum(r["추정퇴직금"] for r in rows)
    headcount = len(rows)

    k1, k2 = st.columns(2)
    with k1:
        styles.kpi("정리 대상 인원", f"{headcount}명")
    with k2:
        styles.kpi("추정 퇴직금 총액", f"{total_severance:,.0f}원", "최우선 변제채권 · 우선순위 확인 필수", "#B0413E")

    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button("📥 명단 CSV 다운로드", data=csv, file_name="퇴직금_추정_명단.csv", mime="text/csv")

    if st.button("🗑️ 명단 초기화"):
        st.session_state["hr_rows"] = []
        st.rerun()
else:
    st.info("아직 등록된 직원이 없습니다. 위 양식으로 추가해주세요.")
    total_severance, headcount = 0, 0

st.write("")
styles.section_title("인사·노무 정리 체크리스트")
render_checklist("hr")

styles.footer()
