import os
import discord # أو import telegram

# الحصول على التوكن من متغيرات البيئة
BOT_TOKEN = os.getenv('BOT_TOKEN')

if BOT_TOKEN is None:
    print("خطأ: لم يتم العثور على توكن البوت في متغيرات البيئة. يرجى تعيين BOT_TOKEN.")
    exit()

# مثال لبوت ديسكورد بسيط (يمكن استبداله بكود بوت تيليجرام)
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'تم تسجيل الدخول كـ {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('مرحباً!')

client.run(BOT_TOKEN)
