from telegram import ParseMode, KeyboardButton, KeyboardButtonPollType, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters, CallbackContext, CallbackQueryHandler
import mysql.connector

import time
import datetime
import random
import json
import threading

# ---------------------
#   FUNCIONES BASICAS
# ---------------------

# def start(update, context):
#     addPlayerIfNoExist(update.effective_user.id)
#     context.bot.send_message(
#         chat_id=update.effective_chat.id,
#         text="🎰 Ksino Version 0.8 🎰",
#         reply_markup=InlineKeyboardMarkup([
#             [InlineKeyboardButton(text="Roulette", callback_data="roulette")],
#             [InlineKeyboardButton(text="Send coins 💰", callback_data="coins"), InlineKeyboardButton(text="Receive coins 💰", callback_data="coins")],
#             [InlineKeyboardButton(text="@KeviNsitOgorRin 💻🇨🇺", url="t.me/KeviNsitOgorRin")]
#         ])
#     )
#     # context.bot.send_message(chat_id=update.effective_chat.id, text="-------- 🎲 Ksino Version 0.8 🎲 --------\n\n¡Apuesta y gana!\n\nJuegos:\n/roulette - seguido del monto a jugar. La ruleta, apuesta por un color y gana\n/\n\nComandos:\n/coins - saldo actual de su cuenta\n/send - seguido del monto que desea transferir\n/receive - seguido del ID de la transacción para ser recibida\n\nEste bot es solamente un minijuego, no pretende ser un casino virtual real y por lo tanto no hay dinero real de por medio.\n\nProgramado por @KeviNsitOgorRin 💻🇨🇺", reply_markup=createMenu(options=[['Roulette 🎡', '@kevin'], ['Programado por @KeviNsitOgorRin 💻🇨🇺', '-', 't.me/KeviNsitOgorRin']], n_cols=1))

# def coins(update, context):
#     addPlayerIfNoExist(update.effective_user.id)
#     context.bot.send_message(chat_id=update.effective_chat.id, text=f"Saldo actual de su cuenta: ${getPlayerCoins(update.effective_user.id)}.")

# def createMenu(options, n_cols = 1):
#     return InlineKeyboardMarkup([[InlineKeyboardButton(text=option[0], url=option[2] if len(option) > 2 else '', callback_data=option[1]) for option in options][i:i+n_cols] for i in range(0, len(options), n_cols)])

# def getPlayersList():
#     file = open('players.json', 'r+')
#     fileContent = json.loads(file.read())
#     file.close()
#     return fileContent

# def savePlayersList(players):
#     file = open('players.json', 'r+')
#     fileContent = json.loads(file.read())
#     file.seek(0)
#     file.truncate()
#     file.write(json.dumps(players))
#     file.close()

# def addPlayerIfNoExist(user_id):
#     players = getPlayersList()
#     if players.get(repr(user_id)) == None:
#         players[repr(user_id)] = {'user_id':user_id, 'coins':100}
#         print(f"{user_id} ha entrado al Ksino.")
#     savePlayersList(players)

# def getPlayerCoins(user_id):
#     players = getPlayersList()
#     return 0 if players.get(repr(user_id)) == None else players[repr(user_id)]['coins']

# def setPlayerCoins(user_id, coins):
#     players = getPlayersList()
#     players[repr(user_id)]['coins'] = coins
#     savePlayersList(players)

# # ---------------------
# #     TRANSFERENCIAS
# # ---------------------

# transfers = {}

# def send(update, context):
#     global transfers
#     addPlayerIfNoExist(update.effective_user.id)
#     playerCoins = getPlayerCoins(update.effective_user.id)
#     messageParameters = update.message.text.split(" ")
#     response = "Formato incorrecto del comando."
#     if (len(messageParameters) == 2) and messageParameters[1].isdigit():
#         amount = int(messageParameters[1])
#         if playerCoins > 0 and playerCoins >= amount:
#             setPlayerCoins(update.effective_user.id, playerCoins-amount)
#             transferId = random.randint(1000, 9999)
#             transfers[transferId] = {'transfer_id':transferId, 'amount':amount, 'first_name':update.effective_user.first_name}
#             response = f"Usted ha transferido ${amount}.\nID de la transferencia: {transferId}.\nSaldo actual de su cuenta: ${playerCoins-amount}."
#         else:
#             response = "No tiene saldo suficiente para la transferencia."
#     context.bot.send_message(chat_id=update.effective_chat.id, text=response)

# def receive(update, context):
#     global transfers
#     addPlayerIfNoExist(update.effective_user.id)
#     playerCoins = getPlayerCoins(update.effective_user.id)
#     messageParameters = update.message.text.split(" ")
#     response = "Formato incorrecto del comando."
#     if (len(messageParameters) == 2) and messageParameters[1].isdigit():
#         transferId = int(messageParameters[1])
#         if transfers.get(transferId) == None:
#             response = f"No se ha encontrado la transferencia con ID {transferId}."
#         else:
#             transfer = transfers[transferId]
#             del(transfers[transferId])
#             setPlayerCoins(update.effective_user.id, playerCoins+transfer['amount'])
#             response = f"Ha recibido la transferencia de ${transfer['amount']} hecha por {transfer['first_name']}.\nID de la transferencia: {transfer['transfer_id']}.\nSaldo actual de su cuenta: ${playerCoins+transfer['amount']}."
#     context.bot.send_message(chat_id=update.effective_chat.id, text=response)

# # ---------------------
# #        JUEGOS
# # ---------------------

# roulettes = {}
# rouletteColors = [['Rojo 🔴 (x2)', 'red', 2], ['Negro ⚫️ (x2)', 'black', 2], ['Verde 🟢 (x14)', 'green', 14]]

# def startRoulette(update, context):
#     global roulettes
#     global rouletteColors
#     addPlayerIfNoExist(update.effective_user.id)
#     messageParameters = update.message.text.split(" ")
#     if (len(messageParameters) == 2) and messageParameters[1].isdigit():
#         amount = int(messageParameters[1])
#         playerCoins = getPlayerCoins(update.effective_user.id)
#         if playerCoins > 0 and playerCoins >= amount:
#             message = context.bot.send_message(chat_id=update.effective_chat.id, text=f"¿Por qué color apuesta ${amount}?", reply_markup=createMenu(options=[[option[0], option[1]] for option in rouletteColors], n_cols=2))
#             roulettes[message.chat_id] = {'message':message, 'user_id':update.effective_user.id, 'amount':amount}
#             return
#         else:
#             response = "No tiene saldo suficiente para jugar."
#     else:
#         response = "Formato incorrecto del comando."
#     context.bot.send_message(chat_id=update.effective_chat.id, text=response)

# def spinRoulette(update, context, roulette, color):
#     global rouletteColors
#     context.bot.send_message(chat_id=roulette['message'].chat.id, text="Girando...")
#     time.sleep(2)
#     randomNum = random.randint(1, 100)
#     colorWinner = rouletteColors[(2 if randomNum <= 2 else 1) if randomNum <= 52 else 0]
#     earned = 0 if colorWinner[1] != color else roulette['amount']*colorWinner[2]
#     newPlayerCoins = getPlayerCoins(roulette['user_id'])-roulette['amount']+earned
#     setPlayerCoins(roulette['user_id'], newPlayerCoins)
#     context.bot.send_message(chat_id=roulette['message'].chat.id, text=f"Ha parado de girar en el... ¡¡{colorWinner[0]}!!\nHa ganado ${earned}.\nSaldo actual: ${newPlayerCoins}.")

# def pressButton(update, context):
#     global roulettes
#     chat_id = update.callback_query.message.chat.id
#     if (roulettes.get(chat_id) != None) and roulettes[chat_id]['message'].message_id == update.callback_query.message.message_id:
#         context.bot.delete_message(chat_id=roulettes[chat_id]['message'].chat.id, message_id=roulettes[chat_id]['message'].message_id)
#         thread = threading.Thread(target=spinRoulette, args=(update, context, roulettes[chat_id], update.callback_query.data)).start()
#         del(roulettes[chat_id])

# def gifts(update, context):
#     while True:
#         time.sleep(60*60*3)
#         players = getPlayersList()
#         for player in players:
#             setPlayerCoins(players[player]['user_id'], players[player]['coins']+10)
#             dispatcher.bot.send_message(chat_id=players[player]['user_id'], text="🎁 Ha recibido $10 de regalo. 🎁")

# START
def start(update, context):
    user_id, query, message = update.effective_user.id, update.callback_query, {'text': '🎰 Ksino Version 0.8 🎰', 'reply_markup': InlineKeyboardMarkup([
        [InlineKeyboardButton(text='🎲 Roulette', callback_data="roulette")],
        [InlineKeyboardButton(text='📤 Transferir monedas', callback_data="send-coins")],
        [InlineKeyboardButton(text='💰 Monedas', callback_data='coins')]
    ])}
    addPlayerIfNoExist(user_id)
    if query == None:
        msg = update.message.text.split(' ')
        if len(msg) == 2:
            code = msg[1]
            check = context.bot_data.get(code)
            update.message.reply_text('⚠️ Lo sentimos, el cheque no está disponible.' if check == None else f'💵 Ha cobrado el cheque #{code.replace("check-", "")} de ${check}.')
            if check != None:
                setPlayerCoins(user_id, getPlayerCoins(user_id)+check)
                del(context.bot_data[code])
        else:
            update.message.reply_text(text=message['text'], reply_markup=message['reply_markup'])
    else:
        query.answer()
        token = str(query.message.chat.id)+'-'+str(query.message.message_id)
        if context.bot_data.get(token) != None:
            del(context.bot_data[token])
        query.edit_message_text(text=message['text'], reply_markup=message['reply_markup'])

# VIEW COINS
def coins(update, context):
    user_id, query = update.effective_user.id, update.callback_query
    addPlayerIfNoExist(user_id)
    message = {'text': f'Monedas disponibles: ${getPlayerCoins(user_id)}', 'reply_markup': InlineKeyboardMarkup([[InlineKeyboardButton(text="⬅️ Regresar", callback_data="start")]])}
    if query == None:
        update.message.reply_text(text=message['text'], reply_markup=message['reply_markup'])
    else:
        query.answer()
        query.edit_message_text(text=message['text'], reply_markup=message['reply_markup'])

# SELECT COINS
coinsMenuFor = {
    'roulette': {'to': 'apostar', 'startText': '🎲 Jugar', 'startData': 'select-color-roulette'},
    'send-coins': {'to': 'transferir', 'startText': '📤 Transferir', 'startData': 'create-check'}
}

def selectCoins(update, context):
    global coinsMenuFor
    user_id, query, currentFor = update.effective_user.id, update.callback_query, update.callback_query.data
    addPlayerIfNoExist(user_id)
    query.answer()
    context.bot_data[str(query.message.chat.id)+'-'+str(query.message.message_id)] = [1, currentFor]
    query.edit_message_text(text=createCoinsMenuText(coinsMenuFor[currentFor]['to'], 1, getPlayerCoins(user_id)), reply_markup=createCoinsMenu(coinsMenuFor[currentFor]['startText'], coinsMenuFor[currentFor]['startData']))

def modifyCoins(update, context):
    global coinsMenuFor
    query, amount = update.callback_query, update.callback_query.data.replace('-coins', '')
    currentToken = str(query.message.chat.id)+'-'+str(query.message.message_id)
    currentMsg = context.bot_data.get(currentToken)
    if currentMsg != None:
        totalCoins, currentCoins, currentFor = getPlayerCoins(update.effective_user.id), currentMsg[0], coinsMenuFor[currentMsg[1]]
        newCoins = totalCoins if amount == 'all' else (1 if amount == 'reset' else currentCoins + int(amount))
        answer = f'Debes {currentFor["to"]} $1 como mínimo.' if newCoins <= 0 else (f'No puedes {currentFor["to"]} más de lo que tienes.' if newCoins > totalCoins else '')
        if answer == '':
            query.answer()
            if newCoins != currentCoins:
                context.bot_data[currentToken][0] = newCoins
                query.edit_message_text(text=createCoinsMenuText(currentFor['to'], newCoins, totalCoins), reply_markup=createCoinsMenu(currentFor['startText'], currentFor['startData']))
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text=answer)

# SELECT COINS MENU
def createCoinsMenuText(to, amount, totalCoins):
    return f'Monedas a {to}: ${amount}\nMonedas disponibles: ${totalCoins}'

def createCoinsMenu(startText, startData):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text='-1', callback_data='-1'), InlineKeyboardButton(text='+1', callback_data='1')],
        [InlineKeyboardButton(text='-10', callback_data='-10'), InlineKeyboardButton(text='+10', callback_data='10')],
        [InlineKeyboardButton(text='-100', callback_data='-100'), InlineKeyboardButton(text='+100', callback_data='100')],
        [InlineKeyboardButton(text='-1000', callback_data='-1000'), InlineKeyboardButton(text='+1000', callback_data='1000')],
        [InlineKeyboardButton(text='Reset', callback_data='reset'), InlineKeyboardButton(text='All', callback_data='all')],
        [InlineKeyboardButton(text=startText, callback_data=startData)],
        [InlineKeyboardButton(text='⬅️ Regresar', callback_data='start')]
    ])

def createCheck(update, context):
    user_id, query = update.effective_user.id, update.callback_query
    addPlayerIfNoExist(user_id)
    currentToken = str(query.message.chat.id)+'-'+str(query.message.message_id)
    currentCoins = context.bot_data.get(currentToken)
    playerCoins = getPlayerCoins(user_id)
    if currentCoins != None:
        coins = currentCoins[0]
        if coins > playerCoins:
            context.bot.answer_callback_query(callback_query_id=query.id, text='No tienes las monedas suficientes para enviar.')
        else:
            code = f'check-{random.randint(100000, 999999)}'
            context.bot_data[code] = coins
            setPlayerCoins(user_id, playerCoins-coins)
            del(context.bot_data[currentToken])
            query.edit_message_text(text=f'Ha expedido un cheque de ${coins}, use el siguiente link para cobrarlo: t.me/ksinobot/?start={code}', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='⬅️ Regresar', callback_data='start')]]))

rouletteColors = [['Rojo 🔴 (x2)', 'red', 2], ['Negro ⚫️ (x2)', 'black', 2], ['Verde 🟢 (x14)', 'green', 14]]

def selectColorRoulette(update, context):
    global rouletteColors
    user_id, query = update.effective_user.id, update.callback_query
    addPlayerIfNoExist(user_id)
    currentToken = str(query.message.chat.id)+'-'+str(query.message.message_id)
    currentCoins = context.bot_data.get(currentToken)
    if currentCoins != None:
        coins = currentCoins[0]
        if coins > getPlayerCoins(user_id):
            context.bot.answer_callback_query(callback_query_id=query.id, text='No tienes las monedas suficientes para jugar.')
        else:
            query.edit_message_text(text=f'¿Por qué color apuesta ${currentCoins[0]}?', reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text="Rojo 🔴 (x2)", callback_data="start")],
                [InlineKeyboardButton(text="Negro ⚫️ (x2)", callback_data="start")],
                [InlineKeyboardButton(text="Verde 🟢 (x14)", callback_data="start")],
                [InlineKeyboardButton(text="⬅️ Regresar", callback_data="start")]
            ]))

def runRoulette(update, context):
    pass

def getPlayersList():
    file = open('players.json', 'r+')
    fileContent = json.loads(file.read())
    file.close()
    return fileContent

def getPlayerCoins(playerId):
    return getPlayersList()[repr(playerId)]['coins']

def setPlayerCoins(playerId, coins):
    players = addPlayerIfNoExist(playerId)
    players[repr(playerId)]['coins'] = coins
    file = open('players.json', 'w+')
    file.write(json.dumps(players))
    file.close()

def addPlayerIfNoExist(user_id):
    global DBConnection
    query = DBConnection.cursor()
    query.execute("SELECT * FROM players WHERE player_id = '%i'", (user_id))
    # print(query.fetchall())
    # print(user_id)
    if len(query.fetchall()) == 0:
        print(1)
        query2 = DBConnection.cursor()
        query2.execute("INSERT INTO players (player_id, coins) VALUES (%(user_id)s, %(coins)s)", {'user_id': user_id, 'coins': 100})

if __name__ == '__main__':
    DBConfig = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'db': 'ksinobot'
    }
    DBConnection = mysql.connector.connect(**DBConfig)

    # connection = mysql.connector.connect(host='localhost', user='root', passwd='', db='ksinobot')
    # cursor = connection.cursor()
    # cursor.execute('SELECT * FROM checks')
    # print('xd')
    # print(cursor.fetchall())
    # print('xd2')

    updater = Updater(token='1827935007:AAFm15C_fXu74VdmLv4tpZ_yBBQlavNnA7g')
    dp = updater.dispatcher
    dp.add_handler(ConversationHandler(entry_points=[
        CommandHandler('start', start),
        CallbackQueryHandler(pattern='start', callback=start),
        CommandHandler('coins', coins),
        CallbackQueryHandler(pattern='coins', callback=coins),
        CallbackQueryHandler(pattern='roulette', callback=selectCoins),
        CallbackQueryHandler(pattern='select-color-roulette', callback=selectColorRoulette),
        CallbackQueryHandler(pattern='red-roulette', callback=runRoulette),
        CallbackQueryHandler(pattern='black-roulette', callback=runRoulette),
        CallbackQueryHandler(pattern='green-roulette', callback=runRoulette),
        CallbackQueryHandler(pattern='send-coins', callback=selectCoins),
        CallbackQueryHandler(pattern='create-check', callback=createCheck),
        CallbackQueryHandler(pattern='-1', callback=modifyCoins),
        CallbackQueryHandler(pattern='1', callback=modifyCoins),
        CallbackQueryHandler(pattern='reset', callback=modifyCoins),
        CallbackQueryHandler(pattern='all', callback=modifyCoins),
        # CommandHandler('roulette', startRoulette),
        # CallbackQueryHandler(pattern="roulette", callback=startRoulette)
    ], states={
    }, fallbacks=[]))
    # giftsThread = threading.Thread(target=gifts, args=(Update, CallbackContext)).start()
    updater.start_polling()
    updater.idle()