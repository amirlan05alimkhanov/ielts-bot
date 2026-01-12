import telebot
import json
import os

# 1. Вставь сюда свой токен (он такой же, как вчера)
token = '8055988079:AAFHOXP907f1OIjk_l2Xx9nOxpvZ4zqqaMI'

bot = telebot.TeleBot(token)

# Имя файла, где будет храниться наша "база данных"
FILE_NAME = 'words.json'


# --- ФУНКЦИИ ДЛЯ РАБОТЫ С ФАЙЛОМ ---

def load_words():
    """Загружает слова из файла при запуске"""
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}  # Если файла нет, возвращаем пустой словарь


def save_words(words_dict):
    """Сохраняет словарь в файл"""
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        # indent=4 делает файл красивым и читаемым для человека
        json.dump(words_dict, f, ensure_ascii=False, indent=4)


# Загружаем память при старте
user_words = load_words()


# --- ЛОГИКА БОТА ---

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     "Привет! Я помогаю учить английский.\n"
                     "Команды:\n"
                     "1. Напиши слово и перевод через пробел, чтобы добавить. \n"
                     "   Пример: Cat Кошка\n"
                     "2. /list - Показать все слова\n"
                     "3. /delete <слово> - Удалить слово")


@bot.message_handler(commands=['list'])
def show_list(message):
    """Показывает список всех слов"""
    if not user_words:
        bot.send_message(message.chat.id, "Твой словарь пока пуст! Напиши слово и перевод.")
        return

    # Формируем красивый список
    text_message = "📖 Твой словарь:\n"
    for eng, ru in user_words.items():
        text_message += f"{eng} — {ru}\n"

    bot.send_message(message.chat.id, text_message)


@bot.message_handler(commands=['delete'])
def delete_word(message):
    """Удаляет слово. Пример: /delete Cat"""
    try:
        # Отрезаем команду /delete и берем слово
        word_to_delete = message.text.split()[1]
        if word_to_delete in user_words:
            del user_words[word_to_delete]
            save_words(user_words)  # Обязательно сохраняем изменения!
            bot.send_message(message.chat.id, f"Слово '{word_to_delete}' удалено.")
        else:
            bot.send_message(message.chat.id, "Такого слова нет в словаре.")
    except IndexError:
        bot.send_message(message.chat.id, "Напиши, что удалить. Пример: /delete Cat")


@bot.message_handler(commands=['info'])
def show_info(message):
    bot.send_message(message.chat.id,
                     f'Я бот-словарь. Версия 1.0. \n'
                     f'Меня создал amirlan05alimkhanov. \n'
                     f'Всего слов в словаре: {len(user_words)}')


# Этот обработчик ловит ПРОСТО ТЕКСТ (добавление слов)
@bot.message_handler(content_types=['text'])
def add_new_word(message):
    try:
        # Пытаемся разбить сообщение на 2 части: Слово и Перевод
        text_parts = message.text.split()

        # Если слов меньше 2 (например, просто "Cat"), ругаемся
        if len(text_parts) < 2:
            bot.send_message(message.chat.id, "Нужно два слова! Пример: Dog Собака")
            return

        eng_word = text_parts[0]
        translation = " ".join(text_parts[1:])  # Все остальное - перевод

        # Записываем в память
        user_words[eng_word] = translation
        save_words(user_words)  # Сохраняем в файл

        bot.send_message(message.chat.id, f"✅ Добавлено: {eng_word} — {translation}")

    except Exception as e:
        bot.send_message(message.chat.id, "Что-то пошло не так. Попробуй еще раз.")


print("Бот с памятью запущен...")
bot.polling(none_stop=True)