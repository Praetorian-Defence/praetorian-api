# Sada funkcií

## Pripojenie klienta na SSH server Praetorian API

1. ...

## Pripojenie Praetorian API na koncové zariadenie



## Registrácia



## Prihlásenie



## SSH Proxy

1. ssh server vypublikuje port a bude mat tabulku ssh povolenych klientov (property, expiracia, je jednorazovy?)

1. zavolam post create session

2. vrati heslo meno pouzivatela alebo certifikat

## Pridanie nového projektu



## Pridanie nového zariadenia klienta



## Pridanie nového koncového zariadenia

Featurky:
1. Moznost mat interaktivny shell priamo cez praetorian-ssh-proxy

Ak sa uskutocnuje deploy cez fabric vytvori sa docatny user ktory je autentifikovany klucom a bool hodnotou
is_interactive na False.

Ak existuje normalny pouzivatel postgres/ldap tak ma hodnotu is_interactive na True, tak moze pouzit interaktivny shell
ako napriklad: `ssh zurek+afs@localhost -p 22`, vtedy mu bude spristupnena interaktivna shell na dane koncove zariadenie.
Ak nezadá koncove zariadenie: `ssh zurek@localhost -p 22`, praetorian-ssh-proxy mu da na vyber z koncovych zariadeni na
ktore sa moze pripojit.

2. Whitelist/blacklist na commandy, ktore budu/nebudu moct byt povolene.

3. Reporting pre danu ssh session - pri zahajeni novej session sa vytvori docasny file ktory bude zaznamenavat vsetky
commandy aj s vystupom. Po skonceni ssh session sa obsah súboru nakopíruje do databázy a súbor sa zmaže. Format moze byt
dict s klucami timestamp (potom by sa to dalo pretavit do videa).
