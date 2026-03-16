#!/usr/bin/env python3
"""
Generate job application report for a specific date range.

Usage:
    python generate-date-range-report.py
"""

import csv
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
CSV_FILE = SCRIPT_DIR / "applications.csv"

def parse_date(date_str):
    """Parse date string, return None if invalid."""
    if not date_str or date_str.startswith('status:') or date_str == 'Unknown':
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None

def generate_report(start_date_str, end_date_str):
    """Generate report for applications in date range."""
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

    applications = []

    with open(CSV_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            date_applied = parse_date(row['Date Applied'])
            if date_applied and start_date <= date_applied <= end_date:
                applications.append(row)

    # Sort by date applied
    applications.sort(key=lambda x: parse_date(x['Date Applied']))

    # Generate report
    print(f"\n{'='*80}")
    print(f"JOB APPLICATIONS SUBMITTED: {start_date_str} through {end_date_str}")
    print(f"{'='*80}\n")

    if not applications:
        print("No applications submitted during this period.\n")
        return

    print(f"Total Applications: {len(applications)}\n")

    for i, app in enumerate(applications, 1):
        print(f"{i}. {app['Company']} — {app['Role']}")
        print(f"   Date Applied: {app['Date Applied']}")
        print(f"   Location: {app['Location']}")
        print(f"   Status: {app['Status']}")
        if app['Fit Score']:
            print(f"   Fit Score: {app['Fit Score']}")
        if app['Source URL'] and not app['Source URL'].startswith('status:'):
            print(f"   Source: {app['Source URL']}")
        print(f"   Directory: jobs/{app['Directory']}/")
        print()

    # Summary by date
    print(f"\n{'-'*80}")
    print("SUMMARY BY DATE")
    print(f"{'-'*80}\n")

    by_date = {}
    for app in applications:
        date = app['Date Applied']
        if date not in by_date:
            by_date[date] = []
        by_date[date].append(app)

    for date in sorted(by_date.keys()):
        apps = by_date[date]
        print(f"{date} ({len(apps)} application{'s' if len(apps) > 1 else ''}):")
        for app in apps:
            print(f"  • {app['Company']} — {app['Role']}")
        print()

if __name__ == "__main__":
    generate_report("2026-03-08", "2026-03-13")
