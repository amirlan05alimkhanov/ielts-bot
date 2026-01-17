import telebot
import json
import os
import random

# Вставь сюда свой токен
token = '8055988079:AAFHOXP907f1OIjk_l2Xx9nOxpvZ4zqqaMI'

bot = telebot.TeleBot(token)

FILE_NAME = 'words.json'


# --- ПАМЯТЬ БОТА ---
# Загрузка слов из файла
def load_words():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_words(words_dict):
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        json.dump(words_dict, f, ensure_ascii=False, indent=4)


user_words = load_words()

# --- ВРЕМЕННАЯ ПАМЯТЬ ДЛЯ ВИКТОРИНЫ ---
# Здесь мы будем хранить, кто сейчас играет и какое слово угадывает
# Формат: {id_пользователя: "правильный_ответ"}
quiz_users = {}


# --- КОМАНДЫ ---

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     "Привет! Я бот для IELTS.\n"
                     "Команды:\n"
                     "📝 Пиши слова: 'Cat Кошка' (чтобы добавить)\n"
                     "🧠 /quiz - Начать тест (проверка знаний)\n"
                     "📖 /list - Список слов\n"
                     "ℹ️ /info - Информация о боте")


@bot.message_handler(commands=['info'])
def show_info(message):
    bot.send_message(message.chat.id,
                     f'IELTS Bot v2.0 (Quiz Mode).\n'
                     f'Разработчик: amirlan05alimkhanov.\n'
                     f'Слов в базе: {len(user_words)}')


@bot.message_handler(commands=['list'])
def show_list(message):
    if not user_words:
        bot.send_message(message.chat.id, "Словарь пуст.")
        return
    text = "Твои слова:\n"
    for eng, ru in user_words.items():
        text += f"{eng} — {ru}\n"
    bot.send_message(message.chat.id, text)


# --- ЛОГИКА ВИКТОРИНЫ (/quiz) ---

@bot.message_handler(commands=['quiz'])
def start_quiz(message):
    if not user_words:
        bot.send_message(message.chat.id, "Словарь пуст! Добавь слова, прежде чем играть.")
        return

    # 1. Выбираем случайное английское слово (ключ)
    random_eng_word = random.choice(list(user_words.keys()))
    # 2. Берем его перевод
    russian_translation = user_words[random_eng_word]

    # 3. Запоминаем, что этот пользователь сейчас угадывает именно это слово
    quiz_users[message.chat.id] = random_eng_word

    # 4. Спрашиваем пользователя
    bot.send_message(message.chat.id, f"🤔 Как переводится: **{russian_translation}**?")


# --- ОБРАБОТКА ТЕКСТА (ОТВЕТЫ И ДОБАВЛЕНИЕ) ---

@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_id = message.chat.id
    text = message.text.strip()

    # СЦЕНАРИЙ 1: Пользователь в режиме викторины (отвечает на вопрос)
    if user_id in quiz_users:
        correct_answer = quiz_users[user_id]  # Вспоминаем правильный ответ

        # Сравниваем (приводим к нижнему регистру, чтобы Apple и apple были равны)
        if text.lower() == correct_answer.lower():
            bot.send_message(user_id, f"✅ Правильно! Это {correct_answer}.")
        else:
            bot.send_message(user_id, f"❌ Неверно. Правильный ответ: {correct_answer}")

        # Удаляем пользователя из режима викторины (игра закончена)
        del quiz_users[user_id]
        bot.send_message(user_id, "Пиши /quiz, чтобы сыграть еще раз.")

    # СЦЕНАРИЙ 2: Пользователь просто добавляет новое слово
    else:
        try:
            parts = text.split()
            if len(parts) < 2:
                bot.send_message(user_id, "Чтобы добавить слово, пиши: English Русский")
                return

            eng = parts[0]
            ru = " ".join(parts[1:])

            user_words[eng] = ru
            save_words(user_words)
            bot.send_message(user_id, f"💾 Сохранено: {eng} — {ru}")

        except Exception:
            bot.send_message(user_id, "Ошибка. Попробуй еще раз.")


print("Бот с викториной запущен...")
bot.polling(none_stop=True)