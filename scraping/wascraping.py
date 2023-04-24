from bs4 import BeautifulSoup
import requests

from sqlite3 import DatabaseError, IntegrityError, OperationalError, connect
from contextlib import closing

def verify(td):
    for val in td:
        if val == None or val == "":
            return False
    return True

def main():
    DATABASE_URL = './WALawyers.sqlite'
    # CREATE TABLE "Field" (
    # 	"Field"	TEXT NOT NULL,
    # 	"LicenseNumber"	INTEGER NOT NULL,
    # 	PRIMARY KEY("Field","LicenseNumber")
    # )

    # CREATE TABLE "Lawyer" (
    # 	"LicenseNumber"	INTEGER NOT NULL UNIQUE,
    # 	"Name"	TEXT NOT NULL,
    # 	"City"	TEXT NOT NULL,
    # 	"Status"	TEXT NOT NULL,
    # 	"Phone"	TEXT NOT NULL,
    # 	PRIMARY KEY("LicenseNumber")
    # )


    with connect(DATABASE_URL, isolation_level=None,uri=True) as connection:
        with closing(connection.cursor()) as cursor:
            for field in ["Juvenile", "Guardianships", "Cannabis", "Civil+Rights", "Criminal", "Human+Rights", "Immigration-Naturaliza", "Indian", "LGBTQ"]:
            # field = "Civil+Rights" #change this for different practice fields u want to add; don't add same one twice (causes problems - too lazy to fix rn)
            #["Juvenile", "Guardianships", "Cannabis", "Civil+Rights"]
            # ["Juvenile", "Guardianships", "Cannabis", "Civil+Rights", "Criminal", "Disability", "Employment", "Family" ,"Foreclosure", "Health", "Housing", "Human+Rights", "Immigration-Naturaliza", "Indian", "LGBTQ"]
                URL = "https://www.mywsba.org/PersonifyEbusiness/LegalDirectory.aspx?ShowSearchResults=TRUE&EligibleToPractice=Y&AreaOfPractice="
                URL += field
                page = requests.get(URL)
                soup = BeautifulSoup(page.content, "html.parser")
                results = int((soup.find('span', class_ = "results-count").text).split()[0]) 
                pages = (results - 1) // 20 
                URL += "&Page="
                for i in range(0, pages + 1):
                    URLi = URL + str(i) #adds actual page we check
                    page = requests.get(URLi)
                    soup = BeautifulSoup(page.content, "html.parser")
                    table_rows = soup.table.find_all('tr', class_ = "grid-row")

                    for tr in table_rows:
                        td = tr.find_all('td')
                        if verify(td):
                            try: 
                                stmt_str = "INSERT INTO Lawyer (LicenseNumber, Name, City, Status, Phone) \
                                    VALUES (:id, :name, :city, :status, :phone)"
                                cursor.execute(stmt_str, {"id": int(td[0].text),
                                                        "name": td[1].text + " " + td[2].text,
                                                        "city": td[3].text,
                                                        "status":td[4].text,
                                                        "phone": td[5].text})
                                # cursor.fetchall()
                            except IntegrityError:
                                print("Repeat")
                                print(td)
                            stmt_str = "INSERT INTO Field (Field, LicenseNumber) \
                                        VALUES (:field, :id)"
                            cursor.execute(stmt_str, {"field": field,
                                                    "id": int(td[0].text)})

if __name__ == '__main__':
    main()
