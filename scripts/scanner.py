import pandas as pd
from datetime import datetime
import os

SENSITIVE_FIELDS = {
    "email": ("GDPR Article 6 – Consent required", "High"),
    "full_name": ("GDPR Article 5 – Data minimization", "Medium"),
    "ip_address": ("GDPR Recital 30 – Online identifiers", "Medium"),
    "date_of_birth": ("GDPR Article 5 – Storage limitation", "High"),
    "phone": ("GDPR Article 6 – Consent required", "High")
}

RETENTION_YEARS = 5


def scan_file(file_path):
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []

    report = []

    for column in df.columns:
        if column.lower() in SENSITIVE_FIELDS:
            gdpr_ref, severity = SENSITIVE_FIELDS[column.lower()]
            report.append({
                "field": column,
                "issue": "Contains sensitive personal data",
                "gdpr_reference": gdpr_ref,
                "severity": severity
            })

    if "consent_given" not in df.columns:
        report.append({
            "field": "consent_given",
            "issue": "Missing consent tracking field",
            "gdpr_reference": "GDPR Article 6 – Lawful basis for processing",
            "severity": "High"
        })
    else:
        missing_consent = df[df["consent_given"].fillna("FALSE").str.upper() != "TRUE"]
        if not missing_consent.empty:
            report.append({
                "field": "consent_given",
                "issue": f"{len(missing_consent)} record(s) missing or denied consent",
                "gdpr_reference": "GDPR Article 6 – Lawful basis for processing",
                "severity": "High"
            })

    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
        expired = df[df["created_at"] < pd.Timestamp.now() - pd.DateOffset(years=RETENTION_YEARS)]
        if not expired.empty:
            report.append({
                "field": "created_at",
                "issue": f"{len(expired)} record(s) exceed retention limit of {RETENTION_YEARS} years",
                "gdpr_reference": "GDPR Article 5 – Storage limitation",
                "severity": "Medium"
            })

    return report


def save_report(results):
    os.makedirs("../reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = f"../reports/compliance_report_{timestamp}.md"

    with open(report_path, "w") as f:
        f.write("# GDPR Compliance Report\n\n")
        f.write(f"Scan Timestamp: {datetime.now()}\n\n")
        f.write("## Issues Detected\n\n")

        if not results:
            f.write("No issues found.\n")
        else:
            for item in results:
                f.write(f"- Field: `{item['field']}`\n")
                f.write(f"  - Issue: {item['issue']}\n")
                f.write(f"  - Severity: {item['severity']}\n")
                f.write(f"  - GDPR Reference: {item['gdpr_reference']}\n\n")

    print(f"Report saved to: {report_path}")


def write_audit_log(file_path, result_count):
    os.makedirs("../logs", exist_ok=True)
    log_path = "../logs/audit_log.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_path, "a") as f:
        f.write(f"[{timestamp}] Scanned {file_path} – {result_count} issue(s) found\n")


if __name__ == "__main__":
    file_path = "/Users/kalyani/gdpr-compliance-tool/data/sample_data.csv"
    results = scan_file(file_path)

    print("\nGDPR Compliance Scan Results:")
    if not results:
        print("No issues found.")
    else:
        for item in results:
            print(f"- Field: {item['field']}")
            print(f"  Issue: {item['issue']}")
            print(f"  Severity: {item['severity']}")
            print(f"  GDPR Reference: {item['gdpr_reference']}\n")

    save_report(results)
    write_audit_log(file_path, len(results))

