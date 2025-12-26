import os
from typing import List, Dict
import requests

from .interfaces import RakutenGoraService


class RakutenGoraServiceClient(RakutenGoraService):
    """Real Rakuten Gora API client (minimal).

    Reads RAKUTEN_APPLICATION_ID from environment. Returns a list of plan dicts with
    keys: course_id, course_name, plan_name, price, address, play_date, start_time, ic
    """

    ENDPOINT = "https://app.rakuten.co.jp/services/api/Gora/GoraPlanSearch/20170623"

    def __init__(self, application_id: str = None, timeout: int = 10):
        self.application_id = application_id or os.environ.get('RAKUTEN_APPLICATION_ID')
        if not self.application_id:
            raise ValueError('RAKUTEN_APPLICATION_ID is required in environment to call Rakuten Gora API')
        self.timeout = timeout

    def _safe_address(self, item: dict) -> str:
        # Prefer explicit address fields if provided, otherwise compose from prefecture + ic
        addr = item.get('address') or item.get('golfCourseAddress') or ''
        if addr:
            return addr
        parts = []
        if item.get('prefecture'):
            parts.append(item.get('prefecture'))
        if item.get('ic'):
            parts.append(item.get('ic'))
        if parts:
            return ' '.join(parts)
        # fallback to course name
        return item.get('golfCourseName', '')

    def search_plans(self, area_code: int, play_date: str, min_price: int = None, max_price: int = None, start_time_zone: int = None) -> List[Dict]:
        params = {
            'applicationId': self.application_id,
            'format': 'json',
            'areaCode': area_code,
            'playDate': play_date,
            # paging を制限して必要分だけ取る（最大 30 件）
            'page': 1,
            'hits': 30,
        }

        if min_price is not None:
            params['minPrice'] = min_price
        if max_price is not None:
            params['maxPrice'] = max_price
        if start_time_zone is not None:
            params['startTimeZone'] = start_time_zone

        try:
            resp = requests.get(self.ENDPOINT, params=params, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
        except Exception:
            # On error, don't raise to upper layers; return empty list so caller can handle gracefully
            return []

        items = data.get('Items') or []
        results: List[Dict] = []

        for wrapper in items:
            item = wrapper.get('Item') if isinstance(wrapper, dict) else None
            if not item:
                continue

            # Each item may contain multiple plans
            plan_infos = item.get('planInfo') or []
            for pi in plan_infos:
                plan = pi.get('plan') or {}
                # price may be nested under plan
                price = plan.get('price')

                # Extract reservation URL: prefer plan-level callInfo -> plan-level -> item-level -> mobile fallback
                plan_call = plan.get('callInfo') or {}
                item_call = item.get('callInfo') or {}
                reserve_url = (
                    plan_call.get('reservePageUrlPC')
                    or plan.get('reservePageUrlPC')
                    or item_call.get('reservePageUrlPC')
                    or item.get('reservePageUrlPC')
                    or item_call.get('reservePageUrlMobile')
                    or item.get('reservePageUrlMobile')
                    or None
                )

                result = {
                    'course_id': item.get('golfCourseId') or item.get('golfCourseId'),
                    'course_name': item.get('golfCourseName'),
                    'plan_name': plan.get('planName'),
                    'price': price,
                    'address': self._safe_address(item),
                    'play_date': plan_call.get('playDate') or play_date,
                    'start_time': plan.get('startTimeZone') or plan.get('startTime') or '',
                    'ic': item.get('ic'),
                    'reservePageUrlPC': reserve_url
                }

                # Apply simple client-side filters if API didn't filter
                if min_price is not None and (price is None or price < min_price):
                    continue
                if max_price is not None and (price is None or price > max_price):
                    continue

                results.append(result)

        return results
