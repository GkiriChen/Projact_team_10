from collections import UserDict
from datetime import date, datetime
import pickle


class AddressBook(UserDict):
    def __init__(self, data={}):
        self.data = data
        self.index = 0
        self.__iterator = None

    def __repr__(self):
        records_str = [repr(record) for record in self.data.values()]
        return '\n'.join(records_str)
    
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
    
    # def birthday(self, args):
    #     if args >= self.days_to_birthday():
    #         print(self.days_to_birthday())

    # def birthday(self, args):
    #     days_to_birthday = self.days_to_birthday()
    #     if int(args[0]) >= days_to_birthday:
    #         print(days_to_birthday)


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
        self.__value = datetime.strptime(new_value, '%d/%m/%Y').date()


class Email(Field):
    pass


class Address(Field):
    pass


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None, email: Email = None, address: Address = None):
        self.name = name
        self.phones = []
        self.birthday = ''
        self.email = ''
        self.address = ''
        if phone:
            self.phones.append(phone)
        if birthday:
            self.birthday = birthday
        if email:
            self.email = email
        if address:
            self.address = address

    def __str__(self):
        email_str = f', {self.email.value}' if self.email else ''
        address_str = f', {self.address.value}' if self.address else ''
        return f'Contact: {self.name.value}, number: {self.phones}, BD: {self.birthday.value}, Days to BD: {self.days_to_birthday()}{email_str}{address_str}'
    
    def __repr__(self):
        email_str = f', {self.email.value}' if self.email else ''
        address_str = f', {self.address.value}' if self.address else ''
        return f'Contact: {self.name.value}, number: {self.phones}, BD: {self.birthday.value}, Days to BD: {self.days_to_birthday()}{email_str}{address_str}'

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
        today = datetime.today().date()
        next_birthday = date(today.year, self.birthday.value.month, self.birthday.value.day)
        if today > next_birthday:
            next_birthday = date(today.year + 1, self.birthday.value.month, self.birthday.value.day)
        days_left = (next_birthday - today).days
        return days_left
    
    def birthday(self, args):
        days_to_birthday = self.days_to_birthday()
        if int(args[0]) >= days_to_birthday:
            print(days_to_birthday)
    
        
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
    record = phone_book.data.get(args[0])
    if record is None:
        name = Name(args[0])
        phone = Phone(args[1]) if len(args) > 1 else None
        birthday = Birthday(args[2]) if len(args) > 2 else None
        email = Email(args[3]) if len(args) > 3 else None
        address = Address(args[4]) if len(args) > 4 else None
        record = Record(name, phone, birthday, email, address)
        phone_book.add_record(record)
        print(f'A new contact: {args[0]} has been added.')
    else:
        record.add_phone(args[1])
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
def show_all():
    if phone_book.data:
        for contact_name, contact in phone_book.data.items():
            print(f'Name: {contact_name}, {contact}')
    else:
        print("Address book is empty.")


@input_error
def main():
    try:
        unpack_data()
    except Exception:
        global phone_book
        phone_book = AddressBook()

    commands = ['add', 'change', 'phones', 'hello', 'show all', 'next', 'good bye', 'close', 'exit', 'del', 'birthday']
    while True:
        b = input('Enter command:')
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
        elif d == 'birthday':
            for record in phone_book.data.values():
                record.birthday(args)
        else:
            print('Please enter correct command. Use command "help" to see more.')


if __name__ == "__main__":
    main()