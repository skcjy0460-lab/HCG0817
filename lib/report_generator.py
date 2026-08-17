"""
종합 진단 HTML 리포트 생성기.
재무진단 + 체크리스트 진행률 + 리스크 스코어 + AI 진단 결과를 하나의 프리미엄 HTML 문서로 출력.
외부 의존성 없이(순수 HTML/CSS) 어디서나 열람 가능하도록 구성.
"""

from datetime import datetime
import html as _html

NAVY = "#0F1B2D"
DEEP_NAVY = "#0A1420"
GOLD = "#C9A24B"
PAPER = "#FBFAF7"
BORDER = "#E4DFD4"
MUTED = "#6B7685"


def _esc(s):
    return _html.escape(str(s)) if s is not None else ""


def _risk_color(band):
    return {"critical": "#B0413E", "high": "#B8862E", "normal": "#8A6A1E", "low": "#2E6B4F"}.get(band, "#6B7685")


def _progress_bar_html(pct, color=GOLD):
    return f"""
    <div style="background:#EFEBE0;border-radius:6px;height:10px;width:100%;overflow:hidden;">
      <div style="background:{color};height:10px;width:{pct}%;"></div>
    </div>
    """


def _markdown_lite_to_html(md_text: str) -> str:
    """AI 응답(마크다운)을 아주 단순한 HTML로 변환 (##, -, 굵게 정도만 지원)."""
    if not md_text:
        return "<p style='color:#6B7685;'>AI 진단 결과가 없습니다.</p>"
    lines = md_text.split("\n")
    out = []
    in_list = False
    for line in lines:
        line = line.rstrip()
        if line.startswith("## "):
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append(f"<h3 style='color:{NAVY};border-left:4px solid {GOLD};padding-left:10px;margin-top:22px;'>{_esc(line[3:])}</h3>")
        elif line.startswith("# "):
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append(f"<h2 style='color:{NAVY};'>{_esc(line[2:])}</h2>")
        elif line.strip().startswith("- ") or line.strip().startswith("* "):
            if not in_list:
                out.append("<ul style='line-height:1.8;color:#1C2733;'>")
                in_list = True
            content = line.strip()[2:]
            content = content.replace("**", "")
            out.append(f"<li>{_esc(content)}</li>")
        elif line.strip() == "":
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append("<div style='height:6px;'></div>")
        else:
            if in_list:
                out.append("</ul>")
                in_list = False
            content = line.replace("**", "")
            out.append(f"<p style='line-height:1.8;color:#1C2733;margin:4px 0;'>{_esc(content)}</p>")
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


def build_report_html(context: dict) -> str:
    """
    context keys:
        org_name, generated_at, selected_path_label,
        financial: dict(total_assets,total_liabilities,net_asset,cash_in,cash_out,cash_gap,is_insolvent,is_illiquid),
        progress: {카테고리명: {total,done,pct,critical_total,critical_done,critical_pct}},
        risk: {score,band,label,color},
        hr_summary: {headcount, total_severance},
        ai_result: str (markdown) or None,
        ai_model_used: str or None,
    """
    org_name = context.get("org_name") or "(기관명 미입력)"
    generated_at = context.get("generated_at") or datetime.now().strftime("%Y-%m-%d %H:%M")
    fin = context.get("financial", {})
    progress = context.get("progress", {})
    risk = context.get("risk", {})
    hr = context.get("hr_summary", {})
    ai_result = context.get("ai_result")
    ai_model_used = context.get("ai_model_used")

    progress_rows = ""
    for name, p in progress.items():
        progress_rows += f"""
        <tr>
          <td style="padding:10px 8px;border-bottom:1px solid {BORDER};font-weight:600;color:{NAVY};">{_esc(name)}</td>
          <td style="padding:10px 8px;border-bottom:1px solid {BORDER};width:40%;">{_progress_bar_html(p.get('pct',0))}</td>
          <td style="padding:10px 8px;border-bottom:1px solid {BORDER};text-align:right;color:{MUTED};">{p.get('done',0)}/{p.get('total',0)} ({p.get('pct',0)}%)</td>
          <td style="padding:10px 8px;border-bottom:1px solid {BORDER};text-align:right;color:{MUTED};">핵심 {p.get('critical_pct',0)}%</td>
        </tr>
        """

    risk_color = risk.get("color", _risk_color(risk.get("band")))

    ai_html = _markdown_lite_to_html(ai_result) if ai_result else (
        "<p style='color:#6B7685;'>AI 종합진단이 아직 실행되지 않았습니다. "
        "'AI 종합진단' 페이지에서 진단을 실행한 뒤 리포트를 다시 생성해주세요.</p>"
    )

    html_doc = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>{_esc(org_name)} · 폐업·해산·파산 종합 진단 리포트</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@600;700;900&family=Noto+Sans+KR:wght@400;500;600;700&display=swap');
  * {{ box-sizing: border-box; }}
  body {{
    font-family: 'Noto Sans KR', sans-serif;
    background: {PAPER};
    color: #1C2733;
    margin: 0;
    padding: 0;
  }}
  .page {{
    max-width: 880px;
    margin: 0 auto;
    padding: 48px 40px 80px 40px;
  }}
  .cover {{
    background: linear-gradient(135deg, {DEEP_NAVY} 0%, {NAVY} 55%, #16283F 100%);
    border: 1px solid {GOLD};
    border-radius: 6px;
    padding: 44px 40px;
    margin-bottom: 34px;
    position: relative;
    overflow: hidden;
  }}
  .cover::before {{
    content: "";
    position: absolute; top:0; right:0; bottom:0; width:7px;
    background: linear-gradient(180deg, #E4C97A, {GOLD});
  }}
  .cover .eyebrow {{
    color: #E4C97A; letter-spacing: .2em; font-size: 12px; font-weight:700; text-transform:uppercase;
  }}
  .cover h1 {{
    font-family:'Noto Serif KR',serif; color:#F7F5EF; font-size:30px; margin: 14px 0 10px 0; line-height:1.4;
  }}
  .cover .meta {{ color:#C7CEDA; font-size:13.5px; line-height:1.9; }}
  .section-title {{
    font-family:'Noto Serif KR',serif; font-size:19px; font-weight:700; color:{NAVY};
    border-left:5px solid {GOLD}; padding-left:12px; margin: 34px 0 16px 0;
  }}
  .kpi-grid {{ display:flex; gap:14px; flex-wrap:wrap; margin-bottom: 10px;}}
  .kpi {{
    flex:1; min-width:170px; background:#fff; border:1px solid {BORDER}; border-top:3px solid {GOLD};
    border-radius:5px; padding:14px 16px;
  }}
  .kpi .label {{ font-size:11.5px; color:{MUTED}; font-weight:700; text-transform:uppercase; letter-spacing:.03em; }}
  .kpi .value {{ font-family:'Noto Serif KR',serif; font-size:21px; font-weight:800; color:{NAVY}; margin-top:4px; }}
  table {{ width:100%; border-collapse: collapse; background:#fff; border:1px solid {BORDER}; border-radius:5px; }}
  .risk-banner {{
    border-radius:6px; padding:20px 24px; color:#fff; background:{risk_color};
    display:flex; justify-content:space-between; align-items:center; margin-bottom: 8px;
  }}
  .risk-banner .score {{ font-family:'Noto Serif KR',serif; font-size:34px; font-weight:900; }}
  .card {{ background:#fff; border:1px solid {BORDER}; border-radius:6px; padding:20px 24px; margin-bottom:14px; }}
  .footer {{
    margin-top: 50px; padding-top: 18px; border-top:1px solid {BORDER}; color:{MUTED}; font-size:11.5px; line-height:1.9;
  }}
  .disclaimer {{
    background:#FBF3E4; border:1px solid #E9D19E; color:#8A6A1E; border-radius:5px; padding:14px 18px; font-size:12.8px; line-height:1.75; margin-top: 10px;
  }}
</style>
</head>
<body>
<div class="page">

  <div class="cover">
    <div class="eyebrow">MEDIEM · 병원 폐업·해산·파산 실무 가이드 PRO</div>
    <h1>{_esc(org_name)}<br>종합 진단 리포트</h1>
    <div class="meta">
      생성일시: {_esc(generated_at)}<br>
      권장/선택 경로: {_esc(context.get("selected_path_label", "-"))}
    </div>
  </div>

  <div class="section-title">1. 재무 진단 요약</div>
  <div class="kpi-grid">
    <div class="kpi"><div class="label">총자산(처분가액)</div><div class="value">{fin.get('total_assets',0):,.0f}원</div></div>
    <div class="kpi"><div class="label">총부채</div><div class="value">{fin.get('total_liabilities',0):,.0f}원</div></div>
    <div class="kpi"><div class="label">순자산</div><div class="value" style="color:{'#B0413E' if fin.get('is_insolvent') else '#2E6B4F'}">{fin.get('net_asset',0):,.0f}원</div></div>
    <div class="kpi"><div class="label">월 현금흐름 갭</div><div class="value" style="color:{'#B0413E' if fin.get('is_illiquid') else '#2E6B4F'}">{fin.get('cash_gap',0):,.0f}원</div></div>
  </div>
  <div class="card">
    채무초과 여부: <b>{"해당 (채무초과)" if fin.get("is_insolvent") else "해당없음"}</b> &nbsp;|&nbsp;
    영업불능 여부: <b>{"해당 (영업불능)" if fin.get("is_illiquid") else "해당없음"}</b>
  </div>

  <div class="section-title">2. 종합 리스크 스코어</div>
  <div class="risk-banner">
    <div>
      <div style="font-size:12px;letter-spacing:.1em;opacity:.85;">RISK LEVEL</div>
      <div style="font-size:20px;font-weight:800;margin-top:4px;">{_esc(risk.get('label','-'))}</div>
    </div>
    <div class="score">{risk.get('score', '-')}<span style="font-size:16px;">/100</span></div>
  </div>
  <div style="color:{MUTED};font-size:12.5px;">점수가 높을수록(60 이상) 리스크가 높음을 의미합니다. (체크리스트 이행률 60% + 재무 리스크 20% + 금지행위 해당여부 20% 가중)</div>

  <div class="section-title">3. 영역별 체크리스트 진행률</div>
  <table>
    <thead>
      <tr style="background:#F3F0E8;">
        <th style="text-align:left;padding:10px 8px;">영역</th>
        <th style="text-align:left;padding:10px 8px;">진행률</th>
        <th style="text-align:right;padding:10px 8px;">완료/전체</th>
        <th style="text-align:right;padding:10px 8px;">핵심항목</th>
      </tr>
    </thead>
    <tbody>
      {progress_rows}
    </tbody>
  </table>

  <div class="section-title">4. 인사·노무 요약</div>
  <div class="kpi-grid">
    <div class="kpi"><div class="label">정리 대상 인원</div><div class="value">{hr.get('headcount',0)}명</div></div>
    <div class="kpi"><div class="label">추정 퇴직금 총액</div><div class="value">{hr.get('total_severance',0):,.0f}원</div></div>
  </div>

  <div class="section-title">5. AI 종합진단 {f"(모델: {_esc(ai_model_used)})" if ai_model_used else ""}</div>
  <div class="card">
    {ai_html}
  </div>

  <div class="disclaimer">
    ⚠️ 본 리포트는 실무 참고용으로 자동 생성되었으며, 법률·세무·노무 자문을 대체하지 않습니다. 사안별 사실관계 및
    관할기관(보건소·주무관청·법원·세무서)에 따라 절차·서류가 달라질 수 있으므로, 중요한 의사결정 전 반드시
    변호사·회계사·노무사 등 전문가와 사전 협의하시기 바랍니다.
  </div>

  <div class="footer">
    ⓒ Mediem Co. · 병원 폐업·해산·파산 실무 가이드 PRO · 본 리포트는 라이선스 사용자 전용으로 제공되며 무단 복제·재배포를 금합니다.
  </div>

</div>
</body>
</html>
"""
    return html_doc
