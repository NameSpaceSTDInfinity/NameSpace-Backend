from fpdf import FPDF
import json
import os

LOG_FILE = 'logs/conversations.json'

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Chat Logs', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

def generate_pdf(logs, filename):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)

    for log in logs:
        timestamp = log['timestamp']
        user_id = log['user_id']
        user_message = log['user_message']
        bot_response = log['bot_response']

        pdf.chapter_title(f"Timestamp: {timestamp} - User ID: {user_id}")
        pdf.chapter_body(f"User Message: {user_message}\n\nBot Response: {bot_response}\n\n")

    pdf.output(filename)

def fetch_logs_for_user(user_id):
    if not os.path.exists(LOG_FILE):
        return []

    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Filter logs by user_id
    filtered_logs = [entry for entry in data if entry['user_id'] == user_id]
    return filtered_logs
