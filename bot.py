import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from rembg import remove
import os

BOT_TOKEN = "8206936147:AAGZsHT60O_x2pR2vgbp7yKYWN6UuDy4xAU"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        KeyboardButton("🖼 Remove Background"),
        KeyboardButton("📖 How It Works"),
        KeyboardButton("ℹ️ About")
    )

    bot.send_message(
        message.chat.id,
        "✨ *AI Background Remover Bot*\n\n"
        "🚀 Professional tool to remove image background in HD quality.\n\n"
        "👇 Choose an option:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda m: m.text == "📖 How It Works")
def how_it_works(message):
    bot.send_message(
        message.chat.id,
        "1️⃣ Click *Remove Background*\n"
        "2️⃣ Upload your image\n"
        "3️⃣ Wait a few seconds ⏳\n"
        "4️⃣ Get HD image 🎉",
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda m: m.text == "ℹ️ About")
def about(message):
    bot.send_message(
        message.chat.id,
        "🤖 AI-powered Background Remover\n"
        "⚡ Fast & Secure\n"
        "🎨 High Quality Output",
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda m: m.text == "🖼 Remove Background")
def ask_image(message):
    bot.send_message(
        message.chat.id,
        "📤 Please upload your image (JPG / PNG)",
        parse_mode="Markdown"
    )

@bot.message_handler(content_types=['photo'])
def handle_image(message):
    try:
        bot.send_chat_action(message.chat.id, "typing")

        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        input_file = f"{message.chat.id}_input.png"
        output_file = f"{message.chat.id}_output.png"

        with open(input_file, 'wb') as f:
            f.write(downloaded_file)

        bot.send_message(message.chat.id, "⏳ Processing image...")

        with open(input_file, 'rb') as i:
            result = remove(i.read())

        with open(output_file, 'wb') as o:
            o.write(result)

        with open(output_file, 'rb') as img:
            bot.send_photo(
                message.chat.id,
                img,
                caption="✅ Background removed (HD Quality)"
            )

        os.remove(input_file)
        os.remove(output_file)

    except:
        bot.send_message(message.chat.id, "❌ Error! Please try another image.")

print("Bot is running...")
bot.polling(none_stop=True)
