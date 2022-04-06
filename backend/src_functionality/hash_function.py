# -*- coding: utf-8 -*-
"""
Author:
    lprtk

Description:
    This script is part of a project called The FastSummarizer, realized as part of 
    an introduction course to Linux and Git / GitHub. The project allows to set up 
    a secure webapp with a functionality allowing to summarize a text file according 
    to a number of sentence. Specifically, this file contains the functions that
    encrypt users' login information.

License:
    MIT License
"""

#--------------------------------- PACKAGES ----------------------------------
from hashlib import sha256

#--------------------------------- FUNCTIONS ---------------------------------
    # Security
def make_hashes(password: str) -> str:
    """
    Function that allows to secure a password with an encryption. SHA for Secure Hash Algorithm.

    Parameters
    ----------
    password : string
        Password to encrypt.

    Returns
    -------
    string
        Encrypted password.

    """
    return sha256(str.encode(password)).hexdigest()

def check_hashes(password: str, hashed_text: str):
    """
    Function that checks if the password given in parameter matches the encrypted 
    password that is stocked. To do this, we use the make_hashes function.

    Parameters
    ----------
    password : string
        Password to verify.
    hashed_text : string
        Encrypted password.

    Returns
    -------
    string or boolean
        Encrypted password if condition is True, else returns False.

    """
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False