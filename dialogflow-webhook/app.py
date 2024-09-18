from flask import Flask, request, jsonify, send_file
from storage import save_log_entry
from pdf_generator import fetch_logs_for_user, generate_pdf
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    user_message = req['queryResult']['queryText']
    bot_response = req['queryResult']['fulfillmentText']
    user_id = req['originalDetectIntentRequest']['payload'].get('userId', 'anonymous')

    # Store the conversation in local storage
    save_log_entry(user_id, user_message, bot_response)

    return jsonify({'fulfillmentText': bot_response})

@app.route('/export-pdf', methods=['GET'])
def export_pdf():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    logs = fetch_logs_for_user(user_id)
    if not logs:
        return jsonify({'error': 'No logs found for the given user_id'}), 404

    pdf_filename = f'{user_id}_chat_logs.pdf'
    generate_pdf(logs, pdf_filename)

    return send_file(pdf_filename, as_attachment=True, mimetype='application/pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
