import os
import threading
from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask

# ---- Telegram Bot Config ----
API_ID = int(os.getenv("22480303"))
API_HASH = os.getenv("99c931b6c1ae6f8c3c3e87da173fa424")
BOT_TOKEN = os.getenv("8300056150:AAExVt4MbfcyuhLetjZz53KrJAyaSwQ8lUM")

bot = Client(
    "universal_video_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ---- Flask App (Dummy Web Service for Railway) ----
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Universal Video Bot is running on Railway!"

# ---- Bot Handlers ----
@bot.on_message(filters.document & filters.private)
async def handle_file(client, message: Message):
    doc = message.document

    if not doc.file_name.endswith(".txt"):
        await message.reply("❌ कृपया केवल `.txt` फाइल भेजें जिसमें video links हों।")
        return

    download_path = f"{doc.file_id}.txt"
    html_path = f"{doc.file_id}.html"

    # फाइल डाउनलोड करो
    await message.download(file_name=download_path)

    # TXT पढ़ो
    with open(download_path, "r", encoding="utf-8") as f:
        links = [line.strip() for line in f if line.strip()]

    if not links:
        await message.reply("⚠️ फाइल खाली है या कोई valid link नहीं मिला।")
        os.remove(download_path)
        return

    players = ""
    script_parts = []
    m3u8_count = 0

    header_html = """
    <h1>Made by @inventor_king_09 😊</h1>
    <h2>अपना भाई (owner2) @captain_kingg_09</h2>
    <button class="toggle-btn" onclick="toggleTheme()">🌗 Toggle Theme</button>
    <hr>
    """

    for i, link in enumerate(links, 1):
        if link.endswith(".m3u8"):
            m3u8_count += 1
            players += f"""
            <div class="video-box">
              <video id="video{m3u8_count}" controls></video>
              <p>तेरे बिना हर शाम अधूरी लगती है ❤️</p>
            </div>
            """
            script_parts.append(f'"{link}"')
        elif link.endswith((".mp4", ".webm", ".mkv")):
            players += f"""
            <div class="video-box">
              <video controls>
                <source src="{link}">
                Your browser does not support the video tag.
              </video>
              <p>तेरे बिना हर शाम अधूरी लगती है ❤️</p>
            </div>
            """
        elif "youtube.com" in link or "youtu.be" in link:
            if "watch?v=" in link:
                video_id = link.split("watch?v=")[-1].split("&")[0]
            elif "youtu.be/" in link:
                video_id = link.split("youtu.be/")[-1].split("?")[0]
            else:
                video_id = ""
            if video_id:
                embed_link = f"https://www.youtube.com/embed/{video_id}"
                players += f"""
                <div class="video-box">
                  <iframe src="{embed_link}" frameborder="0" allowfullscreen></iframe>
                  <p>तेरे बिना हर शाम अधूरी लगती है ❤️</p>
                </div>
                """
            else:
                players += f"<p>Invalid YouTube link: {link}</p>"
        else:
            players += f"""
            <p>🔗 <a href="{link}" target="_blank">{link}</a></p>
            """

    script_code = ""
    if m3u8_count > 0:
        script_code = f"""
        <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
        <script>
          const m3u8Links = [
            {", ".join(script_parts)}
          ];
          m3u8Links.forEach((link, i) => {{
            let video = document.getElementById("video" + (i+1));
            if (Hls.isSupported()) {{
              let hls = new Hls();
              hls.loadSource(link);
              hls.attachMedia(video);
            }} else if (video.canPlayType('application/vnd.apple.mpegurl')) {{
              video.src = link;
            }}
          }});
        </script>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Universal Video Player</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      background: #f4f4f4;
      color: #111;
      text-align: center;
      transition: all 0.3s;
    }}
    .video-box {{
      margin: 20px auto;
      max-width: 720px;
      border: 2px solid #0078ff;
      padding: 10px;
      border-radius: 10px;
      background: #fff;
    }}
    video, iframe {{
      width: 100%;
      height: 400px;
      border-radius: 8px;
    }}
    body.dark {{
      background: #111;
      color: #eee;
    }}
    body.dark .video-box {{
      background: #222;
      border-color: #0ff;
    }}
    .toggle-btn {{
      padding: 8px 15px;
      margin: 10px;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-size: 14px;
    }}
  </style>
</head>
<body>
  {header_html}
  {players}
  {script_code}
  <script>
    function toggleTheme() {{
      document.body.classList.toggle("dark");
    }}
  </script>
</body>
</html>
"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    await message.reply_document(html_path, caption="✅ Universal HTML तैयार है।")

    os.remove(download_path)
    os.remove(html_path)

@bot.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply("👋 मुझे `.txt` फाइल भेजें जिसमें video links हों (m3u8/mp4/YouTube आदि), मैं stylish HTML player बना दूँगा।")

# ---- Run Both Bot + Flask ----
def run_flask():
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))

def run_bot():
    bot.run()

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_bot()