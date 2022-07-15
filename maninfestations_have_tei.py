import glob
import xml.etree.ElementTree as ET
import pandas as pd

files = glob.glob('./werke/*/*.xml')

ns = {"tei": "http://www.tei-c.org/ns/1.0", "xml": "https://www.w3.org/XML/1998/namespace"}

data = []
for x in files:
    tree = ET.parse(x)
    for work_id in tree.findall(".//tei:seriesStmt/tei:idno[@type='api']", namespaces=ns):
        work_id_text = work_id.text
        work_id = work_id_text.split('/')[-1]
    for man_id in tree.findall(".//tei:listBibl/tei:bibl/tei:idno[@type='api']", namespaces=ns):
        man_id = man_id.text
        man_id = man_id.split('/')[-1]
    data.append([x.split('/')[-1], work_id, man_id, True])
    
df = pd.DataFrame(data, columns=['file', "work_id", 'man_id', "tei"])

df.to_csv("manifestations_have_tei.csv", sep=',', encoding='utf-8', index=False)