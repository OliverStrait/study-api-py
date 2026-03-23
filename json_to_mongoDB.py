
import pymongo

import json

URI = "mongodb://localhost:27017/"

client = pymongo.MongoClient(URI)

db = client["yritysrekisteri"]
yri = db["tekniset_yritykset"]

def transfer():
    with open("suomi_ohjelmointi_tekninen.json", "r" , encoding="utf-8") as f:
        data = json.load(f,)
        print(data[0])
        for doc in data:
            yri.insert_one(doc)

def fetch_test():
    data = yri.find({
        # "Kaupunki": "HELSINKI",
                    #  "Website": {"$ne": None},
                     "Toimialakoodi":"/^62/"
                    }
                     )
    result = data.to_list()

    print("sample: ", result[0])
    print("Result: ", len(result))

# fetch()
transfer()