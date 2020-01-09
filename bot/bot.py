import random
import os
import telegram
import matplotlib.pyplot as plt
import networkx as nx
import pickle
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import PicklePersistence
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Benvingut a EnquestaBot! Escriu /help per veure les diferents possibles comandes")


def help(bot, update):
    help_message = """Comandes:
• /start: Engega el bot.
• /help: Mostra aquest missatge d'ajuda.
• /author: Mostra informació de l'autor.
• /quiz <idEnquesta> <do\_quiz>?: Inicialitza i posa com a activa l'enquesta amb nom <idEnquesta>. En cas de que <do\_quiz> == 0, simplement canvia l'enquesta activa per <idEnquesta> però sense inicialitzar-la.
• /bar <idPregunta>: Mostra un gràfic de barres amb les respostes donades a la pregunta <idPregunta> de l'enquesta activa.
• /pie <idPregunta>: Mostra un gràfic de formatget amb els percentatges de cada resposta donades a la pregunta <idPregunta> de l'enquesta activa.
• /report: Mostra una pseudotaula amb el nombre de respostes obtingudes per cada valor de cada pregunta."""
    bot.send_message(chat_id=update.message.chat_id, parse_mode=telegram.ParseMode.MARKDOWN, text=help_message)


def bar(bot, update, user_data, args):
    try:
        title = user_data['title']
    except KeyError or IndexError:
        bot.send_message(chat_id=update.effective_chat.id, text="No hi ha cap enquesta activa")
    try:
        data = pickle.load(open('respostes' + title + '.pickle', 'rb'))
    except (OSError, IOError) as e:
        G = user_data['graf']
        data = init_data(G)
        pickle.dump(data, open('respostes' + title + '.pickle', 'wb'))
    try:
        idP = args[0]
    except IndexError:
        bot.send_message(chat_id=update.effective_chat.id, text="Falta l'argument <idPregunta>")
        return
    try:
        D = data[idP]
    except KeyError:
        bot.send_message(chat_id=update.effective_chat.id, text="L'<idPregunta> introduït (" + idP + ") no existeix a l'enquesta actual (" + title + ")")
        return
    res = []
    val = []
    for e in D:
        res.append(str(e))
        val.append(D[e])
    fitxer = "%d.png" % random.randint(1000000, 9999999)
    plt.clf()
    plt.bar(res, val)
    plt.savefig(fitxer, bbox_inches='tight')
    bot.send_photo(chat_id=update.message.chat_id, photo=open(fitxer, 'rb'))
    os.remove(fitxer)


def pie(bot, update, user_data, args):
    try:
        title = user_data['title']
    except KeyError or IndexError:
        bot.send_message(chat_id=update.effective_chat.id, text="No hi ha cap enquesta activa")
    try:
        data = pickle.load(open('respostes' + title + '.pickle', 'rb'))
    except (OSError, IOError) as e:
        G = user_data['graf']
        data = init_data(G)
        pickle.dump(data, open('respostes' + title + '.pickle', 'wb'))
    try:
        idP = args[0]
    except IndexError:
        bot.send_message(chat_id=update.effective_chat.id, text="Falta l'argument <idPregunta>")
        return
    try:
        D = data[idP]
    except KeyError:
        bot.send_message(chat_id=update.effective_chat.id, text="L'<idPregunta> introduït (" + idP + ") no existeix a l'enquesta actual (" + title + ")")
        return
    res = []
    val = []
    for e in D:
        res.append(str(e))
        val.append(D[e])
    explode = (0.1,) * len(res)
    fitxer = "%d.png" % random.randint(1000000, 9999999)
    plt.clf()
    plt.pie(val, labels=res, explode=explode, shadow=True, autopct='%1.1f%%')
    plt.savefig(fitxer, bbox_inches='tight')
    bot.send_photo(chat_id=update.message.chat_id, photo=open(fitxer, 'rb'))
    os.remove(fitxer)


def report(bot, update, user_data):
    try:
        title = user_data['title']
    except KeyError or IndexError:
        bot.send_message(chat_id=update.effective_chat.id, text="No hi ha cap enquesta activa")
    try:
        data = pickle.load(open('respostes' + title + '.pickle', 'rb'))
    except (OSError, IOError) as e:
        G = user_data['graf']
        data = init_data(G)
        pickle.dump(data, open('respostes' + title + '.pickle', 'wb'))
    txt = "*pregunta valor respostes* \n"
    for i in data:
        for j in data[i]:
            if data[i][j] > 0:
                txt += str(i) + ' ' + str(j) + ' ' + str(data[i][j]) + '\n'
    bot.send_message(chat_id=update.message.chat_id, text=txt, parse_mode='Markdown')


# Inicialitza el diccionari de respostes quan s'ha de guardar per primer cop.
def init_data(G):
    items = nx.get_edge_attributes(G, 'id')
    data = {}
    for i in items:
        idP = i[0]
        data[idP] = {}
        idR = i[1]
        dict = G.nodes[idR]['res']
        for j in dict:
            data[idP][j] = 0
    return data


# Processa un node del graf i envia les preguntes i respostes d'aquest.
def procesar_node(bot, update, user_data):
    G = user_data['graf']
    node = user_data['node']
    if user_data['isAlt']:
        node = user_data['alt']
    type = G.nodes[node]['type']
    title = G.graph['title']
    if type == 'enquesta_init':
        bot.send_message(chat_id=update.message.chat_id, text='Enquesta ' + node + ':')
        for e in G[node]:
            if G[node][e]['type'] == 'enquesta':
                user_data['node'] = e
                procesar_node(bot, update, user_data)
    elif type == 'enquesta_end':
        bot.send_message(chat_id=update.message.chat_id, text=title + '> Gracies pel teu temps!')
        user_data['inQuiz'] = False
        respostes = user_data['res']
        try:
            data = pickle.load(open('respostes' + title + '.pickle', 'rb'))
        except (OSError, IOError) as e:
            data = init_data(G)
            pickle.dump(data, open('respostes' + title + '.pickle', 'wb'))
        for i in respostes:
            j = int(respostes[i])
            data[i][j] += 1
        with open('respostes' + title + '.pickle', 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    elif type == 'pregunta':
        p = G.nodes[node]['pregunta']
        txt = ''
        txt += str(title) + '> ' + str(p) + '\n'
        for r in G[node]:
            if G[node][r]['type'] == 'item':
                dict = G.nodes[r]['res']
                user_data['pos_res'] = dict
                for i in dict:
                    txt += (str(i) + ': ' + str(dict[i]) + '\n')
                bot.send_message(chat_id=update.message.chat_id, text=txt)


def author(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Joan Francesc Muntaner Gonzalez, joan.francesc.muntaner@est.fib.upc.edu")


def quiz(bot, update, user_data, args):
    try:
        idE = args[0]
    except IndexError:
        bot.send_message(chat_id=update.effective_chat.id, text="Falta l'argument <idEnquesta>")
        return
    name = "graf" + idE
    path = "../cl/" + name + ".gpickle"
    try:
        G = nx.read_gpickle(path)
    except FileNotFoundError:
        bot.send_message(chat_id=update.effective_chat.id, text='No existeix cap enquesta amb el nom: ' + idE)
        return
    user_data['graf'] = G.copy()
    user_data['res'] = {}
    user_data['node'] = idE
    user_data['isAlt'] = False
    user_data['inQuiz'] = True
    user_data['title'] = G.graph['title']
    try:
        do_quiz = args[1]
    except IndexError:
        do_quiz = 1
    if do_quiz == '0':
        bot.send_message(chat_id=update.effective_chat.id, text="L'enquesta activa s'ha canviat correctament a: " + idE)
        return
    procesar_node(bot, update, user_data)


# Processa els missatges que envia l'usuari, particularment només atén les respostes quan estem dins /quiz i apunta al següent node.
def procesar_resposta(bot, update, user_data):
    if not user_data['inQuiz']:
        return
    res = update.message.text
    pos_res = user_data['pos_res']
    # Comprova que la resposta sigui vàlida
    try:
        if int(res) not in user_data['pos_res']:
            bot.send_message(chat_id=update.effective_chat.id, text='Aquesta resposta no esta entre les opcions possibles. Torna a provar.')
            return
    except ValueError:
        bot.send_message(chat_id=update.effective_chat.id, text='Resposta no vàlida (han de ser números)')
        return
    # Recull la informació de user_data
    G = user_data['graf']
    node = user_data['node']
    if user_data['isAlt']:
        node = user_data['alt']
    user_data['res'][node] = res
    if user_data['isAlt']:
        user_data['isAlt'] = False
    else:
        next = ''
        for e in G[node]:
            if G[node][e]['type'] == 'enquesta':
                next = e
                user_data['node'] = next
            elif G[node][e]['type'] == 'alternativa':
                if G[node][e]['resposta'] == res:
                    user_data['alt'] = e
                    user_data['isAlt'] = True
    procesar_node(bot, update, user_data)


persist = PicklePersistence(filename='userdata.pickle')
TOKEN = open('token.txt').read().strip()
updater = Updater(token=TOKEN, persistence=persist)
dispatcher = updater.dispatcher
dispatcher.persistence = persist
dispatcher.user_data = persist.get_user_data()

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('author', author))
dispatcher.add_handler(CommandHandler('quiz', quiz, pass_user_data=True, pass_args=True))
dispatcher.add_handler(CommandHandler('bar', bar, pass_user_data=True, pass_args=True))
dispatcher.add_handler(CommandHandler('pie', pie, pass_user_data=True, pass_args=True))
dispatcher.add_handler(CommandHandler('report', report, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text, procesar_resposta, pass_user_data=True))

updater.start_polling()
updater.idle()
