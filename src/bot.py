import time
import logging
import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from config.auth import token
from telegram import InlineKeyboardButton, InlineKeyboardMarkup,Sticker,File
import inbox
import send
import sendattch
import urllib.request

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('PiedPiperUCV')

updater = Updater(token=token)
dispatcher = updater.dispatcher

class emailAddress:
        email = ''
        password = ''

class emailData:
        From = ''
        To =  ''
        Subject = ''
        Body = ''
        file_name = ''
        file_url = ''
        

class validations:
        login = [False,False,False]
        sendImail = [False,False,False,False,False]

class iterators:
        min = 0
        max = 10

credentials = emailAddress()

validate = validations()

index = iterators()

data = emailData()

def start(bot, update):
        logger.info('He recibido un comando start')
        hour = int(time.strftime("%H"))
        text = ''
        if hour >= 0 and hour <= 11:
                text="Good Morning!"

        elif hour >= 12 and hour <= 18:
                text="Good Afternoon!"

        elif hour >= 17 and hour <= 23:
                text="Good Evening!"

        keyboard = [[InlineKeyboardButton("Login", callback_data='1'),
                 InlineKeyboardButton("Close", callback_data='8')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(text)
        bot.send_message(chat_id=update.message.chat_id,text='Select an option:',
                              reply_markup=reply_markup)


def Verification(bot, update):
        text = update.message.text
        if not validate.login[2]:
                if not validate.login[0] and not validate.login[1]:
                        if not validate.login[0] and emailVerification(text):
        
                                validate.login[0] = True
                                validate.login[1] = True
                                credentials.email = text
                                bot.send_message(
                                        chat_id=update.message.chat_id,
                                        text='Introduce your password:'
                                )

                        elif not validate.login[0] and not emailVerification(text):
                                bot.send_message(
                                        chat_id=update.message.chat_id,
                                        text='Email invalid!\nIntroduce your email address:'
                                )

                elif validate.login[0] and validate.login[1]:
                        credentials.password = text
                        bot.send_message(chat_id=update.message.chat_id,text='Loading, please wait....')
                        auth = inbox.Authenticator(credentials.email,credentials.password)
                        if auth == 'ok':
                                validate.login[2] = True
                                keyboard = [[InlineKeyboardButton("Inbox", callback_data='4'),
                                InlineKeyboardButton("Send a email", callback_data='5'),InlineKeyboardButton("Logout", callback_data='7')]]
                                reply_markup = InlineKeyboardMarkup(keyboard)
                                newsticker = Sticker(file_id= 'CAADAgAD8wIAApzW5wrgLgRxhQ_BAgI', width= 512, height= 512)
                                bot.send_sticker(chat_id=update.message.chat_id, sticker= newsticker)
                                bot.send_message(chat_id=update.message.chat_id, text='Your login was success')
                                update.message.reply_text('Select an option:',reply_markup=reply_markup)

                        else:
                                validate.login[0] = False
                                validate.login[1] = False
                                credentials.email = ''
                                credentials.password = ''
                                newsticker = Sticker(file_id= 'CAADAgADCAMAApzW5wqTpbtQDP42agI', width= 512, height= 512)
                                bot.send_sticker(chat_id=update.message.chat_id, sticker= newsticker)
                                bot.send_message(chat_id=update.message.chat_id, text='Has been an error')
                                bot.send_message(chat_id=update.message.chat_id,text='Email or password incorrect!')
                                bot.send_message(chat_id=update.message.chat_id,text='Try again!')
                                bot.send_message(chat_id=update.message.chat_id,text='Introduce your email address:')
        elif validate.login[2]:
                print(validate.sendImail)
                contain = update.message.text.find(',') 
                emails = ''
                if contain != -1:
                        emails = update.message.text.split(',')
                else:
                       emails = update.message.text


                if validate.sendImail[0] and not validate.sendImail[1] and not emailVerification(update.message.text):
                        bot.send_message(
                                chat_id=update.message.chat_id,
                                text='Email invalid'
                        )
                        bot.send_message(
                                chat_id=update.message.chat_id,
                                text='From:'
                        )
                
                elif validate.sendImail[0] and validate.sendImail[1] and not validate.sendImail[2] and contain != -1:
                        validation = True
                        for i in range(0,len(emails)):
                                if not emailVerification(emails[i]):
                                        bot.send_message(
                                                chat_id=update.message.chat_id,
                                                text='Email invalid'
                                        )
                                        bot.send_message(
                                                chat_id=update.message.chat_id,
                                                text='To:'
                                        )
                                        validation = False
                                
                        if validation and validate.sendImail[0] and validate.sendImail[1] and not validate.sendImail[2] and not validate.sendImail[3] and not validate.sendImail[4]:
                                validate.sendImail[2] = True
                                data.To = update.message.text
                                bot.send_message(
                                        chat_id=update.message.chat_id,
                                        text='Subject:'
                                )
                                
                elif validate.sendImail[0] and validate.sendImail[1] and not validate.sendImail[2] and not emailVerification(update.message.text):
                        
                        bot.send_message(
                                chat_id=update.message.chat_id,
                                text='Email invalid'
                        )
                        bot.send_message(
                                chat_id=update.message.chat_id,
                                text='To:'
                        )
                else:
                        if validate.sendImail[0] and not validate.sendImail[1] and not validate.sendImail[2] and not validate.sendImail[3] and not validate.sendImail[4]:
                                validate.sendImail[1] = True
                                data.From = update.message.text
                                bot.send_message(
                                        chat_id=update.message.chat_id,
                                        text='To:'
                                )
                        elif validate.sendImail[0] and validate.sendImail[1] and not validate.sendImail[2] and not validate.sendImail[3] and not validate.sendImail[4]:
                                validate.sendImail[2] = True
                                data.To = emails
                                bot.send_message(
                                        chat_id=update.message.chat_id,
                                        text='Subject:'
                                )
                        elif validate.sendImail[0] and validate.sendImail[1] and validate.sendImail[2] and not validate.sendImail[3] and not validate.sendImail[4]:
                                validate.sendImail[3] = True
                                data.Subject = update.message.text
                                bot.send_message(
                                        chat_id=update.message.chat_id,
                                        text='Body:'
                                )
                        elif validate.sendImail[0] and validate.sendImail[1] and validate.sendImail[2] and validate.sendImail[3] and not validate.sendImail[4]:
                                data.Body = update.message.text
                                keyboard = [[InlineKeyboardButton("YES", callback_data='9'),InlineKeyboardButton("NO", callback_data='10')]]
                                reply_markup = InlineKeyboardMarkup(keyboard)
                                bot.send_message(chat_id=update.message.chat_id, text= 'Are you want to send a any file ?',
                                        reply_markup=reply_markup)

                        


                
def emailVerification(email):
        expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
        return re.match(expresion_regular, email) is not None             
        

        
def button(bot, update):
        query = update.callback_query
        keyboard = [[InlineKeyboardButton("Start again", callback_data='3')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
    
        if query.data == '0':
                index.min = 0
                index.max= 10
                validate.sendImail = [False,False,False,False,False]
                bot.deleteMessage(chat_id=query.message.chat_id, message_id=query.message.message_id)

                keyboard = [[InlineKeyboardButton("Inbox", callback_data='4'),
                                InlineKeyboardButton("Send a email", callback_data='5'),InlineKeyboardButton("Logout", callback_data='7')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                bot.send_message(chat_id=query.message.chat_id,text='Select an option:',
                                reply_markup=reply_markup)

        if query.data == '1':
                #bot.send_photo(chat_id=query.message.chat_id, photo=open('./src/stickers/notWorking.png', 'rb'),caption='Out of service now!',reply_markup=reply_markup)
                bot.deleteMessage(chat_id=query.message.chat_id, message_id=query.message.message_id)

                bot.send_message(
                        chat_id=query.message.chat_id,
                        text='Introduce your email address:'
                )

        elif query.data == '2':
                keyboard = [[InlineKeyboardButton("Read more", callback_data='8'),InlineKeyboardButton("Close", callback_data='9')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                bot.send_message(chat_id=query.message.chat_id,text='Bye!',reply_markup=reply_markup)
                bot.deleteMessage(chat_id=query.message.chat_id, message_id=query.message.message_id)
    
        elif query.data == '3':
                validate.login = [False,False,False]
                validate.sendImail = [False,False,False,False,False]
                credentials.email = ''
                credentials.password = ''
                hour = int(time.strftime("%H"))
                text = ''
                if hour >= 0 and hour <= 11:
                        text="Good Morning!"

                elif hour >= 12 and hour <= 18:
                        text="Good Afternoon!"

                elif hour >= 17 and hour <= 23:
                        text="Good Evening!"

                keyboard = [[InlineKeyboardButton("Login", callback_data='1'),InlineKeyboardButton("Close", callback_data='2')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                bot.deleteMessage(chat_id=query.message.chat_id, message_id=query.message.message_id)
                bot.send_message(chat_id=query.message.chat_id, text= text+'\n\n Select an option:',
                                reply_markup=reply_markup)

        elif query.data == '4':
                keyboard = [[InlineKeyboardButton("Read more", callback_data='4'),InlineKeyboardButton("Main menu", callback_data='0')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                bot.deleteMessage(chat_id=query.message.chat_id, message_id=query.message.message_id)
                bot.send_message(chat_id=query.message.chat_id,text='Searching emails, please wait....')
                inboxlist = inbox.OpenInbox(index.min,index.max)
                index.min = index.min+10
                index.max= index.max+10
                #print(inboxlist)
                
                for info_email in inboxlist:
                         bot.send_message(chat_id=query.message.chat_id,text=info_email)

                bot.send_message(chat_id=query.message.chat_id,text='Select an option:',
                              reply_markup=reply_markup)
        elif query.data == '5':
                bot.deleteMessage(chat_id=query.message.chat_id, message_id=query.message.message_id)
                validate.sendImail[0] = True
                bot.send_message(
                        chat_id=query.message.chat_id,
                        text='From:'
                )
        elif query.data == '6':
                validate.sendImail = [False,False,False,False,False]
                keyboard = [[InlineKeyboardButton("Inbox", callback_data='4'),
                        InlineKeyboardButton("Send a email", callback_data='5'),
                        InlineKeyboardButton("Logout", callback_data='7')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                bot.deleteMessage(chat_id=query.message.chat_id, message_id=query.message.message_id)  
                bot.send_message(chat_id=query.message.chat_id,text='Sending email, please wait....')
                result = ''
                if data.file_url == '' and data.file_name == '':
                        result = send.Send(credentials.email,credentials.password,data.From,data.To,data.Subject,data.Body)
                else:
                        result = sendattch.Send(credentials.email,credentials.password,data.From,data.To,data.Subject,data.Body,data.file_url,data.file_name)

                if result == 'ok':
                        data.Body = ''
                        data.From = ''
                        data.To = ''
                        data.Subject = ''
                        newsticker = Sticker(file_id= 'CAADAgADAgMAApzW5woU5Cm1Ey_jtAI', width= 512, height= 512)
                        bot.send_sticker(chat_id=query.message.chat_id, sticker= newsticker)
                        bot.send_message(chat_id=query.message.chat_id,text='The email has been sent....')
                        bot.send_message(chat_id=query.message.chat_id,text='Select an option:',
                              reply_markup=reply_markup) 
                else:
                        data.Body = ''
                        data.From = ''
                        data.To = ''
                        data.Subject = ''
                        newsticker = Sticker(file_id= 'CAADAgADCAMAApzW5wqTpbtQDP42agI', width= 512, height= 512)
                        bot.send_sticker(chat_id=update.message.chat_id, sticker= newsticker)
                        bot.send_message(chat_id=query.message.chat_id,text='Has been an error, try again....')
                        bot.send_message(chat_id=query.message.chat_id,text='Select an option:',
                              reply_markup=reply_markup)                  
        elif query.data == '7':
                validate.login = [False,False,False]
                validate.sendImail = [False,False,False,False,False]
                credentials.email = ''
                credentials.password = ''
                index.min = 0
                index.max= 10
                inbox.Logout()
                newsticker = Sticker(file_id= 'CAADAgAD9QIAApzW5woDP3qDEC4ObwI', width= 512, height= 512)
                bot.send_sticker(chat_id=query.message.chat_id, sticker= newsticker)
                bot.send_message(chat_id=query.message.chat_id,text='Bye!',reply_markup=reply_markup)
                bot.deleteMessage(chat_id=query.message.chat_id, message_id=query.message.message_id)
        elif query.data == '8':
                validate.login = [False,False,False]
                validate.sendImail = [False,False,False,False,False]
                credentials.email = ''
                credentials.password = ''
                index.min = 0
                index.max= 10
                newsticker = Sticker(file_id= 'CAADAgAD9QIAApzW5woDP3qDEC4ObwI', width= 512, height= 512)
                bot.send_sticker(chat_id=query.message.chat_id, sticker= newsticker)
                bot.send_message(chat_id=query.message.chat_id,text='Bye!',reply_markup=reply_markup)
                bot.deleteMessage(chat_id=query.message.chat_id, message_id=query.message.message_id)
        elif query.data == '9':
                validate.sendImail[4] = True
                bot.deleteMessage(chat_id=query.message.chat_id, message_id=query.message.message_id)
                bot.send_message(chat_id=query.message.chat_id,text='Add your file') 
        elif query.data == '10':
                bot.deleteMessage(chat_id=query.message.chat_id, message_id=query.message.message_id)
                keyboard = [[InlineKeyboardButton("Send", callback_data='6'),InlineKeyboardButton("Main menu", callback_data='0')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                bot.send_message(chat_id=query.message.chat_id, text= 'Select an option:',
                                        reply_markup=reply_markup)
    
def SendFile(bot,update):
        if validate.sendImail[4]:
                data.file_name = update.message.document.file_name   
                file = bot.getFile(update.message.document.file_id)   
                data.file_url = file.file_path
                keyboard = [[InlineKeyboardButton("Send", callback_data='6'),InlineKeyboardButton("Main menu", callback_data='0')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                bot.send_message(chat_id=update.message.chat_id, text= 'Select an option:',
                                        reply_markup=reply_markup)
                #print(file.file_path)      
                #print(name)   
                #sendattch.send(file.file_path,name) 
            

        
if __name__ == '__main__':
        
        dispatcher.add_handler(CommandHandler('start', start))
        dispatcher.add_handler(MessageHandler(Filters.text, Verification))
        dispatcher.add_handler(MessageHandler(Filters.document, SendFile))
        dispatcher.add_handler(CallbackQueryHandler(button))
        updater.start_polling() 
        updater.idle()

    
