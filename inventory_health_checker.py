import argparse
import csv
import json
from datetime import datetime
from pathlib import Path

JSON_DATA_FILE = Path("data/asset_inventory.json")
CSV_DATA_FILE = Path("data/asset_inventory.csv")

REPORT_TXT_FILE = Path("reports/database_health_report.txt")
REPORT_JSON_FILE = Path("reports/database_health_report.json")
REPORT_CSV_FILE = Path("reports/database_health_report.csv")

ALERT_FILE = Path("alerts/high_risk_alerts.txt")
LOG_FILE = Path("logs/inventory_events.log")

STALE_CHECK_DAYS = 30


def load_inventory_json():
    with JSON_DATA_FILE.open("r", encoding="utf-8-sig") as file:
        return json.load(file)


def load_inventory_csv():
    assets = []

    with CSV_DATA_FILE.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            assets.append(
                {
                    "asset_id": row["asset_id"],
                    "asset_name": row["asset_name"],
                    "asset_type": row["asset_type"],
                    "owner": row["owner"],
                    "status": row["status"],
                    "last_checked_days": int(row["last_checked_days"]),
                }
            )

    return assets


def log_event(asset_id, event_type, message, environment):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with LOG_FILE.open("a", encoding="utf-8") as log:
        log.write(
            f"{datetime.now().isoformat(timespec='seconds')} | "
            f"{environment.upper()} | {event_type} | {asset_id} | {message}\n"
        )


def calculate_risk_score(findings, asset):
    score = 0

    if "Missing asset owner" in findings:
        score += 4

    if "Asset is not active" in findings:
        score += 5

    if "Asset health check is overdue" in findings:
        score += 4

    if asset["asset_type"].lower() in ["database", "api"]:
        score += 1

    return score


def classify_risk(score):
    if score >= 8:
        return "HIGH"

    if score >= 4:
        return "MEDIUM"

    return "LOW"


def generate_recommendation(risk_level):
    if risk_level == "HIGH":
        return "Immediate operational review required. Assign ownership, verify status, and update health records."

    if risk_level == "MEDIUM":
        return "Schedule follow-up review and update missing or stale inventory data."

    return "No immediate action required. Continue routine inventory monitoring."


def evaluate_asset(asset, environment):
    findings = []

    if not asset.get("owner"):
        findings.append("Missing asset owner")

    if asset["status"].lower() != "active":
        findings.append("Asset is not active")

    if asset["last_checked_days"] > STALE_CHECK_DAYS:
        findings.append("Asset health check is overdue")

    risk_score = calculate_risk_score(findings, asset)
    risk_level = classify_risk(risk_score)
    recommendation = generate_recommendation(risk_level)

    if risk_level == "HIGH":
        log_event(asset["asset_id"], "ALERT", "High-risk asset requires immediate review", environment)
    elif risk_level == "MEDIUM":
        log_event(asset["asset_id"], "REVIEW", "Asset requires scheduled follow-up", environment)
    else:
        log_event(asset["asset_id"], "AUDIT", "Asset passed inventory health checks", environment)

    return {
        "asset_id": asset["asset_id"],
        "asset_name": asset["asset_name"],
        "asset_type": asset["asset_type"],
        "owner": asset["owner"] if asset["owner"] else "UNASSIGNED",
        "status": asset["status"],
        "last_checked_days": asset["last_checked_days"],
        "findings": findings,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "recommendation": recommendation,
    }


def analyze_inventory(inventory, environment):
    if LOG_FILE.exists():
        LOG_FILE.unlink()

    return [evaluate_asset(asset, environment) for asset in inventory]


def generate_text_report(results, environment, source):
    REPORT_TXT_FILE.parent.mkdir(parents=True, exist_ok=True)

    total = len(results)
    high_risk = sum(1 for item in results if item["risk_level"] == "HIGH")
    medium_risk = sum(1 for item in results if item["risk_level"] == "MEDIUM")
    low_risk = sum(1 for item in results if item["risk_level"] == "LOW")
    overdue = sum(1 for item in results if item["last_checked_days"] > STALE_CHECK_DAYS)
    unassigned = sum(1 for item in results if item["owner"] == "UNASSIGNED")

    lines = [
        "Cloud Asset Governance And Health Monitoring Report",
        "=" * 62,
        f"Environment: {environment.upper()}",
        f"Source: {source.upper()}",
        f"Total Assets Reviewed: {total}",
        f"High Risk Assets: {high_risk}",
        f"Medium Risk Assets: {medium_risk}",
        f"Low Risk Assets: {low_risk}",
        f"Overdue Health Checks: {overdue}",
        f"Unassigned Assets: {unassigned}",
        "",
    ]

    for item in results:
        lines.append(f"Asset ID: {item['asset_id']}")
        lines.append(f"Asset Name: {item['asset_name']}")
        lines.append(f"Asset Type: {item['asset_type']}")
        lines.append(f"Owner: {item['owner']}")
        lines.append(f"Status: {item['status']}")
        lines.append(f"Last Checked: {item['last_checked_days']} days ago")
        lines.append(f"Risk Score: {item['risk_score']}")
        lines.append(f"Risk Level: {item['risk_level']}")

        if item["findings"]:
            lines.append("Findings:")
            for finding in item["findings"]:
                lines.append(f"- {finding}")
        else:
            lines.append("Findings: No major issues detected")

        lines.append("Recommended Action:")
        lines.append(f"- {item['recommendation']}")
        lines.append("-" * 62)

    REPORT_TXT_FILE.write_text("\n".join(lines), encoding="utf-8")


def export_json_report(results, environment, source):
    REPORT_JSON_FILE.parent.mkdir(parents=True, exist_ok=True)

    output = {
        "environment": environment.upper(),
        "source": source.upper(),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "results": results,
    }

    REPORT_JSON_FILE.write_text(json.dumps(output, indent=2), encoding="utf-8")


def export_csv_report(results):
    REPORT_CSV_FILE.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "asset_id",
        "asset_name",
        "asset_type",
        "owner",
        "status",
        "last_checked_days",
        "risk_score",
        "risk_level",
        "recommendation",
    ]

    with REPORT_CSV_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for item in results:
            writer.writerow(
                {
                    "asset_id": item["asset_id"],
                    "asset_name": item["asset_name"],
                    "asset_type": item["asset_type"],
                    "owner": item["owner"],
                    "status": item["status"],
                    "last_checked_days": item["last_checked_days"],
                    "risk_score": item["risk_score"],
                    "risk_level": item["risk_level"],
                    "recommendation": item["recommendation"],
                }
            )


def write_high_risk_alerts(results, environment):
    ALERT_FILE.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "High Risk Asset Alerts",
        "=" * 30,
        f"Environment: {environment.upper()}",
        "",
    ]

    high_risk_items = [item for item in results if item["risk_level"] == "HIGH"]

    if not high_risk_items:
        lines.append("No high-risk assets detected.")
    else:
        for item in high_risk_items:
            lines.append(
                f"{item['asset_id']} | {item['asset_name']} | {item['risk_level']} | {item['recommendation']}"
            )

    ALERT_FILE.write_text("\n".join(lines), encoding="utf-8")


def print_api_response(results, environment, source):
    response = {
        "service": "cloud-asset-health-api",
        "environment": environment.upper(),
        "source": source.upper(),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "asset_count": len(results),
        "high_risk_count": sum(1 for item in results if item["risk_level"] == "HIGH"),
        "results": results,
    }

    print(json.dumps(response, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Cloud Asset Governance And Health Monitoring System")
    parser.add_argument("--env", default="dev", help="Environment name, for example dev, test, or prod")
    parser.add_argument("--source", choices=["json", "csv"], default="json", help="Inventory input source")
    parser.add_argument("--export-json", action="store_true", help="Export machine-readable JSON report")
    parser.add_argument("--export-csv", action="store_true", help="Export CSV report for operations teams")
    parser.add_argument("--api-output", action="store_true", help="Print API-style JSON response to console")

    args = parser.parse_args()

    if args.source == "json":
        inventory = load_inventory_json()
    else:
        inventory = load_inventory_csv()

    results = analyze_inventory(inventory, args.env)

    generate_text_report(results, args.env, args.source)
    write_high_risk_alerts(results, args.env)

    if args.export_json:
        export_json_report(results, args.env, args.source)

    if args.export_csv:
        export_csv_report(results)

    if args.api_output:
        print_api_response(results, args.env, args.source)
    else:
        print("Cloud Asset Governance And Health Monitoring System")
        print("=" * 62)
        print("Asset governance and health monitoring completed successfully.")
        print(f"Environment: {args.env.upper()}")
        print(f"Source: {args.source.upper()}")
        print(f"Text report created: {REPORT_TXT_FILE}")
        print(f"Alert file created: {ALERT_FILE}")

        if args.export_json:
            print(f"JSON report created: {REPORT_JSON_FILE}")

        if args.export_csv:
            print(f"CSV report created: {REPORT_CSV_FILE}")

        print(f"Event log updated: {LOG_FILE}")
        print("")
        print(REPORT_TXT_FILE.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
