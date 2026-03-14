import logging
import os
from openai import OpenAI
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Bot Token and OpenAI API Key from environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

client = OpenAI(api_key=OPENAI_API_KEY)
OPENAI_MODEL = "gpt-4.1-mini"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"مرحباً {user.mention_html()}! أنا بوت التدقيق اللغوي \"Feras Hritani\". أرسل لي أي نص وسأقوم بتصحيحه وتنسيقه وإضافة علامات الترقيم المناسبة."
    )

async def correct_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Corrects and formats the received text using OpenAI API."""
    user_text = update.message.text
    await update.message.reply_text("جاري معالجة النص... الرجاء الانتظار.")

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "أنت مساعد لغوي متخصص في التدقيق الإملائي والنحوي، ترتيب النصوص الطويلة، وتصحيح علامات الترقيم. قم بتصحيح النص المعطى، أعد ترتيبه إذا لزم الأمر، وأضف علامات الترقيم المناسبة. يجب أن يكون الرد باللغة العربية الفصحى."},
                {"role": "user", "content": user_text}
            ],
            temperature=0.7,
            max_tokens=1000,
        )
        corrected_text = response.choices[0].message.content
        await update.message.reply_text(corrected_text)
    except Exception as e:
        logger.error(f"Error communicating with OpenAI: {e}")
        await update.message.reply_text("عذراً، حدث خطأ أثناء معالجة النص. الرجاء المحاولة مرة أخرى لاحقاً.")

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, correct_text))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
