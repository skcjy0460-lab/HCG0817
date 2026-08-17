"""
프리미엄 UI 테마 - 네이비 & 골드 톤의 로펌/회계법인 스타일
"""

import streamlit as st

PRIMARY_NAVY = "#0F1B2D"
DEEP_NAVY = "#0A1420"
GOLD = "#C9A24B"
GOLD_LIGHT = "#E4C97A"
INK = "#1C2733"
PAPER = "#FBFAF7"
MUTED = "#6B7685"
DANGER = "#B0413E"
DANGER_BG = "#FBEEED"
WARN = "#B8862E"
WARN_BG = "#FBF3E4"
OK = "#2E6B4F"
OK_BG = "#EAF4EF"
BORDER = "#E4DFD4"


def inject_base_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;500;600;700;900&family=Noto+Sans+KR:wght@300;400;500;600;700;800&display=swap');

        html, body, [class*="css"]  {{
            font-family: 'Noto Sans KR', sans-serif;
        }}

        .stApp {{
            background: {PAPER};
        }}

        /* 사이드바 */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {DEEP_NAVY} 0%, {PRIMARY_NAVY} 100%);
            border-right: 1px solid {GOLD};
        }}
        section[data-testid="stSidebar"] * {{
            color: #EDEBE3 !important;
        }}
        section[data-testid="stSidebar"] hr {{
            border-color: rgba(201,162,75,0.25);
        }}

        /* 메인 헤더 배너 */
        .mediem-hero {{
            background: linear-gradient(135deg, {DEEP_NAVY} 0%, {PRIMARY_NAVY} 55%, #16283F 100%);
            border: 1px solid {GOLD};
            border-radius: 4px;
            padding: 34px 38px;
            margin-bottom: 26px;
            position: relative;
            overflow: hidden;
        }}
        .mediem-hero::before {{
            content: "";
            position: absolute; top: 0; right: 0; bottom: 0; width: 6px;
            background: linear-gradient(180deg, {GOLD_LIGHT}, {GOLD});
        }}
        .mediem-hero .eyebrow {{
            color: {GOLD_LIGHT};
            letter-spacing: .18em;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            margin-bottom: 10px;
        }}
        .mediem-hero h1 {{
            font-family: 'Noto Serif KR', serif;
            color: #F7F5EF;
            font-size: 30px;
            font-weight: 700;
            margin: 0 0 8px 0;
            line-height: 1.35;
        }}
        .mediem-hero p {{
            color: #C7CEDA;
            font-size: 14.5px;
            margin: 0;
            line-height: 1.65;
        }}

        /* 섹션 타이틀 */
        .mediem-section-title {{
            font-family: 'Noto Serif KR', serif;
            font-size: 21px;
            font-weight: 700;
            color: {PRIMARY_NAVY};
            border-left: 5px solid {GOLD};
            padding-left: 14px;
            margin: 6px 0 4px 0;
        }}
        .mediem-section-sub {{
            color: {MUTED};
            font-size: 13.5px;
            padding-left: 19px;
            margin-bottom: 18px;
        }}

        /* 카드 */
        .mediem-card {{
            background: #FFFFFF;
            border: 1px solid {BORDER};
            border-radius: 4px;
            padding: 22px 24px;
            margin-bottom: 16px;
            box-shadow: 0 1px 2px rgba(15,27,45,0.04);
        }}
        .mediem-card.gold-edge {{
            border-left: 4px solid {GOLD};
        }}
        .mediem-card h4 {{
            margin: 0 0 8px 0;
            color: {PRIMARY_NAVY};
            font-size: 16px;
            font-weight: 700;
        }}
        .mediem-card p {{
            color: {INK};
            font-size: 13.8px;
            line-height: 1.7;
            margin: 0;
        }}

        /* 경고 / 위험 박스 */
        .mediem-alert {{
            border-radius: 4px;
            padding: 16px 20px;
            margin: 14px 0;
            font-size: 13.6px;
            line-height: 1.7;
            border: 1px solid;
        }}
        .mediem-alert.danger {{
            background: {DANGER_BG}; border-color: #E3B9B6; color: {DANGER};
        }}
        .mediem-alert.warn {{
            background: {WARN_BG}; border-color: #E9D19E; color: {WARN};
        }}
        .mediem-alert.ok {{
            background: {OK_BG}; border-color: #B9DCC8; color: {OK};
        }}
        .mediem-alert b {{ font-weight: 800; }}

        /* KPI */
        .kpi-box {{
            background: #FFFFFF;
            border: 1px solid {BORDER};
            border-top: 3px solid {GOLD};
            border-radius: 4px;
            padding: 16px 18px;
            text-align: left;
        }}
        .kpi-box .label {{
            color: {MUTED}; font-size: 12px; font-weight: 600; letter-spacing: .04em;
            text-transform: uppercase; margin-bottom: 6px;
        }}
        .kpi-box .value {{
            color: {PRIMARY_NAVY}; font-size: 25px; font-weight: 800;
            font-family: 'Noto Serif KR', serif;
        }}
        .kpi-box .delta {{ font-size: 12.5px; margin-top: 4px; }}

        /* 뱃지 */
        .badge {{
            display: inline-block; padding: 3px 10px; border-radius: 12px;
            font-size: 11.5px; font-weight: 700; letter-spacing: .02em;
        }}
        .badge-gold {{ background: #FBF2DD; color: #8A6A1E; border: 1px solid #E4C97A;}}
        .badge-navy {{ background: #E7EBF2; color: {PRIMARY_NAVY}; border: 1px solid #C4CCDA;}}
        .badge-danger {{ background: {DANGER_BG}; color: {DANGER}; border: 1px solid #E3B9B6;}}
        .badge-ok {{ background: {OK_BG}; color: {OK}; border: 1px solid #B9DCC8;}}

        /* 버튼 */
        .stButton>button {{
            background: {PRIMARY_NAVY};
            color: #F7F5EF;
            border: 1px solid {PRIMARY_NAVY};
            border-radius: 3px;
            font-weight: 600;
            padding: 8px 20px;
            transition: all .15s ease;
        }}
        .stButton>button:hover {{
            background: {GOLD};
            border-color: {GOLD};
            color: {DEEP_NAVY};
        }}
        .stDownloadButton>button {{
            background: #FFFFFF;
            color: {PRIMARY_NAVY};
            border: 1.4px solid {GOLD};
            border-radius: 3px;
            font-weight: 700;
        }}
        .stDownloadButton>button:hover {{
            background: {GOLD};
            color: #FFFFFF;
        }}

        /* 진행률 텍스트 */
        .progress-caption {{
            font-size: 12.5px; color: {MUTED}; margin-top: -6px; margin-bottom: 10px;
        }}

        /* footer */
        .mediem-footer {{
            margin-top: 46px;
            padding: 22px 4px 10px 4px;
            border-top: 1px solid {BORDER};
            color: {MUTED};
            font-size: 11.8px;
            line-height: 1.9;
        }}
        .mediem-footer b {{ color: {PRIMARY_NAVY}; }}

        /* 타임라인 스텝 */
        .step-num {{
            display: inline-flex; align-items:center; justify-content:center;
            width: 30px; height: 30px; border-radius: 50%;
            background: {PRIMARY_NAVY}; color: {GOLD_LIGHT}; font-weight: 800;
            font-size: 13.5px; margin-right: 10px; flex-shrink: 0;
        }}

        hr {{ border-color: {BORDER}; }}

        div[data-testid="stExpander"] {{
            border: 1px solid {BORDER};
            border-radius: 4px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle: str, eyebrow: str = "MEDIEM · 병원 폐업·해산·파산 실무 가이드"):
    st.markdown(
        f"""
        <div class="mediem-hero">
            <div class="eyebrow">{eyebrow}</div>
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(title: str, sub: str = ""):
    st.markdown(f'<div class="mediem-section-title">{title}</div>', unsafe_allow_html=True)
    if sub:
        st.markdown(f'<div class="mediem-section-sub">{sub}</div>', unsafe_allow_html=True)


def alert(kind: str, html: str):
    st.markdown(f'<div class="mediem-alert {kind}">{html}</div>', unsafe_allow_html=True)


def kpi(label: str, value: str, delta: str = "", delta_color: str = "#6B7685"):
    st.markdown(
        f"""
        <div class="kpi-box">
            <div class="label">{label}</div>
            <div class="value">{value}</div>
            <div class="delta" style="color:{delta_color};">{delta}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def footer():
    st.markdown(
        """
        <div class="mediem-footer">
        <b>본 프로그램은 실무 참고용 유료 서비스이며, 법률·세무·노무 자문을 대체하지 않습니다.</b><br>
        사안별 사실관계 및 관할기관(보건소·주무관청·법원·세무서)에 따라 절차와 서류가 달라질 수 있으므로,
        중요한 의사결정 전 반드시 변호사·회계사·노무사 등 전문가와 사전 협의하시기 바랍니다.<br>
        ⓒ Mediem Co. 병원 폐업·해산·파산 실무 가이드 · 무단 복제 및 재배포를 금합니다.
        </div>
        """,
        unsafe_allow_html=True,
    )
