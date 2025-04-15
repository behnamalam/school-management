def menu_start():
    print("1 - admin")
    print("2 - user")
    selection = int(input("please enter you selection : "))
    return selection


def menu_enter_user():
    print("1 - login")
    print("2 - signup")
    print("3 - back")
    selection = int(input("please enter you selection : "))
    return selection


def admin_menu():
    print("1 - set date/time exam")
    print("2 - add/edit students info")
    print("3 - show/reply tickets")
    selection = int(input("plz enter your selection : "))
    return selection


def user_menu():
    print("1 - start exam")
    print("2 - show your grade")
    print("3 - submit/show a ticket")
    print("4 - show billboard")
    selection = int(input("plz enter your selection : "))
    return selection
