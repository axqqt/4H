from flask import Flask, request, jsonify
from plyer import notification
import threading

app = Flask(__name__)

# Function to display a desktop notification
def show_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=10  # Notification stays visible for 10 seconds
    )

@app.route('/webhook', methods=['POST'])
def webhook():
    # Extract data from the TradingView webhook payload
    data = request.json
    pair = data.get('pair', 'Unknown Pair')
    alert_message = data.get('message', 'No message provided')

    # Display a desktop notification
    threading.Thread(target=show_notification, args=(f"Alert for {pair}", alert_message)).start()

    # Respond to TradingView to acknowledge receipt of the alert
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    # Run the Flask server on localhost at port 5000
    app.run(host='0.0.0.0', port=5000)