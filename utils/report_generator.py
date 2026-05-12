import json
import os
from datetime import datetime


class ReportGenerator:

    def __init__(self, reports_dir="reports"):
        self.reports_dir = reports_dir
        os.makedirs(reports_dir, exist_ok=True)

    def generate_json_report(self, data, filename=None):
        """Genera un reporte en formato JSON."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"security_report_{timestamp}.json"

        filepath = os.path.join(self.reports_dir, filename)

        report = {
            "generated_at": datetime.now().isoformat(),
            "target": data.get("target", ""),
            "summary": data.get("summary", {}),
            "findings": data.get("findings", []),
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4, ensure_ascii=False)

        print(f"[REPORTE JSON]: Guardado en {filepath}")
        return filepath

    def generate_html_report(self, data, filename=None):
        """Genera un reporte HTML visual."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"security_report_{timestamp}.html"

        filepath = os.path.join(self.reports_dir, filename)
        findings = data.get("findings", [])
        target = data.get("target", "N/A")
        generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        high   = sum(1 for f in findings if f.get("risk") == "High")
        medium = sum(1 for f in findings if f.get("risk") == "Medium")
        low    = sum(1 for f in findings if f.get("risk") == "Low")
        info   = sum(1 for f in findings if f.get("risk") == "Informational")

        rows = ""
        for f in findings:
            risk = f.get("risk", "Info")
            color = {
                "High":          "#e74c3c",
                "Medium":        "#e67e22",
                "Low":           "#f1c40f",
                "Informational": "#3498db",
            }.get(risk, "#95a5a6")

            rows += f"""
            <tr>
                <td><span style="background:{color};color:white;
                    padding:3px 8px;border-radius:4px;
                    font-size:12px;">{risk}</span></td>
                <td>{f.get("name", "")}</td>
                <td><code>{f.get("url", "")}</code></td>
                <td>{f.get("description", "")}</td>
            </tr>"""

        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Security Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px;
               background: #f5f5f5; color: #333; }}
        h1   {{ color: #2c3e50; }}
        .meta  {{ color: #666; margin-bottom: 30px; }}
        .cards {{ display: flex; gap: 20px; margin-bottom: 30px; }}
        .card  {{ background: white; padding: 20px 30px;
                  border-radius: 8px; text-align: center;
                  box-shadow: 0 2px 6px rgba(0,0,0,.1); flex: 1; }}
        .card h2 {{ margin: 0 0 8px; font-size: 36px; }}
        .high   {{ color: #e74c3c; }}
        .medium {{ color: #e67e22; }}
        .low    {{ color: #f1c40f; }}
        .info   {{ color: #3498db; }}
        table  {{ width: 100%; border-collapse: collapse;
                  background: white; border-radius: 8px;
                  box-shadow: 0 2px 6px rgba(0,0,0,.1); overflow: hidden; }}
        th     {{ background: #2c3e50; color: white;
                  padding: 12px 16px; text-align: left; }}
        td     {{ padding: 12px 16px;
                  border-bottom: 1px solid #eee; }}
        tr:last-child td {{ border-bottom: none; }}
        tr:hover td {{ background: #f9f9f9; }}
    </style>
</head>
<body>
    <h1>🔒 Security Testing Report</h1>
    <div class="meta">
        <strong>Target:</strong> {target} &nbsp;|&nbsp;
        <strong>Generado:</strong> {generated_at}
    </div>

    <div class="cards">
        <div class="card"><h2 class="high">{high}</h2><p>High</p></div>
        <div class="card"><h2 class="medium">{medium}</h2><p>Medium</p></div>
        <div class="card"><h2 class="low">{low}</h2><p>Low</p></div>
        <div class="card"><h2 class="info">{info}</h2><p>Info</p></div>
    </div>

    <table>
        <thead>
            <tr>
                <th>Riesgo</th>
                <th>Vulnerabilidad</th>
                <th>URL</th>
                <th>Descripción</th>
            </tr>
        </thead>
        <tbody>{rows}</tbody>
    </table>
</body>
</html>"""

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"[REPORTE HTML]: Guardado en {filepath}")
        return filepath