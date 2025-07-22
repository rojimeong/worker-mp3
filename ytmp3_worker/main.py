import telebot
import os
import yt_dlp

BOT_TOKEN = "ISI_TOKEN_BOT_KEDUA"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["mp3"])
def download_mp3(message):
    if len(message.text.split()) < 2:
        bot.reply_to(message, "❗ Kirim perintah seperti ini:\n/mp3 https://youtube.com/...")
        return

    url = message.text.split(" ", 1)[-1]
    msg = bot.send_message(message.chat.id, "⏳ Sedang download...")

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'music.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        with open("music.mp3", "rb") as f:
            bot.send_audio(message.chat.id, f)
        os.remove("music.mp3")
        bot.delete_message(message.chat.id, msg.id)
    except Exception as e:
        bot.edit_message_text(f"❌ Gagal: {e}", message.chat.id, msg.id)

bot.polling(non_stop=True)
