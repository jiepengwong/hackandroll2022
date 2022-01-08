# Import python telegram bot
from enum import unique
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from db import *
# Import Api KEY
from dotenv import load_dotenv
from bson.objectid import ObjectId

import os

load_dotenv()
API_KEY = os.getenv('API_KEY')
# Creation of telegram bot
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['list'])
#  Get all owe and lent amount from database
def getList(message):
    queryUserId = message.from_user.username
    queryDatabase = {"name": queryUserId}
    verdict = records.find(queryDatabase)
    infoDict = {}
    lendArr = []
    oweArr = []
    updatemsg = ""

    # Generating the message to send
    for result in verdict:

        if (result["status"] == "LEND"):
            lendArr.append(result)
        else:
            oweArr.append(result)

    updatemsg += "LENDINGS \n"

    for lendlistings in lendArr:
        updatemsg += f"{lendlistings['lendto']} - {lendlistings['money']} \n"

    updatemsg += "OWNINGS \n"

    for owelistings in oweArr:
        updatemsg += f"{owelistings['oweto']} - {owelistings['money']} \n"

    bot.send_message(message.chat.id, updatemsg)


def exit(message):
    bot.send_message(message.chat.id, "Exit")


@bot.message_handler(commands=['exit'])
def exit(message):
    bot.send_message(message.chat.id, "Exit")

# Start command


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "/Start to start")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to SplitYourMoneyLahBot")
    bot.reply_to(message, "Choose one of the options",
                 reply_markup=displayOptions())


# display Options
def displayOptions():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row("/createExpense")
    markup.row("/payments")
    return markup


temp = {}
tempObjectID = ""
# Return Money


@bot.message_handler(commands=['payments'])
def payment(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    #  Start query to data base here
    #  Check data base for instance structure
    usernameid = message.from_user.username
    # Query the columns
    myquery = {"name": usernameid, "status": "OWE"}
    verdict = records.find(myquery)

    # Find out who the user owes in a particular telegram group
    peopleDict = {}
    for result in verdict:
        # Name : ID
        # print(result['_id'])
        peopleDict[result['oweto']] = result["_id"]

    # Passing unique id via text through replyMarkUpKeyboard

    for key, value in peopleDict.items():
        text = f"/returnMoney {key} id={value}"
        markup.row(text)
    bot.reply_to(message,
                 """Welcome to the payments section,
Please Choose the person which you want to pay using the replyMarkUp keyboard below.
    """, reply_markup=markup)


# returnMoney
@bot.message_handler(commands=['returnMoney'])
def returnMon(message):

    # Query the user id here.

    print(message)

    text = message.text
    # Get the name of the person that you are paying back to
    personName = text.split()
    print(personName)

    usernameid = message.from_user.username
    # Setting up query
    myquery = {"name": usernameid, "status": "OWE", "oweto": personName[1]}

    uniqueid = personName[len(personName) - 1][3:]
    print(uniqueid)

    querydelete = {"_id": uniqueid}

    # Delete unique ID from owe list
    records.delete_one({"_id": ObjectId(uniqueid)})

    bot.send_message(
        message.chat.id, "Your transaction has been updated in the database! ")

# Create expense


@bot.message_handler(commands=['createExpense'])
def startCreateExpense(message):
    msg = bot.send_message(message.chat.id, "Enter Name of Expense")
    bot.register_next_step_handler(msg, handleExpenseName)

# {'owner': [861768079, 'Wkaggin'], 'listing': ['cy', 'jp'],
# 'total': 100, 'totalNumofPpl': 3, 'splitMethod': 'Evenly', 'payableAmount': 33.333333333333336}


def text(data):  # @Wkaggin owes @Chun_yangg $117.00 @jpoggers owes @Chun_yangg $117.00
	list = []
	# sum = "@"+ str(data['owner'][1]) + " owes "
	if data['splitMethod'] == 'Manually':
		for value in data['listing']:
			sumstate = "@" + value + " owes"  + " $" + str(data['payableAmount'][value]) + " to " + "@" + data['owner'][1]
			list.append(sumstate)
			sumstate = ""
	else:
		for value in data['listing']:
			roundoff = round(data['payableAmount'], 2)
			sumstate = "@" + value + " owes"  + " $" + str(roundoff) + " to " + "@" + data['owner'][1]
			list.append(sumstate)
			sumstate = ""
		return list


def printSummary(message):
    print(temp)
   # emptyString = ""
   # for key,value in temp.items():
    # print(key)
    # print(value)
    # emptyString += f"{key}: {value} \n"
    # if(key == "whoOweYou"):
    #     strWhoOweYou = ",".join(temp[key])
    #     msg = bot.send_message(message.chat.id, key +" "+strWhoOweYou)
    # elif(key == "totalAmtAfterTax"):
    #     msg = bot.send_message(message.chat.id, key +" "+str(temp[key]))

    # elif(type(temp[key]) == int):
    #     msg = bot.send_message(message.chat.id, key +" "+str(temp[key]))
    # else:
    #     print(key,temp[key])
    data = text(temp)
    for m in data:
        bot.send_message(message.chat.id, str(m))
    # bot.send_message(message.chat.id,emptyString)


def handleExpenseName(message):  # input expense name
    print(message)
    temp["owner"] = [message.from_user.id, message.from_user.username]
    temp["listing"] = message.text
    msg = bot.send_message(
        message.chat.id, "Enter Expense Amount Before Taxes")
    bot.register_next_step_handler(msg, handleInputAmt)


def handleInputAmt(message):
    temp["total"] = int(message.text)
    msg = bot.send_message(
        message.chat.id, "Enter your FRIEND thats owe you money, it can multiple , just seperate using a space, using the desired username (eg Chun_yangg jpoggers")
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
    msg = bot.send_message(
        message.chat.id, "Do you want to split evenly or manually?", reply_markup=markup)
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
        bot.register_next_step_handler(msg, handleManualSplit)


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