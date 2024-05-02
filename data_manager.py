import pickle

def save_data(filename, data):
    with open(filename, "wb") as file:
        pickle.dump(data, file)

def load_data(filename):
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except (FileNotFoundError, EOFError):
        return []