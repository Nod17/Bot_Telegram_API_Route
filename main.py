# Projeto de redes de computadores: Python + API
import requests
import telebot

# ----------------------------------------------------------------
chave_api = #Inserir a chave API do bot telegram

bot = telebot.TeleBot(chave_api)


# ----------------------------------------------------------------
# Rota informando ponto de partida e chegada.

@bot.message_handler(commands=['coordenadas'])
def coordenadas(mensagem):

    texto = """
    Informe o ponto de partida da seguinte forma:
    /inicio_e_fim + latitude,longitude/latitude,longitude 
    
    """
    bot.reply_to(mensagem, texto)

@bot.message_handler(commands=['inicio_e_fim'])
def inicio(mensagem):
    point = mensagem.json

    start = (((point['text'])[16:]).split('/')[0])
    end = ((point['text']).split('/')[2])

    call3 = route(start, end)

    x = 0

    for item in call3:
        res = (call3[x]['instruction'])
        if 'right' in res:
            bot.send_message(mensagem.chat.id, '➡️  ' + res)
        if 'left' in res:
            bot.send_message(mensagem.chat.id, '⬅️  ' + res)
        if 'continue' in res:
            bot.send_message(mensagem.chat.id, '🔼 ' + res)
        if 'destination' in res:
            bot.send_message(mensagem.chat.id, '⏹ ' + res)
        else:
            bot.send_message(mensagem.chat.id, res)
        print(res)
        x = x + 1

# ------------------------------------------------------------------------

# ------------------------ ROTA IFRN ----------------------------
# Rota definida para o IFRN, informar apenas ponto de partida.

@bot.message_handler(commands=['ifrn'])
def ifrn(mensagem):
    texto = """
    Informe o ponto de partida da seguinte forma:
    /inicio + latitude,longitude 

    """

    bot.reply_to(mensagem, texto)

@bot.message_handler(commands=['inicio'])
def inicio(mensagem):
# recebe start, end=ifrn

    point = mensagem.json

    start = (point['text'])[8:]
    end = '-35.2044804873921,-5.81171023255824'

    call3 = route(start, end)

    x = 0

    for item in call3:
        res = (call3[x]['instruction'])
        if 'right' in res:
            bot.send_message(mensagem.chat.id, '➡️  ' + res)
        if 'left' in res:
            bot.send_message(mensagem.chat.id, '⬅️  ' + res)
        if 'continue' in res:
            bot.send_message(mensagem.chat.id, '🔼 ' + res)
        if 'destination' in res:
            bot.send_message(mensagem.chat.id, '⏹ ' + res)
        else:
            bot.send_message(mensagem.chat.id, res)
        print(res)
        x = x + 1

# ------------------------------------------------------------------------
# MENU INICIAL, Verifica a mensagem e responde com o menu inicial

def verificar(mensagem):
    return True

@bot.message_handler(func=verificar)
def responder(mensagem):
    texto = """
    Escolha uma opção:
       
    /coordenadas 🌎 Informar coordendas
    
    /ifrn 🌎 Rota para o IFRN central
    
    """
    print(mensagem)
    bot.reply_to(mensagem, texto)


# ---------------- FUNÇÃO API ROUTE ---------------------------------------

def route(start, end):

    route_key= #Inserir chave API OpenRouteService

    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    }
    call = requests.get(
        'https://api.openrouteservice.org/v2/directions/driving-car?api_key='+ route_key +'&start=' + start + '&end=' + end,
        headers=headers)

    call = call.json()
    call2 = call['features'][0]['properties']['segments'][0]['steps']

    return call2
# --------------------------------------------------------------------------------

bot.polling()