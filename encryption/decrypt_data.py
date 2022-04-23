from cryptography.fernet import Fernet
import os


key = 'xFJwWVWsL2gZlbGqqi2N_7A8xNDpdXlw9A3EbW4cetQ='
filename = 'data'

def decrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it encrypts the file and write it
    """
    f = Fernet(key)

    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()
        # encrypt data
        encrypted_data = f.decrypt(file_data)
        # write the encrypted file
        with open('data.txt', "wb") as file:
            file.write(encrypted_data)

if os.path.isfile(filename):
    decrypt(filename, key)
    print(f'το {filename} είναι έτοιμο')
else:
    print(f'Δεν βρέθηκε το {filename} περάστε το κρυπτογραφημένο αρχείο {filename} με τις διαδρομές και ξανά τρέξτε το decrypt.')
