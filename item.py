from dataclasses import dataclass, fields
from datetime import datetime


@dataclass
class Vacancy:
    date: datetime
    title: str
    location: str
    job_info: list[str]
    description: str
    views: int
    responses: int
    salary: str | None


VACANCY_FIELDS = [field.name for field in fields(Vacancy)]
