# Import python telegram bot  
import telebot 
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton 
 
# Import Api KEY 
from dotenv import load_dotenv 
import os 

load_dotenv() 
API_KEY = os.getenv('API_KEY') 
# Creation of telegram bot 
bot = telebot.TeleBot(API_KEY) 
 
@bot.message_handler(commands=['exit'])
def exit(message):
    bot.send_message(message.chat.id, "Exit") 

#Start command 
@bot.message_handler(commands=['help']) 
def send_welcome(message): 
    bot.reply_to(message, "/Start to start")

@bot.message_handler(commands=['start']) 
def send_welcome(message): 
    bot.reply_to(message, "Welcome to SplitYourMoneyLahBot") 
    bot.reply_to(message, "Choose one of the options", reply_markup=displayOptions()) 

 
#display Options 
def displayOptions(): 
    markup = InlineKeyboardMarkup() 
    markup.row_width = 1 
    markup.add(InlineKeyboardButton("Create Expenses", callback_data="create_expense"), 
                               InlineKeyboardButton("Return Money", callback_data="return_money")) 
    return markup 
 
@bot.callback_query_handler(func=lambda call: True) 
def callback_query(call): 
    if call.data == "create_expense": 
        inputExpenseName(call.message) 
    elif call.data == "return_money": 
        bot.answer_callback_query(call.id, "You Clicked Return Money") 
 
temp = {}
     
@bot.message_handler() 
def inputExpenseName(message): #input expense name 
    print("First message is " + message.text)
    msg = bot.send_message(message.chat.id, "Enter Name of Expense") 
    bot.register_next_step_handler(msg, inputAmt)
    #temp.append(message.text)

def inputAmt(message): 
    temp["Name"] = message.text#text is from inputexpense
    print(temp)
    msg = bot.send_message(message.chat.id, "Enter Amount before Tax") 
    bot.register_next_step_handler(msg, Paymentmethod)

def Paymentmethod(message): 
    temp["Cost"] = message.text#text is from inputexpense
    print(temp)
    msg = bot.send_message(message.chat.id, "Even or manually") 
    bot.register_next_step_handler(msg, numberofpeople)

def numberofpeople(message):
	temp["even or manual"] = message.text
	print(temp)
	msg = bot.send_message(message.chat.id, "Number of people?")
	bot.register_next_step_handler(msg, peoplename)
	# print(type(message.text))
	# int_msg = int(message.text)
	# if int_msg.isnumeric():
	# 	bot.register_next_step_handler(msg, people)
	# else:
	# 	msg = bot.send_message(message.chat.id, "Invalid input!!!")
	# 	bot.register_next_step_handler(msg, numberofpeople)

def peoplename(message):
	# temp["number of people"] = message.text
	# print(type(message.text))
	#int_msg = int(message.text)
	if message.text.isnumeric():
		temp["number of people"] = message.text
		print(type(message.text))
		bot.register_next_step_handler(msg, people)
		# temp["number of people"] = message.text
		# print(type(message.text))
	else:
		msg = bot.send_message(message.chat.id, "Invalid input!!!")
		bot.register_next_step_handler(msg, numberofpeople)

	

def people(message): 
    temp["Payment method"] = message.text
    print(temp)
    msg = bot.send_message(message.chat.id, "name pls")




bot.polling()