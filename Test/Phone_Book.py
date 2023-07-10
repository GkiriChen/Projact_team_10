from collections import UserDict, UserList
from datetime import date, datetime
import pickle

from termcolor import colored, cprint
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
from prettytable import PrettyTable

class IntentCompleter(Completer):
    def __init__(self, commands):
        super().__init__()
        self.intents = commands

    def get_completions(self, document, complete_event):
        text_before_cursor = document.text_before_cursor
        word_before_cursor = text_before_cursor.split()[-1] if text_before_cursor else ''

        for intent in self.intents:
            if intent.startswith(word_before_cursor):
                yield Completion(intent, start_position=-len(word_before_cursor))


class AddressBook(UserDict):
    def __init__(self, data={}):
        self.data = data
        self.index = 0
        self.__iterator = None
        
    def add_record(self, record):
        self.data[record.name.value] = record

    def show_phones(self, args):
        if args[0] in self.data.keys():
            for i, j in self.data.items():
                if args[0] == i:
                    print(j.phones)
        else:
            print(f'No {args[0]} in Address_book')

    def iterator(self):
        if not self.__iterator:
            self.__iterator = iter(self)
        return self.__iterator

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.data):
            self.index = 0
            raise StopIteration
        else:
            result = list(self.data)[self.index]
            self.index += 1
            return result

    def search_in(self, args):
        search_result = []
        for i in self.data:
            if args[0] in str(self.data[i].name):
                search_result.append(self.data[i])
            else:
                for j in list(self.data[i].phones):
                    if args[0] in str(j):
                        search_result.append(self.data[i])
                        break
        return print(search_result)
    
    def add_contact(self, args):        
        record = self.data.get(args[0])
        print(self.data.get(args[0]))
        if record is None:
            if len(args) > 2:
                record = Record(Name(args[0]), Phone(args[1]), Birthday(args[2]))
            elif len(args) == 2:
                record = Record(Name(args[0]), Phone(args[1]))
            elif len(args) == 1:
                record = Record(Name(args[0]))
            self.add_record(record)
            cprint(f'A new contact: {args[0]}, has been added.', 'green')
        else:
            record.add_phone(args[1])
            cprint('Added one more phone number', 'red')

    def delete_contact(self, contact_name):
        """
        Deletes a contact record based on the provided contact_name.
        If the contact is found and deleted, it returns "Contact deleted".
        If the contact is not found, it returns "Contact not found".
        """
        contact_to_delete = self.data.get(contact_name)
        if contact_to_delete:
            del self.data[contact_name]
            cprint ("Контакт успішно видалений", 'green')
        else:
            cprint ("Контакт не знайдено", 'red')

    def edit_contact(self, contact_name):
        """
        Edit a contact.       
        """
        contact_to_change = self.data.get(contact_name)
        if contact_to_change:
            list_commands = ['done']
            new_dict = contact_to_change.__dict__.copy()
            cprint ("+---------------------+", 'blue')
            cprint ("Доступні поля для зміни", 'blue')
            for key, value  in contact_to_change.__dict__.items():
                print(f'{key} - {value}')
                list_commands.append(key)
            cprint ("+---------------------+", 'blue')
            session = PromptSession(auto_suggest=AutoSuggestFromHistory(), completer=IntentCompleter(list_commands))
            
            while True:                
                input = session.prompt('Введіть перші літери поля яке хочете змінити, або "done" щоб завершити редагування > ')
                input = input.split(' ')[0].strip()
                if input == 'done':
                    break
                else:
                    session2 = PromptSession(auto_suggest=AutoSuggestFromHistory(), completer=IntentCompleter([]))
                    new_value = session2.prompt(f'Введіть нове значення для поля {input} > ')                    
                    
                    if input in new_dict:
                        if input == 'birthday':
                           new_dict[input] = Birthday(new_value) 
                        else:
                           new_dict[input] = new_value
                        
                    else:                    
                        cprint ('Не знайдено або невірна команда', 'red')
            
            phone_book.delete_contact(contact_name)
            phone_book.add_contact(list(new_dict.values()))

            cprint ("Контакт успішно оновлено", 'green')
        else:
            cprint ("Контакт не знайдено", 'red')



class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value


class Name(Field):
    pass


class Phone(Field):
    pass


class Birthday(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
       if new_value: 
            self.__value = datetime.strptime(new_value, '%d/%m/%Y').date()


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phones = []
        self.birthday = ''
        if phone:
            self.phones.append(phone)
        if birthday:
            self.birthday = birthday
    def __str__(self):
        return f' Phone numbers: {self.phones} BD: {self.birthday} Days to BD: {self.days_to_birthday()}'

    def __repr__(self):
        return f' Phone numbers:{self.phones} BD:{self.birthday} Days to BD:{self.days_to_birthday()}'

    def add_phone(self, phone):
        self.phones.append(phone)

    def change_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone == old_phone:
                self.add_phone(new_phone)
                self.phones.remove(phone)
                return True

    def delete_phone(self, new_phone):
        for phone in self.phones:
            if phone == new_phone:
                self.phones.remove(phone)
                return True

    def days_to_birthday(self):
        if not self.birthday:
            return ' '
        today = date.today()
        birthday_this_year = date(today.year, self.birthday.value.month, self.birthday.value.day)
        if birthday_this_year >= today:
            delta = birthday_this_year - today
        else:
            delta = date(today.year + 1, self.birthday.value.month, self.birthday.value.day) - today
        return delta.days


file_name = 'Address_Book.bin'
commands = ['add', 'change', 'phones', 'hello', 'show all', 'next', 'good bye', 'close', 'exit', 'del', 'del_contact', 'edit_contact']

def pack_data():
    with open(file_name, "wb") as f:
        pickle.dump(phone_book, f)

def unpack_data():
    with open(file_name, "rb") as f:
        unpacked = pickle.load(f)
        global phone_book
        phone_book = unpacked

def input_error(func):
    def inner(*args):
        try: 
            return func(*args)  
        except KeyError:
            print('Enter user name.')
        except ValueError:
            print('Incorrect data in input. Check the phone number(should be digit) and Birthday (in dd/mm/Y)!')
        except IndexError:
            print('You entered not correct number of args')
        except TypeError:
            print('Use commands')
        except StopIteration:
            print('This was last contact')
    return inner

@input_error
def add_contact(args):   
   global phone_book
   phone_book.add_contact(args) 
    
@input_error     
def change_contact(args):  
    record = phone_book.data.get(args[0]) 
    print(record)
    if args[0] not in phone_book.keys():  
        record.add_phone(args)  
        print(f'{args[0]} added to contacts!')     
    else:          
        for key in phone_book.keys():            
            if key == args[0]:
                record.change_phone(args[1], args[2])
                print(f'{key} changed his number!')   

@input_error
def del_phone(args):
    record = phone_book.data.get(args[0])
    for key in phone_book.keys():            
            if key == args[0]:
                record.delete_phone(args[1])
                print(f'Phone {args[1]} was deleted from {key} contact!')

def search(args):
    return AddressBook.search_in(phone_book, args)

def show_greeting():      
     
    x = PrettyTable(align='l')    # ініціалізуєм табличку, вирівнюєм по лівому краю 

    x.field_names = [colored("Доступні команди:", 'light_blue')]
    for el in commands:
        x.add_row([colored(el,"blue")])     
    print(x) # показуємо табличку

@input_error
def del_record(args):
    global phone_book
    return phone_book.delete_contact(args[0])

@input_error
def edit_contact(args):
    global phone_book
    return phone_book.edit_contact(args[0])

@input_error
def show():
    return print(next(phone_book.iterator()))

@input_error
def main():
    try:
        unpack_data()
    except Exception:
        global phone_book
        phone_book = AddressBook()

    session = PromptSession(auto_suggest=AutoSuggestFromHistory(), completer=IntentCompleter(commands))
    show_greeting()
    while True:
        
        b = session.prompt('Введіть потрібну вам команду > ').strip() 
        c = ['good bye', 'close', 'exit']
        d, *args = b.split(' ')
        if b in c:
            pack_data()
            print('See you soon!')
            break
        elif b == 'show all':
            print(phone_book)
        elif b == 'hello':
            print('How can i help you?')
        elif b == 'help':
            print(commands)
        elif b == 'next':
            show()
        elif b in commands:
            print('Enter arguments to command')
        elif d == 'add':
            add_contact(args)
        elif d == 'change':
            change_contact(args)
        elif d == 'phones':
            phone_book.show_phones(args)
        elif d == 'del':
            del_phone(args)
        elif d == 'search':
            search(args)
        elif d == 'del_contact':
            del_record(args)
        elif d == 'edit_contact':
            edit_contact(args)
        else:
            cprint('Please enter correct command. Use command "help" to see more.', 'red')

if __name__ == "__main__":
    main()
