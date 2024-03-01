from typing import Final
from typing import Final
from telegram import Update, Bot, ReplyKeyboardMarkup
from telegram.ext import (
  Updater,
  CommandHandler,
  CallbackContext,
  MessageHandler,
  filters
)

import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from req import get_data
from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler


api_data_about_us = get_data()

async def data_handler(json_api):
    results = []
    for json_data in json_api:
        name = json_data['name']
        description = json_data['description']
        ans = "Our title is " + name + " and our description is " + description
        results.append(ans)
    return results


#my bot
bot = Bot(token="")
BOT_USERNAME: Final = ''

#buttons
start_keyboard = [['👨‍💻دوره ها👩‍💻', 'خدمات 🌐'], ['درباره من ℹ️','ارتباط با من 🆔'], ['چگونه با من آشنا شدی 📱']]

courses_keyboard = [['بازگشت ⬅️'], ['1⃣', '2⃣']]

inner_keyboard = [['بازگشت ⬅️']]


#Command answers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  markup = ReplyKeyboardMarkup(start_keyboard, resize_keyboard=True)
  await update.message.reply_text('سلام به ربات ما خوش آمدید. لطفا یک دکمه را انتخاب کنید.', reply_markup=markup)

async def courses_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  markup = ReplyKeyboardMarkup(courses_keyboard, resize_keyboard=True)
  await update.message.reply_text('کورس هامون به دو دسته ی اول و دوم تقسیم میشن. از بین کلیدهای زیر کورس مورد نظر خودتون رو انتخاب کنید.', reply_markup=markup)


async def nextron_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  markup = ReplyKeyboardMarkup(courses_keyboard, resize_keyboard=True)
  await update.message.reply_text('دسته اول:')
  result = await data_handler(api_data_about_us)
  await update.message.reply_text(result[0], reply_markup=markup)

async def zerotopro_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  markup = ReplyKeyboardMarkup(courses_keyboard, resize_keyboard=True)
  await update.message.reply_text('دسته دوم:')
  result = await data_handler(api_data_about_us)
  await update.message.reply_text(result[1], reply_markup=markup)
  
async def services_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  markup = ReplyKeyboardMarkup(inner_keyboard, resize_keyboard=True)
  await update.message.reply_text('our services', reply_markup=markup)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  markup = ReplyKeyboardMarkup(inner_keyboard, resize_keyboard=True)
  await update.message.reply_text('Parham Shabani, from iran, tehran. Junior developer of python and .net developer', reply_markup=markup)


#******************************************************

array = []
async def meet_us_command(update: Update, context):
    markup = ReplyKeyboardMarkup(inner_keyboard, resize_keyboard=True)
    question = 'از چه طریقی با ربات من آشنا شدی؟ برامون بنویس تا بدونیم 👇'
    await update.message.reply_text(question, reply_markup=markup)
    
    if update.effective_chat.type == 'private':
      text = update.message.text
      array.append(text)
      


async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  markup = ReplyKeyboardMarkup(inner_keyboard, resize_keyboard=True)
  await update.message.reply_text('Contact @prhmshbni', reply_markup=markup)

async def home_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  markup = ReplyKeyboardMarkup(start_keyboard, resize_keyboard=True)
  await update.message.reply_text('⬅️')
  await update.message.reply_text('صفحه اصلی', reply_markup=markup)


async def save_user_messages(update: Update, arr):
  print(arr)
  ignore_messages = ['بازگشت ⬅️', '']
  meet_us = 'چگونه با من آشنا شدی 📱'
  if len(arr) >= 2:
    for i in range(len(arr)):
      if arr[i] == meet_us:
        if arr[i+1] not in ignore_messages:
          await update.message.reply_text("مرسی از جوابت. بوس")
          user_message = arr[i+1]
          with open('messages.txt', 'a', encoding='utf-8') as file:
            file.write(user_message + '\n')   
        
  arr.clear()
  


async def handle_message(update: Update, context: CallbackContext):
  if update.effective_chat.type == 'private':
    text = update.message.text
    print(f'Received message: {text}')
    # Run the courses command
    if text == '👨‍💻دوره ها👩‍💻':
      await courses_command(update, context)

    # Run the nextron command
    elif text == '1⃣':
      await nextron_command(update, context)  
    
    # Run the zerotopro command
    elif text == '2⃣':
      await zerotopro_command(update, context)  
    
    # Run the services command
    elif text == 'خدمات 🌐':
      await services_command(update, context)

    # Run the about command
    elif text == 'درباره من ℹ️':
      await about_command(update, context)
    
    # Run the identify command
    elif text == 'چگونه با من آشنا شدی 📱':
      await meet_us_command(update, context)

    # Run the contact command
    elif text == 'ارتباط با من 🆔':
      await contact_command(update, context)

    # Run the home command
    elif text == 'بازگشت ⬅️':
      await home_command(update, context)

    else:
      array.append(text)
      print(array)
      if len(array) >=2:
        print("hoooo")
        if array[-2] == 'چگونه با من آشنا شدی 📱':
          await save_user_messages(update, array)
        else:
          await update.message.reply_text("Not valid command")   
      else:
        await update.message.reply_text("Not valid command")  


# Error handler
async def error(update: Update, context: CallbackContext):
  print(f'Update {update} caused error {context.error}')




def main():
  app = Application.builder().token(bot.token).build()
  
  #Commands
  app.add_handler(CommandHandler('start', start_command))

  

  # Messages
  app.add_handler(MessageHandler(filters.TEXT, handle_message))


  # Log all errors
  app.add_error_handler(error)



  print('Polling...')
  # Run the bot
  app.run_polling(poll_interval=1)
  



if __name__ == '__main__':
  main()
