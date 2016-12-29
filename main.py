import sqlite3
import hashlib
import sha3
import os,sys
import random
from getpass import *

def generateID(length):
    chars = "0123456789"
    result = ""
    for i in range(length):
        result+=random.choice(chars)
    return result

def generateHash():
    handler = hashlib.sha3_256()
    userInputPass = getpass()
    handler.update(userInputPass.encode())
    result = handler.hexdigest()
    return result

def main():
    global connection
    print("""User input commands:
    a - Add new User to database
    c - Check password for Username
    g - Get Specific User info
    v - View All database records
    """)
    ## Connect to database. If data.db doesn't exist, create db & table
    FILENAME = "data.db"
    if FILENAME not in os.listdir():
        print("Database file not present")
        connection = sqlite3.connect("data.db")
        print("data.db file created")
        createNewTable()  
    else:
        connection = sqlite3.connect("data.db")
        print("Connected to database")
    connection.close()
    ## Ask user for new information
    while True:
        userInput = input("-> ")
        if userInput == "a":
            addNewUser()
        elif userInput == "c":
            compareUserInfo()
        elif userInput == "g":
            getUserInfo()
        elif userInput == "v":
            viewDatabase()
        else:
            pass
        
def createNewTable():
    connection.execute("""
        CREATE TABLE users
        (ID INT PRIMARY KEY NOT NULL,
        USERNAME TEXT       NOT NULL,
        HASH  TEXT          NOT NULL
        );
    """)
    print("New Table created")

def addNewUser():
    IDLENGTH = 8
    ## Connect to Database
    connection = sqlite3.connect("data.db")
    ## Generate & Fetch User ID & Password Hash
    userID = generateID(IDLENGTH)
    username = input("Username: ")
    userHash = generateHash()
    print("Hash:",userHash)
    ## Insert data into database
    #TODO check for same usernames
    insertValues = userID+",'"+username+"','"+userHash+"'"
    connection.execute("INSERT INTO users (ID,USERNAME,HASH) VALUES ("+insertValues+")")
    connection.commit()
    print("New user information added successfully")
    ## Close Connection
    connection.close()

def getUserInfo():
    ## Connect to Database
    connection = sqlite3.connect("data.db")
    ## Request User ID
    userID = input("User ID: ")
    ## Fetch Data from database
    result = connection.execute("SELECT ID,USERNAME,HASH FROM users")
    success = False
    for row in result:
        if str(row[0])==userID:
            success = True
            print("User '"+row[1]+":\nHash:",row[2])
    if not success:
        print("No Records with user ID found")
    connection.close()

def compareUserInfo():
    ## Connect to Database
    connection = sqlite3.connect("data.db")
    ## Request Username
    username = input("Username: ")
    userHash = generateHash()
    ## Fetch Data from database
    result = connection.execute("SELECT ID,USERNAME,HASH FROM users")
    success = False
    for row in result:
        if row[1]==username:
            success = True
            if row[2]==userHash:
                print("Password for user '"+username+"' correct!")
            else:
                print("Wrong password...")
    if not success:
        print("No records with username '"+username+"' found")

    connection.close()

def viewDatabase():
    ## Connect to Database
    connection = sqlite3.connect("data.db")
    ## Fetch data from Database
    result = connection.execute("SELECT ID,USERNAME,HASH FROM users")
    print("User ID\tUsername\tHash")
    for row in result:
        print(str(row[0])+"\t"+row[1]+"\t"+row[2])
    connection.close()

if __name__ == "__main__":
    main()
