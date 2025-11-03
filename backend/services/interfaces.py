from typing import List, Dict

class RakutenGoraService:
    """Interface for Rakuten Gora service."""
    def search_plans(self, area_code: int, play_date: str, min_price: int = None, max_price: int = None, start_time_zone: int = None) -> List[Dict]:
        """Return a list of plan dicts. Each dict should contain keys like course_name, plan_name, price, address, play_date, start_time."""
        raise NotImplementedError()


class GoogleMapsService:
    """Interface for Google Maps Distance Matrix service."""
    def get_travel_times(self, origin_address: str, destinations: List[str]) -> Dict[str, int]:
        """Return a mapping destination_address -> travel_time_in_minutes."""
        raise NotImplementedError()
