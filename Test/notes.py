from collections import UserDict
from datetime import datetime
import pickle


class Notes(UserDict):
    filename = 'notes.sav'
    notes = {}

    def add_note(self, note):
        note = Note(note)
        print(note.datetime)
        self.data[note.datetime] = note

    def find_in_notes(self):
        pass

    def edit_note(self):
        pass

    def del_note(self):
        pass

    def find_by_tag(self):
        pass

    def show_notes(self):
        res = '-' * 20 + '\n'
        for k, v in self.data.items():
            res += v.text + '\n'
            res += k.strftime("%d-%m-%Y") + '\n'
            res += '-' * 20 + '\n'
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

    # def find(self, string):
    #     res = []
    #     for k, v in self.data.items():
    #         if k.find(string) >= 0:
    #             res.append((k, v)) 
    #         else:
    #             for phone in v.phones:
    #                 if phone.find(string):
    #                     res.append((k, v))
    #     return res


class Note:
    MAX_NOTE_LEN = 50   # max lenth of note

    def __init__(self, note):
        self.text = note[:self.MAX_NOTE_LEN]
        self.tags = ()
        self.datetime = datetime.now()

    def add_tags(self, tags):
        self.tags.add(tags)
        pass

    def del_tag(self, tag):
        self.tags.remove(tag)