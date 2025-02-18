#!/usr/bin/python3

from __future__ import annotations
import glob
import os
import pathlib
import random
from typing import List
import datetime

# Add entries here with the format NAME_<Name>

NAME_NATE = "Nate Sterling AKA Nate Dog"
NAME_ALEX = "Alex Sterling AKA Gatita Jefita"
NAME_ALFONSO = "Alfonso Hernandez AKA FoFo"
NAME_ANGELA = "Angela Hernandez AKA Mimi"
NAME_DIEGO = "Diego AKA Santiago Diablo"
NAME_JUAN = "Juanito Bonito"
NAME_TONI = "Toni"
NAME_LUIISA = "Luiisa"
NAME_CARMENMARIA = "Carmen Maria"
NAME_ANNA = "Anna AKA Anita (daughter of Juan and Toni)"
NAME_MARIA = "Maria Lee"
NAME_CHRIS = "Chris Lee AKA Chrisy Poo AKA Tio Chris"

# Constants: This is the file path to save the text file to

CURR_PATH = str(pathlib.Path(__file__).parent.resolve())
current_date = datetime.datetime.now()
print("Current path: " + str(current_date)+ CURR_PATH) #this is showing the current filepath
print('hello world' + str(current_date))# this shows that we are able to run the script

FILE_FMT = "For_{}.txt"
print("File format: " + FILE_FMT)

# # Class for each secret santa and their person
# class SecretSanta:
#     # Constants 
#     PRINT_FMT = "SecretSanta: {}, Person: {}"
#     SAVE_FMT = "This is for {}!\nYou have been given {}!\nDon't tell anyone!"
#     #This is where we define who the email sender is
#     def __init__(self, me: str):
#         """Initializer

#         Args:
#             me (str): Who is this secret santa
#         """
#         self._me = me
#         self._person = None

#     def __repr__(self) -> str:
#         return self.PRINT_FMT.format(self._me, self._person)

#     def getMe(self) -> str:
#         return self._me

#     def getPerson(self) -> str | None:
#         return self._person

#     def setPerson(self, person: str):
#         """Set this Secret Santa's person manually (only do this in bad state)

#         Args:
#             person (str): The person to set us to
#         """
#         self._person = person

#     def selectPerson(self, selectionPool: list) -> str | None:
#         """Select a person for this secret santa

#         Args:
#             selectionPool (list): The list of candidates to choose from
#         Returns:
#             str | None: The person that was selected or None on invalid selection
#         """

#         pool = selectionPool.copy()
#         if self._me in pool:
#             # Take ourselves out first
#             pool.remove(self._me)

#         if not pool:
#             # Empty, invalid selection
#             return None

#         # Randomly select a person
#         self._person = random.choice(pool)

#         # Return who we got
#         return self._person

#     def swapPerson(self, ss: SecretSanta):
#         """Swap the given Secret Santa with this Secret Santa.
#         This is only used in the case of a loop in the selection process.

#         Args:
#             ss (SecretSanta): The Secret Santa to take on
#         """

#         # Assign us to the given SS
#         oldPerson = self._person
#         self._person = ss._me
#         if not oldPerson:
#             print("Valid SS found to be invalid. Exitting.")
#             exit()

#         # Assign the given SS our now old person to fix loop
#         ss.setPerson(oldPerson)

#     def validate(self) -> bool:
#         """Validate that this Secret Santa is valid

#         Returns:
#             bool: True for valid False for invalid
#         """

#         if not self._me or not self._person:
#             return False
#         elif self._me == self._person:
#             return False

#         return True

#     def save(self):
#         """Save our Secret Santa to a text file"""
#         with open(FILE_FMT.format(self._me), "w") as f:
#             f.write(self.SAVE_FMT.format(self._me, self._person))


# def cleanup():
#     """Remove old files that match the constant FILE_FMT"""
#     for name in glob.glob(os.path.join(CURR_PATH, FILE_FMT.format("*"))):
#         os.remove(name)


# if __name__ == "__main__":
#     # Remove old files
#     cleanup()

#     # Create list with all names from constants
#     varsDict = locals().copy()
#     peopleLst = []
#     for name, val in varsDict.items():
#         if name.startswith("NAME_"):
#             peopleLst.append(val)

#     SSList: List[SecretSanta] = []
#     for ss in peopleLst:
#         SSList.append(SecretSanta(ss))

#     # Do the selection drawings
#     for SS in SSList:
#         selected = SS.selectPerson(peopleLst)
#         if not selected:
#             # Bad draw state, swap with person before
#             index = SSList.index(SS)
#             if index <= 1:
#                 # Should never happen
#                 print("Invalid state for Secret Santa, stopping.")
#                 exit()

#             # Get the previous person and do a swap
#             prevSS = SSList[index - 1]
#             prevSS.swapPerson(SS)
#         else:
#             # Valid selection, remove it from list
#             peopleLst.remove(selected)

#     # Done, validate selections
#     for SS in SSList:
#         if not SS.validate():
#             print("Invalid SS found: {}".format(SS))
#             exit()

#     # Save selections to text files to be emailed (No Peeking!!!)
#     for SS in SSList:
#         SS.save()
