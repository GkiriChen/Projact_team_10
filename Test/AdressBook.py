import contextlib
from collections import UserDict, UserList
from datetime import date, datetime
import pickle
import re
from prettytable import PrettyTable
from termcolor import colored, cprint


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
        # x = PrettyTable(align='l')    # ініціалізуєм табличку, вирівнюєм по лівому краю 
        # x.field_names = [colored("Що вдалося знайти:", 'light_blue')]
        # x.field_names = [colored("Name", 'light_blue'),colored("Phone", 'light_blue'),colored("Email", 'light_blue'),colored("Birthday", 'light_blue')]
        # for key, values in search_result:
        #     x.add_row([colored(f"{key}","blue"),colored(f"{values.phones}","blue"),colored(f"{values.email}","blue"),colored(f"{values.birthday}","blue")])
        # return x
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

    def show_all_cont(self):
        x = PrettyTable(align='l')    # ініціалізуєм табличку, вирівнюєм по лівому краю 
        x.field_names = [colored("Name", 'light_blue'),colored("Phone", 'light_blue'),colored("Email", 'light_blue'),colored("Birthday", 'light_blue'),colored("Address", 'light_blue')]
        for key, values in self.data.items():
            x.add_row([colored(f"{key}","blue"),colored(f"{values.phones}","blue"),colored(f"{values.email}","blue"),colored(f"{values.birthday}","blue"),colored(f"{values.address}","blue")])
        return x
    
    def birthday_in_days(self):
        for key, value in phone_book.data.items():
            value = str(value)
            start_index = value.find("]") + 1
            end_index = value.find("]") + 11
            birthday = value[start_index:end_index]
            try:
                birthday = datetime.strptime(birthday, '%Y-%m-%d')
            except ValueError:
                continue

            number = int(self[0])
            today = date.today()
            birthday_this_year = date(today.year, birthday.month, birthday.day)
            birthday_next_year = date(today.year + 1, birthday.month, birthday.day)
            
            if birthday_this_year >= today:
                delta = birthday_this_year - today
                delta_plus = abs(delta.days)
                if number >= delta_plus:
                    print(f"Contact {key} has a birthday in {delta_plus} days ")
                else:
                    continue
            elif birthday_next_year >= today:
                delta = birthday_next_year - today
                delta_plus = abs(delta.days)
                if number >= delta_plus:
                    print(f"Contact {key} has a birthday in {delta_plus} days ")
                else:
                    continue
            else:
                print(f"No contacts whose birthday is in {number} days")


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
        elif  len(value) < 9 or len(value) > 12:
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

class Address(Field):
    pass


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None, email: Email = None, address: Address = None):
        self.name = name
        self.phones = []
        self.birthday = ''
        self.email = ''
        self.address = ''
        if phone and phone != '.':
            self.phones.append(phone)
        if birthday and birthday != '.':
            self.birthday = birthday
        if email and email != '.':
            self.email = email
        if address and address != '.':
            self.address = address
    def __str__(self):
        return f'{self.name}{self.phones}{self.birthday}{self.email}'

    def __repr__(self):
        return f'{self.name}{self.phones}{self.birthday}{self.email}'

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def change_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone == old_phone:
                self.add_phone(new_phone)
                self.phones.remove(phone)
                return True

    def change_birthday(self, birthday: Birthday):
        self.birthday = birthday
        return True
    
    def change_email_iner(self, email: Email):
        self.email = email
        return True
    
    def change_address_iner(self, address: Address):
        self.address = address
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

def show_help():      
    x = PrettyTable(align='l')    # ініціалізуєм табличку, вирівнюєм по лівому краю 

    x.field_names = [colored("Робота з адресною книгою, наразі доступні наступні команди:", 'light_blue')]
    for a, i in enumerate(commands, start=1):
        x.add_row([colored(f"{a}. {i}","blue")])
    x.add_row([colored("0. close, exit", "blue")])
    return x # показуємо табличку

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
            print('Incorrect data in input.')
        except IndexError:
            print('You entered not correct number of args')
        except TypeError:
            print('Use commands')
        except StopIteration:
            print('This was last contact')
    return inner

@input_error
def add_contact(args):
    if args is str:
        record = Record(Name(args))
        phone_book.add_record(record)
        return f'New contact was added: {record}'
    record = phone_book.data.get(args[0])
    if record is None:
        if len(args) != 4:
            return 'Please enter all arguments (Name, Phone, Birthday, Email, Address). \nIf argument is not needed you can skip it using "."\nf.e. Name . . email@domen.com'
        record = Record(Name(args[0]), Phone(args[1]), Birthday(args[2]), Email(args[3], Address(args[4])))
        phone_book.add_record(record)
        # elif len(args) == 3:
        #     record = Record(Name(args[0]), Phone(args[1]), Birthday(args[2]))
        # elif len(args) == 2:
        #     record = Record(Name(args[0]), Phone(args[1]))


        return f'A new contact: {args[0]}, has been added.'
    else:
        record.add_phone(Phone(args[1]))
        return 'Added one more phone number'

@input_error     
def change_contact(args):  
    record = phone_book.data.get(args[0]) 
    if args[0] not in phone_book.keys():  
        record.add_phone(args)  
        return f'{args[0]} added to contacts!'
    else:          
        for key in phone_book.keys():            
            if key == args[0]:
                record.change_phone(args[1], args[2])
                return f'{key} changed his number!'

@input_error 
def change_email(args):
    if args[0] not in phone_book.keys():
        return f'{args[0]} is not in contacts!'
    record = phone_book.data.get(args[0])
    for key in phone_book.keys():            
        if key == args[0]:
            record.change_email_iner(Email(args[1]))
            return (f'Email was changed in Contact > {record}')

@input_error
def change_birthday(args): 
    if args[0] not in phone_book.keys():
        return f'{args[0]} is not in contacts!'
    record = phone_book.data.get(args[0])
    for key in phone_book.keys():            
        if key == args[0]:
            record.change_birthday(Birthday(args[1]))
            return (f'BD was changed in Contact > {record}')
        
@input_error 
def change_address(args):
    if args[0] not in phone_book.keys():
        return f'{args[0]} is not in contacts!'
    record = phone_book.data.get(args[0])
    for key in phone_book.keys():            
        if key == args[0]:
            record.change_address_iner(Email(args[1]))
            return (f'Email was changed in Contact > {record}')

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
commands = ['add', 'change', 'phones', 'hello', 'show all', 'next', 'del_phone', 'del_contact', 'change_email', 'change_bd', 'change_address', 'birthday_in_days']

@input_error
def main():
    try:
        unpack_data()
    except Exception:
        global phone_book
        phone_book = AddressBook()

    # commands = ['add', 'change', 'phones', 'hello', 'show all', 'next', 'good bye', 'close', 'exit', 'del', 'del_contact', 'change_email', 'change_bd']
    print(show_help())
    while True:
        b = input(colored('Зробіть свій вибір > ', 'yellow'))
        c = ['good bye', 'close', 'exit']
        d, *args = b.split(' ')
        with contextlib.suppress(ValueError):
            if int(d):
                for a, i in enumerate(commands, start=1):
                    if a == int(d):
                        d = i

        if b in c or d in c or d == '0':
            pack_data()
            cprint('See you soon!','green')
            break
        elif b == 'show all' or d == 'show all':
            print(phone_book.show_all_cont())
        elif b == 'hello' or d == 'hello':
            print('How can i help you?')
        # elif b == 'help' or d == 'help':
        #     print(show_greeting())
        elif b == 'next' or d == 'next':
            show()
        elif b in commands:
            cprint('Enter arguments to command', 'red')
        elif d == 'add':
            cprint(add_contact(args), 'blue')
        elif d == 'change':
            cprint(change_contact(args), 'green')
        elif d == 'change_email':
            cprint(change_email(args), 'green')
        elif d == 'change_bd':
            cprint(change_birthday(args), 'green')
        elif d == 'change_address':
            cprint(change_address(args), 'green')
        elif d == 'phones':
            phone_book.show_phones(args)
        elif d == 'del_phone':
            del_phone(args)
        elif d == 'search':
            search(args)
        elif d == 'birthday_in_days':
            AddressBook.birthday_in_days(args)
        elif d == 'del_contact':
            del_record(args)
        else:
            print('Please enter correct command. Use command "help" to see more.')

if __name__ == "__main__":
    main()
