# Praetorian API

[Nasadenie vzdialeného prístupu](https://www.ibm.com/support/knowledgecenter/en/SSZJPZ_11.5.0/com.ibm.swg.im.iis.ds.parjob.dev.doc/topics/c_deeref_Remote_Deployment.html) 
spočíva v nasadení finálneho produktu poskytovateľa ku koncovým zariadeniam zákazníka bez nutnosti fyzického prístupu k zariadeniu. 
Praetorian API pokrýva všetky bezpečnostné aspekty tohto prípadu použitia ako napríklad [ochrana osobných údajov](https://en.wikipedia.org/wiki/Privacy), 
[autentifikácia](https://techterms.com/definition/authentication) alebo [autorizácia](https://auth0.com/docs/authorization).

## Motivácia

Hlavnou myšlienkou je nasadenie produktu vzdialeným prístupom jednoduchou a bezpečnou cestou, pričom medzi dôležité 
vlastnosti by mala byť zaradená správa konfiguračných nastavení a prístupov. Spôsobov prístupu by malo byť taktiež na 
výber niekoľko cez základný management.

Samotné riešenie by malo v procese nasadzovania zaujať takzvanú tretiu stranu, pričom klient by o koncovom zariadení 
nemal vedieť žiadne dôležité informácie ani naopak. Všetky dôležité informácie by mali byť uložené na bezpečnom mieste, 
ku ktorému má prístup iba samotná tretia strana.

## Príklady komunitných riešení nasadenia vzdialeného prístupu 

- [fabric](https://github.com/fabric/fabric)
- [capistrano](https://github.com/capistrano/capistrano)

## Testy

> Pracujeme na tom ...
