# Import python telegram bot 
import telebot

# Import Api KEY
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')
# Creation of telegram bot
bot = telebot.TeleBot(API_KEY)

# Start command
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Welcome to SplitYourMoneyLahBot")



# Check for messages
bot.polling() #hello world