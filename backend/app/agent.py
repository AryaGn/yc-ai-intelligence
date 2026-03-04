import time
from sqlalchemy import text
from app.database import SessionLocal
from app.tasks import get_pending_tasks, complete_task
from app.llm import analyze_company, score_company


def run_agent():
    while True:
        tasks = get_pending_tasks()

        for task in tasks:

            # ==================================================
            # 1️⃣ ANALYZE COMPANY
            # ==================================================
            if task["task_type"] == "ANALYZE_COMPANY":

                company_id = task["input_payload"]["company_id"]

                db = SessionLocal()

                company = db.execute(text("""
                    SELECT name, domain
                    FROM companies
                    WHERE id=:id
                """), {"id": company_id}).fetchone()

                if not company:
                    db.close()
                    continue

                analysis = analyze_company({
                    "name": company.name,
                    "domain": company.domain
                })

                scores = score_company({
                    "name": company.name,
                    "domain": company.domain
                })

                # Insert SUMMARY
                db.execute(text("""
                    INSERT INTO ai_insights (
                        company_id, insight_type, insight_text,
                        confidence_score, model_name, prompt_version
                    )
                    VALUES (
                        :cid, 'SUMMARY', :text,
                        0.9, 'mock-model', 'v2'
                    )
                """), {
                    "cid": company_id,
                    "text": analysis
                })

                # Insert GROWTH
                db.execute(text("""
                    INSERT INTO ai_insights (
                        company_id, insight_type, insight_text,
                        confidence_score, model_name, prompt_version
                    )
                    VALUES (
                        :cid, 'GROWTH', :text,
                        0.85, 'mock-model', 'v2'
                    )
                """), {
                    "cid": company_id,
                    "text": f"Growth Score: {scores['growth_score']}\n{scores['explanation']}"
                })

                # Insert RISK
                db.execute(text("""
                    INSERT INTO ai_insights (
                        company_id, insight_type, insight_text,
                        confidence_score, model_name, prompt_version
                    )
                    VALUES (
                        :cid, 'RISK', :text,
                        0.85, 'mock-model', 'v2'
                    )
                """), {
                    "cid": company_id,
                    "text": f"Risk Score: {scores['risk_score']}\n{scores['explanation']}"
                })

                # Insert INNOVATION
                db.execute(text("""
                    INSERT INTO ai_insights (
                        company_id, insight_type, insight_text,
                        confidence_score, model_name, prompt_version
                    )
                    VALUES (
                        :cid, 'INNOVATION', :text,
                        0.9, 'mock-model', 'v2'
                    )
                """), {
                    "cid": company_id,
                    "text": f"Innovation Score: {scores['innovation_score']}\n{scores['explanation']}"
                })

                db.commit()
                db.close()

                complete_task(task["id"], {"status": "done"})

            # ==================================================
            # 2️⃣ TREND DETECTION (NEW)
            # ==================================================
            if task["task_type"] == "DETECT_TREND":

                db = SessionLocal()

                domain_counts = db.execute(text("""
                    SELECT domain, COUNT(*) as count
                    FROM companies
                    GROUP BY domain
                    ORDER BY count DESC
                    LIMIT 5
                """)).fetchall()

                if not domain_counts:
                    db.close()
                    complete_task(task["id"], {"status": "no_data"})
                    continue

                trend_text = "Emerging domain clusters detected:\n\n"

                for row in domain_counts:
                    trend_text += f"{row.domain} → {row.count} companies\n"

                db.execute(text("""
                    INSERT INTO ai_insights (
                        company_id,
                        insight_type,
                        insight_text,
                        confidence_score,
                        model_name,
                        prompt_version
                    )
                    VALUES (
                        NULL,
                        'TREND',
                        :text,
                        0.88,
                        'mock-model',
                        'trend-v1'
                    )
                """), {
                    "text": trend_text
                })

                db.commit()
                db.close()

                complete_task(task["id"], {"status": "done"})

        # ==================================================
        # 3️⃣ SNAPSHOT ANOMALY DETECTION
        # ==================================================
            if task["task_type"] == "CHECK_ANOMALY":

                company_id = task["input_payload"]["company_id"]

                db = SessionLocal()

                snapshots = db.execute(text("""
                    SELECT id, snapshot_hash, raw_data, scraped_at
                    FROM company_snapshots
                    WHERE company_id = :cid
                    ORDER BY scraped_at DESC
                    LIMIT 2
                """), {"cid": company_id}).fetchall()

                if len(snapshots) < 2:
                    db.close()
                    complete_task(task["id"], {"status": "not_enough_data"})
                    continue

                latest = snapshots[0]
                previous = snapshots[1]

                if latest.snapshot_hash != previous.snapshot_hash:

                    anomaly_text = f"""
Change detected for company {company_id}.

Previous snapshot hash: {previous.snapshot_hash}
Latest snapshot hash: {latest.snapshot_hash}

This indicates significant data update.
"""

                    db.execute(text("""
                        INSERT INTO ai_insights (
                            company_id,
                            insight_type,
                            insight_text,
                            confidence_score,
                            model_name,
                            prompt_version
                        )
                        VALUES (
                            :cid,
                            'ANOMALY',
                            :text,
                            0.92,
                            'mock-model',
                            'anomaly-v1'
                        )
                    """), {
                        "cid": company_id,
                        "text": anomaly_text
                    })

                    # Automatically trigger re-analysis
                    db.execute(text("""
                        INSERT INTO ai_tasks (task_type, status, input_payload)
                        VALUES (
                            'ANALYZE_COMPANY',
                            'PENDING',
                            :payload
                        )
                    """), {
                        "payload": f'{{"company_id": {company_id}}}'
                    })

                    db.commit()

                db.close()
                complete_task(task["id"], {"status": "done"})

        time.sleep(5)