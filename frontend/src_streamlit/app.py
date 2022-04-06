# -*- coding: utf-8 -*-
"""
Author:
    lprtk

Description:
    This script is part of a project called The FastSummarizer, realized as part of 
    an introduction course to Linux and Git / GitHub. The project allows to set up 
    a secure webapp with a functionality allowing to summarize a text file according 
    to a number of sentence. Specifically, this file contains the layout of the webapp.

License:
    MIT License
"""

#--------------------------------- PACKAGES ----------------------------------
import app_function

import hash_function

from PIL import Image

import sgbd

import streamlit as st

from sqlite3 import connect

#--------------------------------- FUNCTIONS ---------------------------------
    # App
def main() -> None:
    """
    This method allows to launch the webapp by calling modules defined with the 
    functionalities necessary for the functioning of the application.

    Returns
    -------
    None.

    """
    #---------------------------------- SQLITE 3 -----------------------------
        # Connection to MogoDB database
    conn = connect("data.db", check_same_thread=False)
    c = conn.cursor()
    
    #------------------------------- PAGE SETTINGS ---------------------------
    image = Image.open("logoAI.png")
    
    st.set_page_config(
         page_title="The FastSummarizer - AI",
         page_icon=image,
         layout="wide",
         initial_sidebar_state="expanded",
         menu_items={
             "Get help": "https://github.com/lprtk/text-summarizer",
             "Report a bug": "https://github.com/lprtk/text-summarizer/issues",
             "About": "Hi, welcome on my App! If you have a bug or anythings that which prevents you from use the functionalities of the App, please report it to my GitHub page."
         }
    )
    
    #------------------------------- DESIGN / CODE ---------------------------
    col1, col2 = st.columns(2)
    col1.image(image, width=230)
    col2.subheader(
        "Group CDO MoSEF \n"
        "Strategic Needs Artificial Intelligence"
        )
    
    st.markdown(
        """
        <h1 style='text-align: center'>
            <font color='#FFFFFF'>
                The FastSummarizer
            </font>
        </h1>
        """, True
        )
    
    st.markdown(
        """
        <h2 style='font-family: Arial'>
            <font color='#FFFFFF'>
                🤖💬 Hi!
            </font>
        </h2>
        """, True
        )
    
    st.markdown(
        """
        <h4 style='text-align: justify'>
            <font color= '#FFFFFF'>
                Don't you want to read? Don't worry, I'm like you! Welcome to this application 
                that will allow you to stop reading. Enter a text and I will give you a summary 
                of it.
            </font>
        </h4>
        """, True
        )
    
    st.markdown("<br/>", True)
    
    st.markdown(
        """
        <h4 style='text-align: center'>
            <font color='#FFFFFF'>
                Like you, many people don't want to read anymore! *
            </font>
        </h4>
        """, True
        )
    
    col1, col2, col3, col4 = st.columns(4)
    col2.metric("Last week's attendance", "82%", "26.8%")
    col3.metric("Number of texts summarized", "727", "14%")
    col4.metric("Customer satisfaction", "92%", "5%")
    st.markdown(
        """
        <p>
            <font color='#FFFFFF'>
                *compared to last week's activity
            </font>
        </p>
        """, True
        )
    
    st.markdown("<br/>", True)
    
    #-------------------------------- APP CONTENT ----------------------------
    menu = ["Home", "LogIn", "SignUp"]
    
    st.sidebar.markdown(
        """
        <h4>
            <font color='#FFFFFF'>
                Connexion 🔒
            </font>
        </h4>
        """, True
        )
    
    choice = st.sidebar.selectbox("Menu", menu)
    
    col1, col2, col3 = st.columns(3)
    
    if choice == "Home":
        st.markdown(
            """
            <h2 style='font-family: Arial'>
                <font color='#FFFFFF'>
                    Home
                </font>
            </h2>
            """, True
            )
    
        st.markdown(
            """
            <h4>
                <font color='#FFFFFF'>
                    About the App 🔎
                </font>
            </h4>
            """, True
            )
        
        with st.expander("About"):
            st.markdown(
                """
                <p>
                    <font color='#FFFFFF'>
                        Do you want to quickly summarize a text? Use The FastSummarizer 
                        to help you on a daily basis. Log in, import your file, select 
                        the length of your summary and download it!
                    </font>
                </p>
                """, True
                )
                
        with st.sidebar:
            st.info(
                """
                ☝ Please use the menu above to authenticate yourself before using the App.
                """
                )
    
    elif choice == "LogIn":
        st.markdown(
            """
            <h2 style='font-family: Arial'>
                <font color='#FFFFFF'>
                    LogIn Section 🔐
                </font>
            </h2>
            """, True
            )
        
        with st.sidebar:
            # User ID
            user = st.empty()
            username = user.text_input("User Name", key=1)
            
            # User passeword
            pswd = st.sidebar.empty()
            password = pswd.text_input("Password", type="password", key=2)
            
            # Callback
            col1, col2, col3 = st.columns(3)
            
            loggedin_check = col1.checkbox(label="LogIn", 
                                           key="LoggedIn")
            
            if not loggedin_check:
                forgotten_check = col3.checkbox(label="Forgot password", 
                                                key="ForgottenCheck")
                
                if forgotten_check:
                    st.markdown("<br/>", True)
                    
                    st.markdown(
                        """
                        <h3 style='font-family: Arial'>
                            <font color='#FFFFFF'>
                                Forgot your password 🔏
                            </font>
                        </h3>
                        """, True
                        )
                    
                    # Call function
                    app_function.forgot_password()
        
        if loggedin_check:
            # ID verification
            sgbd.create_usertable()
            hashed_pswd = hash_function.make_hashes(password)
            result = sgbd.login_user(username, hash_function.check_hashes(password, hashed_pswd))
            
            if result:
                st.success(f"✔️ Hi {username}, you have successfully Logged In!")
                
                # Reset text area
                username = user.text_input("User Name", value="", key=3)
                password = pswd.text_input("Password", value="", key=4)
                
                #-------------------------------------------------------------
                # App content
                
                st.markdown("<br/>", True)
                
                st.markdown(
                    """------------------------------------------------------------""", True
                    )
                
                
                st.markdown(
                    """
                    <h2 style='font-family: Arial'>
                        <font color='#FFFFFF'>
                            How to use the application's functionalities:
                        </font>
                    </h2>
                    <ol>
                        <li>Upload your data: you must load a text file to be summarized in the drag and drop area.</li>
                        <li>Select the length of the summary that the FastSummarizer should make.
                        <li>Download your data: you just have to click on the button to download the summary of your text.</li>
                    </ol>
                    """, True
                    )
                
                st.markdown("<br/>", True)
                
                st.markdown(
                    """
                    <h3 style='font-family: Arial'>
                        <font color='#FFFFFF'>
                            1. Import a text file
                        </font>
                    </h3>
                    """, True
                    )
                
                st.markdown(
                    """
                    <p>
                        Choose a text file that you want to summarize 📥.
                    </p>
                    """, True
                    )
                
                upload_file = st.file_uploader("", type=["txt"])
                if upload_file:                
                    st.write("● Filename: ", upload_file.name)
                    st.write("● Filtype: ", upload_file.type)
                    st.write("● Filsize: ", upload_file.size)
                    data = upload_file.name
                    
                    file = open(data, "r")
                    filedata = file.readlines()
                    article = filedata[0].split(". ")
                    sentences = []

                    for sentence in article:
                        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
                    sentences.pop() 
                    
                    file.close()
                    
                    length_file = len(sentences)
                    
                    st.write("● Number of sentences:", length_file)
                    
                    st.markdown("<br/>", True)
                    st.markdown("<br/>", True)
                    
                    number_list = []
                    for i in range(0, length_file+1, 1):
                        number_list += [str(i)]

                    length = number_list
                    
                    st.markdown(
                        """
                        <h3 style='font-family: Arial'>
                            <font color='#FFFFFF'>
                                2. Select a length for the summary
                            </font>
                        </h3>
                        """, True
                        )
                    
                    st.markdown(
                        """
                        <p>
                            Select the number of sentences 🛑.
                        </p>
                        """, True
                        )
                    
                    length_choice = st.selectbox("", length)
                    
                    length_choice = int(length_choice)
                    
                    if length_choice > 0:
                        resumed_text = app_function.generate_summary(data, length_choice)
                        
                        st.markdown("<br/>", True)
                        st.markdown("<br/>", True)
                        
                        st.success("✔️ Done! You can download the file.")
                        
                        filename = upload_file.name.split(".")
                        
                        st.markdown("<br/>", True)
                        
                        st.markdown(
                            """
                            <h3 style='font-family: Arial'>
                                <font color='#FFFFFF'>
                                    3. Download your text file
                                </font>
                            </h3>
                            """, True
                            )
                        
                        st.markdown(
                            """
                            <p>
                                Download the summary text 📤.
                            </p>
                            """, True
                            )
                        
                        st.markdown("<br/>", True)
                        
                        st.download_button(
                            label="Download file 📄",
                            data=resumed_text,
                            file_name=f"{filename[0]}_summarized.txt",
                            mime="text/plain"
                            )
                    
                #-------------------------------------------------------------
                
                # LogOut configuration
                loggedout_check = col3.checkbox(label="LogOut", 
                                                key="LoggedOut",
                                                on_change=app_function.log_out)
                
                with st.sidebar:
                    st.sidebar.markdown("<br/>", True) 
                    col1, col2 = st.columns(2)
                
                    # Reset password configuration
                    resetpswd_check = col1.checkbox(label="Reset password", 
                                                    key="ResetPswd")
                
                with st.sidebar:
                    col1, col2 = st.columns(2)
                
                    # Delete account configuration
                    deleteaccount_check = col1.checkbox(label="Delete account", 
                                                        key="DeletedAccount")
                
                # LogOut process
                if loggedout_check:
                    st.warning("Disconnect, see you soon! 👋")
                    
                # Reset password process
                if resetpswd_check:
                    with st.sidebar:
                        st.markdown("<br/>", True)
                        
                        st.markdown(
                            """
                            <h3 style='font-family: Arial'>
                                <font color='#FFFFFF'>
                                    Reset your password 🔏
                                </font>
                            </h3>
                            """, True
                            )
                    
                        # Call function
                        app_function.reset_password()
                    
                # Delete account process
                if deleteaccount_check:
                    with st.sidebar:
                        st.markdown("<br/>", True)
                        
                        st.markdown(
                            """
                            <h3 style='font-family: Arial'>
                                <font color='#FFFFFF'>
                                    Delete your account 🔒
                                </font>
                            </h3>
                            """, True
                            )
    
                        # Call function
                        app_function.delete_account()
                    
            else:
                # Reset text area
                username = user.text_input("User Name", value="", key=20)
                password = pswd.text_input("Password", value="", key=21)
                
                # Information message
                st.error("❌ Incorrect Username/Password. Please retry.")
                
                with st.sidebar:
                    col1, col2, col3 = st.columns(3)
                    
                    # Callback
                    loggedin_retry = col3.checkbox(label="Retry", 
                                                   key="LoggedTry", 
                                                   on_change=app_function.log_error)
        else:
            st.info(
                """
                👈 Please use the menu in the left side to authenticate yourself before using the App.
                """
                )
    
    elif choice == "SignUp":
        st.markdown(
            """
            <h2 style='font-family: Arial'>
                <font color='#FFFFFF'>
                    Create New Account 👀
                </font>
            </h2>
            """, True
            )
    
        st.info(
            """
            Welcome on our App! 👋 You are not already register, create your account to use our analytics tools.
            """
            )
                
        new_user = st.text_input("User Name")
        question = st.selectbox("Question",["What is your favorite color?",
                                            "What was the name of your school?",
                                            "In which city did you grow up?"])
        answer = st.text_input("Answer")
        new_password = st.text_input("Password", type="password")
        
        st.sidebar.markdown(
            """
            <h4>
                <font color='#FFFFFF'>
                    About the App 🔎
                </font>
            </h4>
            """, True
            )
        
        with st.sidebar.expander("About"):
            st.markdown(
                """
                <p>
                    <font color='#FFFFFF'>
                        Do you want to quickly summarize a text? Use The 
                        FastSummarizer to help you on a daily basis. Log in, 
                        import your file, select the length of your summary 
                        and download it!
                    </font>
                </p>
                """, True
                )
        
        if st.button("SignUp"):
            sgbd.create_usertable()
            sgbd.add_userdata(new_user, hash_function.make_hashes(new_password), question, answer)
            st.success("✔️ You have successfully created a valid account!")
            st.info("Go to LogIn Menu to login. 🔐")
    
    #---------------------------------- SQLITE 3 -----------------------------
        # Close the database
    conn.commit()
    c.close()


if __name__ == '__main__':
	main()