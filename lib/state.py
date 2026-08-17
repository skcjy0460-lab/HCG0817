"""
세션 상태 초기화 및 진행상황 저장/불러오기(JSON) 헬퍼.
Streamlit Cloud는 별도 DB가 없는 경우가 많으므로, 사용자가 JSON으로 진행상황을
다운로드/업로드하여 다음 세션에 이어서 작업할 수 있도록 지원.
"""

import json
import streamlit as st
from datetime import datetime

DEFAULTS = {
    "checked_items": {},          # {checklist_key: set(item_ids)}
    "org_name": "",
    "financial_inputs": {
        "total_assets": 0,
        "total_liabilities": 0,
        "monthly_cash_in": 0,
        "monthly_cash_out": 0,
    },
    "selected_path": None,        # "liquidation" | "bankruptcy" | None
    "forbidden_flags": {
        "편파변제 의심 정황": False,
        "관재인/청산인 승인 없는 자산 처분 이력": False,
        "장부 조작 또는 자산 은닉 정황": False,
        "시가 대비 현저히 낮은 자산 처분 이력": False,
    },
    "hr_rows": [],                # 퇴직금 계산기 입력 행들
    "extra_note": "",
    "ai_result": None,
    "ai_model_used": None,
    "ai_generated_at": None,
    "template_field_values": {},
}


def init_state():
    for key, default in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = json.loads(json.dumps(default)) if isinstance(default, (dict, list)) else default
    for cl_key in ["closure", "liquidation", "bankruptcy", "hr", "tax"]:
        st.session_state["checked_items"].setdefault(cl_key, [])


def get_checked_set(checklist_key: str) -> set:
    return set(st.session_state["checked_items"].get(checklist_key, []))


def toggle_item(checklist_key: str, item_id: str, checked: bool):
    lst = set(st.session_state["checked_items"].get(checklist_key, []))
    if checked:
        lst.add(item_id)
    else:
        lst.discard(item_id)
    st.session_state["checked_items"][checklist_key] = list(lst)


def export_state_json() -> str:
    payload = {
        "exported_at": datetime.now().isoformat(),
        "org_name": st.session_state.get("org_name", ""),
        "checked_items": st.session_state.get("checked_items", {}),
        "financial_inputs": st.session_state.get("financial_inputs", {}),
        "selected_path": st.session_state.get("selected_path"),
        "forbidden_flags": st.session_state.get("forbidden_flags", {}),
        "hr_rows": st.session_state.get("hr_rows", []),
        "extra_note": st.session_state.get("extra_note", ""),
        "ai_result": st.session_state.get("ai_result"),
        "ai_model_used": st.session_state.get("ai_model_used"),
        "template_field_values": st.session_state.get("template_field_values", {}),
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def import_state_json(raw: str):
    data = json.loads(raw)
    for key in ["org_name", "checked_items", "financial_inputs", "selected_path",
                "forbidden_flags", "hr_rows", "extra_note", "ai_result",
                "ai_model_used", "template_field_values"]:
        if key in data and data[key] is not None:
            st.session_state[key] = data[key]
    init_state()
