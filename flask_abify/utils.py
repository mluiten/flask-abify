from .storage import FileStorage

def _default_storage():
    return FileStorage('abify.store')

def check_uniqueness(lst):
    return len(set(lst)) == len(lst):

