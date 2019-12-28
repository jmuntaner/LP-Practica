import telegram
import matplotlib.pyplot as plt
import networkx as nx
import pickle
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hola!")

def help(bot, update):
    help_message = """Soc un bot amb comandes:

/start
/help
/author
/quiz <idEnquesta>
/bar <idPregunta>
/pie <idPregunta>
/report"""
    bot.send_message(chat_id=update.message.chat_id, text=help_message)

# def bar(bot, update, user_data, args):
# def pie(bot, update, user_data, args):
def report(bot, update, user_data):
    title = user_data['title']
    try:
        data = pickle.load(open('respostes' + title + '.pickle', 'rb'))
    except (OSError, IOError) as e:
        G = user_data['graf']
        data = init_data(G)
        pickle.dump(data, open('respostes' + title + '.pickle', 'wb'))
    txt = ''
    for i in data:
        for j in data[i]:
            if data[i][j]>0:
                txt += str(i) + ' ' + str(j) + ' ' + str(data[i][j]) + '\n'
    bot.send_message(chat_id=update.message.chat_id, text=txt)

def init_data(G):
    items = nx.get_edge_attributes(G,'id')
    data = {}
    for i in items:
        idP = i[0]
        data[idP]={}
        idR = i[1]
        dict = G.nodes[idR]['res']
        for j in dict:
            data[idP][j]=0
    return data

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
        user_data['inQuiz']=False
        respostes = user_data['res']
        try:
            data = pickle.load(open('respostes' + title + '.pickle', 'rb'))
        except (OSError, IOError) as e:
            data = init_data(G)
            pickle.dump(data, open('respostes' + title + '.pickle', 'wb'))
        for i in respostes:
            j = int(respostes[i])
            data[i][j]+=1
        with open('respostes' + title + '.pickle', 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    elif type == 'pregunta':
        p = G.nodes[node]['pregunta']
        txt = ''
        txt += str(title) + '> ' + str(p) + '\n'
        for r in G[node]:
            if G[node][r]['type'] == 'item':
                dict = G.nodes[r]['res']
                user_data['pos_res']=dict
                for i in dict:
                    txt += (str(i) + ': ' + str(dict[i]) + '\n')
                bot.send_message(chat_id=update.message.chat_id, text=txt)



def author(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Joan Francesc Muntaner Gonzalez, joan.francesc.muntaner@est.fib.upc.edu")

def quiz(bot, update, user_data, args):
    idE = args[0]
    name = "graf" + idE
    path = "../Compilador/" + name + ".gpickle"
    G=nx.read_gpickle(path)
    user_data['graf']=G.copy()
    user_data['res']={}
    user_data['node']=idE
    user_data['isAlt']=False
    user_data['inQuiz']=True
    user_data['title'] = G.graph['title']
    procesar_node(bot, update, user_data)

def procesar_resposta(bot, update, user_data):
    if not user_data['inQuiz']:
        return
    res = update.message.text
    pos_res = user_data['pos_res']
    if int(res) not in user_data['pos_res']:
            bot.send_message(chat_id=update.effective_chat.id, text='Aquesta resposta no esta entre les opcions possibles. Torna a provar.')
            return
    G = user_data['graf']
    node = user_data['node']
    bot.send_message(chat_id=update.effective_chat.id, text='resposta' + res)
    if user_data['isAlt']:
        node = user_data['alt']
    user_data['res'][node]=res
    if user_data['isAlt']:
        user_data['isAlt']=False
    else:
        next = ''
        for e in G[node]:
            if G[node][e]['type'] == 'enquesta':
                next = e
                user_data['node']=next
            elif G[node][e]['type'] == 'alternativa':
                if G[node][e]['resposta'] == res:
                    user_data['alt']=e
                    user_data['isAlt']=True
    procesar_node(bot, update, user_data)


TOKEN = open('token.txt').read().strip()
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('author', author))
dispatcher.add_handler(CommandHandler('quiz', quiz, pass_user_data=True, pass_args=True))
# dispatcher.add_handler(CommandHandler('bar', bar, pass_user_data=True, pass_args=True))
# dispatcher.add_handler(CommandHandler('pie', pie, pass_user_data=True, pass_args=True))
dispatcher.add_handler(CommandHandler('report', report, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text, procesar_resposta, pass_user_data=True))

updater.start_polling()
updater.idle()

# updater.stop()
