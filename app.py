import streamlit as st
from lib import styles, state, license_gate

st.set_page_config(
    page_title="병원 폐업·해산·파산 실무 가이드 PRO | Mediem",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

styles.inject_base_css()
state.init_state()

# ── 유료 라이선스 게이트 ─────────────────────────────────────────
if not license_gate.render_gate():
    st.stop()

# ── 사이드바: 기관 정보 + 저장/불러오기 ───────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style="padding:6px 2px 14px 2px;">
            <div style="font-size:11px;letter-spacing:.2em;color:#C9A24B;font-weight:700;">MEDIEM</div>
            <div style="font-family:'Noto Serif KR',serif;font-size:18px;font-weight:800;color:#F7F5EF;line-height:1.4;margin-top:4px;">
                병원 폐업·해산·파산<br>실무 가이드 PRO
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.text_input("기관(병원/의료법인)명", key="org_name", placeholder="예: 메디엄병원")
    st.markdown("---")
    st.caption("진행 상황 저장 / 불러오기")
    st.download_button(
        "💾 현재 진행상황 JSON 저장",
        data=state.export_state_json(),
        file_name="mediem_closure_progress.json",
        mime="application/json",
        use_container_width=True,
    )
    uploaded = st.file_uploader("불러오기(JSON)", type=["json"], label_visibility="collapsed")
    if uploaded is not None:
        try:
            state.import_state_json(uploaded.read().decode("utf-8"))
            st.success("진행상황을 불러왔습니다.")
        except Exception as e:
            st.error(f"불러오기 실패: {e}")
    st.markdown("---")
    st.caption(f"라이선스: {st.session_state.get('_license_key_masked','-')}")
    if st.button("로그아웃", use_container_width=True):
        st.session_state["_licensed"] = False
        st.rerun()

# ── 페이지 네비게이션 ─────────────────────────────────────────────
pages = [
    st.Page("views/page_00_home.py", title="홈 · 핵심개념", icon="🏠", default=True),
    st.Page("views/page_01_diagnosis.py", title="경로 진단(해산 vs 파산)", icon="🧭"),
    st.Page("views/page_02_roadmap.py", title="전체 일정 로드맵", icon="🗓️"),
    st.Page("views/page_03_closure.py", title="① 의료기관 폐업", icon="🏥"),
    st.Page("views/page_04_liquidation.py", title="② 해산·청산 절차", icon="⚖️"),
    st.Page("views/page_05_bankruptcy.py", title="③ 파산 절차", icon="🏛️"),
    st.Page("views/page_06_hr.py", title="④ 인사·노무 정리", icon="👥"),
    st.Page("views/page_07_tax.py", title="⑤ 세무·보험·행정", icon="🧾"),
    st.Page("views/page_08_risk.py", title="최종 리스크 체크리스트", icon="🚨"),
    st.Page("views/page_09_templates.py", title="문서 템플릿 생성", icon="📄"),
    st.Page("views/page_10_ai_report.py", title="AI 종합진단 · 리포트", icon="🤖"),
]

nav = st.navigation(pages, position="sidebar")
nav.run()
