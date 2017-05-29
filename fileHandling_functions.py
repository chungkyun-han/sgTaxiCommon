import os
import pickle
import fnmatch


path_merge = lambda path1, path2 : os.path.join(path1, path2)


def check_path_exist(path):
    return True if os.path.exists(path) else False


def check_dir_create(path):
    if not os.path.exists(path):
        os.makedirs(path)

def save_pickle_file(path, _objects):
    with open(path, 'wb') as fp:
        pickle.dump(_objects, fp)
    del _objects


def load_pickle_file(path):
    with open(path, 'rb') as fp:
        return pickle.load(fp)


def get_all_files(path, wildcard_expression):
    return sorted([fn for fn in os.listdir(path) if fnmatch.fnmatch(fn, wildcard_expression)])