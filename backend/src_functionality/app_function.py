# -*- coding: utf-8 -*-
"""
Author:
    lprtk

Description:
    This script is part of a project called The FastSummarizer, realized as part of 
    an introduction course to Linux and Git / GitHub. The project allows to set up 
    a secure webapp with a functionality allowing to summarize a text file according 
    to a number of sentence. Specifically, this file contains the heart of the
    webapp e.g. its main functions.

License:
    MIT License
"""

#--------------------------------- PACKAGES ----------------------------------
import hash_function

from networkx import from_numpy_array, pagerank

import nltk
from nltk.cluster.util import cosine_distance
from nltk.corpus import stopwords

import numpy as np

import password_generator

import sgbd

import streamlit as st

#--------------------------------- FUNCTIONS ---------------------------------
    # App functionnalities
def log_out() -> None:
    """
    Method that allows to change the state of an element of a Streamlit class.
    For logout functionality.

    Returns
    -------
    None.

    """
    st.session_state.LoggedIn = False
    st.session_state.LoggedOut = False
    
def log_error() -> None:
    """
    Method that allows to change the state of an element of a Streamlit class.
    For login failure functionality.
    
    Returns
    -------
    None.

    """
    st.session_state.LoggedIn = False
    st.session_state.LoggedTry = False
    
def log_reset() -> None:
    """
    Method that allows to change the state of an element of a Streamlit class.
    For reset password functionality.

    Returns
    -------
    None.

    """
    st.session_state.ResetedCheck = False
    st.session_state.ResetPswd = False
    st.session_state.LoggedIn = False

def log_reset_error() -> None:
    """
    Method that allows to change the state of an element of a Streamlit class.
    For password reset failure functionality.

    Returns
    -------
    None.

    """
    st.session_state.ResetedRetry = False
    st.session_state.ResetedCheck = False

def log_delete() -> None:
    """
    Method that allows to change the state of an element of a Streamlit class.
    For delete account functionality.

    Returns
    -------
    None.

    """
    st.session_state.DeletedCheck = False
    st.session_state.DeletedAccount = False
    st.session_state.LoggedIn = False
    
def log_delete_error() -> None:
    """
    Method that allows to change the state of an element of a Streamlit class.
    For delete account failure functionality.

    Returns
    -------
    None.

    """
    st.session_state.DeletedRetry = False
    st.session_state.DeletedCheck = False

def log_forgot() -> None:
    """
    Method that allows to change the state of an element of a Streamlit class.
    For forgotten password functionality.

    Returns
    -------
    None.

    """
    st.session_state.ValidatedCheck = False
    st.session_state.ForgottenCheck = False
    
def log_forgot_error() -> None:
    """
    Method that allows to change the state of an element of a Streamlit class.
    For forgotten password failure functionality.

    Returns
    -------
    None.

    """
    st.session_state.ForgottenTry = False
    st.session_state.ValidatedCheck = False

def forgot_password() -> None:
    """
    Method that allows a user to reset his password from his login and the 
    answer to a security question given when he created his account. A new 
    random password is given to him and is updated in the database.

    Returns
    -------
    None.

    """
    # User ID
    user = st.empty()
    username = user.text_input("User Name", key=30)
    
    # User informations
    question = st.selectbox("Question",["What is your favorite color?",
                                        "What was the name of your school?",
                                        "In which city did you grow up?"])
    answr = st.empty()
    answer = answr.text_input("Answer", key=31)
    
    # Callback
    validated_check = st.checkbox(label="Validate", 
                                  key="ValidatedCheck"
                                  )
    
    if validated_check:
        # ID verification
        sgbd.create_usertable()
        result = sgbd.forgot_pswd(username, question, answer)
        
        if result:
            # New password generator
            new_password = password_generator.generate_random_password()
            
            col1, col2 = st.columns(2)
            
            col1.markdown("New password:")
            code = f"{new_password}"
            col2.code(code, language="python")
            
            # Reset password in database
            sgbd.reset_pswd(username, hash_function.make_hashes(new_password))
            
            # Task validated
            st.success("✔️ Your password has been reseted.")
            
            # Redirection button
            st.button("👉 Go to LogIn menu", on_click=log_forgot)
            
        else:
            # Reset text area
            username = user.text_input("User Name", value="", key=32)
            answer = answr.text_input("Answer", value="", key=33)
            
            # Information message
            st.error("❌ Incorrect Username/Question/Answer. Please retry.")
            
            with st.sidebar:
                col1, col2, col3 = st.columns(3)
                
                # Callback
                forgotten_retry = col3.checkbox(label="Retry", 
                                                 key="ForgottenTry", 
                                                 on_change=log_forgot_error)
                
def reset_password() -> None:
    """
    Method that allows a user to change their password and update the new 
    password in the database.

    Returns
    -------
    None.

    """
    # User ID
    user = st.empty()
    username = user.text_input("User Name", key=5)
    
    # User passeword
    old_pswd = st.empty()
    old_password = old_pswd.text_input("Old password", type="password", key=6)
    new_pswd = st.empty()
    new_password = new_pswd.text_input("New password", type="password", key=7)
    
    # Callback
    reseted_check = st.checkbox(label="Reset", 
                                key="ResetedCheck",
                                #on_change=log_reset
                                )
    
    if reseted_check:
        # ID verification
        sgbd.create_usertable()
        hashed_pswd = hash_function.make_hashes(old_password)
        result = sgbd.login_user(username, hash_function.check_hashes(old_password, hashed_pswd))
        
        if result:
            st.success("✔️ Logged In, password being re-initialized.")
            sgbd.reset_pswd(username, hash_function.make_hashes(new_password))
            
            # Reset text area
            username = user.text_input("User Name", value="", key=8)
            old_password = old_pswd.text_input("Old password", value="", key=9)
            new_password = new_pswd.text_input("New password", type="password", key=10)
            
            # Task validated
            st.success("✔️ Your passeword has been re-initialized.")
            
            # Information message
            st.info("Please LogIn with your new password. 🔐")
            
            # Redirection button
            st.button("👉 Go to LogIn menu", on_click=log_reset)
            
        else:
            # Reset text area
            username = user.text_input("User Name", value="", key=11)
            old_password = old_pswd.text_input("Old password", value="", key=12)
            new_password = new_pswd.text_input("New password", type="password", key=13)
            
            # Task failed
            st.error("❌ Incorrect Username/Password. Please retry.")
            
            # Callback
            reseted_retry = st.checkbox(label="Retry", 
                                        key="ResetedRetry", 
                                        on_change=log_reset_error)


def delete_account() -> None:
    """
    Method that allows a user to delete his account from the database.

    Returns
    -------
    None.

    """
    # User ID
    user = st.empty()
    username = user.text_input("User Name", key=14)
    
    # User passeword
    pswd = st.empty()
    password = pswd.text_input("Password", type="password", key=15)
    
    # Callback
    deleted_check = st.checkbox(label="Delete", 
                                key="DeletedCheck",
                                #on_change=log_delete
                                )

    if deleted_check:
        # ID verification
        sgbd.create_usertable()
        hashed_pswd = hash_function.make_hashes(password)
        result = sgbd.login_user(username, hash_function.check_hashes(password, hashed_pswd))
        
        if result:
            st.success("✔️ Logged In, account being deleted.")
            sgbd.delete_user(username, hash_function.make_hashes(password))
            
            # Reset text area
            username = user.text_input("User Name", value="", key=16)
            password = pswd.text_input("Password", value="", key=17)
            
            # Task validated
            st.success("✔️ Your account has been deleted.")
            
            # Information message
            st.info("Your account has been deleted. Se you next time! 👋")
            
        else:
            # Reset text area
            username = user.text_input("User Name", value="", key=18)
            password = pswd.text_input("Password", value="", key=19)
            
            # Task failed
            st.error("❌ Incorrect Username/Password. Please retry.")
            
            # Callback
            reseted_retry = st.checkbox(label="Retry", 
                                        key="DeletedRetry", 
                                        on_change=log_delete_error)


    # App functions
def read_article(file_name: str) -> list:
    """
    Function that reads a text file and returns a list of clean sentences.
    
    Parameters
    ----------
    file_name : string
        The name of the input text file (with his extension).

    Returns
    -------
    sentences : list
        List of clean sentences.

    """
    file = open(file_name, "r")
    filedata = file.readlines()
    article = filedata[0].split(". ")
    sentences = []

    for sentence in article:
        #print(sentence)
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    sentences.pop() 
    
    file.close()
    
    return sentences


def sentence_similarity(sent1: str, sent2: str, stopwords=None) ->float:
    """
    A function that calculates the similarity between sentences in a text with 
    cosine similarity. It returns a similarity measure.

    Parameters
    ----------
    sent1 : string
        First sentence with which we will calculate the similarity.
    sent2 : string
        Second sentence with which we will calculate the similarity.
    stopwords : list, optional
        The default is None.

    Returns
    -------
    float
        The similarity measure with cosine similarity.

    """
    if stopwords is None:
        stopwords = []
 
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]
 
    all_words = list(set(sent1 + sent2))
 
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
 
    # build the vector for the first sentence
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1
 
    # build the vector for the second sentence
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1
 
    return 1 - cosine_distance(vector1, vector2)
 
def build_similarity_matrix(sentences: list, stop_words: list):
    """
    Function to retrieve the similarity measures between two sentences and put 
    them in a matrix.

    Parameters
    ----------
    sentences : list
        List of clean sentences.
    stop_words : list
        List of stopwords.

    Returns
    -------
    similarity_matrix : np.array
        Similarity matrix.

    """
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
 
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2: #ignore if both are same sentences
                continue 
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

    return similarity_matrix


def generate_summary(file_name, top_n: int) -> str:
    """
    This method will call all the other functions to keep our summarization 
    pipeline running. It takes 4 steps: 
        1) Read the text file and cut out all the sentences read_article();
        2) Compute the cosine similarity measure between sentences with the 
           sentence_similarity() function;
        3) Generate a similarity matrix between sentences with the 
           build_similarity_matrix() function;
        4) Sort the sentences by order of importance and display the text 
           summary with the generate_summary() function.

    Parameters
    ----------
    file_name : file
        Input text file.
    top_n : int
        Number of sentences to display in the summary.

    Returns
    -------
    summarized_text : string
        Summarized text.

    """
    nltk.download("stopwords")
    stop_words = stopwords.words("english")
    summarize_text = []

    # Step 1 - Read text anc split it
    sentences =  read_article(file_name)

    # Step 2 - Generate Similary Martix across sentences
    sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)

    # Step 3 - Rank sentences in similarity martix
    sentence_similarity_graph = from_numpy_array(sentence_similarity_martix)
    scores = pagerank(sentence_similarity_graph)

    # Step 4 - Sort the rank and pick top sentences
    ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)    
    #print("Indexes of top ranked_sentence order are ", ranked_sentence)    

    for i in range(top_n):
      summarize_text.append(" ".join(ranked_sentence[i][1]))
    
    # Add a . at the end of the summary
    summarize_text.append(" ")
    
    # Step 5 - Offcourse, output the summarize text
    #print("Summarize Text: \n", ". ".join(summarize_text))
    summarized_text = ". ".join(summarize_text)
    
    return summarized_text