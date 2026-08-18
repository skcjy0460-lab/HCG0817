import streamlit as st
from lib import styles
from lib.content_data import CORE_CONCEPTS, DECISION_STEPS, GLOSSARY, FAQ, RISK_WARNINGS, ENTITY_COMPARISON

styles.hero(
    "의료법인·의료기관 및 개인 병의원<br>폐업·해산·파산·개인회생 실무 가이드",
    "자본잠식·채무초과·영업불능 상황까지 포함한 일정별 실행 체크리스트 · "
    "재무진단부터 AI 종합진단, 문서 자동생성까지 한 번에 관리하는 프리미엄 컨설팅 도구입니다.",
)

styles.section_title("가장 먼저 확인하세요: 어떤 트랙에 해당하나요?", "운영 형태에 따라 적용되는 절차와 법률이 완전히 다릅니다.")

org_type_labels = {"corporation": "의료법인(재단) — 이사회·해산·청산·법인파산 트랙", "individual": "개인사업자 병의원(원장 개인 명의) — 폐업신고·개인회생·개인파산 트랙"}
current_type = st.session_state.get("org_type")
sel = st.radio(
    "운영 형태를 선택하세요",
    options=["corporation", "individual"],
    format_func=lambda x: org_type_labels[x],
    index=["corporation", "individual"].index(current_type) if current_type in ["corporation", "individual"] else 0,
    horizontal=False,
)
st.session_state["org_type"] = sel

if sel == "corporation":
    st.success("👉 사이드바에서 **'경로 진단' → '② 해산·청산 절차' / '③ 파산 절차'** 메뉴를 이용하세요.")
else:
    st.success("👉 사이드바에서 **'⑥ 개인 병의원 트랙' 섹션의 '개인 병의원 개요' → '개인회생' / '개인파산·면책'** 메뉴를 이용하세요.")

with st.expander("법인 vs 개인사업자 — 무엇이 다른가요? (비교표 펼쳐보기)"):
    rows_html = ""
    for row in ENTITY_COMPARISON:
        rows_html += f"""
        <tr>
          <td style="padding:9px 10px;border-bottom:1px solid #E4DFD4;font-weight:700;color:#0F1B2D;white-space:nowrap;">{row['item']}</td>
          <td style="padding:9px 10px;border-bottom:1px solid #E4DFD4;color:#1C2733;">{row['corp']}</td>
          <td style="padding:9px 10px;border-bottom:1px solid #E4DFD4;color:#1C2733;">{row['individual']}</td>
        </tr>
        """
    st.markdown(
        f"""
        <table style="width:100%;border-collapse:collapse;background:#fff;border:1px solid #E4DFD4;font-size:13px;">
          <thead>
            <tr style="background:#F3F0E8;">
              <th style="text-align:left;padding:9px 10px;">구분</th>
              <th style="text-align:left;padding:9px 10px;">의료법인(재단)</th>
              <th style="text-align:left;padding:9px 10px;">개인사업자 병의원</th>
            </tr>
          </thead>
          <tbody>{rows_html}</tbody>
        </table>
        """,
        unsafe_allow_html=True,
    )

st.write("")

c1, c2, c3 = st.columns(3)
with c1:
    styles.kpi("전체 소요기간", "8~15개월+", "경로 선택에 따라 변동", "#6B7685")
with c2:
    styles.kpi("핵심 관리 영역", "5개 영역", "폐업 · 청산 · 파산 · 인사노무 · 세무행정")
with c3:
    styles.kpi("AI 종합진단", "Gemini 연동", "실시간 리스크 자문", "#2E6B4F")

st.write("")
styles.section_title("핵심 개념", "의료기관 폐업과 의료재단 종료(해산·청산/파산)의 차이를 먼저 이해해야 합니다.")

cols = st.columns(3)
for col, concept in zip(cols, CORE_CONCEPTS):
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

styles.alert(
    "warn",
    "<b>실무 팁 —</b> '의료기관 폐업'과 '의료재단 종료(해산·파산)'는 절차가 분리되어 병행됩니다. "
    "의료기관만 폐업하고 법인은 존속시킬 수도 있고, 동시에 진행할 수도 있습니다. 현재 상황과 목표를 명확히 하는 것이 첫 단계입니다.",
)

st.write("")
styles.section_title("경로 선택 의사결정 흐름", "해산·청산 vs 파산: 4단계로 판단합니다. (상세 진단은 '경로 진단' 메뉴에서 실행)")

for step in DECISION_STEPS:
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

styles.alert("danger", f"<b>⚠️ 중대 리스크 경고 —</b> {RISK_WARNINGS['path_selection']}")

st.write("")
styles.section_title("용어 사전", "실무에서 자주 쓰이는 핵심 용어를 미리 정리했습니다.")
gc1, gc2 = st.columns(2)
half = (len(GLOSSARY) + 1) // 2
for col, items in zip([gc1, gc2], [GLOSSARY[:half], GLOSSARY[half:]]):
    with col:
        for term, definition in items:
            st.markdown(
                f"""<div class="mediem-card" style="padding:14px 18px;">
                <b style="color:#0F1B2D;">{term}</b>
                <div style="color:#1C2733;font-size:13px;margin-top:4px;line-height:1.65;">{definition}</div>
                </div>""",
                unsafe_allow_html=True,
            )

st.write("")
styles.section_title("자주 묻는 질문 (FAQ)")
for q, a in FAQ:
    with st.expander(q):
        st.write(a)

styles.footer()
