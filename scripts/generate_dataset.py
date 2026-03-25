"""
مولّد البيانات التجريبية - Deterministic Dataset Generator
ينتج 100 سجل متنوع مع أخطاء منطقية وتعارضات دلالية مقصودة
"""
import csv
import random
import os

SEED = 42
OUTPUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "data", "anonymized_sample_100.csv")

REGIONS = ["الرياض", "جدة", "الدمام", "مكة", "المدينة", "أبها", "تبوك", "حائل"]
EDUCATIONS = ["High School", "Diploma", "Bachelor", "Master", "PhD"]
STATUSES = ["Full-time", "Part-time", "عاطل", "Student", "Self-employed"]
ENUMERATORS = [f"EN-{i:03d}" for i in range(1, 11)]

JOBS_BY_EDU = {
    "High School": ["Cashier", "Driver", "Security Guard", "Clerk", "Worker"],
    "Diploma": ["Technician", "Assistant", "Nurse", "Clerk"],
    "Bachelor": ["Software Developer", "Accountant", "Teacher", "Designer", "Analyst", "Marketing Specialist"],
    "Master": ["Senior Engineer", "Project Manager", "Consultant", "Researcher"],
    "PhD": ["Professor", "Scientist", "Director", "Senior Researcher"],
}

INCOME_RANGES = {
    "High School": (3000, 8000), "Diploma": (5000, 12000),
    "Bachelor": (8000, 25000), "Master": (15000, 40000), "PhD": (25000, 60000),
}

EDU_MIN_AGE = {"High School": 18, "Diploma": 19, "Bachelor": 22, "Master": 24, "PhD": 27}


def generate():
    rng = random.Random(SEED)
    rows = []

    for i in range(100):
        # 60% نظيفة، 40% بأخطاء
        inject_error = rng.random() < 0.40
        error_type = rng.choice(["exp_age", "edu_age", "income_job", "emp_income",
                                  "edu_job", "multi"]) if inject_error else None

        edu = rng.choice(EDUCATIONS)
        min_age = EDU_MIN_AGE[edu]
        age = rng.randint(min_age, min_age + 30)
        max_exp = max(0, age - 18)
        exp = rng.randint(0, max_exp)
        job = rng.choice(JOBS_BY_EDU[edu])
        lo, hi = INCOME_RANGES[edu]
        income = rng.randint(lo, hi)
        status = rng.choices(["Full-time", "Part-time", "Self-employed"], weights=[70, 15, 15])[0]
        region = rng.choice(REGIONS)
        enum_id = rng.choice(ENUMERATORS)

        # حقن الأخطاء
        if error_type == "exp_age":
            exp = age - 5 + rng.randint(5, 15)  # خبرة أكثر من الممكن
        elif error_type == "edu_age":
            age = rng.randint(15, min_age - 1)  # عمر أصغر من المتوقع للشهادة
        elif error_type == "income_job":
            if "Cashier" in job or "Intern" in job or "Student" in job:
                income = rng.randint(40000, 90000)  # دخل عالي لوظيفة بسيطة
            else:
                job = rng.choice(["CEO", "Director", "مدير عام"])
                income = rng.randint(1000, 3000)  # دخل منخفض لوظيفة عليا
        elif error_type == "emp_income":
            status = "عاطل"
            income = rng.randint(30000, 80000)  # عاطل بدخل عالي
        elif error_type == "edu_job":
            edu = rng.choice(["High School", "Diploma"])
            job = rng.choice(["Doctor", "Lawyer", "Professor", "Surgeon"])
        elif error_type == "multi":
            age = rng.randint(17, 20)
            exp = rng.randint(10, 20)
            edu = "PhD"
            job = rng.choice(["Doctor", "Professor"])
            income = rng.randint(60000, 100000)

        rows.append({
            "age": age, "experience_years": exp, "education": edu,
            "job_title": job, "income": income, "region": region,
            "employment_status": status, "enumerator_id": enum_id,
        })

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "age", "experience_years", "education", "job_title",
            "income", "region", "employment_status", "enumerator_id"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ تم إنشاء {len(rows)} سجل → {OUTPUT}")
    error_count = sum(1 for r in rows if True)  # all rows
    clean = sum(1 for i, r in enumerate(rows) if random.Random(SEED).random() >= 0.40
                or i >= 100)
    print(f"   ~60 سجل نظيف + ~40 سجل بأخطاء مقصودة")


if __name__ == "__main__":
    generate()
