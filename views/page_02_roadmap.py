import streamlit as st
import plotly.graph_objects as go
from lib import styles
from lib.checklist_data import ROADMAP_PHASES, ROADMAP_PHASES_INDIVIDUAL
from lib.content_data import ROADMAP_NARRATIVE, BANKRUPTCY_TIMELINE

org_type = st.session_state.get("org_type", "corporation")
is_individual = org_type == "individual"

styles.hero(
    "전체 프로세스 로드맵" + (" (개인 병의원 트랙)" if is_individual else " (의료법인 트랙)"),
    "선택한 경로에 따라 8개월에서 15개월, 경우에 따라 그 이상이 소요될 수 있습니다. "
    "각 단계별 소요 기간과 핵심 업무를 사전에 파악하고 체계적으로 관리하세요.",
    eyebrow="STEP 2 · 일정 관리",
)

st.caption(
    "현재 홈 화면에서 선택된 트랙: **" + ("개인 병의원(개인회생·개인파산)" if is_individual else "의료법인(해산·청산·파산)") +
    "** — 트랙을 바꾸려면 '홈' 메뉴에서 재선택하세요."
)

phases = ROADMAP_PHASES_INDIVIDUAL if is_individual else ROADMAP_PHASES

if not is_individual:
    styles.section_title("4단계 프로세스 요약")
    cols = st.columns(4)
    for col, item in zip(cols, ROADMAP_NARRATIVE):
        with col:
            st.markdown(
                f"""
                <div class="mediem-card gold-edge" style="min-height:190px;">
                    <span class="badge badge-navy">STEP {item['no']}</span>
                    <h4 style="margin-top:10px;">{item['title']}</h4>
                    <div style="color:#C9A24B;font-weight:700;font-size:13px;margin-bottom:6px;">소요 {item['duration']}</div>
                    <p style="font-size:12.8px;">{item['desc']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.write("")

styles.section_title(
    "간트 차트 (주 단위)",
    "선택 경로에 따라 3-A(해산·청산/개인회생) 또는 3-B(파산/개인파산) 트랙만 진행됩니다." if not is_individual
    else "선택 경로에 따라 3-A(개인회생) 또는 3-B(개인파산·면책) 트랙만 진행됩니다.",
)

selected_path = st.session_state.get("selected_path")
if is_individual:
    path_note = {
        "individual_rehab": "현재 선택 경로: 개인회생 → 개인파산 트랙은 참고용으로 함께 표시됩니다.",
        "individual_bankruptcy": "현재 선택 경로: 개인파산·면책 → 개인회생 트랙은 참고용으로 함께 표시됩니다.",
        None: "경로가 아직 확정되지 않았습니다. '개인 병의원 개요·진단' 메뉴에서 먼저 진단을 진행하세요.",
    }
else:
    path_note = {
        "liquidation": "현재 선택 경로: 해산·청산 → 파산 트랙은 참고용으로 함께 표시됩니다.",
        "bankruptcy": "현재 선택 경로: 파산 → 해산·청산 트랙은 참고용으로 함께 표시됩니다.",
        None: "경로가 아직 확정되지 않았습니다. '법인 경로 진단' 메뉴에서 먼저 진단을 진행하세요.",
    }
st.caption(path_note.get(selected_path, ""))

fig = go.Figure()
colors = {
    "1. 사전 정리": "#0F1B2D",
    "2. 의료기관 폐업": "#1B3A5C",
    "3-A. 해산·청산 경로": "#2E6B4F",
    "3-B. 파산 경로": "#B0413E",
    "3-A. 개인회생 경로": "#2E6B4F",
    "3-B. 개인파산·면책 경로": "#B0413E",
    "4. 세무·노무 정산(병행)": "#C9A24B",
}
dim_targets = {
    "liquidation": "3-B. 파산 경로", "bankruptcy": "3-A. 해산·청산 경로",
    "individual_rehab": "3-B. 개인파산·면책 경로", "individual_bankruptcy": "3-A. 개인회생 경로",
}
for phase in phases:
    name = phase["phase"]
    opacity = 0.25 if dim_targets.get(selected_path) == name else 1.0
    fig.add_trace(go.Bar(
        y=[name],
        x=[phase["duration_weeks"]],
        base=[phase["start_week"]],
        orientation="h",
        name=name,
        marker=dict(color=colors.get(name, "#6B7685"), opacity=opacity),
        hovertemplate=f"<b>{name}</b><br>{phase['desc']}<br>%{{x}}주 소요<extra></extra>",
        showlegend=False,
    ))

fig.update_layout(
    height=340,
    margin=dict(l=10, r=10, t=10, b=10),
    xaxis_title="경과 주(Week)",
    plot_bgcolor="#FBFAF7",
    paper_bgcolor="#FBFAF7",
    font=dict(family="Noto Sans KR, sans-serif", size=12.5, color="#1C2733"),
    xaxis=dict(gridcolor="#E4DFD4"),
)
st.plotly_chart(fig, use_container_width=True)

st.write("")
if not is_individual:
    styles.section_title("파산 경로 상세 일정 (참고)")
    for t in BANKRUPTCY_TIMELINE:
        st.markdown(
            f"""<div class="mediem-card" style="display:flex;gap:16px;align-items:center;">
            <span class="badge badge-gold" style="min-width:96px;text-align:center;">{t['period']}</span>
            <span style="color:#1C2733;font-size:13.5px;">{t['desc']}</span>
            </div>""",
            unsafe_allow_html=True,
        )
else:
    styles.section_title("개인회생·개인파산 참고 일정")
    ind_timeline = [
        {"period": "1개월차", "desc": "채무·재산 조사 + 사전정리 + 법원 신청서 제출"},
        {"period": "2~3개월차", "desc": "회생위원 면담/보정 또는 파산 심문 + 선고·인가 여부 결정"},
        {"period": "개인회생: 인가 후 3~5년", "desc": "매월 변제계획 이행 → 완료 시 면책 결정"},
        {"period": "개인파산: 4~8개월차", "desc": "채권자집회(필요 시) → 면책 심사 → 면책 결정"},
    ]
    for t in ind_timeline:
        st.markdown(
            f"""<div class="mediem-card" style="display:flex;gap:16px;align-items:center;">
            <span class="badge badge-gold" style="min-width:150px;text-align:center;">{t['period']}</span>
            <span style="color:#1C2733;font-size:13.5px;">{t['desc']}</span>
            </div>""",
            unsafe_allow_html=True,
        )

styles.alert(
    "warn",
    "<b>일정 변동 요인 —</b> 실제 소요 기간은 관할기관의 처리 속도, 자산 환가의 난이도, 소송 발생 여부, "
    "채권자와의 협의 진행 상황 등에 따라 크게 달라질 수 있습니다. 여유 있는 일정 계획과 지속적인 모니터링이 필요합니다.",
)

styles.footer()
