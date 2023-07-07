import pickle
import datetime


class Record:
    def __init__(self, name, birthday=None, email=None, address=None):
        self.name = name
        self.phones = []
        self.birthday = birthday
        self.email = email
        self.address = address

    def add_phone(self, phone):
        if isinstance(phone, Phone):
            self.phones.append(phone)
        else:
            raise ValueError("Invalid phone object")

    def remove_phone(self, phone):
        if phone in self.phones:
            self.phones.remove(phone)
        else:
            raise ValueError("Phone not found")

    def edit_phone(self, old_phone, new_phone):
        if old_phone in self.phones:
            index = self.phones.index(old_phone)
            self.phones[index] = new_phone
        else:
            raise ValueError("Phone not found")

    def set_birthday(self, birthday):
        if isinstance(birthday, Birthday):
            self.birthday = birthday
        else:
            raise ValueError("Invalid birthday object")

    def set_email(self, email):
        if isinstance(email, Email):
            self.email = email
        else:
            raise ValueError("Invalid email object")

    def set_address(self, address):
        if isinstance(address, Address):
            self.address = address
        else:
            raise ValueError("Invalid address object")

    def days_to_birthday(self, num_days):
        today = datetime.date.today()
        next_birthday_contacts = []

        for contact in self.data.values():
            if contact.birthday:
                next_birthday = datetime.date(today.year, contact.birthday.month, contact.birthday.day)
                if today > next_birthday:
                    next_birthday = datetime.date(today.year + 1, contact.birthday.month, contact.birthday.day)
                days_left = (next_birthday - today).days

                if days_left <= num_days:
                    next_birthday_contacts.append(contact)

        return next_birthday_contacts


    @property
    def name_value(self):
        return self.name.value

    @property
    def birthday_value(self):
        return self.birthday.value if self.birthday else None

    @birthday_value.setter
    def birthday_value(self, value):
        if value is None or isinstance(value, Birthday):
            self.birthday = value
        else:
            raise ValueError("Invalid birthday object")

class Email:
    def __init__(self, value):
        self.value = value

class Address:
    def __init__(self, value):
        self.value = value

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def __iter__(self):
        return self.iterator()

    def iterator(self, n=1):
        keys = list(self.data.keys())
        num_records = len(keys)
        current_index = 0

        while current_index < num_records:
            yield [self.data[keys[i]] for i in range(current_index, min(current_index + n, num_records))]
            current_index += n
        
    def save_to_file(self, filename):
        data = {
            'records': [
                {
                    'name': record.name.value,
                    'phones': [phone.value for phone in record.phones],
                    'birthday': record.birthday.value if record.birthday else None,
                    'email': record.email.value if record.email else None,
                    'address': record.address.value if record.address else None
                }
                for record in self.data.values()
            ]
        }
        with open(filename, 'wb') as file:
            pickle.dump(data, file)

    def load_from_file(self, filename):
        with open(filename, 'rb') as file:
            data = pickle.load(file)
            self.data = {}
            for record_data in data['records']:
                record = Record(Name(record_data['name']), Birthday(record_data['birthday']))   #Треба звернути увигу на назви классу коли будемо зшивати код
                for phone_value in record_data['phones']:
                    record.add_phone(Phone(phone_value))        
                if 'email' in record_data and record_data['email']:
                    record.set_email(Email(record_data['email']))
                if 'address' in record_data and record_data['address']:
                    record.set_address(Address(record_data['address']))
                self.add_record(record)

    def add_email(self, contact_name, email):
        if contact_name in self.data:
            self.data[contact_name].set_email(email)
        else:
            print(f"Contact '{contact_name}' not found.")

    def add_address(self, contact_name, address):
        if contact_name in self.data:
            self.data[contact_name].set_address(address)
        else:
            print(f"Contact '{contact_name}' not found.")
