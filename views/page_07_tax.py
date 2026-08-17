import streamlit as st
from lib import styles
from lib.checklist_ui import render_checklist

styles.hero(
    "⑤ 세무·4대보험·건보/심평원·행정 통합 정리",
    "세무, 4대보험, 건강보험공단 및 심사평가원, 임대차, 대외 공지 등 행정 정리는 동시다발적으로 진행되며 "
    "각각의 마감 기한이 다릅니다.",
    eyebrow="PHASE 5 · 세무·보험·행정 (병행 진행)",
)

styles.alert(
    "warn",
    "<b>실무 팁: 통합 일정표 작성이 핵심 —</b> '폐업'은 하루에 끝나지만 '정산'은 몇 달이 걸립니다. "
    "세무(부가세·원천세·법인세), 4대보험(상실·정산), 건보/심평원(청구 종료·환수), 임대차(해지·원상복구·보증금)를 "
    "한 장의 엑셀 일정표로 통합 관리하세요. 각 영역의 담당자와 마감일, 제출 서류를 명확히 기록하고, 주 단위로 "
    "진행 상황을 점검하면 누락을 방지할 수 있습니다.",
)

areas = [
    ("1", "세무 정리", "폐업일 확정(20일 이내 신고), 부가세 확정신고(폐업일 다음달 25일까지), 원천세·법인세 정산"),
    ("2", "4대보험 정리", "사업장 상실 신고(퇴직자 개별 상실과 별도), 보험료 정산, 고용·산재보험 정산 신고"),
    ("3", "건보/심평원 정리", "요양급여 청구 마감·최종 청구, 환수금 통지 확인, 요양기관 지정 취소 절차"),
    ("4", "임대차·자산 정리", "해지 통지, 원상복구 범위 협의(증빙 확보), 보증금 정산 일정 문서화"),
    ("5", "대외 공지 및 민원 대비", "환자/직원/거래처 공지문, 민원 대응 Q&A 문서 작성 및 담당자 지정"),
]
styles.section_title("영역별 세부 개요")
cols = st.columns(len(areas))
for col, (no, title, desc) in zip(cols, areas):
    with col:
        st.markdown(
            f"""<div class="mediem-card" style="min-height:220px;">
            <span class="badge badge-gold">{no}</span>
            <h4 style="margin-top:8px;">{title}</h4>
            <p style="font-size:12.6px;">{desc}</p>
            </div>""",
            unsafe_allow_html=True,
        )

st.write("")
styles.section_title("통합 실행 체크리스트")
render_checklist("tax")

styles.footer()
