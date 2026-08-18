import streamlit as st
import plotly.graph_objects as go
from lib import styles, state
from lib.calculations import checklist_progress, overall_risk_score, financial_diagnosis, individual_path_diagnosis
from lib.checklist_data import CHECKLISTS

org_type = st.session_state.get("org_type", "corporation")
is_individual = org_type == "individual"

styles.hero(
    "최종 리스크 체크리스트 & 종합 스코어",
    "5개 영역의 이행 현황과 재무 리스크, 금지행위 해당여부를 종합하여 하나의 리스크 스코어로 산출합니다.",
    eyebrow="종합 대시보드 (" + ("개인 병의원 트랙" if is_individual else "의료법인 트랙") + ")",
)

# 전체 진행률 취합 (트랙에 따라 해산·청산/파산 또는 개인회생/개인파산 체크리스트를 사용)
if is_individual:
    labels = {"closure": "① 의료기관 폐업", "individual_rehab": "② 개인회생", "individual_bankruptcy": "③ 개인파산·면책",
              "hr": "④ 인사·노무", "tax": "⑤ 세무·보험·행정"}
else:
    labels = {"closure": "① 의료기관 폐업", "liquidation": "② 해산·청산", "bankruptcy": "③ 파산",
              "hr": "④ 인사·노무", "tax": "⑤ 세무·보험·행정"}
all_progress = {}
for key, label in labels.items():
    checked = state.get_checked_set(key)
    all_progress[label] = checklist_progress(checked, CHECKLISTS[key])

if is_individual:
    ind = st.session_state.get("individual_inputs", {})
    ind_result = individual_path_diagnosis(
        ind.get("total_assets", 0), ind.get("total_debt", 0),
        ind.get("monthly_income", 0), ind.get("monthly_living_cost", 0),
        ind.get("has_stable_income", True),
    )
    fin_risk_level = "critical" if ind_result["recommended_path"] == "individual_bankruptcy" and ind_result["monthly_available"] <= 0 else \
                      ("high" if ind_result["recommended_path"] == "review" else "normal")
else:
    fin = st.session_state.get("financial_inputs", {})
    fin_result = financial_diagnosis(
        fin.get("total_assets", 0), fin.get("total_liabilities", 0),
        fin.get("monthly_cash_in", 0), fin.get("monthly_cash_out", 0),
    )
    fin_risk_level = fin_result["risk_level"]

forbidden_flags = st.session_state.get("forbidden_flags", {})
risk = overall_risk_score(all_progress, fin_risk_level, forbidden_flags)

styles.section_title("종합 리스크 게이지")
gauge_col, kpi_col = st.columns([1.3, 1])
with gauge_col:
    color = risk["color"]
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk["score"],
        number={"suffix": " / 100", "font": {"size": 34, "color": "#0F1B2D"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#6B7685"},
            "bar": {"color": color},
            "bgcolor": "#FBFAF7",
            "steps": [
                {"range": [0, 15], "color": "#EAF4EF"},
                {"range": [15, 35], "color": "#FBF3E4"},
                {"range": [35, 60], "color": "#FBE7DC"},
                {"range": [60, 100], "color": "#FBEEED"},
            ],
        },
    ))
    fig.update_layout(height=260, margin=dict(l=20, r=20, t=20, b=10),
                       paper_bgcolor="#FBFAF7", font=dict(family="Noto Sans KR, sans-serif"))
    st.plotly_chart(fig, use_container_width=True)
with kpi_col:
    styles.kpi("종합 리스크 등급", risk["label"], f"스코어 {risk['score']}/100", risk["color"])
    styles.kpi("재무 리스크", fin_risk_level.upper())
    hit_count = sum(1 for v in forbidden_flags.values() if v)
    styles.kpi("금지행위 자가진단 적발", f"{hit_count}건", "0건이 정상" if hit_count == 0 else "즉시 전문가 상담 필요",
               "#2E6B4F" if hit_count == 0 else "#B0413E")

st.write("")
styles.section_title("영역별 진행률 요약")
for name, prog in all_progress.items():
    c1, c2 = st.columns([1, 4])
    with c1:
        st.markdown(f"**{name}**")
    with c2:
        st.progress(prog["pct"] / 100, text=f"{prog['pct']}% ({prog['done']}/{prog['total']}) · 필수항목 {prog['critical_pct']}%")

st.write("")
styles.section_title("🚨 최종 리스크 체크리스트", "실행 직전, 아래 5개 카테고리를 마지막으로 점검하세요.")

final_checks = {
    "경로 선택 및 절차": [
        "채무초과·영업불능(또는 개인 채무초과) 여부 판단 완료",
        "특정 채권자만 변제하거나 재산 임의 처분·이전 금지 확인",
        "이사회 결의(해산 또는 파산) 완료 및 회의록 보관" if not is_individual else "개인회생/개인파산 신청서 및 첨부서류 최종 점검 완료",
        "주무관청(청산) 또는 법원(파산) 서류 제출 일정 확정" if not is_individual else "법원 제출 서류 및 신청 일정 확정",
    ],
    "의료기관 폐업 및 환자 보호": [
        "폐업일 확정 및 보건소 신고 완료",
        "예약/치료 중인 환자 안내 및 이관 계획 수립",
        "진료기록 보관 책임자 지정 및 연락처 공개",
        "진료기록 발급·열람 프로세스 유지 확인",
    ],
    "인사·노무": [
        "미지급 임금·퇴직금 산정표 작성 (근거 자료 포함)",
        "체불 최소화 계획 수립 (분할 합의 시 서면 작성)",
        "퇴직 서류(사직서/합의서/해고통지) 징구 완료",
        "4대보험 상실 및 정산 절차 진행",
    ],
    "세무·보험·행정": [
        "사업자등록 폐업 신고 및 부가세·원천세 정산 일정 확정",
        "4대보험 상실 신고 및 체납 보험료 확인",
        "건보/심평원 청구 종료 및 환수금 가능성 검토",
        "임대차 해지 통지 및 원상복구 범위 협의 (증빙 확보)",
    ],
    "자산 처분 및 거래처": [
        "자산 분류 및 처분 기준 수립 (시가·감정 근거 확보)",
        "의료장비·재고 처분 시 견적서 2~3개 비교",
        "미수금 회수 가능성 분류 (상/중/하)",
        "거래처 계약 종료 통지 및 정산 협의 완료",
    ],
    "대외 공지 및 증빙 보관": [
        "환자·직원·거래처 대상 공지문 작성 및 발송",
        "민원 대응 Q&A 및 담당자 지정",
        "모든 계약서·정산서·입금증·회의록 통합 보관",
        "법적 분쟁 대비 증빙자료 정리 완료",
    ],
}

if "final_check_state" not in st.session_state:
    st.session_state["final_check_state"] = {}

fc_done, fc_total = 0, 0
for cat, items in final_checks.items():
    with st.expander(f"**{cat}**", expanded=False):
        for i, item in enumerate(items):
            key = f"final_{cat}_{i}"
            checked = st.checkbox(item, value=st.session_state["final_check_state"].get(key, False), key=key)
            st.session_state["final_check_state"][key] = checked
            fc_total += 1
            if checked:
                fc_done += 1

st.progress((fc_done / fc_total) if fc_total else 0, text=f"최종 체크리스트 {fc_done}/{fc_total} 완료")

styles.footer()
