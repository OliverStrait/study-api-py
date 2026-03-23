"""Example of usage of jsonTransfer structures.
Vailed json-objects are saved into own file for debug-purposes
"""

import json
from json_transfer import OHJELMATEKNINEN
from pathlib import Path

read_json = Path("results/yritys_data_all.json").resolve()

with open(read_json, "r", encoding="utf-8") as f:
    jos = json.load(f)
    print("at start, lines", len(jos), flush=True)
    new_set = []
    failed = []
    for item in jos:

        try:
            valid, new_data = OHJELMATEKNINEN.transform(item)
            if valid:
                new_set.append(new_data)

        except Exception as e:
            name:str = item["names"][0]["name"]
            print("new exception failing: ", item["names"][0]["name"])
            failed.append(item)
            continue

    print("Valid transforms: ", len(new_set))
    print("Failed transforms: ", len(failed))

with open("suomi_ohjelmointi_tekninen" + ".json", "w", encoding="utf-8") as f:
    json.dump(new_set, f, ensure_ascii=False, indent=2)

with open("suomi_ohjelmointi_failed" + ".json", "w", encoding="utf-8") as f:
    json.dump(failed, f, ensure_ascii=False, indent=2)