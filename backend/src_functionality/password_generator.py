# -*- coding: utf-8 -*-
"""
Author:
    lprtk

Description:
    This script is part of a project called The FastSummarizer, realized as part of 
    an introduction course to Linux and Git / GitHub. The project allows to set up 
    a secure webapp with a functionality allowing to summarize a text file according 
    to a number of sentence. Specifically, this file contains that allow to generate
    a new random password.

License:
    MIT License
"""

#--------------------------------- PACKAGES ----------------------------------
from random import choice, shuffle

from string import ascii_letters, digits, punctuation

#--------------------------------- FUNCTIONS ---------------------------------
    # Password generator
def generate_random_password(pswd_length: int=10) -> str:
    """
    Function to generate a random password with letters, numbers and special characters.

    Parameters
    ----------
    pswd_length : int, optional
        The password's length, in terms of characters. The default is 10.

    Returns
    -------
    string
        Randomly generated password.

    """
    # Import special characters
    characters = list(ascii_letters + digits + punctuation)

	# Shuffling the characters
    shuffle(characters)
	
	# Picking random characters from the list
    password = []
    for i in range(pswd_length):
        password.append(choice(characters))
    
    # Shuffling the resultant password
    shuffle(password)

	# Converting the list to string
    return "".join(password)