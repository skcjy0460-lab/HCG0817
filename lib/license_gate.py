"""
유료 전용 라이선스 게이트.
Streamlit Cloud Secrets에 LICENSE_KEYS = "KEY1,KEY2,KEY3" 형태로 등록.
raw 키를 secrets에 그대로 저장하지 않고 싶다면 hashlib.sha256 해시 리스트로 관리 가능
(LICENSE_KEY_HASHES 사용 시 자동 전환).
"""

import hashlib
import time
import streamlit as st

APP_TITLE = "병원 폐업·해산·파산 실무 가이드 PRO"


def _hash(key: str) -> str:
    return hashlib.sha256(key.strip().encode("utf-8")).hexdigest()


def _valid_keys() -> set:
    try:
        raw = st.secrets.get("LICENSE_KEYS", "")
    except Exception:
        raw = ""
    return {k.strip() for k in raw.split(",") if k.strip()}


def _valid_hashes() -> set:
    try:
        raw = st.secrets.get("LICENSE_KEY_HASHES", "")
    except Exception:
        raw = ""
    return {k.strip().lower() for k in raw.split(",") if k.strip()}


def _check(key: str) -> bool:
    key = (key or "").strip()
    if not key:
        return False
    if key in _valid_keys():
        return True
    if _hash(key) in _valid_hashes():
        return True
    return False


def is_licensed() -> bool:
    return bool(st.session_state.get("_licensed", False))


def render_gate():
    """라이선스 미인증 시 입력 폼을 표시하고 앱 실행을 막음. 인증 시 True 반환."""
    if is_licensed():
        return True

    st.markdown(
        """
        <div style="max-width:560px;margin:60px auto 0 auto;">
        </div>
        """,
        unsafe_allow_html=True,
    )

    col = st.columns([1, 2, 1])[1]
    with col:
        st.markdown(
            f"""
            <div style="text-align:center;margin-bottom:18px;">
                <div style="font-size:12px;letter-spacing:.2em;color:#C9A24B;font-weight:700;">MEDIEM · PREMIUM</div>
                <div style="font-family:'Noto Serif KR',serif;font-size:24px;font-weight:800;color:#0F1B2D;margin-top:6px;">
                    {APP_TITLE}
                </div>
                <div style="color:#6B7685;font-size:13px;margin-top:6px;">
                    본 프로그램은 유료 라이선스 사용자 전용입니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.form("license_form", clear_on_submit=False):
            key_input = st.text_input("라이선스 키(License Key)를 입력하세요", type="password", placeholder="예: MEDIEM-XXXX-XXXX-XXXX")
            submitted = st.form_submit_button("잠금 해제", use_container_width=True)
        if submitted:
            if _check(key_input):
                st.session_state["_licensed"] = True
                st.session_state["_license_key_masked"] = key_input[:4] + "•" * max(0, len(key_input) - 4)
                st.session_state["_login_ts"] = time.time()
                st.rerun()
            else:
                st.error("라이선스 키가 유효하지 않습니다. 구매 정보 또는 담당 컨설턴트에게 문의해주세요.")
        st.caption("라이선스 구매/문의: 메디엄(Mediem Co.) · 본 프로그램은 재배포·무단 공유가 금지됩니다.")
    return False
