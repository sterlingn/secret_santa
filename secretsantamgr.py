from secretsanta import SecretSanta


class SecretSantaMgr:
    """Manager for all secret santas
    """

    def __init__(self):
        """Initializer
        """
        self._SSList = []
        self._selectionList = []

    def addSecretSanta(self, name: str, email: str = ""):
        """Add a new secret santa

        Args:
            str (name): The name of the secret santa
            str (email, optional): The email address of the secret santa. Defaults to "".
        """
        self._SSList.append(SecretSanta(name, email))
        self._selectionList.append(name)
    
    def runSelections(self) -> bool:
        """Select a person for each secret santa

        Returns:
            bool: Whether or not selections succeeded
        """
        for SS in self._SSList:
            selected = SS.selectPerson(self._selectionList)
            if not selected:
                # Bad draw state, swap with person before
                index = self._SSList.index(SS)
                if index <= 1:
                    # Should never happen
                    print("Invalid state for Secret Santa, stopping.")
                    return False

                # Get the previous person and do a swap
                prevSS = self._SSList[index - 1]
                prevSS.swapPerson(SS)
            else:
                # Valid selection, remove it from list
                self._selectionList.remove(selected)

        # Done, validate selections
        for SS in self._SSList:
            if not SS.validate():
                print("Invalid SS found: {}".format(SS))
                return False

        return True
    
    def emailSelections(self):
        """Email selections to all secret santas
        """
        for SS in self._SSList:
            # Check if they have email
            if SS.hasEmail():
                print("Sending email to {} via {}".format(SS.getMe(), SS.getEmail()))
                # TODO: Have manager send email
                SS.sendEmail()
            else:
                print("Email not found for {}".format(SS.getMe()))
    
    def saveSelections(self):
        """Save a text file formatted by the secret santas name to the current
        directory
        """
        for SS in self._SSList:
            print("Saving file for {} to {}".format(SS.getMe(), SS.getFileName()))
            SS.save()
