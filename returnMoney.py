# Import python telegram bot  
import telebot 
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from db import *
# Import Api KEY 
from dotenv import load_dotenv 
import os 

load_dotenv() 
API_KEY = os.getenv('API_KEY') 
# Creation of telegram bot 
bot = telebot.TeleBot(API_KEY) 

people = ["a", "b"]
 
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
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row("/createExpense")
    markup.row("/payments")
   
    return markup 
 
@bot.callback_query_handler(func=lambda call: True) 
def callback_query(call): 
    if call.data == "create_expense": 
        startCreateExpense(call.message) 
    elif call.data == "return_money": 
        msg = bot.send_message(call.message.chat.id, "Type /pay to start")

        bot.answer_callback_query(call.id, msg)
        

temp = {}
# Return Money
@bot.message_handler(commands=['payments'])
def payment(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    for i in people:
        text = f"/returnMoney {i}"
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





# Create expense

@bot.message_handler(commands=['createExpense'])
def startCreateExpense(message):
    msg = bot.send_message(message.chat.id, "Enter Name of Expense") 
    bot.register_next_step_handler(msg, handleExpenseName)


def printSummary(message):
    print(temp)
    emptyString = ""
    for key,value in temp.items():
        print(key)
        print(value)
        emptyString += f"{key}: {value} \n"
        # if(key == "whoOweYou"):
        #     strWhoOweYou = ",".join(temp[key])
        #     msg = bot.send_message(message.chat.id, key +" "+strWhoOweYou)
        # elif(key == "totalAmtAfterTax"):
        #     msg = bot.send_message(message.chat.id, key +" "+str(temp[key]))
        
        # elif(type(temp[key]) == int):
        #     msg = bot.send_message(message.chat.id, key +" "+str(temp[key]))
        # else:
        #     print(key,temp[key])
    
    

    bot.send_message(message.chat.id,emptyString)
        

        

def handleExpenseName(message): #input expense name 
    print(message)
    temp["owner"] = [message.from_user.id,message.from_user.username] 
    temp["listing"] = message.text
    msg = bot.send_message(message.chat.id, "Enter Expense Amount Before Taxes") 
    bot.register_next_step_handler(msg, handleInputAmt)

def handleInputAmt(message): 
    temp["total"] = int(message.text)
    msg = bot.send_message(message.chat.id, "Enter your FRIEND thats owe you money, it can multiple , just seperate using a space, using the desired username (eg Chun_yangg jpoggers") 
    bot.register_next_step_handler(msg, handleWhoOweYou)


def handleWhoOweYou(message): 
    listOfWhoOweYou = message.text.split()
    temp["listing"] = listOfWhoOweYou
    temp["totalNumofPpl"] = len(listOfWhoOweYou) + 1
    splitMethodOptions(message)

def splitMethodOptions(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row("Evenly")
    markup.row("Manually")
    msg = bot.send_message(message.chat.id,"Do you want to split evenly or manually?", reply_markup=markup)
    bot.register_next_step_handler(msg, handleSplitMethod)

def handleSplitMethod(message):
    temp["splitMethod"] = message.text

    if temp["splitMethod"] == "Evenly":
        temp["payableAmount"] = temp["total"] / (len(temp['listing']) + 1)
        for i in temp["listing"]:
            new_owe_instance = {
                'name': i,
                'status': "OWE",
                'money': temp["payableAmount"],
                "oweto": message.from_user.username,
                "lendto": "-"
            }
            new_lend_instance = {
                 'name': message.from_user.username,
                'status': "LEND",
                'money': temp["payableAmount"],
                "oweto": "-",
                "lendto": i

            }
            records.insert_one(new_owe_instance)    
            records.insert_one(new_lend_instance)    


            

            
            
        msg = bot.send_message(message.chat.id, "Summary")
        printSummary(message)
        return


    elif temp["splitMethod"] == "Manually":
        
        msg = bot.send_message(message.chat.id, """
        You have selected manualy, please type the specific amount people owe you such as... 
(E.g jp:50,cy:50)
        """)
        bot.register_next_step_handler(msg,handleManualSplit)

def handleManualSplit(message):
    temp["payableAmount"] = {}

    test = message.text 
    testArray = message.text.split(",")


    for person in testArray:
        details = person.split(":")
        temp["payableAmount"][details[0]] = details[1]



        new_owe_instance = {
            'name': person,
            'status': "OWE",
            'money': temp["payableAmount"][details[0]],
            "oweto": message.from_user.username,
            "lendto": "-"
            }
        new_lend_instance = {
            'name': message.from_user.username,
            'status': "LEND",
            'money': temp["payableAmount"][details[0]],
            "oweto": "-",
            "lendto": person

        }

        
        records.insert_one(new_owe_instance)    
        records.insert_one(new_lend_instance)    


    msg = bot.send_message(message.chat.id, "Summary")
    printSummary(message)



# def handleGSTandTax(message):
#     temp["gstAndTax"] = int(message.text)
#     totalamtAfterTax = temp["totalAmtBeforeTax"]
#     multipler = 1 + temp["gstAndTax"]/100
#     totalamtAfterTax = round(temp["totalAmtBeforeTax"] *  multipler, 2) 
#     temp["totalAmtAfterTax"] = totalamtAfterTax
#     handleSplitBills(message)
    

def handleSplitBills(message):
    print("hi i am rendered")
    printSummary(message)







bot.polling()