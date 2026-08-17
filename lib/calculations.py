"""
핵심 계산 로직: 퇴직금 산정, 채무초과/영업불능 판정, 리스크 스코어링
정밀 계산을 위해 Decimal을 사용합니다.
"""

from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from datetime import date


def D(value) -> Decimal:
    """안전한 Decimal 변환."""
    if value is None or value == "":
        return Decimal("0")
    try:
        return Decimal(str(value))
    except InvalidOperation:
        return Decimal("0")


def round2(value: Decimal) -> Decimal:
    return value.quantize(Decimal("1"), rounding=ROUND_HALF_UP)


def calc_service_period(hire_date: date, end_date: date):
    """근속 일수 및 (년, 개월, 일) 반환."""
    if not hire_date or not end_date or end_date <= hire_date:
        return 0, (0, 0, 0)
    total_days = (end_date - hire_date).days
    years = total_days // 365
    remainder = total_days - years * 365
    months = remainder // 30
    days = remainder - months * 30
    return total_days, (int(years), int(months), int(days))


def calc_severance_pay(avg_monthly_wage, total_service_days: int) -> Decimal:
    """
    근로기준법 제34조 / 근로자퇴직급여보장법 기준 퇴직금 산정(단순 모델).
    퇴직금 = 1일 평균임금 × 30일 × (재직일수 / 365)
    1일 평균임금 = 평균 월급여 × 3 / 사유발생일 이전 3개월간 총 일수(근사 90일)로 근사.
    실무에서는 최근 3개월 실지급 총액 기준 정밀 산정이 필요합니다(본 값은 참고용 추정치).
    """
    avg_wage = D(avg_monthly_wage)
    if total_service_days < 365:
        # 계속근로기간 1년 미만은 법정 퇴직금 지급의무 없음 (참고용으로 일할 계산 표시)
        pass
    daily_avg_wage = (avg_wage * Decimal("3")) / Decimal("90")
    severance = daily_avg_wage * Decimal("30") * (Decimal(total_service_days) / Decimal("365"))
    return round2(severance)


def financial_diagnosis(total_assets, total_liabilities, monthly_cash_in, monthly_cash_out, months_runway_input=None):
    """
    채무초과·영업불능 여부를 판단하여 권장 경로를 산출.
    반환: dict(is_insolvent, is_illiquid, recommended_path, net_asset, cash_gap, risk_level)
    """
    assets = D(total_assets)
    liabilities = D(total_liabilities)
    cash_in = D(monthly_cash_in)
    cash_out = D(monthly_cash_out)

    net_asset = assets - liabilities
    is_insolvent = net_asset < 0  # 채무초과

    cash_gap = cash_in - cash_out
    is_illiquid = cash_gap < 0  # 영업불능(현금흐름 악화) 근사 판단

    if is_insolvent and is_illiquid:
        recommended_path = "bankruptcy"
        risk_level = "critical"
    elif is_insolvent and not is_illiquid:
        recommended_path = "review"  # 채무초과지만 현금흐름 유지 -> 전문가 검토 필요
        risk_level = "high"
    elif (not is_insolvent) and is_illiquid:
        recommended_path = "review"
        risk_level = "high"
    else:
        recommended_path = "liquidation"
        risk_level = "normal"

    return {
        "net_asset": net_asset,
        "is_insolvent": is_insolvent,
        "cash_gap": cash_gap,
        "is_illiquid": is_illiquid,
        "recommended_path": recommended_path,
        "risk_level": risk_level,
    }


def checklist_progress(checked_ids: set, checklist_def: dict):
    """특정 체크리스트(dict of groups)의 진행률(전체/critical) 계산."""
    total, done = 0, 0
    critical_total, critical_done = 0, 0
    for items in checklist_def["groups"].values():
        for item_id, _, _, importance in items:
            total += 1
            if item_id in checked_ids:
                done += 1
            if importance == "critical":
                critical_total += 1
                if item_id in checked_ids:
                    critical_done += 1
    pct = round((done / total) * 100) if total else 0
    critical_pct = round((critical_done / critical_total) * 100) if critical_total else 0
    return {
        "total": total, "done": done, "pct": pct,
        "critical_total": critical_total, "critical_done": critical_done, "critical_pct": critical_pct,
    }


def overall_risk_score(all_progress: dict, financial_risk_level: str, forbidden_act_flags: dict):
    """
    종합 리스크 스코어(0~100, 낮을수록 안전) 산출.
    - 체크리스트 미이행 비중 60%
    - 재무 리스크 20%
    - 금지행위 해당여부 20%
    """
    if not all_progress:
        checklist_score = 100
    else:
        pcts = [v["pct"] for v in all_progress.values()]
        checklist_score = 100 - (sum(pcts) / len(pcts))

    fin_map = {"normal": 0, "high": 55, "critical": 100}
    fin_score = fin_map.get(financial_risk_level, 30)

    forbidden_hits = sum(1 for v in forbidden_act_flags.values() if v)
    forbidden_score = min(100, forbidden_hits * 40)

    total_score = checklist_score * 0.6 + fin_score * 0.2 + forbidden_score * 0.2
    total_score = round(total_score)

    if total_score >= 60:
        band = ("critical", "매우 높음", "#B0413E")
    elif total_score >= 35:
        band = ("high", "높음", "#B8862E")
    elif total_score >= 15:
        band = ("normal", "보통", "#8A6A1E")
    else:
        band = ("low", "낮음", "#2E6B4F")

    return {"score": total_score, "band": band[0], "label": band[1], "color": band[2]}
