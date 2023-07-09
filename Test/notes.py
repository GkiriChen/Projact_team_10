from collections import UserDict
from datetime import datetime
import pickle
import time

class Notes(UserDict):
    filename = 'notes.sav'
    MAX_STR_LEN = 50
    # notes = {}

    def add_note(self, note):
        note = Note(note)
        self.data[note.datetime] = note

    def find_in_notes(self, string):
        res = {}
        for k, v in self.data.items():
            if v.text.lower().find(string.lower()) >= 0:
                res[k] = v
        return res

    def edit_note(self):
        pass

    def del_note(self):
        pass

    def find_by_tag(self):
        pass

    def show_notes(self, data = None):
        if not data:
            data = self.data
        res = '-' * 30 + '\n'
        for k, v in data.items():
            t = v.text
            while len(t):
                res += t[:self.MAX_STR_LEN] + '\n'
                t = t[50:]
            res += k.strftime("<%d-%m-%Y %H:%M>") + '\n'
            res += '-' * 30 + '\n'
        return res

    def iterator(self, step=5):
        data = list(self.data.values())
        while data:
            res = data[:step]
            data = data[step:]
            yield res

    def save_to_file(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self, file)

    def read_from_file(self):
        with open(self.filename, "rb") as file:
            content = pickle.load(file)
        return content


class Note:
    MAX_NOTE_LEN = 150   # max lenth of note

    def __init__(self, note):
        self.text = note[:self.MAX_NOTE_LEN]
        self.tags = ()
        self.datetime = datetime.now()

    def add_tags(self, tags):
        self.tags.add(tags)
        pass

    def del_tag(self, tag):
        self.tags.remove(tag)