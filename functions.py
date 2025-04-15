import re
import datetime
import os
import json
import pyfiglet
import pandas as pd
import requests
from bs4 import BeautifulSoup
from arabic_reshaper import reshape
from bidi.algorithm import get_display

# r : read
# w : write
# a : append

def json_books():
    if not os.path.exists("books.json"):
        with open("books.json","w") as myfile :
            json.dump({},myfile)


def request_website():
    # request a site 
    response = requests.get("http://chap.sch.ir/guide-books")
    return response


def show_bilboard():
    names = []
    with open("users.json","r") as myfile:
        result = json.load(myfile)
        for every_user in result.keys():
            if float((result[every_user]["data"]["score"])) >= 19 :
                names.append(every_user)
    
    # show billboard
    item_name = 1
    for every_user in names:
        print(f"{item_name}-{every_user}")
        item_name += 1
        
def extract_site(response):
    
    grades = ["7th","8th","9th"]
    index_grade = 0
    content = BeautifulSoup(response.content,"html.parser")
    # list
    all_tables = content.find_all("table")
    with open("books.json" ,"r" , encoding="utf-8") as myfile:
       
        result = json.load(myfile)
        for every_table in all_tables:
            if index_grade == 3 :
                break
            # list 
            all_trs = every_table.find_all("tr")  
            books = []  
            for every_tr in all_trs:
                #list
                all_tds = every_tr.find_all("td")
                for every_td in all_tds:
                    books.append("".join(re.findall(r"[آ-ی\s]+",every_td.get_text())).strip("\n"))
            result[grades[index_grade]] = books
            print(result)
            index_grade += 1
            print("**************************")
    
    with open("books.json","w" , encoding="utf-8") as myfile:
        json.dump(result,myfile,ensure_ascii=False)


def show_books(username):
    with open("users.json","r") as myfile :
        grade =  json.load(myfile)[username]["data"]["grade"]
        with open("books.json","r",encoding="utf-8") as myfile2:
            result_books = json.load(myfile2)
            item = 1 
            if grade == "7":
                for every_book in (result_books["7th"]):
                    print(f"{item}-{get_display(reshape(every_book))}")
                    item += 1
            elif grade == "8":
               for every_book in (result_books["8th"]):
                    print(f"{item}-{get_display(reshape(every_book))}")
                    item += 1
            elif grade == "9":
                for every_book in (result_books["9th"]):
                    print(f"{item}-{get_display(reshape(every_book))}")
                    item += 1


def check_json_file_exist_or_not():
    if not os.path.exists("users.json"):
        with open("users.json", "w") as myfile:
            json.dump({}, myfile)


def signup_user(username: str, password: str):
    with open("users.json", "r") as myfile:
        result = json.load(myfile)  # {}

    result[username] = {"data":{"email":None,"grade":None,"score":None},"password": password, "tickets": []}  # {"behnam1381":"1234"}

    with open("users.json", "w") as myfile:
        json.dump(result, myfile)


def login_user(username, password):
    with open("users.json", "r") as myfile:
        result = json.load(myfile)
    try:
        password_save = result[username]["password"]
        if password_save == password:
            return pyfiglet.figlet_format(f"Welcome {username}", font="digital"), True
        else:
            return "please check username or password", False
    except KeyError:
        return f"{username} not valid", False

def show_edit_profile(username):
    with open("users.json","r") as myfile:
        result = json.load(myfile)
        data_user = result[username]["data"]
        df = pd.DataFrame(data=data_user,index=[f"data {username}"])
        print(df)
        selection_change = int(input("which element do you want to change ?\n1.email\n2.grade\n3.score "))
        if selection_change == 1:
            new_email = input(f"please enter email's {username} : ")
            data_user["email"] = new_email
            with open("users.json","w") as myfile:
                json.dump(result,myfile)
        elif selection_change == 2:
            new_grade = input(f"please enter grade's {username} : ")
            data_user["grade"] = new_grade
            with open("users.json","w") as myfile:
                json.dump(result,myfile)
        elif selection_change == 3:
            new_score = input(f"please enter score's {username} : ")
            data_user["score"] = new_score
            with open("users.json","w") as myfile:
                json.dump(result,myfile)
        else:
            data = input(f"please enter the data's {username}\ne.x => info@example.com 7 : ").split()
            data_user["email"] = data[0]
            data_user["grade"] = data[1]
            with open("users.json","w") as myfile:
                json.dump(result,myfile)
        

def check_unread_ticket(username:str):
    with open("users.json","r") as myfile:
        result = json.load(myfile)
        tickets_user = result[username]["tickets"]
        for every_ticket in tickets_user:
            replies = every_ticket[2]    
            if len(replies) != 0:
                for every_reply in replies:
                    if every_reply[2] == False:
                      
                        print("✉︎  you have one unread message ")


def show_current_ticket_for_user(username):
    with open("users.json", "r") as myfile:
        result = json.load(myfile)
        all_tickets = result[username]["tickets"]
        df = pd.DataFrame(all_tickets, columns=["ticket", "sender", "replies"],index=[f"ticket{i+1}" for i in range(len(all_tickets))])
        print(df)
        reply = input("please select which ticket do you want to reply ? : ")
        index = int("".join(re.findall(r"\d",reply))) - 1
        all_replies = all_tickets[index][2]
        if len(all_replies) == 0:
            print("there is no reply ...")
        else:
            filter_row = df.loc[reply,"replies"]
            print(pd.DataFrame(data=filter_row,columns=["replies","sender"],index=[f"reply{i+1}" for i in range(len(all_replies))]))   
        print("\n\n")
        new_message = input("please enter reply to message : ")
        all_replies.append([new_message,"user"])


        with open("users.json","w") as myfile2:
                json.dump(result,myfile2)


def submit_ticket(ticket, username):
    with open("users.json", "r") as myfile:
        result = json.load(myfile)
        data_user = result[username]
        ticket_data = data_user["tickets"]
        ticket_data.append([ticket, "user", []])
        data_user["tickets"] = ticket_data

    with open("users.json", "w") as myfile:
        json.dump(result, myfile)


def show_reply_tickets(username:str):
    with open("users.json", "r") as myfile:
        result = json.load(myfile)
        if username in result.keys():
            all_tickets = result[username]["tickets"]
            df = pd.DataFrame(all_tickets, columns=["ticket", "sender", "replies"],index=[f"ticket{i+1}" for i in range(len(all_tickets))])
            print(df)
            reply = input("please select which ticket do you want to reply ? : ")
            index = int("".join(re.findall(r"\d",reply))) - 1
            all_replies = all_tickets[index][2]
            if len(all_replies) == 0:
                print("there is no any reply")
            else:
                filter_row = df.loc[reply,"replies"]
                print(pd.DataFrame(data=filter_row,columns=["replies","sender"],index=[f"reply{i+1}" for i in range(len(all_replies))]))   
            print("\n\n")
            new_message = input("please enter reply to message : ")
            all_replies.append([new_message,"admin",False])


            with open("users.json","w") as myfile2:
                json.dump(result,myfile2)
                

            
        else:
            return f"{username} not found !"



def set_date_time_exam(
    copy_var: str,
    dateexam: datetime.date,
    timeexam: datetime.time,
    datetimeexam: datetime.datetime,
):
    if re.search(
        r"(?:20[0-9][0-9]\/(?:0[0-9]|1[0-2])\/(?:[0-2][0-9]|3[01])|20[0-9][0-9]-(?:0[0-9]|1[0-2])-(?:[0-2][0-9]|3[01]))\s(?:(?:(?:1[0-9]|2[0-3])|(?:[0-9])):(?:[0-5][0-9]|0))",
        copy_var,
    ):
        oldDateTime = datetimeexam
        dateTimeSplit = copy_var.split()
        if "/" in dateTimeSplit[0]:
            dateSplit = dateTimeSplit[0].split("/")
        elif "-" in dateTimeSplit[0]:
            dateSplit = dateTimeSplit[0].split("-")

        TimeSplit = dateTimeSplit[1].split(":")
        datetimeexam = datetime.datetime(
            int(dateSplit[0]),
            int(dateSplit[1]),
            int(dateSplit[2]),
            int(TimeSplit[0]),
            int(TimeSplit[1]),
            0,
        )
        return f"DateTime changed from {oldDateTime} to {datetimeexam}", datetimeexam
    elif re.search(r"\b(?:(?:1[0-9]|2[0-3])|(?:[0-9])):(?:[0-5][0-9]|0)", copy_var):
        oldTime = timeexam
        timeSplit = copy_var.split(":")
        timeexam = datetime.time(int(timeSplit[0]), int(timeSplit[1]), 0)
        return f"Time Changed from {oldTime} to {timeexam}", timeexam
    elif re.search(
        r"(?:20[0-9][0-9]\/(?:0[0-9]|1[0-2])\/(?:[0-2][0-9]|3[01])|20[0-9][0-9]-(?:0[0-9]|1[0-2])-(?:[0-2][0-9]|3[01]))",
        copy_var,
    ):
        oldDate = dateexam
        if "/" in copy_var:
            dateSplit = copy_var.split("/")
        elif "-" in copy_var:
            dateSplit = copy_var.split("-")

        # change date
        dateexam = datetime.date(
            int(dateSplit[0]), int(dateSplit[1]), int(dateSplit[2])
        )
        return f"Date Changed from {oldDate} to {dateexam}", dateexam


def check_date_time(datetimeexam: str):
    date, time = datetimeexam.split()
    time = ":".join(time.split(":")[:2])
    # print(date_time)
    if "-" in date:
        now_date, now_time = datetime.datetime.now().date().strftime(
            "%Y-%m-%d"
        ), datetime.datetime.now().time().strftime("%H:%M")
    elif "/" in date:
        now_date, now_time = datetime.datetime.now().date().strftime(
            "%Y/%m/%d"
        ), datetime.datetime.now().time().strftime("%H:%M")

    print(date == now_date)
    print(time == now_time)

    # 18:30 --> 18:29 --> 18:28
    # 18:30 --> 18:31 --> 18:32

    # NOW
    now_hour, now_minute = int(now_time.split(":")[0]), int(now_time.split(":")[1])

    # ADMIN
    admin_hour, admin_minute = int(time.split(":")[0]), int(time.split(":")[1])

    after, before = int(admin_minute) + 2, int(admin_minute) - 2
    after_list = list(range(int(admin_minute), after + 1, 1))
    before_list = list(range(int(admin_minute), before + 1, -1))

    if now_hour == admin_hour and (
        int(now_minute) in after_list or int(now_minute) in before_list
    ):

        print("now you can start exam")
    else:
        print("try again later")
