"""
Gemini API 연동 - AI 종합진단 엔진
모델 자동 폴백: gemini-3.6-flash → gemini-3.5-flash-lite → gemini-2.5-flash → gemini-2.0-flash
"""

import streamlit as st

MODEL_FALLBACK_CHAIN = [
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
]

SYSTEM_INSTRUCTION = """당신은 대한민국 의료기관/의료법인 전문 경영 컨설턴트입니다.
병원 개원·경영 컨설팅 전문회사 '메디엄(Mediem)'의 AI 자문 엔진으로서,
의료기관 폐업, 의료재단(의료법인) 해산·청산, 파산 절차에 대해
실무적이고 구체적이며 즉시 활용 가능한 조언을 제공합니다.

다음 원칙을 반드시 지키세요.
1. 답변은 한국어로, 실무자가 바로 활용할 수 있는 톤(전문 컨설턴트 보고서 톤)으로 작성합니다.
2. 의료법, 근로기준법, 채무자회생 및 파산에 관한 법률 등 관련 법령의 취지를 일반적인 수준에서 언급하되,
   특정 사건에 대한 법률 자문이 아니라 '일반적인 실무 가이드'임을 톤에 반영합니다.
3. 입력된 재무 데이터와 체크리스트 진행 상황을 근거로, 막연한 원론이 아니라
   해당 병원의 현재 상황에 맞춘 구체적 조언을 제시합니다.
4. 특정 채권자 우선변제, 임의 자산처분, 장부조작 등 위법 소지가 있는 행위는
   명확히 경고하고 대안을 제시합니다.
5. 마지막에는 반드시 "전문가(변호사·회계사·노무사) 사전 상담을 권장한다"는 문구를 포함합니다.
6. 답변은 마크다운 형식으로, 아래 구조를 따르세요.
   ## 종합 진단
   ## 우선순위 조치사항 (Top 5)
   ## 리스크 경고
   ## 다음 30일 실행 로드맵
"""


def _get_api_key():
    try:
        return st.secrets.get("GEMINI_API_KEY", None)
    except Exception:
        return None


def build_user_prompt(context: dict) -> str:
    """진단에 필요한 컨텍스트를 프롬프트 문자열로 구성."""
    lines = []
    lines.append(f"[기관명] {context.get('org_name') or '(미입력)'}")
    lines.append(f"[진단 시점] {context.get('today')}")
    lines.append("")
    lines.append("## 재무 현황")
    fin = context.get("financial", {})
    lines.append(f"- 총자산(처분가능액 기준): {fin.get('total_assets', 0):,} 원")
    lines.append(f"- 총부채(확정+추정): {fin.get('total_liabilities', 0):,} 원")
    lines.append(f"- 순자산: {fin.get('net_asset', 0):,} 원")
    lines.append(f"- 월 현금유입: {fin.get('cash_in', 0):,} 원 / 월 현금유출: {fin.get('cash_out', 0):,} 원")
    lines.append(f"- 채무초과 여부: {'예' if fin.get('is_insolvent') else '아니오'}")
    lines.append(f"- 영업(현금흐름) 불능 여부: {'예' if fin.get('is_illiquid') else '아니오'}")
    lines.append(f"- 시스템 권장 경로: {context.get('recommended_path_label')}")
    lines.append(f"- 컨설턴트/사용자가 선택한 경로: {context.get('selected_path_label')}")
    lines.append("")
    lines.append("## 체크리스트 이행 현황 (카테고리별 진행률)")
    for name, prog in context.get("progress", {}).items():
        lines.append(f"- {name}: 전체 {prog['pct']}% 완료 (핵심항목 {prog['critical_pct']}% 완료)")
    lines.append("")
    lines.append("## 인사·노무 요약")
    hr = context.get("hr_summary", {})
    lines.append(f"- 정리 대상 인원: {hr.get('headcount', 0)}명")
    lines.append(f"- 추정 퇴직금 총액: {hr.get('total_severance', 0):,} 원")
    lines.append("")
    lines.append("## 금지행위 해당여부 자가진단")
    forbidden = context.get("forbidden_flags", {})
    if any(forbidden.values()):
        hit_list = [k for k, v in forbidden.items() if v]
        lines.append(f"- ⚠ 다음 항목에 해당된다고 응답함: {', '.join(hit_list)}")
    else:
        lines.append("- 해당 없음으로 응답함")
    lines.append("")
    lines.append("## 컨설턴트 추가 메모")
    lines.append(context.get("extra_note") or "(없음)")
    lines.append("")
    lines.append("위 정보를 바탕으로 이 병원/의료법인의 상황에 맞춘 종합 진단 보고서를 작성해주세요.")
    return "\n".join(lines)


def run_ai_diagnosis(context: dict):
    """
    Gemini API 호출. 모델 체인을 순서대로 시도하며 실패 시 다음 모델로 폴백.
    반환: (성공여부, 결과텍스트 또는 에러메시지, 사용된 모델명)
    """
    api_key = _get_api_key()
    if not api_key:
        return False, (
            "GEMINI_API_KEY가 설정되어 있지 않습니다. "
            "Streamlit Cloud의 'Secrets' 설정에서 GEMINI_API_KEY를 등록한 뒤 다시 시도해주세요."
        ), None

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        return False, "google-genai 패키지가 설치되어 있지 않습니다. requirements.txt를 확인해주세요.", None

    client = genai.Client(api_key=api_key)
    prompt = build_user_prompt(context)

    last_error = None
    for model_name in MODEL_FALLBACK_CHAIN:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.4,
                    max_output_tokens=3000,
                ),
            )
            text = getattr(response, "text", None)
            if text:
                return True, text, model_name
            last_error = f"{model_name}: 빈 응답"
        except Exception as e:
            last_error = f"{model_name}: {e}"
            continue

    return False, f"모든 AI 모델 호출에 실패했습니다. (마지막 오류: {last_error})", None
