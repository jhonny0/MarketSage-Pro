from __future__ import annotations

from pathlib import Path
from typing import Dict

from jinja2 import Template
from weasyprint import HTML


def render_pdf_report(metrics: Dict, out_path: str = "reports/daily_report.pdf") -> str:
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    html = Template(
        """
        <html>
          <body>
            <h1>MarketSage-Pro Daily Report</h1>
            <ul>
            {% for k, v in metrics.items() %}
              <li><b>{{k}}</b>: {{v}}</li>
            {% endfor %}
            </ul>
          </body>
        </html>
        """
    ).render(metrics=metrics)
    HTML(string=html).write_pdf(out_path)
    return out_path