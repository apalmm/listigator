from bs4 import BeautifulSoup
import requests
import time

from sqlite3 import DatabaseError, IntegrityError, OperationalError, connect
from contextlib import closing

def verify(td):
    for val in td:
        if val == None or val == "":
            return False
    return True

def main():
    DATABASE_URL = './FLLawyers.sqlite'
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
            #For the loop, have to run not as loop but one by one bc too many requests; can fix later not critical
            for field in [("J02","Juvenile"), ("G09", "Guardianships"), ("C04","Civil+Rights"), ("C16","Criminal"), ("I07","Human+Rights"), ("I01","Immigration-Naturaliza"), ("I02","Indian")]:# missing "Cannabis", "LGBTQ" compared to WA 
                URL = "https://www.floridabar.org/directories/find-mbr/?sdx=N&eligible=Y&deceased=N&pracAreas=" #J02&pageNumber=1"
                URL += field[0]
                URL += "&pageNumber="
                page = requests.get(URL)
                soup = BeautifulSoup(page.content, "html.parser")
                results = 10
                try:
                    results = int(soup.find('p', class_ = "result-message").text.split()[5].replace(',',''))
                except:
                    print(soup.find('p', class_ = "result-message"))
                    print(field)
                    print(URL)
                    time.sleep(150) #cheap fix nvm doesnt work
                    results = int(soup.find('p', class_ = "result-message").text.split()[5].replace(',',''))
                pages = (results - 1) // 50
                print(results) 
                print(pages)
                # URL += "&pageNumber="
                for i in range(1, pages + 2):
                    URLi = URL + str(i) + "&pageSize=50"#adds actual page we check
                    page = requests.get(URLi)
                    soup = BeautifulSoup(page.content, "html.parser")
                    table_rows = soup.find_all('li', class_ = "profile-compact")
                    # print(table_rows)
                    for tr in table_rows:
                        # print(tr)
                        try:
                            name = tr.find('p', class_ = "profile-name").text
                            barid = tr.find('p', class_ = "profile-bar-number").find('span').text[1:]
                            contact = tr.find('div', class_ = "profile-contact").find_all('p')
                            city = str(contact[0]).split("<br/>")[-1].split(',')[0]
                            phone = contact[1].find('a').text
                            try: 
                                stmt_str = "INSERT INTO Lawyer (LicenseNumber, Name, City, Status, Phone) \
                                    VALUES (:id, :name, :city, :status, :phone)"
                                cursor.execute(stmt_str, {"id": int(barid),
                                                        "name": name,
                                                        "city": city,
                                                        "status":'Active',
                                                        "phone": phone})
                                # cursor.fetchall()
                            except IntegrityError:
                                print("Repeat")
                                print(name)
                                print(barid)
                            stmt_str = "INSERT INTO Field (Field, LicenseNumber) \
                                        VALUES (:field, :id)"
                            cursor.execute(stmt_str, {"field": field[1],
                                                    "id": int(barid)})
                        except:
                            print(tr)
                        # print(phone)
                        # td = tr.find_all('td')
                        # if verify(td):
                        

if __name__ == '__main__':
    main()
