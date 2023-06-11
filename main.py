import telebot
import random, codecs
import time, threading, schedule

TOKEN = "token"
bot = telebot.TeleBot(TOKEN)

# default list messages
psychologic_week = []
# sorting: everything that does not relate to the code should lie separately
filename = codecs.open('psychologic_cat.txt', 'r', 'utf_8_sig')
for line in filename:
    psychologic_week.append(line)

commands = {
    '/start': 'запуск',
    '/category': 'узнать какие существуют темы для поддержания жизни в чатике',
    '/set_category': 'задать свою категорию',
    '/about': 'страничка о нас',
    '/default': 'запустить заготовленный пакет фраз разработчиками',
    '/stop': 'остановить бота ',
    '/commands': 'вывести все команды'
    } #done!

@bot.message_handler(commands=['start']) #done!
def send_start_mess(message):
    name_user = message.from_user.first_name
    description = '\nКомандами ниже ты можешь создать свои собственные путеводные звезды (недели) или выбрать уже готовые варианты. ' +\
                  'Раз в неделю, я буду объявлять тему недели, которая будет поводом разбавить ваше общение в чате чем-то новым.\n'
    command_mess = description + '\n /category - ' + commands['/category']\
                               + '\n /set_category - ' + commands['/set_category'] \
                               + '\n /about - ' + commands['/about'] \
                               + '\n /commands -' + commands['/commands']
    bot.send_message(message.chat.id, "\nПривет," + name_user + "!\n" + command_mess)

@bot.message_handler(commands=['commands']) #done!
def show_it(message):
    bot.send_message(message.chat.id, 'Здесь все команды для работы со мной - Великим Астрологом:\n'
                     + '/start - ' + commands['/start']
                     + '\n /category - ' + commands['/category']
                     + '\n /set_category - ' + commands['/set_category']
                     + '\n /about - ' + commands['/about']
                     + '\n /default -' + commands['/default']
                     + '\n /stop - ' + commands['/stop'])

@bot.message_handler(commands=['category']) #done!
def category_default_list(message):
    cat_list = open("category_list.txt", "rb").read()
    bot.send_message(message.chat.id, cat_list)

@bot.message_handler(commands=['about']) #done!
def about_us(message):
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    bot.send_message(message.chat.id, "ABOUT US\n" + url)

#default category commands
# schedule
# done!
def default_category(chat_id) -> None:
    bot.send_message(chat_id, random.choices(psychologic_week))

@bot.message_handler(commands=['default'])
def send_default(message):
    schedule.every(3).seconds.do(default_category, message.chat.id).tag(message.chat.id)

@bot.message_handler(commands=['stop'])
def unset_timer(message):
    schedule.clear(message.chat.id)
    bot.send_message(message.chat.id, 'Вы остановили текущую категорию\n Чтобы выбрать другие темы - /category')

@bot.message_handler(commands=['bye']) # done!
def goodbye(message):
    bot.send_message(message.chat.id, 'Пока! :(')
    bot.leave_chat(message.chat.id)

# it's checking for me if script start
co = [2,4,5,6,7,8,9]
for i in co:
    print(i)
    if i == 7:
        break

if __name__ == '__main__':
    threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
    while True:
        schedule.run_pending()
        time.sleep(1)
