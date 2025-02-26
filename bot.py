import json
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Load users from JSON file
def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save users to JSON file
def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

# Function to format responses
def format_message(command, response):
    return f"💬 **You:** `{command}`\n\n> {response}"

# Function to show the main menu keyboard
def get_main_menu():
    keyboard = [
        ["FACEBOOK ID", "GOOGLE ID"],
        ["TWITTER ID", "🤑BALANCE"],
        ["💰ADD BALANCE", "📞CONTACT"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Function to show the ID list menu
def get_id_list_menu():
    keyboard = [
        ["ID 1", "ID 2", "ID 3"],
        ["ID 4", "ID 5", "ID 6"],
        ["EXIT"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = load_users()
    user_id = str(update.effective_user.id)
    username = update.effective_user.first_name

    if user_id not in users:
        users[user_id] = username
        save_users(users)

    command_text = "/start"
    response_text = (
        "👋 **Welcome,** " + f"__{username.upper()}__ !!\n"
        "🔥 *This is the* __LEVEL 8 ID SELLING BOT__.\n"
        "📩 **Need Help? Contact:** @Gohan52"
    )

    await update.message.reply_text(
        format_message(command_text, response_text),
        reply_to_message_id=update.message.message_id,
        parse_mode="Markdown",
        reply_markup=get_main_menu()
    )

# /users command
async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = load_users()
    total_users = len(users)

    command_text = "/users"
    response_text = f"📊 **Total Registered Users:** `{total_users}`"

    await update.message.reply_text(
        format_message(command_text, response_text),
        reply_to_message_id=update.message.message_id,
        parse_mode="Markdown"
    )

# /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command_text = "/help"
    response_text = (
        "📜 **Available Commands:**\n"
        "🔹 `/start` - Welcome Message\n"
        "🔹 `/users` - View Total Users\n"
        "🔹 `/help` - Show Commands\n"
        "⚡ __More commands coming soon!__"
    )

    await update.message.reply_text(
        format_message(command_text, response_text),
        reply_to_message_id=update.message.message_id,
        parse_mode="Markdown"
    )

# Handle button presses
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text in ["FACEBOOK ID", "GOOGLE ID", "TWITTER ID"]:
        await update.message.reply_text(
            f"📌 **Select an ID from {text}:**",
            reply_markup=get_id_list_menu()
        )

    elif text == "🤑BALANCE":
        await update.message.reply_text(
            "💰 **Your balance is:** `0`",
            reply_to_message_id=update.message.message_id,
            parse_mode="Markdown"
        )

    elif text == "💰ADD BALANCE":
        qr_url = "https://i.postimg.cc/1Rq1mP5Y/IMG-20250226-154350.jpg"
        await update.message.reply_photo(
            photo=qr_url,
            caption="💳 **PAY HOW MUCH YOU WANT 1RS=1BALANCE  TO ADD FUNDS**\n\n📩 **Or Contact:** @Gohan52 **to add funds manually.**",
            parse_mode="Markdown"
        )

    elif text == "📞CONTACT":
        await update.message.reply_text(
            "📩 **YOU CAN CONTACT HERE:** @Gohan52",
            reply_to_message_id=update.message.message_id,
            parse_mode="Markdown"
        )

    elif text == "EXIT":
        await update.message.reply_text(
            "🔙 Returning to Main Menu...",
            reply_markup=get_main_menu()
        )

# Main function to start the bot
def main():
    TOKEN = "8001988418:AAEV2CFV7RJu1L34Qaz8E255E87ie8OhFz8"  # 🔴 Reset your token in BotFather
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("users", users))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
