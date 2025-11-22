from .interfaces import RakutenGoraService, GoogleMapsService
from .models import GolfCourse, SearchResult
from typing import List, Dict
from datetime import datetime


class RakutenGoraServiceStub(RakutenGoraService):
    """Stub implementation that returns sample golf plans varying by area_code and play_date."""
    def search_plans(self, area_code: int, play_date: str, min_price: int = None, max_price: int = None, start_time_zone: int = None) -> List[Dict]:
        # Return different sample data depending on area_code for simple variation
        samples = []
        if area_code == 1:
            samples = [
                {
                    'course_id': '1-100',
                    'course_name': 'Tokyo Hills Golf Club',
                    'plan_name': '平日プラン',
                    'price': 8000,
                    'address': '東京都渋谷区1-1',
                    'play_date': play_date,
                    'start_time': '08:00'
                },
                {
                    'course_id': '1-101',
                    'course_name': 'Shinjuku Greens',
                    'plan_name': '土日プラン',
                    'price': 12000,
                    'address': '東京都新宿区2-2',
                    'play_date': play_date,
                    'start_time': '09:00'
                }
            ]
        else:
            samples = [
                {
                    'course_id': f'{area_code}-200',
                    'course_name': f'Area{area_code} Golf Club',
                    'plan_name': '通常プラン',
                    'price': 7000 + (area_code * 100),
                    'address': f'Prefecture area {area_code}',
                    'play_date': play_date,
                    'start_time': '10:00'
                }
            ]

        # Apply price filters if provided
        if min_price is not None:
            samples = [s for s in samples if s['price'] >= min_price]
        if max_price is not None:
            samples = [s for s in samples if s['price'] <= max_price]

        return samples


class GoogleMapsServiceStub(GoogleMapsService):
    """Stub implementation that returns deterministic travel times for given addresses."""
    def get_travel_times(self, origin_address: str, destinations: List[str]) -> Dict[str, int]:
        # Simple deterministic function: travel time is 30 + length of destination name mod 60
        results = {}
        for dest in destinations:
            t = 30 + (len(dest) % 60)
            results[dest] = t
        return results
