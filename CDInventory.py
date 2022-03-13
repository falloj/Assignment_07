#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# JFallon, 2022-Mar-06, Modified File; moved parts of script body into functions
# JFallon, 2022-Mar-13, Modified File; changed file handling from .txt to .dat; improved error handling
#------------------------------------------#

# import your modules
import sys, pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of dictionaries to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.txt'  # data storage text file
datFileName = 'CDInventory.dat' # data storage file
objFile = None  # file object

# -- PROCESSING -- #
class DataProcessor:
    @staticmethod
    def add_inventory(cd_id, title, artist):
        """Adds user input values for, CD ID, Title, and Artist to a 2D table

        Args:
            cd_id (string): a string of the user selected ID value
            title (string): a string of the user input for CD name
            artist (string): a string of the user input for Artist

        Returns:
            None.

        """
        intID = int(cd_id)
        dicRow = {'ID': intID, 'Title': title, 'Artist': artist}
        lstTbl.append(dicRow)
        IO.show_inventory(lstTbl)
        
    @staticmethod
    def delete_inventory(table):
        """Deletes a user selected CD dict in a 2D table

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.

        """
        # TODone: improve error handling if the user tries deleting a non-numeric ID
        intIDDel = '' # set intIDDel to empty
        while type(intIDDel) != int: # don't let the user go anywhere until they select a numeric ID
            try:
                intIDDel = int(input('Which ID would you like to delete? ').strip())
            except ValueError:
                print('\nSorry, that didn\'t work. Please select an ID from your current inventory.\n')
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == intIDDel:
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('\nThe CD was removed.\n')
        else:
            print('\nCould not find this CD!\n')

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        # TODone modify existing code to work with binary instead of text
        # TODone improve existing error handling in case a user tries to load a non-existant file
        try: # add some error handling in case the file doesn't exist
            table.clear() # this clears existing data and allows to load data from file
            objFile = open(file_name, 'rb') # open the binary file in read mode
            data = pickle.load(objFile) # unpickle it
            for row in data: # iterate through the dictionaries in the list
                table.append(row) # append each dictionary to the global list
            objFile.close() # close the file
        except FileNotFoundError: # added specific FileNotFoundError exception type
            print('\nYour CD inventory is empty! Try adding a CD.\n')

    @staticmethod
    def write_file(file_name, table):
        """Function to save data to text file

        Saves the data from a 2D table to binary file

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        # TOdone modify existing code to work with binary instead of text
        objFile = open(file_name, 'wb') # open the binary file in write mode, will be created if DNE
        pickle.dump(table, objFile) # pickle it
        print('\nYour CD inventory is saved to file now.\n') # give the user some feedback
        objFile.close() # close the file


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] Load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] Delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def get_inventory():
        """Gets user input, and returns values for, CD ID, Title, and Artist 

        Args:
            None.

        Returns:
            cd_id (string): a string of the user selected ID value
            title (string): a string of the user input for CD name
            artist (string): a string of the user input for Artist

        """
        # TODone improve error handling if the user enters a non-numeric ID
        cd_id = '' # set cd_id to empty; we'll get a value for it below
        while type(cd_id) != int: # don't let the user go anywhere until they enter a number
            try: # set up error handling to catch non-numeric id values
                cd_id = int(input('Enter an ID number: ').strip())
            except ValueError: # added ValueError exception type
                print('That value was not a number, or wasn\'t a whole number. Please try again.')        
        title = input('What is the CD\'s title? ').strip()
        artist = input('What is the Artist\'s name? ').strip()
        return cd_id, title, artist
    

# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(datFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('Type \'yes\' to continue and reload from file. Otherwise reload will be canceled: ')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(datFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('Canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        strID, strAlbum, strArtist = IO.get_inventory()
        # 3.3.2 Add item to the table
        DataProcessor.add_inventory(strID, strAlbum, strArtist)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        DataProcessor.delete_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        # 3.5.2 search thru table and delete CD
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(datFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be safe:
    else:
        print('General Error')