"""Esimerkki rajapinnan käytöstä"""

from yritysApi import YritysQuery, YRITYSApi
from json_transfer import YritysRekisteriMuutos, OHJELMATEKNINEN
import json

RESULT_DIR = "/results"

def save_json(dir:str, data):
    with open(dir, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():

    name = "testiHEL"
    all_results = RESULT_DIR + name + "_all" + ".json"
    limited = RESULT_DIR + name + "_lmtd"+".json"
    test = YritysQuery()
    test.mainBusinessLine = 62100
    test.location = "Helsinki"
    test.registrationDateStart = "2020-01-01"
    api = YRITYSApi()

    companies = api.get_pages(test)
    print(f"Haettiin yrityksiä: {len(companies)}")
    save_json(all_results, companies)

    new_set = []
    for company in companies:
        valid, new_data = OHJELMATEKNINEN.transform(company)
        if valid:
            new_set.append(new_data)


    print("Muunnoksen jälkeen tallennetaan: ", len(new_set))
    save_json(limited, new_set)

if __name__ == "__main__":
    main()