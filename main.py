import os
import requests
import schedule
import time
from datetime import datetime

UZUM_API_TOKEN = "M4lHdDDaBA+FBGnmoJX/kmZcA+G8+viN6fkTO9ZKyso="
TELEGRAM_BOT_TOKEN = "8926029722:AAFcksw_URId2Hnl_UM9lg_SOz9mp-z1gac"
TELEGRAM_CHAT_ID = "438934195"
UZUM_URL = "https://api-seller.uzum.uz/api/seller-openapi/v1/finance/orders"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        return requests.post(url, json=payload).json()
    except Exception as e:
        print(f"Xatolik: {e}")

def generate_report():
    headers = {"Authorization": f"Bearer {UZUM_API_TOKEN}", "Content-Type": "application/json"}
    try:
        response = requests.get(UZUM_URL, headers=headers)
        today_date = datetime.now().strftime("%Y-%m-%d")
        if response.status_code == 200:
            send_telegram(f"📊 *UZUM MARKET KUNLIK HISOBOT*\n📅 *Sana:* {today_date}\n\n✅ Uzum API ulanishi muvaffaqiyatli.")
        else:
            send_telegram(f"⚠️ *Uzum API Xatoligi:* Status {response.status_code}\n{response.text}")
    except Exception as e:
        send_telegram(f"⚠️ *Xatolik:* {str(e)}")

# 1. Bot ishga tushgani haqida xabar
send_telegram("🚀 *Uzum Hisobot Boti qayta ishga tushirildi!*")

# 2. Hozirning o'zida Hisobotni ham yuborib test qilamiz:
generate_report()

# 3. Har kuni soat 09:00 da hisobot yuborishni rejalashtirish
schedule.every().day.at("09:00").do(generate_report)

print("Bot ishlayapti...")
while True:
    schedule.run_pending()
    time.sleep(10)
