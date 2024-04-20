from urllib.parse import urljoin


BASE_URL = "https://djinni.co/"

OCCUPATION = "Python"

VACANCIES_URL = urljoin(BASE_URL, f"jobs/?primary_keyword={OCCUPATION}")

COMPANY_TYPE = ["Product", "Outsource", "Outstaff", "Agency"]

WORKPLACE = ["Office або Remote", "Тільки віддалено", "Тільки офіс", "Гібридна робота"]

ENGLISH_LEVEL = [
    "Upper-Intermediate", "Intermediate", "Advanced/Fluent", "Pre-Intermediate", "Beginner/Elementary", "No English"
]

EXCLUSION_WORDS = [
    "Experience", "English", "Knowledge", "Strong", "Developer", "Responsibilities", "Requirements",
    "Develop", "Skills", "Familiarity", "Understanding", "Work", "Flexible", "Collaborate", "Team", "Paid",
    "Competitive", "Design", "Engineer", "Development", "Ability", "Excellent", "Software", "Working", "Proficiency",
    "Good", "Friendly", "Engineering", "Project", "Senior", "Ukraine", "Proven", "Technical", "Lead", "Computer",
    "Key", "DevOps", "Join", "Participate", "Data"
]