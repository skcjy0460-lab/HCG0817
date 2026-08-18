import streamlit as st
from datetime import datetime
from lib import styles, state
from lib.calculations import financial_diagnosis, individual_path_diagnosis, checklist_progress, overall_risk_score
from lib.checklist_data import CHECKLISTS
from lib.gemini_client import run_ai_diagnosis
from lib.report_generator import build_report_html

org_type = st.session_state.get("org_type", "corporation")
is_individual = org_type == "individual"

styles.hero(
    "AI 종합진단 · 최종 리포트 생성",
    "입력된 재무 데이터와 체크리스트 진행 현황을 근거로 Gemini AI가 종합 진단 보고서를 작성합니다. "
    "(모델 자동 폴백: gemini-3.6-flash → gemini-3.5-flash-lite → gemini-2.5-flash → gemini-2.0-flash)",
    eyebrow="AI 자문 엔진 (" + ("개인 병의원 트랙" if is_individual else "의료법인 트랙") + ")",
)

# ── 컨텍스트 구성 ──────────────────────────────────────────────
if is_individual:
    labels = {"closure": "① 의료기관 폐업", "individual_rehab": "② 개인회생", "individual_bankruptcy": "③ 개인파산·면책",
              "hr": "④ 인사·노무", "tax": "⑤ 세무·보험·행정"}
else:
    labels = {"closure": "① 의료기관 폐업", "liquidation": "② 해산·청산", "bankruptcy": "③ 파산",
              "hr": "④ 인사·노무", "tax": "⑤ 세무·보험·행정"}
progress = {}
for key, label in labels.items():
    checked = state.get_checked_set(key)
    progress[label] = checklist_progress(checked, CHECKLISTS[key])

if is_individual:
    ind_in = st.session_state.get("individual_inputs", {})
    ind_result = individual_path_diagnosis(
        ind_in.get("total_assets", 0), ind_in.get("total_debt", 0),
        ind_in.get("monthly_income", 0), ind_in.get("monthly_living_cost", 0),
        ind_in.get("has_stable_income", True),
    )
    financial_ctx = {
        "total_assets": ind_in.get("total_assets", 0),
        "total_liabilities": ind_in.get("total_debt", 0),
        "net_asset": ind_in.get("total_assets", 0) - ind_in.get("total_debt", 0),
        "cash_in": ind_in.get("monthly_income", 0),
        "cash_out": ind_in.get("monthly_living_cost", 0),
        "cash_gap": ind_result["monthly_available"],
        "is_insolvent": ind_in.get("total_debt", 0) > ind_in.get("total_assets", 0),
        "is_illiquid": ind_result["monthly_available"] <= 0,
    }
    path_label_map = {"individual_rehab": "개인회생", "individual_bankruptcy": "개인파산·면책",
                       None: "미확정", "review": "전문가 검토 필요(경계 상태)"}
    recommended_path_label = path_label_map.get(ind_result["recommended_path"], ind_result["recommended_path"])
    fin_risk_level = "critical" if (ind_result["recommended_path"] == "individual_bankruptcy" and ind_result["monthly_available"] <= 0) else \
                      ("high" if ind_result["recommended_path"] == "review" else "normal")
else:
    fin_in = st.session_state.get("financial_inputs", {})
    fin_result = financial_diagnosis(
        fin_in.get("total_assets", 0), fin_in.get("total_liabilities", 0),
        fin_in.get("monthly_cash_in", 0), fin_in.get("monthly_cash_out", 0),
    )
    financial_ctx = {
        "total_assets": fin_in.get("total_assets", 0),
        "total_liabilities": fin_in.get("total_liabilities", 0),
        "net_asset": fin_result["net_asset"],
        "cash_in": fin_in.get("monthly_cash_in", 0),
        "cash_out": fin_in.get("monthly_cash_out", 0),
        "cash_gap": fin_result["cash_gap"],
        "is_insolvent": fin_result["is_insolvent"],
        "is_illiquid": fin_result["is_illiquid"],
    }
    path_label_map = {"liquidation": "해산·청산", "bankruptcy": "파산", None: "미확정",
                       "review": "전문가 검토 필요(경계 상태)"}
    recommended_path_label = path_label_map.get(fin_result["recommended_path"], fin_result["recommended_path"])
    fin_risk_level = fin_result["risk_level"]

selected_path_label = path_label_map.get(st.session_state.get("selected_path"), "미확정")

hr_rows = st.session_state.get("hr_rows", [])
hr_summary = {
    "headcount": len(hr_rows),
    "total_severance": sum(r.get("추정퇴직금", 0) for r in hr_rows),
}

forbidden_flags = st.session_state.get("forbidden_flags", {})
risk = overall_risk_score(progress, fin_risk_level, forbidden_flags)

styles.section_title("① 진단 컨텍스트 요약", "AI에게 전달될 현재 데이터입니다. 값이 비어있다면 이전 메뉴에서 먼저 입력해주세요.")
k1, k2, k3, k4 = st.columns(4)
with k1:
    styles.kpi("기관명", st.session_state.get("org_name") or "미입력")
with k2:
    styles.kpi("시스템 권장 경로", recommended_path_label)
with k3:
    styles.kpi("선택 경로", selected_path_label)
with k4:
    styles.kpi("종합 리스크 스코어", f"{risk['score']}/100", risk["label"], risk["color"])

st.write("")
extra_note = st.text_area(
    "컨설턴트 추가 메모 (AI 진단에 반영됩니다)",
    value=st.session_state.get("extra_note", ""),
    placeholder="예: 채권자 3곳과 이미 개별 협의 진행 중, 대표자는 신속한 폐업을 희망함 등",
    height=90,
)
st.session_state["extra_note"] = extra_note

st.write("")
styles.section_title("② AI 종합진단 실행")

run_col, _ = st.columns([1, 3])
with run_col:
    run_clicked = st.button("🤖 AI 진단 실행", type="primary", use_container_width=True)

if run_clicked:
    context = {
        "org_name": st.session_state.get("org_name"),
        "org_type_label": "개인사업자 병의원(개인회생·개인파산 트랙)" if is_individual else "의료법인(해산·청산·파산 트랙)",
        "today": datetime.now().strftime("%Y-%m-%d"),
        "financial": financial_ctx,
        "recommended_path_label": recommended_path_label,
        "selected_path_label": selected_path_label,
        "progress": progress,
        "hr_summary": hr_summary,
        "forbidden_flags": forbidden_flags,
        "extra_note": extra_note,
    }
    with st.spinner("AI가 재무·체크리스트·인사노무 데이터를 분석 중입니다..."):
        success, result_text, model_used = run_ai_diagnosis(context)
    if success:
        st.session_state["ai_result"] = result_text
        st.session_state["ai_model_used"] = model_used
        st.session_state["ai_generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        st.success(f"AI 진단이 완료되었습니다. (사용 모델: {model_used})")
    else:
        st.error(result_text)

if st.session_state.get("ai_result"):
    st.write("")
    styles.section_title(
        "AI 종합진단 결과",
        f"모델: {st.session_state.get('ai_model_used','-')} · 생성 시각: {st.session_state.get('ai_generated_at','-')}",
    )
    st.markdown(
        f"""<div class="mediem-card gold-edge">{st.session_state["ai_result"]}</div>""",
        unsafe_allow_html=True,
    )
else:
    st.info("아직 AI 진단을 실행하지 않았습니다. 위 'AI 진단 실행' 버튼을 눌러주세요.")

st.write("")
styles.section_title("③ 최종 종합 리포트 다운로드", "재무진단 + 체크리스트 진행률 + 리스크 스코어 + AI 진단을 하나의 HTML 리포트로 제공합니다.")

report_ctx = {
    "org_name": st.session_state.get("org_name"),
    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "selected_path_label": selected_path_label + (" · 개인 병의원 트랙" if is_individual else " · 의료법인 트랙"),
    "financial": financial_ctx,
    "progress": progress,
    "risk": risk,
    "hr_summary": hr_summary,
    "ai_result": st.session_state.get("ai_result"),
    "ai_model_used": st.session_state.get("ai_model_used"),
}
report_html = build_report_html(report_ctx)

st.download_button(
    "📥 종합 진단 리포트 다운로드 (HTML)",
    data=report_html.encode("utf-8"),
    file_name=f"{(st.session_state.get('org_name') or '병원')}_{'개인회생파산' if is_individual else '폐업해산파산'}_종합진단리포트.html",
    mime="text/html",
    use_container_width=True,
)

with st.expander("리포트 미리보기"):
    st.components.v1.html(report_html, height=600, scrolling=True)

styles.footer()
