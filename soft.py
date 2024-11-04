import telebot
import requests
from bs4 import BeautifulSoup

# Замените 'YOUR_TELEGRAM_BOT_TOKEN' на токен вашего бота
bot = telebot.TeleBot("7982533265:AAGD5ud5zqu58mlokI56NZ3ia0oqYBmHcqE")

# Функция для извлечения изображения с пина
def get_pinterest_image(pin_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(pin_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Находим ссылку на изображение
    image_tag = soup.find("meta", property="og:image")
    if image_tag:
        image_url = image_tag["content"]
        return image_url
    return None

# Обработчик сообщений с URL Pinterest
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Отправь мне ссылку на Pinterest, и я загружу изображение.")

@bot.message_handler(func=lambda message: message.text.startswith("https://pin.it"))
def download_pinterest_image(message):
    pin_url = message.text.strip()
    image_url = get_pinterest_image(pin_url)
    
    if image_url:
        # Отправка изображения пользователю
        bot.send_photo(message.chat.id, image_url, caption="Вот изображение с Pinterest")
    else:
        bot.send_message(message.chat.id, "Не удалось найти изображение по этой ссылке.")

# Запуск бота
bot.polling()
