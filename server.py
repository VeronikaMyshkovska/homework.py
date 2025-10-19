from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/convert')
def convert():
    currency = request.args.get('currency')
    amount = request.args.get('amount')

    if not currency or not amount:
        return "Помилка: потрібно вказати параметри ?currency=XXX&amount=YYY", 400

    try:
        amount = float(amount)
        if amount <= 0:
            return "Помилка: сума має бути більше 0", 400
    except ValueError:
        return "Помилка: amount має бути числом", 400

    try:
        response = requests.get("https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11")
        
        if response.status_code != 200:
            return "Помилка: не вдалося отримати курс валют", 500

        data = response.json()

        rate = None
        for item in data:
            if item["ccy"] == currency.upper():
                rate = float(item["sale"])
                break

        if rate is None:
            available_currencies = [item["ccy"] for item in data]
            return f"Помилка: валюта {currency} не знайдена. Доступні: {', '.join(available_currencies)}", 400

        result = amount * rate
        return jsonify({
            "currency": currency.upper(), 
            "amount": amount, 
            "uah": round(result, 2)
        })

    except requests.RequestException:
        return "Помилка: проблема з отриманням курсів", 500
    except (KeyError, ValueError):
        return "Помилка: проблема з обробкою даних про курси", 500

@app.route('/')
def index():
    return "Currency Converter API - використовуйте /convert?currency=XXX&amount=YYY"

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)