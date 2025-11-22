from dataclasses import dataclass
from typing import Optional, List
from datetime import date

@dataclass
class GolfCourse:
    course_id: str
    course_name: str
    plan_name: str
    price: int
    address: str
    play_date: str
    start_time: str
    travel_time: Optional[int] = None

@dataclass
class SearchResult:
    results: List[GolfCourse]
    total_count: int
    search_time: str
