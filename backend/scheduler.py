# scheduler.py
import schedule
from scraper import fetch_companies
from agent import create_analysis_tasks

schedule.every(6).hours.do(fetch_companies)
schedule.every(1).days.do(create_analysis_tasks)
schedule.every().sunday.do(run_trend_detection)