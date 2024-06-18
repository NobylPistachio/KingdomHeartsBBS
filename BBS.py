import requests
from bs4 import BeautifulSoup
import json


def update_tables():
    "This looks at a resource and makes json file for "

    resources = [
        "https://www.finalfantasykingdom.net/bbsmelding.php",
        "https://bbsmeldguide.lol/"
    ]

    BBS_Guide_titles = []
    CRYSTAL_MELDING_OUTCOMES = {}
    CRYSTAL_TYPES = []
    ATTACK_COMMANDS = []
    MAGIC_COMMANDS = []
    ACTION_COMMANDS = []
    SHOTLOCK_COMMANDS = []

    BBS_MELDING_GUIDE = {
    "Crystal Melding Outcomes": CRYSTAL_MELDING_OUTCOMES,
    "Action Commands": ACTION_COMMANDS,
    "Attack Commands": ATTACK_COMMANDS,
    "Magic Commands": MAGIC_COMMANDS,
    "Shotlock Commands": SHOTLOCK_COMMANDS
    }

    r = requests.get(resources[0])
    soup = BeautifulSoup(r.content, "html.parser")

    a = soup.find(class_ = "text2")
    b = a.parent
    for elem in b.find_all("p",align = "center"):
        BBS_Guide_titles.append(elem.text)

    tables = b.find_all("table")

    #Compiles CRYSTAL TYPES
    for crystals in soup.find(class_ = "text2").parent.find_all("table")[1].find_all("tr")[0].find_all("td"):
        CRYSTAL_TYPES.append(crystals.text)

    #Compiles CRYSTAL MELDING OUTCOMES TABLE
    rows = tables[1].find_all("tr")
    for row in rows:
        if row == rows[0]:
            continue
        columns = row.find_all("td")
        crystalType = columns[0].text
        for column in columns:
            if column == columns[0]:
                CRYSTAL_MELDING_OUTCOMES[f"Type {crystalType}"] = {}
                continue
            columnCrystalType = CRYSTAL_TYPES[columns.index(column)-1]
            CRYSTAL_MELDING_OUTCOMES[f"Type {crystalType}"][f"{columnCrystalType}"] = column.text

    def make_table(table_number:int,table_name:list):
        #Compiles COMMANDS TABLE
        rows = tables[table_number].find_all("tr")
        title_row = rows[0].find_all("td")
        for row in rows[1:]:
            row_object = {}
            columns = row.find_all("td")
            for i,column in enumerate(columns):
                column_title = title_row[i].text.strip()
                if column_title == "Used By":
                    usedBy2 = {"Terra": False, "Ventus": False, "Aqua": False}
                    img_sources = ['bbs/dlterra1.png','bbs/dlventus1.png','bbs/dlaqua1.png','bbs/blank.png',]
                    for count,img in enumerate(column.find_all("img")):
                        user = list(usedBy2.keys())[count]
                        if img["src"] != 'bbs/blank.png':
                            usedBy2[user] = True
                        else:
                            usedBy2[user] = False
                    row_object[column_title] = usedBy2
                    continue
                row_object[column_title] = column.text.strip()
            table_name.append(row_object)

    make_table(2,ATTACK_COMMANDS)
    make_table(3,MAGIC_COMMANDS)
    make_table(4,ACTION_COMMANDS)
    make_table(5,SHOTLOCK_COMMANDS)

    def create_json_file(file_name, dictionary):
        try:
            with open(file_name,"x") as file:
                json.dump(dictionary, file, indent=4)
        except:
            print(f"{file_name} already created")

    create_json_file("CRYSTAL_MELDING_OUTCOMES.json",CRYSTAL_MELDING_OUTCOMES)
    create_json_file("ATTACK_COMMANDS.json",ATTACK_COMMANDS)
    create_json_file("MAGIC_COMMANDS.json",MAGIC_COMMANDS)
    create_json_file("ACTION_COMMANDS.json",ACTION_COMMANDS)
    create_json_file("SHOTLOCK_COMMANDS.json",SHOTLOCK_COMMANDS)
    create_json_file("BBS_MELDING_GUIDE.json",BBS_MELDING_GUIDE)

if __name__ == "__main__":
    update_tables()