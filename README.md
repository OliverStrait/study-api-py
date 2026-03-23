# Opiskeluprojekti julkisen Api:n käyttö ja joustavan rajapinnan luonti 

- Api määritelmän mukainen API-pinta joka abstraktoi haun osoitteen muodostuksen ja tarjoaa tyypitetyt muodot käyttäjälle.
- Abstrakteja luokkia käsittelemään `Dictionary` datatyypin puurekenteen ja datan muokkaukseen.
    - Näillä työkaluilla voi rakentaa rajapinnan joka muuntaa dataa kahden json-skeeman välillä

## Esimerkki käytöstä
- `esim_data_fetch_transform.py` tiedosto hakee julkisesta rajapinnasta dataa ja tallentaa sen json muotoon
- `filter_json_file.py` - Validoi ja muokkaa json-tiedoston tietokannan käyttämään formaattiin. Tallentaa uuteen json-tiedostoon
- `json_to_mongoDB.py` - Muunnettu data tallennetaan mongoDB-tietokantaan

## Ulkoiset rajapinnat
- Yritysten data (HTTP/REST): https://avoindata.prh.fi/fi/ytj/swagger-ui

## Jatkoa
- [ ] Luo CLI-rajapinta argumenttien syöttöön.