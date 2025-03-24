import requests
import telebot
from telebot import types
import time
import random
import requests
import re
from peewee import *
import datetime
import calendar
import threading
from web3 import Web3

Token = '7734870298:AAHcEohsz-0fdZRKndROLTLUcnWIS1vwuA0'
root = telebot.TeleBot(Token)

chat = -1002364115755
thread_id = 12494

k = 0
db = SqliteDatabase('fofa.sqlite')


def randomfr(username):
    lista = [f'👍 @{username}, твой лимит восстановлен – запрашивай токены снова.',
             f'✨ @{username}, лимит пополнен, можешь снова брать токены.',
             f'✅ @{username}, лимит обновлён, жми на запрос токенов.',
             f'🚀 @{username}, лимит восстановлен – пора за новыми токенами!',
             f'🎉 @{username}, лимит токенов вернулся, запроси их прямо сейчас.']
    return lista[random.randrange(0, len(lista))]


def web3(address):
    return str(Web3.to_checksum_address(address))


class MoonveilFaucet:
    def __init__(
            self,
            rpc: str = "https://faucet.testnet.moonveil.gg/api/claim",
            address: str = "",
            proxy=None
    ):
        self.rpc = rpc
        self.address = address
        self.proxy = proxy

    def classic(self):
        url = f'{self.rpc}'
        json_data = {
            'address': self.address
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Referer': 'https://faucet.testnet.moonveil.gg/',
            'Content-Type': 'application/json',
            'Origin': 'https://faucet.testnet.moonveil.gg',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'DNT': '1',
            'Priority': 'u=0',
            'TE': 'trailers'}

        request = requests.post(url, json=json_data, headers=headers,
                                proxies={'http': self.proxy, 'https': self.proxy}).json()
        return request["msg"]


class research:
    def reserch_user(userId):
        for user in Person.select().where(Person.userId == userId):
            return user.point

    def reserch_user2(userId):
        for user in SecondSeason.select().where(SecondSeason.userId == userId):
            return user.point2

    def nextdata(userId):
        for user in SecondSeason.select().where(SecondSeason.userId == userId):
            return user.nextsend

    def delandcreat(userId):
        point1 = research.reserch_user(userId)
        point2 = research.reserch_user2(userId)
        print(point1, point2)
        obj = SecondSeason.get(SecondSeason.userId == userId)
        print(obj)
        if obj != None:
            print("afafaf")
            obj.delete_instance()
            SecondSeason.create(userId=userId, lastsend=calendar.timegm(time.gmtime()),
                      nextsend=calendar.timegm(time.gmtime()) + 86400, point1=point1, point2=point2+1)
        else:
            print('sex')
            SecondSeason.create(userId=userId, lastsend=calendar.timegm(time.gmtime()),
                      nextsend=calendar.timegm(time.gmtime()) + 86400, point1=point1, point2=point2+1)



    def povrors(userId):
        h = []
        for person in SecondSeason.select().where(SecondSeason.userId == userId):
            h.append(person.userId)
            if len(h) > 1:
                obj = SecondSeason.get(SecondSeason.userId == userId)
                obj.delete_instance()

    def firstseason(userId):
        for person in Person.select().where(Person.userId == userId):
            return person.point


class Person(Model):
    userId = IntegerField()
    lastsend = IntegerField()
    nextsend = IntegerField()
    point = IntegerField()

    class Meta:
        database = db


class Timeframe(Model):
    lastsend = IntegerField()
    nextsend = IntegerField()
    userId = IntegerField()

    class Meta:
        database = db

class SecondSeason(Model):
    userId = IntegerField()
    lastsend = IntegerField()
    nextsend = IntegerField()
    point1 = IntegerField()
    point2 = IntegerField()
    class Meta:
        database = db


def profile1(message):
    get_user_id = message.from_user.id
    for time in SecondSeason.select().where(SecondSeason.userId == get_user_id):
        user_next_send = time.nextsend

    if user_next_send != None:
         time_now = int(time.time())
         whole_second = user_next_send - time_now
         if whole_second > 0:
            time_now = str(datetime.timedelta(seconds=whole_second))
            time_hours = time_now.split(':')[0]
            time_minutes = time_now.split(':')[1]
    def glagol():
        if time_hours == 1:
            glag = ' час '
        if time_hours == 2 or time_hours == 3 or time_hours == 4 or time_hours == 21 or time_hours == 22 or time_hours == 23:
            glag = ' часа '
        else:
            glag = ' часов '
        return glag

    def glagol1():
        if int(time_minutes)%10==0:
            minu = ' минут '
        if int(time_minutes)%10==1 and int(time_minutes)!=11:
            minu = ' минуту '
        if 5 <= int(time_minutes) <= 20:
            minu = ' минут '
        if int(time_minutes)%10==5 or int(time_minutes)%10==6 or int(time_minutes)%10==7 or int(time_minutes)%10==8 or int(time_minutes)%10==9:
            minu = ' минут '
        else:
            minu = ' минуты '
        return minu

    first_points = research.reserch_user(get_user_id)
    second_points = research.reserch_user2(get_user_id)

    ret = f'🆔 ID {get_user_id}\n1️⃣Запросов 1 сезон: {first_points}\n2️⃣Запросов 2 сезон: {second_points}\n\nСледующий запрос: через {time_hours} {glagol()} {time_minutes} {glagol1()}' 
    return ret



def leaderboard1(message):
    f = ''
    chat_id = message.chat.id
    k = 0
    after = 0
    undo = []
    for person in SecondSeason.select().order_by(SecondSeason.point2.desc()):
        k += 1
        userId = person.userId
        UsrInfo = root.get_chat_member(chat_id, userId).user.username
        undo.append(person.point2)
        if k >= 11 and undo[k - 1] != undo[k - 2]:
            break
        if k >= 11 and undo[k - 1] == undo[k - 2]:
            kol = person.point2
            after += 1
            continue
        f = f + str(k) + f'. @{UsrInfo} — ' + str(person.point2) + ' запрос.\n'

    if after != 0:
        f += f'+{str(after)} пользователей с {kol} запросами'
        return f
    else:
        return f


def print_numbers():
    while True:
        for user in Timeframe.select():
            userId = user.userId
            if user.nextsend <= calendar.timegm(time.gmtime()):
                UsrInfo = root.get_chat_member(userId, userId).user.username
                text = randomfr(UsrInfo)
                root.send_message(chat, f"{text}", message_thread_id=thread_id)
                q = Timeframe.delete().where(Timeframe.userId == userId)
                q.execute()
        time.sleep(60)


thread = threading.Thread(target=print_numbers)
thread.start()

file = open('proxys')
prox = file.readline()
db.create_tables([Person, Timeframe, SecondSeason])

@root.message_handler(commands=['profile'])
def profile(message):
    try:
        h = profile1(message)
        root.reply_to(message, f"👤 <b>Профиль</b>\n\n{h}")
    except Exception as e:
        print(e)



@root.message_handler(commands=['leaderboard'])
def leaderboard2(message):
    try:
        h = leaderboard1(message)
        root.reply_to(message, f'🔥<b>Таблица лидеров:</b>\n{h}', parse_mode='HTML')
    except Exception as e:
        print(e)


@root.message_handler(content_types=['text'])
def address(message):
    try:
        global chat_id
        chat_id = message.chat.id
        print(chat_id)
        message_id = int(message.from_user.id)
        print(message_id)
        address = message.text
        trueadd = web3(str(address))
        for i in range(4):
            result = MoonveilFaucet(proxy=prox, address=trueadd)
            more = result.classic()
            if more != 'invalid address':
                if more.split()[0] == "Txhash:":
                    print(research.reserch_user2(message_id))
                    if research.reserch_user2(message_id) == None:
                        g = research.firstseason(message_id)
                        if g!=None:
                            point1 = g
                            SecondSeason.create(userId=message_id, lastsend=calendar.timegm(time.gmtime()),
                                     nextsend=calendar.timegm(time.gmtime()) + 86400, point1=point1, point2=1)
                            root.reply_to(message,
                                      f"<b>✅ Токены успешно отправлены на указанный адрес!</b>\n\nТранзакция: <a href='https://blockscout.testnet.moonveil.gg/tx/{more.split()[1]}'>Moonveil Explorer»</a>\n\n<b>💎 Статистика по сезонам</b>\n1⃣ Первый: {str(research.reserch_user(message_id))} запрос\n2⃣ Второй: {str(research.reserch_user2(message_id))} запрос",
                                      parse_mode='HTML')
                        else:
                            SecondSeason.create(userId=message_id, lastsend=calendar.timegm(time.gmtime()),
                                     nextsend=calendar.timegm(time.gmtime()) + 86400, point1=0, point2=1)
                            root.reply_to(message,
                                      f"<b>✅ Токены успешно отправлены на указанный адрес!</b>\n\nТранзакция: <a href='https://blockscout.testnet.moonveil.gg/tx/{more.split()[1]}'>Moonveil Explorer»</a>\n\n<b>💎 Статистика по сезонам</b>\n1⃣ Первый: 0 запрос\n2⃣ Второй: {str(research.reserch_user2(message_id))} запрос",
                                      parse_mode='HTML')
                            
                        Timeframe.create(lastsend=calendar.timegm(time.gmtime()),
                                         nextsend=calendar.timegm(time.gmtime()) + 86400, userId=int(message_id))


                        break
                    else:
                        if research.nextdata(message_id) <= calendar.timegm(time.gmtime()):
                            research.delandcreat(message_id)
                            research.povrors(message_id)
                            Timeframe.create(lastsend=calendar.timegm(time.gmtime()),
                                             nextsend=calendar.timegm(time.gmtime()) + 86400, userId=int(message_id))
                            if research.reserch_user(message_id) != None:
                                root.reply_to(message,
                                      f"<b>✅ Токены успешно отправлены на указанный адрес!</b>\n\nТранзакция: <a href='https://blockscout.testnet.moonveil.gg/tx/{more.split()[1]}'>Moonveil Explorer»</a>\n\n<b>💎 Статистика по сезонам</b>\n1⃣ Первый: {str(research.reserch_user(message_id))} запрос\n2⃣ Второй: {str(research.reserch_user2(message_id))} запрос",
                                      parse_mode='HTML')
                            else:
                                root.reply_to(message,
                                      f"<b>✅ Токены успешно отправлены на указанный адрес!</b>\n\nТранзакция: <a href='https://blockscout.testnet.moonveil.gg/tx/{more.split()[1]}'>Moonveil Explorer»</a>\n\n<b>💎 Статистика по сезонам</b>\n1⃣ Первый: 0 запрос\n2⃣ Второй: {str(research.reserch_user2(message_id))} запрос",
                                      parse_mode='HTML')



                            break
                        else:
                            
                            if research.reserch_user(message_id) != None:
                                root.reply_to(message,
                                      f"<b>✅ Токены успешно отправлены на указанный адрес!</b>\n\nТранзакция: <a href='https://blockscout.testnet.moonveil.gg/tx/{more.split()[1]}'>Moonveil Explorer»</a>\n\n<b>💎 Статистика по сезонам</b>\n1⃣ Первый: {str(research.reserch_user(message_id))} запрос\n2⃣ Второй: {str(research.reserch_user2(message_id))} запросц",
                                      parse_mode='HTML')
                            else:
                                root.reply_to(message,
                                      f"<b>✅ Токены успешно отправлены на указанный адрес!</b>\n\nТранзакция: <a href='https://blockscout.testnet.moonveil.gg/tx/{more.split()[1]}'>Moonveil Explorer»</a>\n\n<b>💎 Статистика по сезонам</b>\n1⃣ Первый: 0 запрос\n2⃣ Второй: {str(research.reserch_user2(message_id))} запрос",
                                      parse_mode='HTML')


                            break
                if more.split()[0] != "Txhash":
                    continue
        if more != 'invalid address':
            if more.split()[0] == "Txhash:":
                pass

            elif more.split()[0] == "You":
                otvet = re.findall(r'\d+', more.split()[8])
                if len(otvet) == 3:
                    root.reply_to(message,
                                  f"🤷‍♂️ Cегодня вы уже запрашивали токены, пожалуйста вернитесь через <b>{otvet[0]}</b> часа <b>{otvet[1]}</b> минут и заново их запросите.",
                                  parse_mode='HTML')
                else:
                    root.reply_to(message,
                                  f"🤷‍♂️ Cегодня вы уже запрашивали токены, пожалуйста вернитесь через <b>{otvet[0]}</b> минут и заново их запросите.",
                                  parse_mode='HTML')

            elif more.split()[0] == "Request":
                pass

            else:
                root.reply_to(message, f"🙅‍♂️ <b>Ошибка крана, повторите позже!</b>", parse_mode='HTML')
        else:
            pass

    except Exception as e:
        print(e)


root.infinity_polling(none_stop=True)
