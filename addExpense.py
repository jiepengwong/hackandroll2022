# Import python telegram bot  
import telebot 
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
 
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
    markup.row_width = 2 
    markup.add(InlineKeyboardButton("Create Expenses", callback_data="create_expense"), 
                               InlineKeyboardButton("Return Money", callback_data="return_money")) 
    return markup 
 
@bot.callback_query_handler(func=lambda call: True) 
def callback_query(call): 
    if call.data == "create_expense": 
        startCreateExpense(call.message) 
    elif call.data == "return_money": 
        bot.answer_callback_query(call.id, "You Clicked Return Money")

temp = {}
dictOfDebtors = {}

def startCreateExpense(message):
    msg = bot.send_message(message.chat.id, "Enter Name of Expense") 
    bot.register_next_step_handler(msg, handleExpenseName)

def averageBills():
    return temp["totalAmtAfterTax"] / temp["totalNumofPpl"]


def printSummary(message):
    for key in temp:
        if(key == "whoOweYou"):
            strWhoOweYou = ",".join(temp[key])
            msg = bot.send_message(message.chat.id, key +" "+strWhoOweYou)
        elif(key == "totalAmtAfterTax"):
            msg = bot.send_message(message.chat.id, key +" "+"{:.2f}".format(temp[key]))
        
        elif(type(temp[key]) == int):
            msg = bot.send_message(message.chat.id, key +" "+str(temp[key]))
        else:
            print(key,temp[key])
            msg = bot.send_message(message.chat.id, key +" "+temp[key])
        
    for key1 in dictOfDebtors:
        for key2 in dictOfDebtors[key1]:
            msg = bot.send_message(message.chat.id, key2 +" owes "+key1 +" $"+"{:.2f}".format(dictOfDebtors[key1][key2]))


@bot.message_handler() 
def handleExpenseName(message): #input expense name 
    temp["expenseName"] = message.text
    msg = bot.send_message(message.chat.id, "Enter Expense Amount Before Taxes") 
    bot.register_next_step_handler(msg, handleInputAmt)

def handleInputAmt(message): 
    temp["totalAmtBeforeTax"] = int(message.text)
    msg = bot.send_message(message.chat.id, "Enter who owe you (eg @cy, @jp)")
    print(msg)
    bot.register_next_step_handler(msg, handleWhoOweYou)


def handleWhoOweYou(message): 
    listOfWhoOweYou = message.text.split(",");
    temp["whoOweYou"] = listOfWhoOweYou
    temp["totalNumofPpl"] = len(listOfWhoOweYou) + 1
    splitMethodOptions(message)

def splitMethodOptions(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row("Evenly")
    markup.row("Manually")
    msg = bot.send_message(message.chat.id,"do you want to split evenly or manually?", reply_markup=markup)
    bot.register_next_step_handler(msg, handleSplitMethod)

def handleSplitMethod(message):
    temp["splitMethod"] = message.text
    msg = bot.send_message(message.chat.id, "Enter GST and Taxes if any (eg 17 for 17%), 0 otherwise")
    bot.register_next_step_handler(msg, handleGSTandTax)

def handleGSTandTax(message):
    temp["gstAndTax"] = int(message.text)
    totalamtAfterTax = temp["totalAmtBeforeTax"]
    multipler = 1 + temp["gstAndTax"]/100
    totalamtAfterTax = round(temp["totalAmtBeforeTax"] *  multipler, 2) 
    temp["totalAmtAfterTax"] = totalamtAfterTax
    handleSplitBills(message)
    

def handleSplitBills(message):
    avgbill = float(averageBills())
    your_username = "@"+ message.from_user.username
    dictOfDebtors[your_username] = {}

    for name in temp["whoOweYou"]:
        dictOfDebtors[your_username][name] = avgbill

    printSummary(message)

bot.polling()