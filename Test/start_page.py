
from termcolor import colored, cprint
from prettytable import PrettyTable
import os

def input_text():
    text = colored('Зробіть свій вибір: ', 'yellow')
    return input(text).lower().split(' ')

def show_greeting():      
     
    x = PrettyTable(align='l')    # ініціалізуєм табличку, вирівнюєм по лівому краю 

    x.field_names = [colored("Вас вітає бот помічник, наразі доступні наступні модулі:", 'light_blue')]
    x.add_row([colored("1. Сортування файлів","blue")])     
    x.add_row([colored("2. Робота з адресною книгою","blue")])
    x.add_row([colored("3. Робота з нотатками","blue")])
    x.add_row([colored("0. Закінчити роботу програми","blue")])

    print(x) # показуємо табличку

def run():    
    os.system('cls||clear')  # чистим консоль перед виводом
    
    sorting = False
    addresbook = False
    notes = False
    
    while True:
        
        if not (sorting or addresbook or notes):
            show_greeting()        
            answer = input_text()
        
            try:
                if int(answer[0]) == 0:
                    cprint("Good bye!", 'blue')
                    break
                if int(answer[0]) == 1:
                    sorting = True
                if int(answer[0]) == 2:
                    addresbook = True
                if int(answer[0]) == 3:
                    notes = True
            except ValueError as e:
                cprint('Введіть будь ласка число від 0 до 3', 'red')

        if sorting:
            #  тут буде виклик логіки сортування
            sorting = False
            os.system('cls||clear')  # чистим консоль
        
        if addresbook:
            #  тут буде виклик логіки роботи з контактами
            addresbook = False
        
        if notes:
            #  тут буде виклик логіки роботи з нотатками            
            notes = False

if __name__ == '__main__':
    run()

# from termcolor import colored, cprint
# from prettytable import PrettyTable
# import os

# class MenuOption:
#     def __init__(self, description):
#         self.description = description

#     def execute(self):
#         raise NotImplementedError("execute() method must be implemented in subclasses.")


# class SortingOption(MenuOption):
#     def execute(self):
#         print("Sorting module selected.")
#         # Add sorting module logic here


# class AddressBookOption(MenuOption):
#     def execute(self):
#         print("Address book module selected.")
#         # Add address book module logic here


# class NotesOption(MenuOption):
#     def execute(self):
#         print("Notes module selected.")
#         # Add notes module logic here


# class Menu:
#     def __init__(self):
#         self.options = [
#             MenuOption("Exit program"),
#             SortingOption("Sorting files"),
#             AddressBookOption("Address book"),
#             NotesOption("Notes")
#         ]

#     def show(self):
#         table = PrettyTable(field_names=[colored("Available Modules", 'light_blue')])
#         for option_index, option in enumerate(self.options):
#             table.add_row([f"{option_index}. {option.description}"])
#         print(table)

#     def run(self):
#         os.system('cls||clear')
#         while True:
#             self.show()
#             choice = self.get_choice()
#             if choice == 0:
#                 cprint("Goodbye!", 'blue')
#                 break
#             elif 0 < choice < len(self.options):
#                 self.options[choice].execute()
#             else:
#                 cprint("Invalid choice. Please enter a valid option.", 'red')

#     def get_choice(self):
#         while True:
#             try:
#                 choice = int(input("Enter your choice: "))
#                 return choice
#             except ValueError:
#                 cprint("Invalid input. Please enter a number.", 'red')


# if __name__ == '__main__':
#     menu = Menu()
#     menu.run()
