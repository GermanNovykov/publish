from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import yt_dlp
import os
# Function to handle start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! Send me a TikTok, YouTube, or Instagram link, and I will download the video for you.')

# Function to handle received messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text.startswith('https://www.instagram.com/reel') or update.message.text.startswith('https://www.youtube.com') or update.message.text.startswith('https://youtu.be') or update.message.text.startswith('https://vm.tiktok.com') or update.message.text.startswith('https://www.tiktok.com'):
        url = update.message.text
        # Define yt-dlp options
        ydl_opts = {
            'format': 'best',
            'outtmpl': '%(id)s.%(ext)s',  # Save file as <video_id>.<extension>
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                # Download video
                info_dict = ydl.extract_info(url, download=True)
                video_filename = ydl.prepare_filename(info_dict)
                # Send video back to user
                await context.bot.send_video(chat_id=update.effective_chat.id, video=open(video_filename, 'rb'))
                os.remove(video_filename)
            except Exception as e:
                os.remove(video_filename)
                await update.message.reply_text('An error occurred: ' + str(e))

    else:
        pass

# Function to create and run the bot
def main():
    # Replace 'YOUR_TOKEN_HERE' with your actual bot token
    application = Application.builder().token('6956696727:AAGemZeTMI67MjBF3hUJxAuxLBJoduHTeaU').build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
