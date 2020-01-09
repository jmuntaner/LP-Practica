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

## Decisions de disseny

### Compilador

S'han fet una sèrie de suposicions sobre el llenguatge d'enquestes:

* Els identificadors de preguntes, respostes, alternatives, ítems i enquestes no són lliures i tenen un format determinat:
    * Preguntes: Consistirán de una _P_ majúscula i un _nombre_ qualsevol, per exemple: _P123_
    * Respostes: Consistirán de una _R_ majúscula i un _nombre_ qualsevol, per exemple: _R123_
    * Alternatives: Consistirán de una _A_ majúscula i un _nombre_ qualsevol, per exemple: _A123_
    * Items: Consistirán de una _I_ majúscula i un _nombre_ qualsevol, per exemple: _I123_
    * Enquestes: Consistirán de una _String_ seguida de un _nombre_ qualsevol _opcional_, per exemple: _Enquesta123_, _Ahirenquestà_.
* Tornar a usar un identificador amb el mateix nom que un que aparescut abans el sobreescriu.
* Els Strings poden contenir accents.
* Només es pot fer una comanda ENQUESTA per cada execució, per tant, quan l'intèrpret la detecta, acaba.

També s'ha afegit una pregunta addicional quan s'executa amb un input que sobreescrigui un graf d'enquesta que ja existeixi.

### Bot

* Podem tenir moltes enquestes creades pel Compilador, però són totes independents entre elles.
* Definim l'_enquesta activa_ en un moment de l'execució com l'última enquesta (<idEnquesta>) de la que s'ha fet `/quiz <idEnquesta>`.
* S'ha incorportat una funcionalitat addicional a `quiz` tal que si es fa `quiz <idEnquesta> 0`, <idEnquesta> passa a ser l'_enquesta activa_.
* Les comandes `bar`, `pie` i `report` fan referència a l'_enquesta activa_ en el moment d'executar-se.
* user_data és persistent entre diverses execucions del bot (desde la mateixa màquina) per poder guardar l'estat de l'_enquesta activa_ i començar l'execució del bot podent usar totes les comandes (després de la primera execució).

## Running the tests

### Test run

This is a sample run from the bot. First of all, run the start command

## Tests d'estil de codi

Usa `pycodestyle` amb cada fitxer \*.py per comprovar que compleixen els estàndards pep8 (tret de la llargada de línia).


## Author

Joan Francesc Muntaner González
[joan.francesc.muntaner@est.fib.upc.edu]
