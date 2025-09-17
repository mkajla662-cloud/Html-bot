import os
import telebot
from flask import Flask, request

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Render par env variable set karein
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Render par apni service ka URL set karein

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

def link_to_html_player(link):
    if link.endswith('.m3u8'):
        return f"""
        <video width="640" height="360" controls style="margin:25px 0; border-radius:18px; box-shadow:0 0 15px #00e6e6;">
            <source src="{link}" type="application/x-mpegURL">
            Your browser does not support the video tag.
        </video>
        """
    else:
        return f"""
        <video width="640" height="360" controls style="margin:25px 0; border-radius:18px; box-shadow:0 0 15px #ff66cc;">
            <source src="{link}">
            Your browser does not support the video tag.
        </video>
        """

def generate_html(links):
    players = "\n".join(link_to_html_player(link) for link in links)
    return f"""
    <html>
    <head>
        <title>Custom Video Page</title>
        <meta charset="UTF-8">
        <style>
            body {{
                min-height: 100vh;
                background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
                color: #333;
                font-family: 'Segoe UI', Arial, sans-serif;
                text-align: center;
            }}
            .radhe {{
                font-size: 2.4em;
                color: #ff0099;
                font-weight: bold;
                margin-top: 30px;
                letter-spacing: 1px;
                text-shadow: 2px 2px 8px #ffd700;
            }}
            .heading {{
                font-size: 1.4em;
                color: #005bea;
                margin-top: 18px;
                font-weight: 600;
            }}
            .owner {{
                font-size: 1.1em;
                color: #ff6a00;
                margin-bottom: 24px;
                font-weight: 500;
            }}
            .hindi {{
                font-size: 1.3em;
                color: #d7263d;
                margin: 35px 0 20px 0;
                font-family: 'Noto Sans Devanagari', sans-serif;
                letter-spacing: 0.5px;
            }}
            video {{
                background: #fff;
                border: 3px solid #005bea;
            }}
        </style>
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@500&display=swap" rel="stylesheet">
    </head>
    <body>
        <div class="radhe">राधे राधे ✨</div>
        <div class="heading">made by @inventor_king_09</div>
        <div class="owner">apna bhai (owner2)@captain_kingg_09</div>
        {players}
        <div class="hindi">बस हर शाम अधूरी लगती है तेरे बिना 🙂</div>
    </body>
    </html>
    """

@bot.message_handler(content_types=['document'])
def handle_file(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_content = downloaded_file.decode('utf-8')
        links = [line.strip() for line in file_content.splitlines() if line.strip()]
        html_result = generate_html(links)
        with open("players.html", "w", encoding="utf-8") as f:
            f.write(html_result)
        with open("players.html", "rb") as f:
            bot.send_document(message.chat.id, f)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return '', 200
    return 'Bot running!', 200

if __name__ == "__main__":
    # Set webhook on start
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))