"""Adds pro bono lawyer classification to probono FL Lawyers"""
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


    with connect(DATABASE_URL, isolation_level=None,uri=True) as connection:
        with closing(connection.cursor()) as cursor:
            #For the loop, have to run not as loop but one by one bc too many requests
            for field in [("C16","Criminal",5), ("I01","Immigration-Naturaliza",3)]:#only included ones with lawyers; dont check if none in code so feed "safe" topics for now
                URL = "https://www.floridabar.org/directories/find-mbr/?sdx=N&eligible=Y&deceased=N&pracAreas=" #building out url w search par for scraping
                URL += field[0]
                URL += "&services=PBS"
                URL += "&pageNumber="
                page = requests.get(URL)
                soup = BeautifulSoup(page.content, "html.parser")
                results = 10
                try:
                    #getting number of results found to determine pages to scrape
                    results = int(soup.find('p', class_ = "result-message").text.split()[field[2]].replace(',','')) #if only one result do 3 instead of 5
                except:
                    print(soup.find('p', class_ = "result-message").text.split())
                    print(field)
                    print(URL)
                    time.sleep(150)
                    results = int(soup.find('p', class_ = "result-message").text.split()[field[2]].replace(',',''))
                pages = (results - 1) // 50
                print(results) 
                print(pages)
                for i in range(1, pages + 2):
                    URLi = URL + str(i) + "&pageSize=50"#adds actual page we check on
                    page = requests.get(URLi)
                    soup = BeautifulSoup(page.content, "html.parser")
                    table_rows = soup.find_all('li', class_ = "profile-compact") #profile-compact holds each person's info
                    for tr in table_rows:
                        try:
                            name = tr.find('p', class_ = "profile-name").text #grab name text
                            barid = tr.find('p', class_ = "profile-bar-number").find('span').text[1:] #cut the # and grab id
                            contact = tr.find('div', class_ = "profile-contact").find_all('p') #city and phone are in contact
                            city = str(contact[0]).split("<br/>")[-1].split(',')[0] #city is after the last <br/> and before the comma
                            phone = contact[1].find('a').text #grab first phone contact
                            try: 
                                stmt_str = "DELETE FROM Lawyer WHERE Lawyer.LicenseNumber = :id"
                                cursor.execute(stmt_str, {"id": int(barid)})
                                stmt_str = "INSERT INTO Lawyer (LicenseNumber, Name, City, Status, Phone) \
                                    VALUES (:id, :name, :city, :status, :phone)"
                                cursor.execute(stmt_str, {"id": int(barid),
                                                        "name": name,
                                                        "city": city,
                                                        "status":'Pro Bono',
                                                        "phone": phone})
                            except IntegrityError:
                                print(name)
                                print(barid)
                            #add back field they operate in, determined by search/loop
                            if(field[2]==5):
                                stmt_str = "INSERT INTO Field (Field, LicenseNumber) \
                                            VALUES (:field, :id)"
                                cursor.execute(stmt_str, {"field": field[1],
                                                        "id": int(barid)})
                        except:
                            print(tr)
                        

if __name__ == '__main__':
    main()
