const dotenv = require('dotenv').config(); // إذا كنت تستخدم ملف .env محلياً
const { Client, GatewayIntentBits } = require('discord.js'); // أو 'node-telegram-bot-api'

// الحصول على التوكن من متغيرات البيئة
const BOT_TOKEN = process.env.BOT_TOKEN;

if (!BOT_TOKEN) {
    console.error("خطأ: لم يتم العثور على توكن البوت في متغيرات البيئة. يرجى تعيين BOT_TOKEN.");
    process.exit(1);
}

// مثال لبوت ديسكورد بسيط (يمكن استبداله بكود بوت تيليجرام)
const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.MessageContent, GatewayIntentBits.GuildMessages] });

client.once('ready', () => {
    console.log(`تم تسجيل الدخول كـ ${client.user.tag}!`);
});

client.on('messageCreate', async message => {
    if (message.author.bot) return;

    if (message.content === '!hello') {
        message.channel.send('مرحباً!');
    }
});

client.login(BOT_TOKEN);
