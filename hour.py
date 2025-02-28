from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Initialize Flask app
app = Flask(__name__)

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "dulransamarasinghe3@gmail.com"  # Replace with your email
EMAIL_PASSWORD = "Zigzaggoofyman2005lol"  # Replace with your email password
RECIPIENT_EMAIL = "dulransamarasinghe4@gmail.com"  # Replace with recipient email

def send_email(subject, body):
    try:
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Parse incoming JSON data
        data = request.json
        symbol = data.get("symbol", "Unknown Symbol")
        price = data.get("price", "Unknown Price")
        condition = data.get("condition", "Unknown Condition")

        # Prepare email content
        subject = f"TradingView Alert: {symbol}"
        body = f"""
        Symbol: {symbol}
        Price: {price}
        Condition: {condition}
        """

        # Send the email
        send_email(subject, body)

        return jsonify({"status": "success", "message": "Alert received and email sent."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)