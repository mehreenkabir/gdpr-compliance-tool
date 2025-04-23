# GDPR Compliance Automation Tool

This project is a Python-based data scanner designed to automatically identify and report potential violations of the General Data Protection Regulation (GDPR) in structured datasets.

## Features

- **Sensitive Field Detection**: Flags fields containing personally identifiable information (PII), such as email addresses, IP addresses, names, and dates of birth.
- **Consent Validation**: Verifies the existence of a `consent_given` field and checks if consent is missing or denied.
- **Retention Policy Check**: Identifies records that exceed a defined data retention threshold.
- **Risk Scoring**: Assigns a severity level (High, Medium, Low) to each compliance issue.
- **Markdown Report Generation**: Outputs a compliance report with timestamped details.
- **Audit Logging**: Logs each scan operation with timestamp and issue count for traceability.

## Usage

1. Place your dataset as a CSV file in the `data/` directory.
2. Modify the `file_path` in `scanner.py` to point to your CSV file.
3. Activate your Python environment and install dependencies:

```bash
pip install pandas
```

4. Run the scanner:

```bash
python scripts/scanner.py
```

5. Check the following:
   - Terminal output for a live scan summary
   - `reports/` directory for Markdown reports
   - `logs/audit_log.txt` for audit trail entries

## Project Structure

```
gdpr-compliance-tool/
├── scripts/
│   └── scanner.py
├── data/
│   └── sample_data.csv
├── reports/
│   └── compliance_report_*.md
├── logs/
│   └── audit_log.txt
├── requirements.txt
└── README.md
```

## Example Output

```
GDPR Compliance Scan Results:
- Field: email
  Issue: Contains sensitive personal data
  Severity: High
  GDPR Reference: GDPR Article 6 – Consent required

- Field: created_at
  Issue: 3 record(s) exceed retention limit of 5 years
  Severity: Medium
  GDPR Reference: GDPR Article 5 – Storage limitation
```

## Why It Matters

This project bridges the gap between legal privacy frameworks and real-world data handling by providing:
- Scalable compliance checks
- Developer-friendly privacy reporting
- Audit-readiness through automation

## License
MIT License

