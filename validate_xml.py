from lxml import etree
from datetime import datetime
from pathlib import Path

import os

works = os.listdir('werke')
print(f"{len(works)} Werk(e) gefunden.")

p = Path('logs')
try:
    p.mkdir()
except FileExistsError:
    print("logs directory already exists")

for work in works:
    files = os.listdir(f"werke/{work}")
    for w in files:
        if ".xml" in w:
            print(f"{files.count(w)} Manifestation(en) in {work} gefunden.")
            parser = etree.XMLParser()
            print(f"parsing Manifestation: werke/{work}/{w}")
            try: 
                tree = etree.parse(f"werke/{work}/{w}", parser)       
                with open(f"logs/log__{datetime.today().strftime('%Y-%m-%d_%H:%M:%S')}.txt", "a") as f:
                    data = f"no errors found in werke/{work}/{w} \n"
                    f.write(data)
            except Exception:
                print(f"{len(parser.error_log)} error(s) found. See log file for more info.")
                error = parser.error_log[0]
                with open(f"logs/log__{datetime.today().strftime('%Y-%m-%d_%H:%M:%S')}.txt", "a") as f:
                    data = f"error in file: werke/{work}/{w}: \n {error.message} in line {error.line} of column {error.column} \n"
                    f.write(data)
             
