"""
سكريبت إدخال البيانات - Ingest Dataset via API
يقرأ CSV ويرسل كل صف إلى /ingest لتعبئة Dashboard و Heatmap
"""
import csv
import requests
import os
import sys
import time

API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")
CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                         "data", "anonymized_sample_100.csv")
# Fallback to old file
if not os.path.exists(CSV_PATH):
    CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                             "data", "sample_responses.csv")


def ingest():
    print("═" * 60)
    print("  🛡️  بصير AI – إدخال البيانات التجريبية")
    print("  Basseer AI – Ingesting Sample Data")
    print("═" * 60)

    if not os.path.exists(CSV_PATH):
        print(f"\n❌ ملف البيانات غير موجود: {CSV_PATH}")
        print("   شغّل أولاً: python scripts/generate_dataset.py")
        sys.exit(1)

    # التحقق من الخادم
    try:
        r = requests.get(f"{API_URL}/", timeout=5)
        info = r.json()
        print(f"   الخادم: {info.get('name', 'OK')} | LLM: {info.get('llm_provider', '?')}")
    except Exception:
        print(f"\n❌ الخادم غير متاح على {API_URL}")
        print("   شغّل: uvicorn backend.main:app --port 8000")
        sys.exit(1)

    success, errors = 0, 0
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        total = len(rows)

        for i, row in enumerate(rows, 1):
            try:
                payload = {
                    "record": {
                        "age": int(row["age"]),
                        "experience_years": int(row["experience_years"]),
                        "education": row["education"].strip(),
                        "job_title": row["job_title"].strip(),
                        "income": float(row["income"]),
                        "region": row["region"].strip(),
                        "employment_status": row["employment_status"].strip(),
                        "enumerator_id": row.get("enumerator_id", "default").strip(),
                    }
                }
                resp = requests.post(f"{API_URL}/ingest", json=payload, timeout=30)
                result = resp.json()

                score = result.get("confidence_score", "?")
                warns = result.get("contradictions_count", 0)
                llm = "🤖" if result.get("llm_used") else "📏"
                lat = result.get("latency_ms", 0)
                icon = "✅" if warns == 0 else f"⚠️ ({warns})"

                print(f"  [{i:03d}/{total}] {llm} العمر={int(row['age']):3d} | "
                      f"الخبرة={int(row['experience_years']):2d} | "
                      f"الثقة={score:5.1f} | {lat:6.1f}ms | {icon}")
                success += 1
            except Exception as e:
                print(f"  [{i:03d}/{total}] ❌ {e}")
                errors += 1
            time.sleep(0.02)

    print(f"\n{'═' * 60}")
    print(f"  ✅ {success} نجاح | ❌ {errors} خطأ | المجموع {total}")

    try:
        stats = requests.get(f"{API_URL}/stats").json()
        print(f"\n  📊 إجمالي: {stats['total_responses']} | "
              f"⚠️ تناقضات: {stats['total_contradictions']} | "
              f"📈 ثقة: {stats['average_confidence_score']} | "
              f"⏱️ زمن: {stats['average_latency_ms']}ms")
        print(f"  🔴 أكثر حقل: {stats['top_problematic_field']} | "
              f"📍 أكثر منطقة: {stats['top_problematic_region']}")
    except Exception:
        pass
    print("═" * 60)


if __name__ == "__main__":
    ingest()
