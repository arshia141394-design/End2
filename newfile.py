from rubka import Robot
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from flask import Flask
import threading
import os
TOKEN = "BICAGB0SZXZSXDGXLSORLPNLLOBVHTNXYBPTWSBMROFLETWWEOHOPPWMLBAOKALG"

bot = Robot(TOKEN)


@bot.on_message()
async def commands(client, message):

    text = message.text.strip()

    # ------------------ START ------------------
    if text == "/start":
        await message.reply(
            "⭐ Arshia StarAI\n\n"
            "سلام! خوش اومدی 🤖\n\n"
            "🔎 جستجو — عبارت موردنظر"
        )
        return

    # ------------------ SEARCH ------------------
    if text.startswith("جستجو "):

        query = text.replace("جستجو ", "", 1).strip()

        if not query:
            await message.reply("🔎 لطفاً عبارت موردنظر را وارد کن.")
            return

        url = f"https://html.duckduckgo.com/html/?q={quote(query)}"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        try:
            r = requests.get(
                url,
                headers=headers,
                timeout=10
            )

            if r.status_code == 200:

                soup = BeautifulSoup(
                    r.text,
                    "html.parser"
                )

                results = soup.select(
                    ".result__title a"
                )

                if results:

                    title = results[0].get_text(
                        strip=True
                    )

                    link = results[0]["href"]

                    await message.reply(
                        f"🔎 {title}\n\n{link}"
                    )

                else:
                    await message.reply(
                        "❌ نتیجه‌ای پیدا نشد."
                    )

            else:
                await message.reply(
                    "❌ خطا در اتصال."
                )

        except Exception as e:
            await message.reply(
                f"❌ خطا:\n{e}"
            )
    if text.startswith("ترجمه"):
        sentence = text.replace("ترجمه", "", 1).strip()

        if not sentence:
            await message.reply("🌍 لطفاً متن موردنظر را وارد کن.")
            return

        try:
            from deep_translator import GoogleTranslator

            result = GoogleTranslator(
                source="auto",
                target="en" if any("\u0600" <= c <= "\u06FF" for c in sentence) else "fa"
            ).translate(sentence)

            await message.reply(f"🌍 ترجمه:\n\n{result}")

        except Exception as e:
            await message.reply(f"❌ خطا در ترجمه:\n{e}")
    # ------------------ QUESTION ------------------
    if text.startswith("سوال "):

        question = text.replace("سوال ", "", 1).strip()

        if not question:
            await message.reply("❓ لطفاً سؤال موردنظر را وارد کن.")
            return

        url = f"https://html.duckduckgo.com/html/?q={quote(question)}"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        try:
            r = requests.get(
                url,
                headers=headers,
                timeout=10
            )

            if r.status_code == 200:

                soup = BeautifulSoup(
                    r.text,
                    "html.parser"
                )

                results = soup.select(".result__snippet")

                if results:
                    answer = results[0].get_text(
                        " ",
                        strip=True
                    )

                    await message.reply(
                        f"🤖 پاسخ:\n\n{answer}"
                    )

                else:
                    await message.reply(
                        "❌ پاسخی پیدا نشد."
                    )

            else:
                await message.reply(
                    "❌ خطا در اتصال."
                )

        except Exception as e:
            await message.reply(
                f"❌ خطا:\n{e}"
            )

                
    else:
        await message.reply(
            "❓ دستور نامعتبر است.\n"
            "برای شروع /start را ارسال کن."
        )
# ------------------ RENDER WEB SERVER ------------------
app = Flask(__name__)

@app.route("/")
def home():
    return "Arshia StarAI is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web, daemon=True).start()

bot.run()