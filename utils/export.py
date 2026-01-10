"""
Export functionality for reports (CSV and PDF)
"""
import pandas as pd
from io import BytesIO
from datetime import datetime
from typing import Dict, List, Any, Optional
from fpdf import FPDF
import base64


class PDFReport(FPDF):
    """Custom PDF report generator"""

    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(0, 120, 212)
        self.cell(0, 10, 'Sports Prediction Platform', border=0, ln=True, align='C')
        self.set_font('Helvetica', '', 10)
        self.set_text_color(128, 128, 128)
        self.cell(0, 5, f'Report Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                  border=0, ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', border=0, align='C')

    def add_section_title(self, title: str):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(0, 0, 0)
        self.ln(5)
        self.cell(0, 10, title, border=0, ln=True)
        self.set_draw_color(0, 120, 212)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def add_prediction_card(
        self,
        home_team: str,
        away_team: str,
        home_prob: float,
        confidence: float,
        game_time: str
    ):
        self.set_font('Helvetica', '', 11)
        self.set_text_color(0, 0, 0)

        # Card background
        self.set_fill_color(245, 245, 245)
        y_start = self.get_y()
        self.rect(10, y_start, 190, 35, 'F')

        # Teams
        self.set_xy(15, y_start + 5)
        self.set_font('Helvetica', 'B', 12)
        self.cell(80, 8, f"{home_team} vs {away_team}", ln=False)

        # Game time
        self.set_font('Helvetica', '', 10)
        self.set_text_color(128, 128, 128)
        self.cell(0, 8, game_time, ln=True, align='R')

        # Probabilities
        self.set_xy(15, y_start + 18)
        self.set_font('Helvetica', '', 10)
        self.set_text_color(0, 0, 0)
        self.cell(50, 6, f"Home Win: {home_prob*100:.1f}%", ln=False)
        self.cell(50, 6, f"Away Win: {(1-home_prob)*100:.1f}%", ln=False)

        # Confidence
        if confidence >= 0.6:
            self.set_text_color(76, 175, 80)
        elif confidence >= 0.55:
            self.set_text_color(255, 152, 0)
        else:
            self.set_text_color(244, 67, 54)
        self.cell(0, 6, f"Confidence: {confidence*100:.1f}%", ln=True, align='R')

        self.ln(15)

    def add_table(self, headers: List[str], data: List[List[Any]], col_widths: Optional[List[int]] = None):
        """Add a table to the PDF"""
        if col_widths is None:
            col_widths = [190 // len(headers)] * len(headers)

        # Header row
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(0, 120, 212)
        self.set_text_color(255, 255, 255)
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 8, str(header), border=1, fill=True, align='C')
        self.ln()

        # Data rows
        self.set_font('Helvetica', '', 9)
        self.set_text_color(0, 0, 0)
        fill = False
        for row in data:
            self.set_fill_color(245, 245, 245) if fill else self.set_fill_color(255, 255, 255)
            for i, cell in enumerate(row):
                self.cell(col_widths[i], 7, str(cell), border=1, fill=True, align='C')
            self.ln()
            fill = not fill

    def add_stats_summary(self, stats: Dict[str, Any]):
        """Add statistics summary"""
        self.set_font('Helvetica', '', 10)
        self.set_text_color(0, 0, 0)

        for key, value in stats.items():
            self.cell(60, 6, f"{key}:", ln=False)
            self.set_font('Helvetica', 'B', 10)
            self.cell(0, 6, str(value), ln=True)
            self.set_font('Helvetica', '', 10)


def export_predictions_to_csv(predictions: List[Dict]) -> bytes:
    """Export predictions data to CSV format"""
    df = pd.DataFrame(predictions)
    return df.to_csv(index=False).encode('utf-8')


def export_predictions_to_pdf(
    predictions: List[Dict],
    sport: str,
    date: str
) -> bytes:
    """Export predictions to PDF format"""
    pdf = PDFReport()
    pdf.add_page()

    # Title
    pdf.add_section_title(f"{sport} Predictions - {date}")

    # Add each prediction
    for pred in predictions:
        pdf.add_prediction_card(
            home_team=pred.get('home_team', 'Home'),
            away_team=pred.get('away_team', 'Away'),
            home_prob=pred.get('home_win_prob', 0.5),
            confidence=pred.get('confidence', 0.5),
            game_time=pred.get('game_time', 'TBD')
        )

    return bytes(pdf.output())


def export_backtest_report(
    results: Dict[str, Any],
    sport: str,
    date_range: str
) -> bytes:
    """Export backtest results to PDF"""
    pdf = PDFReport()
    pdf.add_page()

    # Title
    pdf.add_section_title(f"Backtest Report - {sport}")
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 6, f"Date Range: {date_range}", ln=True)
    pdf.ln(5)

    # Summary stats
    pdf.add_section_title("Performance Summary")
    stats = {
        "Total Games": results.get('total_games', 0),
        "Correct Predictions": results.get('correct', 0),
        "Accuracy": f"{results.get('accuracy', 0)*100:.2f}%",
        "ROC-AUC": f"{results.get('roc_auc', 0):.4f}",
        "Sharpe Ratio": f"{results.get('sharpe_ratio', 0):.2f}",
        "Max Drawdown": f"{results.get('max_drawdown', 0)*100:.2f}%"
    }
    pdf.add_stats_summary(stats)

    # Detailed results table
    if 'detailed_results' in results:
        pdf.add_page()
        pdf.add_section_title("Detailed Results")
        headers = ['Date', 'Game', 'Predicted', 'Actual', 'Confidence']
        data = [
            [r['date'], r['game'], r['predicted'], r['actual'], f"{r['confidence']*100:.1f}%"]
            for r in results['detailed_results'][:50]  # Limit to 50 rows
        ]
        pdf.add_table(headers, data, col_widths=[25, 70, 30, 30, 30])

    return bytes(pdf.output())


def export_model_performance_report(
    models: List[Dict[str, Any]],
    sport: str
) -> bytes:
    """Export model performance comparison to PDF"""
    pdf = PDFReport()
    pdf.add_page()

    pdf.add_section_title(f"Model Performance Report - {sport}")

    # Model comparison table
    headers = ['Model', 'Accuracy', 'ROC-AUC', 'Weight', 'Status']
    data = [
        [
            m['name'],
            f"{m.get('accuracy', 0)*100:.2f}%",
            f"{m.get('roc_auc', 0):.4f}",
            f"{m.get('weight', 0)*100:.0f}%",
            m.get('status', 'Active')
        ]
        for m in models
    ]
    pdf.add_table(headers, data, col_widths=[50, 35, 35, 30, 35])

    return bytes(pdf.output())


def create_download_link(data: bytes, filename: str, file_type: str = "csv") -> str:
    """Create a download link for the exported data"""
    b64 = base64.b64encode(data).decode()
    mime_types = {
        "csv": "text/csv",
        "pdf": "application/pdf",
        "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    }
    mime = mime_types.get(file_type, "application/octet-stream")
    return f'<a href="data:{mime};base64,{b64}" download="{filename}" style="text-decoration: none; color: #0078D4; font-weight: 500;">📥 Download {filename}</a>'


def export_dataframe_to_excel(df: pd.DataFrame, sheet_name: str = "Data") -> bytes:
    """Export DataFrame to Excel format"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
    return output.getvalue()
