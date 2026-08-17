"""
체크리스트 공통 렌더링 컴포넌트.
5개 체크리스트(closure/liquidation/bankruptcy/hr/tax) 페이지에서 공통으로 사용.
"""

import streamlit as st
from lib import styles, state
from lib.calculations import checklist_progress
from lib.checklist_data import CHECKLISTS

IMPORTANCE_BADGE = {
    "critical": '<span class="badge badge-danger">필수</span>',
    "high": '<span class="badge badge-gold">중요</span>',
    "normal": '<span class="badge badge-navy">일반</span>',
}


def render_checklist(checklist_key: str):
    cl = CHECKLISTS[checklist_key]
    checked = state.get_checked_set(checklist_key)
    progress = checklist_progress(checked, cl)

    k1, k2, k3 = st.columns(3)
    with k1:
        styles.kpi("전체 진행률", f"{progress['pct']}%", f"{progress['done']}/{progress['total']} 항목 완료")
    with k2:
        styles.kpi("필수(critical) 항목 진행률", f"{progress['critical_pct']}%",
                   f"{progress['critical_done']}/{progress['critical_total']} 완료",
                   "#B0413E" if progress["critical_pct"] < 100 else "#2E6B4F")
    with k3:
        remaining = progress["total"] - progress["done"]
        styles.kpi("남은 항목", f"{remaining}건", "체크 완료 시 자동 반영")

    st.progress(progress["pct"] / 100)
    st.write("")

    for group_name, items in cl["groups"].items():
        st.markdown(f"**{group_name}**")
        for item_id, text, note, importance in items:
            is_checked = item_id in checked
            cols = st.columns([0.06, 0.94])
            with cols[0]:
                new_val = st.checkbox("", value=is_checked, key=f"chk_{item_id}", label_visibility="collapsed")
            with cols[1]:
                badge = IMPORTANCE_BADGE.get(importance, "")
                note_html = f"<div style='color:#6B7685;font-size:12.2px;margin-top:2px;'>{note}</div>" if note else ""
                strike = "text-decoration:line-through;color:#9AA3AF;" if new_val else "color:#1C2733;"
                st.markdown(
                    f"<div style='font-size:13.6px;{strike}'>{text} {badge}</div>{note_html}",
                    unsafe_allow_html=True,
                )
            if new_val != is_checked:
                state.toggle_item(checklist_key, item_id, new_val)
        st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

    return progress
