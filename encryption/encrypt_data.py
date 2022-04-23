from cryptography.fernet import Fernet
import os

# Generates a key
# key = Fernet.generate_key()


key = 'xFJwWVWsL2gZlbGqqi2N_7A8xNDpdXlw9A3EbW4cetQ='
filename = 'data.txt'

def encrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it encrypts the file and write it
    """
    f = Fernet(key)

    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()
        # encrypt data
        encrypted_data = f.encrypt(file_data)
        # write the encrypted file
        with open('data', "wb") as file:
            file.write(encrypted_data)

if os.path.isfile(filename):
    encrypt(filename, key)
    print(f'το {filename} είναι έτοιμο')
else:
    print(f'Δεν βρέθηκε το {filename} φτιάξτε ένα αρχείο {filename} με τις διαδρομές και ξανά τρέξτε το encrypt.')