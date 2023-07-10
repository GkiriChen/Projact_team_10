from collections import UserDict, UserList
from datetime import date, datetime
import pickle
import re
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
            if args[0] in str(self.data[i].name) or args[0] in str(self.data[i]):
                search_result.append(self.data[i])
            else:
                for j in list(self.data[i].phones):
                    if args[0] in str(j):
                        search_result.append(self.data[i])
                        break
        return print(search_result)
    
    def delete_contact(self, contact_name):
        """
        Deletes a contact record based on the provided contact_name.
        If the contact is found and deleted, it returns "Contact deleted".
        If the contact is not found, it returns "Contact not found".
        """
        contact_to_delete = self.data.get(contact_name)
        if contact_to_delete:
            del self.data[contact_name]
            print ("Contact deleted")
        else:
            print ("Contact not found")


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
    # pass
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value: str):
        if value == '.':
            self.__value = None
        elif value[0] == '-':
            self.__value = value[1:]
        elif  len(value) < 9 or len(value) >= 12:
            print(f"Invalid phone: {value}, phone number should consists 10-12 digits. If you wish to save any text as phone use '-' before number")
            raise ValueError()
        else:
            self.__value = value  


# class Birthday(Field):
#     @property
#     def value(self):
#         return self.__value

#     @value.setter
#     def value(self, new_value):
#         self.__value = datetime.strptime(new_value, '%d/%m/%Y').date()
class Birthday(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if new_value == '.':
            self.__value = None
        else:
            try:
                self.__value = datetime.strptime(new_value, '%d/%m/%Y').date()
        
            except (ValueError):
                print("Invalid data. Enter date in format DD/MM/YYYY")
                raise ValueError("Invalid data. Enter date in format dd/mm/YYYY")

class Email(Field):
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value: str):
        if value == '.':
            self.__value = None
        elif not re.match(r"[a-zA-Z]{1}[\w\.]+@[a-zA-Z]+\.[a-zA-Z]{2,}", value):
            print(f"Invalid email format: {value}. Email format should be name@domain.com")
            raise ValueError()
        else:
            self.__value = value

class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None, email: Email = None):
        self.name = name
        self.phones = []
        self.birthday = ''
        self.email = ''
        if phone and phone != '.':
            self.phones.append(phone)
        if birthday and birthday != '.':
            self.birthday = birthday
        if email and email != '.':
            self.email = email
    def __str__(self):
        return f'Name: {self.name} Phone numbers: {self.phones} email: {self.email} BD: {self.birthday}'

    def __repr__(self):
        return f'Name: {self.name} Phone numbers:{self.phones} email: {self.email} BD:{self.birthday}'

    def add_phone(self, phone: Phone):
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
            print('Incorrect data in input. Args should be in next raw: Name Phone Birthday E-mail. if you want to skip argument you can use "."')
        except IndexError:
            print('You entered not correct number of args')
        except TypeError:
            print(TypeError, 'Use commands')
        except StopIteration:
            print('This was last contact')
    return inner

@input_error
def add_contact(args):   
    record = phone_book.data.get(args[0])
    # print(phone_book.data.get(args[0]))
    if record is None:
        if len(args) == 4:
            record = Record(Name(args[0]), Phone(args[1]), Birthday(args[2]), Email(args[3]))
            phone_book.add_record(record)
        else:
            print('Please enter all arguments (Name, Phone, Birthday, Email). If not any argument is not needed you can skip it using "."')
        # elif len(args) == 3:
        #     record = Record(Name(args[0]), Phone(args[1]), Birthday(args[2]))
        # elif len(args) == 2:
        #     record = Record(Name(args[0]), Phone(args[1]))
        # elif len(args) == 1:
        #     record = Record(Name(args[0]))
        
        print(f'A new contact: {args[0]}, has been added.')
    else:
        record.add_phone(Phone(args[1]))
        print('Added one more phone number')

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

# @input_error 
# def change_email(self, email: Email):
#     self.email = email
#     return (f'Email was changed to {self.email}')

# @input_error 
# def change_birthday(args):
#     if args[0] not in phone_book.keys():    
#         print(f'{args[0]} is not in contacts!')
#     else:
#         for key in phone_book.keys():            
#             if key == args[0]:
#             record.change_birthday = args[1]
#         return (f'BD was changed to {self.birthday}')

@input_error
def del_phone(args):
    record = phone_book.data.get(args[0])
    for key in phone_book.keys():            
            if key == args[0]:
                record.delete_phone(args[1])
                print(f'Phone {args[1]} was deleted from {key} contact!')

def search(args):
    return AddressBook.search_in(phone_book, args)

@input_error
def del_record(args):
    global phone_book
    return phone_book.delete_contact(args[0])

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

    commands = ['add', 'change', 'phones', 'hello', 'show all', 'next', 'good bye', 'close', 'exit', 'del', 'del_contact', 'change_email', 'change_bd']
    while True:
        b = input('Enter command > ')
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
        elif d == 'change_email':
            change_email(args)
        elif d == 'change_bd':
            change_contact(args)
        elif d == 'phones':
            phone_book.show_phones(args)
        elif d == 'del':
            del_phone(args)
        elif d == 'search':
            search(args)
        elif d == 'del_contact':
            del_record(args)
        else:
            print('Please enter correct command. Use command "help" to see more.')

if __name__ == "__main__":
    main()
