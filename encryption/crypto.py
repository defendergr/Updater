from cryptography.fernet import Fernet
import json


key = 'xFJwWVWsL2gZlbGqqi2N_7A8xNDpdXlw9A3EbW4cetQ='
filename = 'data'

def encrypted_data_dict(filename, key):
    """
    Given a filename (str) and key (bytes), it encrypts the file and write it
    """
    f = Fernet(key)

    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()
        # encrypt data
        encrypted_data = f.decrypt(file_data)
        # reconstructing the data as a dictionary
        js = json.loads(encrypted_data)

        return js


dict = encrypted_data_dict(filename, key)
print(dict['update'])
print(dict['local'])
print(dict['remote'])