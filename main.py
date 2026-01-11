import telebot

# Вставь сюда токен, который дал BotFather (в кавычках!)
token = '8055988079:AAFHOXP907f1OIjk_l2Xx9nOxpvZ4zqqaMI'

# Создаем бота
bot = telebot.TeleBot(token)

# Эта функция реагирует на команду /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Я твой помощник по IELTS. Готов учиться?")

# Эта функция повторяет (эхо) любой текст, который ты напишешь
@bot.message_handler(content_types=['text'])
def send_text(message):
    user_text = message.text
    # Тут мы будем потом добавлять логику, а пока просто повторим
    bot.send_message(message.chat.id, f"Ты написал: {user_text}")

# Запускаем бота (он будет работать вечно, пока ты не нажмешь Stop)
print("Бот запущен...")
bot.polling(none_stop=True)