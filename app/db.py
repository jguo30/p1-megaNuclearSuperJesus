import sqlite3

DB_FILE = "user.db"

db = sqlite3.connect(DB_FILE,check_same_thread=False)
c = db.cursor()

c.execute("CREATE TABLE IF NOT EXISTS usernames(user TEXT UNIQUE, pass TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS favorites(user TEXT UNIQUE, favorites TEXT)")

#check if username in table: (helper function)
def in_table(username):
    user_list = list(c.execute("SELECT user FROM usernames").fetchall())
    print(user_list)
    for i in user_list:
        for j in i:
            if username == j:
                return True
    return False

#adds new username and password to table if not exist
def add_to_db(username,password):
    if (username == "") or (password == ""):
        return False
    if in_table(username): 
        return False
    else:
        c.execute("INSERT INTO usernames VALUES(?,?)",(username,password))
        # c.execute(f'INSERT INTO usernames VALUES("{username}","{password}")')
    db.commit() 
    return True

def pw_confirm(pw,pw_confirm):
    if pw == pw_confirm:
        return True
    else:
        return False

def get_pass(username):
    if in_table(username):
        user_list = list(c.execute("SELECT * FROM usernames").fetchall())
        for i in user_list:
            if i[0] == username:
                return i[1]
    return False

def correct_passwd(username,password):
    return get_pass(username) == password


def has_likes(username):
    user_list = list(c.execute("SELECT user FROM favorites").fetchall())
    print(user_list)
    for i in user_list:
        for j in i:
            if username == j:
                return True
    return False

def add_liked(username,college):
    if(has_likes(username)):
        string = str(list(c.execute("SELECT favorites FROM favorites WHERE user=?",(username,)).fetchall())[0])
        print(string)
        string = string[2:len(string)-3]
        new_string = str(string) + "," + college
        c.execute("UPDATE favorites SET favorites=? WHERE user=?",(new_string,username))
        db.commit()
    else:
        c.execute("INSERT INTO favorites VALUES(?,?)",(username,college,))
        db.commit()
    
    
def likes(username):
    if(has_likes(username)):
        string = list(c.execute("SELECT favorites FROM favorites WHERE user=?",(username,)).fetchall())[0]
        return string
    return False

def check_college(username,college):
    string = str(list(c.execute("SELECT favorites FROM favorites WHERE user=?",(username,)).fetchall())[0])
    colleges = string.split(",")
    for school in colleges:
        for j in school:
            if college == j:
                return True
    return False

def remove_college(username,college):
    string = str(list(c.execute("SELECT favorites FROM favorites WHERE user=?",(username,)).fetchall())[0])
    colleges = string.split(",")
    for school in colleges:
        for j in school:
            if college == j:
                remove(j)


def remove_all(username):
    if(has_likes(username)):
        c.execute("DELETE from favorites WHERE user=?",(username,))
        db.commit()
        return True
    return False

# print(has_likes("marc"))
# add_liked("marc","New York University")
# print(remove_all("marc"))
# print(likes("marc"))
in_table("marc")