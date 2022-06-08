from lxml import etree
from acdh_tei_pyutils.tei import TeiReader
from datetime import datetime

import os
import requests
import glob

BASEROW_TOKEN = os.environ.get('BASEROW_TOKEN')
XML_TABLE_ID = "71550"
ROW_API = "https://api.baserow.io/api/database/rows/table/"
DIR = "werke"

def verify_xml(dir):
    works = glob.glob('./werke/*/*.xml')
    print(f"{len(works)} Werk(e) gefunden.")
    array = []
    date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    for x in works:
        filename = x
        try:
            doc = TeiReader(x)
            data = "no errors found"
            array.append({
                "verification_errors": data,
                "filename": filename,
                "verified": True,
                "date": date
            })
            print(data)
            print("updating baserow table xml")
        except Exception as e:
            data = e
            array.append({
                "verification_errors": data,
                "filename": filename,
                "verified": False,
                "date": date
            })
            print(data)
            print("updating baserow table xml")
    # print(array)
    return array

# with open(f"logs/log__{datetime.today().strftime('%Y-%m-%d_%H:%M:%S')}.txt", "a") as f:
#     data = f"no errors found in werke/{work}/{w} \n"
#     f.write(data)

def get_base_row():
    url = f"{ROW_API}{XML_TABLE_ID}/?user_field_names=true"
    next_page = True
    while next_page:
        print(url)
        response = None
        result = None
        x = None
        response = requests.get(
            url,
            headers={
                "Authorization": f"Token {BASEROW_TOKEN}"
            }
        )
        result = response.json()
        next_page = result['next']
        url = result['next']
        for x in result['results']:
            yield(x)

def update_base_row():
    rows = verify_xml(DIR)
    for r in rows:
        if r["filename"] in [x["filename"] for x in get_base_row()]:
            # print(r["filename"])
            # print([x["filename"] for x in getBaseRow()])
            id = [x["id"] for x in get_base_row()]
            for i in id:
                url = f"{ROW_API}{XML_TABLE_ID}/{i}/?user_field_names=true"
                print(url)
                try:
                    p = requests.patch(
                        url,
                        headers={
                            "Authorization": f"Token {BASEROW_TOKEN}",
                            "Content-Type": "application/json"
                        },
                        json = r
                    )
                    # print(p.json())
                    # print(p)
                except Exception as err:
                    print(err)
        else:    
            try:
                p = requests.post(
                    f"{ROW_API}{XML_TABLE_ID}/?user_field_names=true",
                    headers={
                        "Authorization": f"Token {BASEROW_TOKEN}",
                        "Content-Type": "application/json"
                    },
                    json = r
                )
                # print(p.json())
            except Exception as err:
                print(err)

update_base_row()
