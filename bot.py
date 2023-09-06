from telebot import types
import telebot
from my_class_2 import NASA
import re
import datetime

API_key = 'YOUR_API_KEY_HERE'  # Замените на ваш API ключ'1rkXksQeXm8LvNhhZHSuDjraBRoMSOq91mv1s0P9'
bot = telebot.TeleBot ('YOUR_BOT_TOKEN_HERE')  # Замените на ваш токен бота'6407381406:AAG56JGhcMlpN_0AYd7W9gMHPqlNMFftUnc')

@bot.message_handler(commands=['help', 'start'])
def handle_commands(message):
    if message.text == '/help':
        help_text = (
            "Привет! Этот бот предоставляет информацию о близких к Земле астероидах.\n\n"
            "Команды:\n"
            "/start - начать работу бота\n"
            "/help - получить справку\n\n"
            "Как использовать бота:\n"
            "1. Начните с команды /start\n"
            "2. Бот запросит у вас ввести дату в формате YYYY-MM-DD\n"
            "3. Если дата введена правильно, бот начнет запрос к API и предоставит информацию о близких астероидах\n"
            "4. Вы можете использовать кнопку 'Объекты сближающиеся с Землей', чтобы запросить информацию об астероидах\n"
            "5. Вы можете использовать кнопку 'СТОП', чтобы остановить работу бота\n\n"
            "Помимо кнопок, вы также можете вводить команды вручную.\n"
            "Если у вас возникли вопросы, используйте команду /help, чтобы получить эту справку."
        )

        bot.send_message(message.chat.id, help_text, parse_mode='html')
    elif message.text == '/start':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_asteroids = types.KeyboardButton('Объекты сближающиеся с Землей')
        button_stop = types.KeyboardButton('СТОП')
        markup.add(button_asteroids)
        markup.add(button_stop)
        message_text = (
            f'Привет, {message.from_user.first_name}!\n'
            f'Нажми:\n<b>Показать объекты сближающиеся с Землей</b> '
            f'для просмотра объектов\n'
            f'Нажми <b>СТОП</b> для остановки работы бота'
        )

        bot.send_message(message.chat.id,
                         message_text,
                         reply_markup=markup,
                         parse_mode='html')

        gif_url = 'https://i.gifer.com/7gRp.gif'
        bot.send_animation(message.chat.id, animation=gif_url)



@bot.message_handler(content_types=['text'])
def handle_button_click(message):
    if message.text == 'Объекты сближающиеся с Землей':
        bot.send_message(message.chat.id, 'Для начала работы бота введите дату в формате "YYYY-MM-DD"')
        bot.register_next_step_handler(message, click_on_asteroids)
    elif message.text == 'СТОП':
        bot.send_message(message.chat.id, f'До свидания {message.from_user.first_name}! Бот остановлен.')
        bot.stop_polling()
    else:
        bot.reply_to(message, f'{message.chat.first_name}, не балуйся. Начни сначала!')


@bot.message_handler(content_types=['text'])
def click_on_asteroids(message):
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if re.match(date_pattern, message.text):
            start_date = message.text
            start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            if start_date_obj.date() == datetime.datetime.now().date():
                end_date = start_date
            else:
                end_date_obj = start_date_obj + datetime.timedelta(days=3)
                end_date = end_date_obj.strftime('%Y-%m-%d')
            
            bot.send_message(message.chat.id, 'Дата введена верно.')
            bot.send_message(message.chat.id, f'Дата начала поиска {start_date}. Дата окончания поиска {end_date}.')
            
            nasa_asteroids = NASA (start_date = start_date, end_date = end_date , api_key = API_key)
            data = nasa_asteroids.get_asteroids()
            bot.send_message (message.chat.id, f'В этот период замечено {data["element_count"]} объектов сближающихся с Землей.')
            
            data1 = nasa_asteroids.get_hazardous_asteroids()
            inf = ""
            for obgekt in data1:
                for key, value in obgekt.items():
                    inf += f"{key}: {value}\n"  
            bot.send_message(message.chat.id, f'Из них потенциально опасны: {len(data1)}')
            
            if end_date == start_date and len(data1) >= 1:
                bot.send_message(message.chat.id, f'ОПАСНОСТЬ ПАДЕНИЯ МЕТИОРИТА, УКРОЙТЕСЬ В УБЕЖИЩЕ!!!!')
                gif_url3 = 'https://i.gifer.com/7BVP.gif'
                bot.send_animation(message.chat.id, animation = gif_url3)
            
            bot.send_message(message.chat.id, inf)
            gif_url2 = 'https://i.gifer.com/AG7C.gif'
            bot.send_animation(message.chat.id,  animation = gif_url2)
        
        else:
            gif_url1 = 'https://i.gifer.com/VAyR.gif'
            bot.send_message(message.chat.id, 'ОШИБКА, ДАТА ВВЕДЕНА НЕ ПРАВИЛЬНО!!!')
            bot.send_animation(message.chat.id,  animation = gif_url1)
            bot.send_message(message.chat.id, 'Попробуйте еще раз. Введите дату в формате "YYYY-MM-DD"')

bot.polling(non_stop= True)