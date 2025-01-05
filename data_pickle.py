import pickle
from address_book import AddressBook

FILE="addressbook.pkl"

class Data_pickle():
    def save_data(self, book):
        with open(FILE, "wb") as f:
            pickle.dump(book, f)

    def load_data(self):
        try:
            with open(FILE, "rb") as f:
                return pickle.load(f)
        except (FileNotFoundError, pickle.UnpicklingError):
            return AddressBook() 
        
data_pickle = Data_pickle()