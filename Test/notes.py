from collections import UserDict
from datetime import datetime
import pickle
import time
from faker import Faker
import random
import os.path


class Notes(UserDict):
    filename = 'notes.sav'
    MAX_STR_LEN = 50
    # notes = {}

    def add_note(self, note):
        id = self.new_id()
        note = Note(note, id)
        self.data[note.id] = note

    def new_id(self):
        if not self.data:
            return 1
        else:
            id_list = list(self.data.keys())
            id_list.sort()
            id = id_list[-1:][0] + 1
            return id

    def find_in_notes(self, string):
        res = {}
        for k, v in self.data.items():
            if v.text.lower().find(string.lower()) >= 0:
                res[k] = v
        return res

    def edit_note(self, note, id):
        self.data[id].edit_note(note)

    def del_note(self, id):
        self.data.pop(id)

    def add_tags(self, id, tags):
        if id in self.data.keys():
            self.data[id].add_note_tags(tags)
            
    def find_by_tag(self, string):
        res = {}
        for k, v in self.data.items():
            if string.lower() in v.tags:
                res[k] = v
        return res

    def show_notes(self, data = None):
        if not data:
            data = self.data
        res = '-' * self.MAX_STR_LEN + '\n'
        for k, v in data.items():
            t = v.text
            while len(t):
                res += t[:self.MAX_STR_LEN] + '\n'
                t = t[self.MAX_STR_LEN:]
            if v.tags:
                res += v.show_tags() + '\n'
            res += v.datetime.strftime("<%d-%m-%Y %H:%M>") + ' ' * 25 + 'id: ' + str(k) + '\n'
            res += '-' * self.MAX_STR_LEN + '\n'
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

    def __init__(self, note, id):
        self.text = note[:self.MAX_NOTE_LEN]
        self.tags = set()
        self.datetime = datetime.now()
        self.id = id

    def add_note_tags(self, tags):
        self.tags.update(tags.split())

    def del_tag(self, tag):
        self.tags.remove(tag)

    def show_tags(self):
        return '#' + ', #'.join(self.tags)

    def edit_note(self, new_text):
        self.text = new_text

def fake_notes(notes):
    fake = Faker(('uk_UA'))
    notes.add_note('Заметка о том, что нужно не забыть делать заметки, чтобы ничего не забывать :-)')
    time.sleep(0.1)
    for _ in range(10):
        i = random.randint(45, 210)
        notes.add_note(fake.text(i))
        time.sleep(0.1)


def main():
    PROMPT = '>'    #приглашение командной строки

    notes = Notes()
    if not os.path.exists(notes.filename):
        fake_notes(notes)
    else:
        notes = notes.read_from_file()
    # print(n.show_notes()) #раскоментировать для просмотра созданных фейковых заметок

    while True:
        answer = input(PROMPT)
        if answer == 'add':     #добавление заметки
            note = input("Tape your note " + PROMPT)
            notes.add_note(note)
            notes.save_to_file()
            print("-- Your note added --")
        elif answer == "show":  #вывод всех заметок
            print(notes.show_notes())
        elif answer == "find":  #поиск по заметкам
            string = input("What find " + PROMPT)
            res = notes.find_in_notes(string)
            if not len(res):
                print("-- No matches found --")
            else:
                print(notes.show_notes(res))
        elif answer == "edit":  #редактирование заметки
            id = int(input("Enter note id " + PROMPT))
            print(notes.show_notes({id: notes.data[id]}))
            note = input("Edit note " + PROMPT)
            notes.edit_note(note, id)
            notes.save_to_file()
            print("-- Note saved --")
        elif answer == "tag":  #добавление тегов в заметку
            id = int(input("Enter note id " + PROMPT))
            print(notes.show_notes({id: notes.data[id]}))
            note = input("Add tags " + PROMPT)
            notes.add_tags(id, note)
            notes.save_to_file()
            print("-- Tags added --")
        elif answer == "tagfind":
            string = input("What tag find " + PROMPT)
            res = notes.find_by_tag(string)
            if not len(res):
                print("-- No matches found --")
            else:
                print(notes.show_notes(res))

        elif answer == "del":  #удаление заметки
            id = int(input("Enter note id " + PROMPT))
            notes.del_note(id)
            notes.save_to_file()
            print("-- Note deleted --")
        elif answer in ["exit", ""]:    #выход из цикла
            notes.save_to_file()
            print("Good bay!")
            break    
    pass


if __name__ == "__main__":
    main()