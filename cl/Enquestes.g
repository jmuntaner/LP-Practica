grammar Enquestes;

root : inst+ enquesta EOF ;

inst : pregunta | resposta | item | alternativa ;


pregunta : pid DOBLEPUNT PTK frase INTERROGATION ;

resposta : rid DOBLEPUNT RTK opcio+ ;

item : iid DOBLEPUNT ITK pid FLETXA rid ;

alternativa : aid DOBLEPUNT ATK iid OPENC (assig COMMA)* assig CLOSEC ;


opcio : NUM DOBLEPUNT frase PUNTCOMA ;

assig : OPENP NUM COMMA iid CLOSEP ;

enquesta : eid DOBLEPUNT ETK iid+ ENDTK ;


INTERROGATION : '?' ;
DOBLEPUNT : ':' ;
PUNTCOMA : ';' ;
FLETXA : '->' ;
OPENC : '[' ;
CLOSEC : ']' ;
COMMA : ',' ;
OPENP : '(' ;
CLOSEP : ')' ;


PTK : 'PREGUNTA' ;
pid : 'P' NUM ;
RTK : 'RESPOSTA' ;
rid : 'R' NUM ;
ITK : 'ITEM' ;
iid : 'I' NUM ;
ATK : 'ALTERNATIVA' ;
aid : 'A' NUM ;
ETK : 'ENQUESTA' ;
eid : STRING NUM?;
ENDTK : 'END' ;

frase: STRING+ ;

NUM : [0-9]+ ;
STRING: [a-zA-Z]+ ;
WS : [ \n\t\r]+ -> skip ;
