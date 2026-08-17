import streamlit as st
from lib import styles
from lib.content_data import TEMPLATES

styles.hero(
    "실무 문서 템플릿 자동 생성",
    "환자·직원·거래처 공지문부터 이사회 결의서, 채권신고 공고문까지 — 기관 정보를 입력하면 바로 사용 가능한 문서를 생성합니다.",
    eyebrow="문서 자동화",
)

FIELD_LABELS = {
    "org_name": "기관(법인)명",
    "closure_date": "폐업(종료)일",
    "dissolution_date": "해산 결의일",
    "contact_person": "담당자명",
    "contact_phone": "담당자 연락처",
    "office_hours": "응대 가능 시간",
    "vendor_name": "거래처명",
    "reply_deadline": "협의 회신 기한",
    "last_work_date": "최종 근무일",
    "severance_pay_date": "퇴직금 지급 예정일",
    "report_deadline": "채권신고 마감일",
    "meeting_date": "이사회 개최일",
    "attendees": "참석 이사(명단)",
    "liquidator_name": "청산인 성명",
    "reason": "결의 사유",
    "representative_name": "대표권자(파산신청) 성명",
    "employee_name": "직원명",
    "severance_amount": "퇴직금(추정) 금액",
    "unpaid_wage": "미지급 임금(추정) 금액",
    "pay_date": "지급 예정일",
}

categories = sorted(set(t["category"] for t in TEMPLATES.values()))
tab_labels = ["전체"] + categories
tabs = st.tabs(tab_labels)

field_values = st.session_state.setdefault("template_field_values", {})
# 공통 필드는 org_name 등 자동 동기화
field_values.setdefault("org_name", st.session_state.get("org_name", ""))
if st.session_state.get("org_name"):
    field_values["org_name"] = st.session_state["org_name"]

for tab, tab_label in zip(tabs, tab_labels):
    with tab:
        items = TEMPLATES.items() if tab_label == "전체" else [
            (k, v) for k, v in TEMPLATES.items() if v["category"] == tab_label
        ]
        for key, tpl in items:
            uid = f"{tab_label}_{key}"  # 탭(전체/카테고리)별로 고유한 위젯 키를 보장
            with st.expander(f"📄 {tpl['title']}", expanded=False):
                cols = st.columns(2)
                for i, field in enumerate(tpl["fields"]):
                    with cols[i % 2]:
                        label = FIELD_LABELS.get(field, field)
                        val = st.text_input(
                            label, value=field_values.get(field, ""),
                            key=f"tpl_{uid}_{field}",
                        )
                        field_values[field] = val
                try:
                    rendered = tpl["body"].format(**{f: (field_values.get(f) or f"({FIELD_LABELS.get(f, f)} 미입력)") for f in tpl["fields"]})
                except Exception:
                    rendered = tpl["body"]

                st.markdown("**미리보기**")
                st.text_area("미리보기 내용", value=rendered, height=220, key=f"preview_{uid}", label_visibility="collapsed")

                dl_col1, dl_col2 = st.columns(2)
                with dl_col1:
                    st.download_button(
                        "📥 텍스트(.txt) 다운로드", data=rendered.encode("utf-8"),
                        file_name=f"{tpl['title']}.txt", mime="text/plain", key=f"dl_txt_{uid}",
                        use_container_width=True,
                    )
                with dl_col2:
                    html_doc = f"""<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8">
                    <title>{tpl['title']}</title>
                    <style>
                    body{{font-family:'Noto Sans KR',sans-serif;background:#FBFAF7;padding:40px;}}
                    .doc{{max-width:640px;margin:0 auto;background:#fff;border:1px solid #E4DFD4;
                          border-top:4px solid #C9A24B;padding:36px 40px;white-space:pre-wrap;
                          line-height:1.9;color:#1C2733;font-size:14px;}}
                    </style></head><body><div class="doc">{rendered}</div></body></html>"""
                    st.download_button(
                        "📥 HTML 다운로드", data=html_doc.encode("utf-8"),
                        file_name=f"{tpl['title']}.html", mime="text/html", key=f"dl_html_{uid}",
                        use_container_width=True,
                    )

st.session_state["template_field_values"] = field_values

styles.footer()
