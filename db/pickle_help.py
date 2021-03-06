import jsonpickle
import pickle


def pickle_to_file(obj, filename):
    """
    :param obj: object to write to file
    :param filename: the file to write to
    """
    outfile = open(filename, 'wb')
    pickle.dump(obj, outfile)
    outfile.close()


def jsonpickle_to_file(obj, filename):
    """
    :param obj: object to write to file
    :param filename: the file to write to
    """
    with open(filename, "w") as f:
        f.write(jsonpickle.encode(obj, make_refs=False))


def pickle_from_file(filename):
    """
    :param filename: file to read from
    :return: the object in file
    """
    infile = open(filename, 'rb')
    data = pickle.load(infile)
    infile.close()
    return data


def jsonpickle_from_file(filename):
    """
    :param filename: file to read from
    :return: the object in file
    """
    with open(filename, "r") as f:
        all_text = f.read()
    data = jsonpickle.decode(all_text)
    return data
