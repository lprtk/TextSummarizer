# -*- coding: utf-8 -*-
"""
Author:
    lprtk

Description:
    This script is part of a project called The FastSummarizer, realized as part of 
    an introduction course to Linux and Git / GitHub. The project allows to set up 
    a secure webapp with a functionality allowing to summarize a text file according 
    to a number of sentence. Specifically, this file contains that allow to manage
    the database in backend.

License:
    MIT License
"""

#--------------------------------- PACKAGES ----------------------------------
from sqlite3 import connect

#--------------------------------- FUNCTIONS ---------------------------------
    # Connection to MogoDB database
conn = connect("data.db", check_same_thread=False)
c = conn.cursor()


    # Data base management
def create_usertable() -> None:
    """
    Method that checks if the table exists, and creates it if not.

    Returns
    -------
    None.

    """
    c.execute("CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT, question TEXT, answer TEXT)")

def add_userdata(username: str, password: str, question: str, answer: str) -> None:
    """
    Method that allows to add a user by a couple (username, password) that 
    will be stored in the table.

    Parameters
    ----------
    username : string
        User's username.
    password : string
        User's password.
    question : string
        Security question chosen by the user.
    answer : string
        User's answer to the security question.

    Returns
    -------
    None.

    """
    c.execute("INSERT INTO userstable(username, password, question, answer) VALUES (?, ?, ?, ?)", (username, password, question, answer))
    conn.commit()

def login_user(username: str, password: str):
    """
    Function that checks if the username and password are in the database and 
    allows identification.

    Parameters
    ----------
    username : string
        User's username.
    password : string
        User's password.

    Returns
    -------
    data : tuple
        Result of the query as a tuple, the tuples are empty if there is no 
        match in the table.

    """
    c.execute("SELECT * FROM userstable WHERE username =? AND password =?", (username, password))
    data = c.fetchall()
    return data

def view_all_users():
    """
    Function to query the database and retrieve the list of usernames and 
    encrypted passwords

    Returns
    -------
    data : list of tuples
        Result of the query as a tuple, (username, password).

    """
    c.execute("SELECT * FROM userstable")
    data = c.fetchall()
    return data

def reset_pswd(username: str, password: str) -> None:
    """
    Method to change / update a password in the database.

    Parameters
    ----------
    username : string
        User's username.
    password : string
        User's password.

    Returns
    -------
    None.

    """
    c.execute("UPDATE userstable SET password =? WHERE username =?", (password, username))
    conn.commit()

def forgot_pswd(username: str, question: str, answer: str) -> None:
    """
    Method to change / update a password in the database.

    Parameters
    ----------
    username : string
        User's username.
    question : string
        Security question chosen by the user.
    answer : string
        User's answer to the security question.

    Returns
    -------
    None.

    """
    c.execute("SELECT * FROM userstable WHERE username =? AND question =? AND answer =?", (username, question, answer))
    data = c.fetchall()
    return data

def delete_user(username: str, password: str) -> None:
    """
    Function that allows you to delete a user from the database.

    Parameters
    ----------
    username : string
        User's username.
    password : string
        User's password.

    Returns
    -------
    None.

    """
    c.execute("DELETE FROM userstable WHERE username =? AND password =?", (username, password))
    conn.commit()