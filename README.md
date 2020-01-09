# QuizBot

Bot de Telegram que constesta textualment i gràficament a preguntes relacionades amb enquestes, així com també recullir les respostes que es donen a aquestes.
El projecte també inclou un compilador que interpreta el llenguatge de les enquestes i genera un graf que és el que usa el Bot per interpretar-les.

## Primeres passes

### Prerrequisits

Aquest projecte requereix que python3 i pip estiguin instal·lats a la vostra màquina. Per instal·lar les llibreries de python necessàries correu la següent comanda desde la carpeta arrel del projecte:

```
pip install -r requirements.txt
```

### Execució Compilador

Per executar el compilador simplement executa la següent comanda desde la carpeta /cl

```
python3 test.main.py el_teu_input.txt
```

On el_teu_input.txt és el fitxer d'entrada que conté l'enquesta que es vol interpretar.

### Execució Bot

Per fer córrer el bot simplement cal executar la següent comanda desde la carpeta /bot

```
python3 bot.py
```

### Usar el Bot

Obre Telegram i obre un xat amb l'usuari @EnquestaLP_bot [https://t.me/EnquestaLP_bot]. Envia la comanda:

```
/start
```

Si necessites ajuda envia la comanda `/help` al Bot i et mostrarà una llista de comandes disponibles.

## Running the tests

### Test run

This is a sample run from the bot. First of all, run the start command

```
/start
```

This will generate a default map with cities with population above 100000 and edges if the distance between them is less than 300 km. Now run the following commands:

```
/nodes
/edges
/components
```

Which gives the number of nodes, edges and components of the graph. The results should be  3527, 48086 and 163. Now, if you run

```
/graph 600 500000
```

the bot will create a new graph with cities above half a million inhabitants and edges if the distance is less than 600 km. Check that the graph now has less nodes and edges. The bot can also generate maps, for example with

```
/plotpop 1000 41.3888 2.1590
```

you'll get a map of the cities less than 1000 km away from Barcelona, with sizes proportional to population. You can now send your current location (with the paperclip icon next to the writing prompt) and re-run the command only with the first parameter, the bot will send a map with cities less than the specified distance from you.

If you replace `plotpop` with `plotmap`, it will also draw edges between nearby cities. Now you can send this command:

```
/route "varselona, es", "pariss, fr"
```

The answer will be a map with the route between the two cities. Note the bot could interpret the command even though the names had typos. If you try to find a non-existent route, for example between "barcelona, es" and "tokyo, jp", the bot wil tell you it doesn't exist.

If you try with another user or device, you'll notice the bot remembers which chat is in and uses the correct graph. If you want to get more information about these and other commands, send `/help` to the bot.

### Tests d'estil de codi

Usa `pycodestyle` amb cada fitxer \*.py per comprovar que compleixen els estàndards pep8 (tret de la llargada de línia).


## Author

Joan Francesc Muntaner González
[joan.francesc.muntaner@est.fib.upc.edu]
