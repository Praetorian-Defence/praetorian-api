# Podporované zdroje prístupov

Praetorian API komunikuje v troch smeroch a to na **klientov** (zariadenia, ktoré napríklad zahajujú nasadenie produktu)
,**servery** (zariadenia koncových používateľov na ktoré sa produkt nasadzuje) a **dátové úložiská**.

## Prístup ku klientom

> Tu sú zahrnuté všetky typy komunikačných protokolov, ktorými sa vie klient spojiť so serverom Praetorian API.

### HTTPS

Prístup ku klientom bude realizovaný pomocou HTTPS protokolu, ktorý bude predovšetkým slúžiť na nastavovanie, získavanie,
ukladanie dát a rôzne iné správy manažmentu servera Praetorian API.

### SSH

Prístup ku klientom bude taktiež realizovaný pomocou SSH protokolu, kde Praetorian API bude zastávať rolu SSH servera,
ku ktorému sa daný klient pri začatí akcie nasadenia pripojí pomocou privátneho kľúča. Daný kľúč sa pri vyžiadaní o pripojenie
skontroluje so zoznamom povolených zariadení. Po úspešnom pripojení bude môcť klient cez SSH server posielať príkazy,
ktoré Praetorian API presmeruje na dané koncové zariadenie.

## Prístup k serverom

> Tu sú zahrnuté všetky typy komunikačných protokolov, ktorými sa vie server Praetorian API spojiť s koncovými zariadeniami.

### SSH

Praetorian API bude uchovávať v dátových úložiskách zašifrované prístupové informácie ku koncovým zariadeniam. Po získaní
prístupov, bude možné na určitý časový interval komunikovať s koncovým zariadením cez SSH protokol, pričom pred ukončením
spojenia a vždy v pravidelnom časovom intervale sa budú prístupové údaje na koncové zariadenia z bezpečnostných dôvodov meniť.

## Prístup k dátovým úložiskám

> Tu sú zahrnuté všetky typy protokolov, ktorými sa vie server Praetorian API spojiť dátovými úložiskami,
> uchovávajúce predovšetkým veľmi dôverné a citlivé dáta.

### TCP/IP (PostgreSQL)

Praetorian API bude cez protokol TCP/IP pripojený k PostgreSQL databáze, ktorá bude uchovávať všetky dôležité prístupové údaje.

### LDAP

V prípade LDAP autentifikácie, bude Praetorian API vedieť komunikovať s nastaveným adresárovým serverom, kde vie skontrolovať
platnosť prístupových údajov.
