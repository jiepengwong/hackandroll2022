# ChaT iD  -781874170


# Import python telegram bot 
import telebot

from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import apihelper
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
apihelper.ENABLE_MIDDLEWARE = True


# Import Api KEY
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')
# Creation of telegram bot
bot = telebot.TeleBot(API_KEY)
import csv


# Data to store the people that own people money

people = ["a","b"]

#  After "Return money" is clicked
# Simulate using /pay

@bot.message_handler(commands=['pay'])
def payment(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    for i in people:
        text = f"/returnMon {i}"
        markup.row(text)
    bot.reply_to(message, 
    """Welcome to the payments section, 

Please Choose the person which you want to pay using the replyMarkUp keyboard below.
    """, reply_markup=markup)




# returnMoney
@bot.message_handler(commands=['returnMoney'])
def returnMon(message):
    print(message)

    
    text = message.text
    # Get the name of the person 
    personName = text.split()
    print(personName)

    bot.send_message(message.chat.id,"Your transaction has been updated in the database! ")
    # Connect to database







    
        


        

    

	





# def command_time(m):
#     text = m.text
#     chatid = m.chat.id
#     print(text) 
#     a = checkFormat(text)
#     print(a)
#     if a != True:
#         bot.send_message(chatid, "Wrong Format!")
#         return
#     else:
#         appt.append(text)
#         msg = bot.send_message(chatid, "What is the time of the appointment? Example:1200")
#         bot.register_next_step_handler(msg, command_des)




# Start command
# PAY command select individual to pay to
# selectedPerson = ['jpoggers','cygay']
# @bot.message_handler(content_types=['image'])
# def photoValidation(person):
#     print(person)
#     return "hi"

# # /pay @jpoggers
# @bot.message_handler(commands=['pay'])
# def lol(message):
#     markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
#             # From database now is just dummy data
#     for person in selectedPerson:
#         markup.add(person)
#     msg = bot.reply_to(message, 'These are the people which you owe money to Jppoggers - 25, cy - 50, selected 1 which you wish to pay ')
#     bot.register_next_step_handler(msg, process_choose_step)



# @bot.message_handler(func=lambda m: True)
# def process_choose_step(message):


#         chat_id = message.chat.id
#         msg = message.text
#         bot.send_message(message, 'Nice to meet you ')


            # if (msg== u'jpoggers') or (msg == u'cygay'):

            #     bot.send_message(message, 'Nice to meet you ')

     
        



# def process_select_user_step(message):
    




# def gen_markup():
#     markup = InlineKeyboardMarkup()
#     markup.row_width = 2

#     for people in selectedPerson:
#          markup.add(InlineKeyboardButton(people, callback_data=people))    
        
#     return markup
# #callback function?


# @bot.callback_query_handler(func=lambda call: True)
# def callback_query(call):
#     for people in selectedPerson:

#         if call.data == people:
#             msg = bot.reply_to(cal, 'Please send a picture to confirm payment')
#             bot.answer_callback_query(call.id, msg)
#             bot.register_next_step_handler(msg, process_picture_step)
#             break
#         elif call.data == "cb_no":
#             bot.answer_callback_query(call.id, "Answer is No")



# def process_picture_step(message):
#     try:
#          chat_id = message.chat.id
#          name = message.text
#          bot.send_message(message.chat, 'paid')
#     except:
#         bot.reply_to(message, "lol")



bot.infinity_polling()
