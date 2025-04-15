from menus import *
from functions import *
import datetime
import json


# 3:30:00
dateexam = datetime.datetime.fromtimestamp(0).date()
timeexam = datetime.datetime.fromtimestamp(0).time()
datetimeexam = str(dateexam) + " " + str(timeexam)

check_json_file_exist_or_not()
json_books()

while True:
    selection = menu_start()
    if selection == 1:
        selection_admin = admin_menu()
        if selection_admin == 1:
            message = input("change date or time or both ?")
            copy_var = None
            if message == "date":
                date = input("please enter the date \n2012/10/10 | 2012-10-10\nEnter : ")
                copy_var = date
            elif message == "time":
                time = input("please enter the time \n12:00 | 12:0\nEnter :  ")
                copy_var = time
            elif message == "both":
                datetime_user = input("please enter the datetime\n2012/10/10 12:00 | 2012-10-10 12:00\nEnter :  ")
                copy_var = datetime_user
            result = set_date_time_exam(copy_var,dateexam,timeexam,datetimeexam)
            if "Date" in result[0] :
                dateexam = result[1]
                datetimeexam = str(dateexam) + " " + str(timeexam)
            elif "Time" in result[0]:
                timeexam = result[1]
                datetimeexam = str(dateexam) + " " + str(timeexam)
            elif "DateTime" in result[0]:
                datetimeexam = result[1]
            print(result[0])
        elif selection_admin == 2:
            username = input("please enter username to show/edit profile : ")
            show_edit_profile(username)
        elif selection_admin == 3:
           
            username = input("please enter username to show/reply her/his tickets : ")
           
            show_reply_tickets(username)
          
            
    elif selection == 2:
        selection_enter_user = menu_enter_user()
        if selection_enter_user == 1:
            username , password = input("please enter username to login : ") , input("please enter password to login : ")
            login_result = (login_user(username,password))
            print(login_result[0])
            check_unread_ticket(username)
            if login_result[1]:
                selection_user = user_menu()
                if selection_user == 1:
                    show_books(username)
                elif selection_user == 2:
                    response = request_website()
                    extract_site(response)
                    

                elif selection_user == 3:
                    message = input("show or submit a new ticket ? ")
                    if message == "show":
                        show_current_ticket_for_user(username)
                    elif message == "submit" : 
                        ticket = input("please enter your ticket : ")
                        submit_ticket(ticket,username)
                elif selection_user == 4:
                    show_bilboard()



        elif selection_enter_user == 2:
            username , password = input("please enter username to signup : ") , input("please enter password to signup : ")
            signup_user(username,password)
        elif selection_enter_user == 3:
            pass
        # selection_user = user_menu()
        # if selection_user == 1:
        #     check_date_time(datetimeexam)
        # elif selection_user == 2:
        #     pass
        # elif selection_user == 3:
        #     pass
        # elif selection_user == 4:
        #     pass
