#importing mysql db (along with decorator function)
import mysql.connector as sql

# #importing libraries for scraping
import requests
import urllib.request
import time
from bs4 import BeautifulSoup

import re

db = sql.connect(host="localhost", user="pranav", passwd="vltnfot", db="py_assignment")

username = input("Please enter your username\n")
n = 0
cname = ""
ccity = ""
cwork = list()
cfav = list()

# decorator function
def check_user(xxx):
    user1 = username

    def inner1(user1):
        cur = db.cursor()
        q1 = "select * from user where username = '{}'".format(user1)
        cur.execute(q1)
        user2 = cur.fetchone()
        if (user2 == None):
            print ("Invalid username")
            cur.close()
            db.close()
            exit()

        cur.close()
        xxx(user1)

    return inner1

@check_user
def test(x):
    pass

#test(username)

class Person:
    
    def __init__(self, name, work = [], city="Roorkee"):
        self.name = name
        self.city = city
        if len(work)!=0:
            self.work = work

    def show(self):
        print(f"My name is {self.name} and my city is {self.city}")


p1 = Person("pranav")
p1.show()
# print(p1.work)


def check(asdd):

        user3 = username

        def inner2(user3):
                print("hgaggkk")
        if n == 0:
                pass

        else:
                p2.show()

        asdd(user3)
        return inner2

@check
def scrap(username):
        print('hi')
        test(username)
        n = 1

        url = f"https://en-gb.facebook.com/{username}"
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page)
    #print (soup.prettify())
    
#     name = soup.find("span", id = "fb-timeline-cover-name").string
        name = soup.find("title", id = "pageTitle").string
        print(name)
        a = name.index('|')
        print(name[0:a])
#     name1 = ""
#     for link in name:
#         name1 = name1 + link

        cname = name
#     print(name1)

        city = soup.find("span", class_="_2iel _50f7").string
        print(city)
        ccity = city
        # for s in city:
        #         print (s)

        # work = soup.find_all("div", class_="_2lzr _50f5 _50f7")
        work = soup.find_all("div", class_="_4qm1")
        # print(work)
        for w in work:
                # print(w)
                ws = w.find("a").string
                # print(ws)
                cwork.append(ws)

        print(cwork)

        fav = soup.find_all("div", id = "u_0_e")
        print(fav)
        for f in fav:

                try:
                        fa = f.find("a").string
                        print(fa)
                        cfav.append(fa)
                except:
                        print("qwerty")
                finally:
                        print(len(cfav))
                        if len(cfav) == 0:
                                print("empty dictionary")
                        else:
                                print(cfav)

p2 = Person(cname, cwork, ccity)

scrap("shaddygarg")
