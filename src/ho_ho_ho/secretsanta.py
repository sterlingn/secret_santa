#!/usr/bin/python3

from __future__ import annotations
import glob
import json
import os
import pathlib
import random
import smtplib
import ssl
from typing import List
from email.message import EmailMessage
# Python script
from dotenv import load_dotenv
from pathlib import Path
import os

# optional: explicit path to .env
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)  # returns True if loaded


TESTING = os.getenv("TESTING", "False").lower() in ("true", "1", "t")
# Add entries here with the format "<name>": "<email>",
ss_dict_env = "SS_DICT_TESTING" if TESTING else "SS_DICT"
ss_dict_value = os.getenv(ss_dict_env)
if not ss_dict_value:
    raise ValueError(f"{ss_dict_env} is missing from environment variables or .env file!")

try:
    SS_DICT = json.loads(ss_dict_value)
except json.JSONDecodeError as exc:
    raise ValueError(f"{ss_dict_env} must contain a valid JSON object.") from exc

if not isinstance(SS_DICT, dict) or not all(
    isinstance(name, str) and isinstance(email, str)
    for name, email in SS_DICT.items()
):
    raise ValueError(f"{ss_dict_env} must be a JSON object of names to email addresses.")

# Constants: This is the file path to save the text files to 
CURR_PATH = str(pathlib.Path(__file__).parent.resolve()) # TODO: doesn't seem to use the files directory
FILE_FMT = "For_{}.txt"
# This is the email address and password to send the emails from
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
if not EMAIL_SENDER or not EMAIL_PASSWORD:
    raise ValueError("CRITICAL: EMAIL_SENDER or EMAIL_PASSWORD is missing from environment variables or .env file!")

# Class for each secret santa and their person
class SecretSanta:
    # Constants this is the format for the text files
    PRINT_FMT = "SecretSanta: {}, Person: {}"
    SAVE_FMT = "🎅 🎄 🎁 ✨ This is for {}!\nYou have been given {}!\nDon't tell anyone! Ho, Ho, Ho and Stuff! 🎅 🎄 🎁 ✨"
    #This is where we define who the email sender is 
    def __init__(self, me: str, email: str = ""):
        """Initializer

        Args:
            me (str): Who is this secret santa
            email (str): Optional email address
        """
        self._me = me
        self._email = email
        self._person = None

    def __repr__(self) -> str:
        return self.PRINT_FMT.format(self._me, self._person)

    def hasEmail(self) -> bool:
        return True if self._email else False

    def getMe(self) -> str:
        return self._me

    def getEmail(self) -> str:
        return self._email

    def getPerson(self) -> str | None:
        return self._person

    def setPerson(self, person: str):
        """Set this Secret Santa's person manually (only do this in bad state)

        Args:
            person (str): The person to set us to
        """
        self._person = person

    def selectPerson(self, selectionPool: list) -> str | None:
        """Select a person for this secret santa

        Args:
            selectionPool (list): The list of candidates to choose from
        Returns:
            str | None: The person that was selected or None on invalid selection
        """

        pool = selectionPool.copy()
        if self._me in pool:
            # Take ourselves out first
            pool.remove(self._me)

        if not pool:
            # Empty, invalid selection
            return None

        # Randomly select a person
        self._person = random.choice(pool)

        # Return who we got
        return self._person

    def swapPerson(self, ss: SecretSanta):
        """Swap the given Secret Santa with this Secret Santa.
        This is only used in the case of a loop in the selection process.

        Args:
            ss (SecretSanta): The Secret Santa to take on
        """

        # Assign us to the given SS
        oldPerson = self._person
        self._person = ss._me
        if not oldPerson:
            print("Valid SS found to be invalid. Exitting.")
            exit()

        # Assign the given SS our now old person to fix loop
        ss.setPerson(oldPerson)

    def validate(self) -> bool:
        """Validate that this Secret Santa is valid

        Returns:
            bool: True for valid False for invalid
        """

        if not self._me or not self._person:
            return False
        elif self._me == self._person:
            return False

        return True

    def toStr(self) -> str:
        """Return the results as a string
        """
        return self.SAVE_FMT.format(self._me, self._person)

    def getFileName(self) -> str:
        """Get the filename associated with this secret santa

        Returns:
            str: The filename
        """
        return FILE_FMT.format(self._me)

    def save(self):
        """Save our Secret Santa to a text file"""
        with open(FILE_FMT.format(self._me), "w") as f:
            f.write(self.getFileName())
    
    def sendEmail(self):
        """Send an email to the holder telling them their selection
        """
        em = EmailMessage()
        em["From"] = EMAIL_SENDER
        em["To"] = self._email
        em["Subject"] = "Secret Santa"
        em.set_content(self.toStr())
        image_path = Path(__file__).resolve().parent /  "christmas_office_meme.jpg"
        em.add_attachment(
            image_path.read_bytes(),
            maintype="image",
            subtype="jpeg",
            filename=image_path.name,
        )

        context = ssl.create_default_context()
        # Change connection method and port:
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
                smtp.starttls(context=context) # Start TLS encryption
                smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
                smtp.sendmail(EMAIL_SENDER, self._email, em.as_string())
                print("Email sent successfully using port 587 (TLS)!")
        except smtplib.SMTPAuthenticationError:
            print("Authentication failed. Double-check your 16-character App Password.")

def cleanup():
    """Remove old files that match the constant FILE_FMT"""
    for name in glob.glob(os.path.join(CURR_PATH, FILE_FMT.format("*"))):
        os.remove(name)


if __name__ == "__main__":
    # Remove old files
    cleanup()

    # Create the Secret Santas from the configured dictionary
    SSList: List[SecretSanta] = []
    for name, email in SS_DICT.items():
        SSList.append(SecretSanta(name, email))

    peopleLst = list(SS_DICT.keys())
    # Do the selection drawings
    for SS in SSList:
        selected = SS.selectPerson(peopleLst)
        if not selected:
            # Bad draw state, swap with person before
            index = SSList.index(SS)
            if index <= 1:
                # Should never happen
                print("Invalid state for Secret Santa, stopping.")
                exit()

            # Get the previous person and do a swap
            prevSS = SSList[index - 1]
            prevSS.swapPerson(SS)
        else:
            # Valid selection, remove it from list
            peopleLst.remove(selected)

    # Done, validate selections
    for SS in SSList:
        if not SS.validate():
            print("Invalid SS found: {}".format(SS))
            exit()

    # Either send selections via email or save to text files to be emailed (No Peeking!!!)
    for SS in SSList:
        # Check if they have email
        if SS.hasEmail():
            print("Sending email to {} via {}".format(SS.getMe(), SS.getEmail()))
            SS.sendEmail()
        else:
            # No email, save to text file instead
            print("Saving file for {} to {}".format(SS.getMe(), SS.getFileName()))
            SS.save()
