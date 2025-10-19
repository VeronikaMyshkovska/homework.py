import requests

currency = input("Введіть валюту (наприклад USD, EUR, PLN): ").upper()
amount = input("Введіть суму: ")

url = f"http://127.0.0.1:5000/convert?currency={currency}&amount={amount}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(f"{data['amount']} {data['currency']} = {data['uah']} UAH")
else:
    print("Помилка:", response.text)