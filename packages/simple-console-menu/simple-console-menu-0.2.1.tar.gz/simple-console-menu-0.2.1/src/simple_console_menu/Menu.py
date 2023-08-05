from enum import Enum
import math
from . import Menu_old


class ValueToReturnEmptyError(Exception):
        """
        raised when the value to return is empty
        """
        def __init__(self, message:str = "Value to return is empty") -> None:
            super().__init__(message)


class menu:
    """
    allows you to create a menu
    """


    class menu_data_type(Enum):
        """
        data types for the menu
        possible values:
        STRING
        INT
        FLOAT
        """
        STRING = 1
        INT = 2
        FLOAT = 3


    class display_type(Enum):
        """
        display types for the menu
        possible values:
        BLOCK
        SIMPLE
        """
        BLOCK = 1
        SIMPLE = 2


    def __init__(self, 
                menu_name:str, 
                menu_items:list, 
                input_question:str = "What do you want to do:", 
                menu_size:int = 76, 
                auto_add_quit:bool = False,
                return_type:menu_data_type = menu_data_type.INT) -> None:
        """
        allows you to create a menu
        :param menu_name: name of the menu (Str)
        :param menu_items: menu items ["item 1","item 2"] (List)
        :param input_question: question to ask the user (Str)
        :param menu_size: size of the menu (Int)
        :param auto_add_quit: automatically add a quit option (Bool)
        :return: None
        """
        self.menu_name = menu_name
        self.menu_items = menu_items
        self.input_question = input_question
        self.menu_size = menu_size
        self.auto_add_quit = auto_add_quit
        self.return_type = return_type

    def __str__(self) -> str:
        """
        returns the menu as a string
        :return: menu as a string
        """
        to_return = ""
        for k, v in self.__dict__.items():
            if not k.startswith("_menu__"):
                to_return += f"{k}: {v}, "
        return to_return[:-2]

    def set_menu_name(self, menu_name:str) -> None:
        """
        sets the menu name
        :param menu_name: name of the menu (Str)
        :return: None
        """
        self.menu_name = menu_name

    def set_menu_items(self, menu_items:list) -> None:
        """
        sets the menu items
        :param menu_items: menu items ["item 1","item 2"] (List)
        :return: None
        """
        self.menu_items = menu_items
        
    def add_menu_item(self, menu_item:str) -> None:
        """
        adds a menu item
        :param menu_item: menu item to add (Str)
        :return: None
        """
        self.menu_items.append(menu_item)

    def set_input_question(self, input_question:str) -> None:
        """
        sets the input question
        :param input_question: question to ask the user (Str)
        :return: None
        """
        self.input_question = input_question

    def set_menu_size(self, menu_size:int) -> None:
        """
        sets the menu size
        :param menu_size: size of the menu (Int)
        :return: None
        """
        self.menu_size = menu_size

    def set_auto_add_quit(self, auto_add_quit:bool) -> None:
        """
        sets the auto add quit option
        :param auto_add_quit: automatically add a quit option (Bool)
        :return: None
        """
        self.auto_add_quit = auto_add_quit
    
    def set_return_type(self, return_type:menu_data_type) -> None:
        """
        sets the return type
        :param return_type: return type (menu_data_type)
        :return: None
        """
        self.return_type = return_type

    def display(self, menu_display_type:display_type = display_type.BLOCK) -> None:
        """
        displays the menu
        :return: None
        """
        self.__menu_items_to_display = self.menu_items
        if self.auto_add_quit:
            self.__menu_items_to_display.append('Quit')
        if menu_display_type == self.display_type.BLOCK:
            self.__menu_number = 1
            self.__choose_amount = 0
            self.__menu_name_length = len(self.menu_name) + 2
            self.__menu_name_length = self.menu_size - self.__menu_name_length
            self.__menu_name_length /= 2
            if (self.__menu_name_length % 2) == 0:
                print('╭'+int(self.__menu_name_length-1)*'─',self.menu_name,int(self.__menu_name_length-1)*'─'+'╮')
            else:
                self.__menu_name_length1 = math.ceil(self.__menu_name_length)
                self.__menu_name_length2 = math.floor(self.__menu_name_length)
                print('╭'+int(self.__menu_name_length1-1)*'─',self.menu_name,int(self.__menu_name_length2-1)*'─'+'╮')
            for x in self.__menu_items_to_display:
                self.__menu_items_with_numbers = str(self.__menu_number)+'. '+x
                print(f'│{self.__menu_items_with_numbers}'+((self.menu_size-2)-len(self.__menu_items_with_numbers))*' '+'│')
                self.__menu_number += 1
            print('╰'+(self.menu_size-2)*'─'+'╯')  
        
        elif menu_display_type == self.display_type.SIMPLE:
            self.__menu_number = 1
            self.__choose_amount = 0
            self.__menu_name_length = len(self.menu_name) + 2
            self.__menu_name_length = self.menu_size - self.__menu_name_length
            self.__menu_name_length /= 2
            if (self.__menu_name_length % 2) == 0:
                #even
                print(int(self.__menu_name_length)*'-',self.menu_name,int(self.__menu_name_length)*'-')
            else:
                #uneven
                menuNameLength1 = math.ceil(self.__menu_name_length)
                menuNameLength2 = int(math.floor(self.__menu_name_length))
                print(int(menuNameLength1)*'-',self.menu_name,int(menuNameLength2)*'-')
            for x in self.__menu_items_to_display:
                print(f'{self.__menu_number}. {x}')
                self.__menu_number += 1
            print(self.menu_size*'-')
        
        else:
            raise Exception("HOW DID YOU GET HERE?")

        
        while True:
            self.value_to_return = input(self.input_question)
            if self.return_type == self.menu_data_type.INT:
                try:
                    self.value_to_return = int(self.value_to_return)
                except ValueError:
                    print("You must enter a number")
                else:
                    break
            elif self.return_type == self.menu_data_type.FLOAT:
                try:
                    self.value_to_return = float(self.value_to_return)
                except ValueError:
                    print("You must enter a number")
                else:
                    break
            elif self.return_type == self.menu_data_type.STRING:
                break

    def get_user_input(self) -> str | int | float:
        """
        returns the user input
        :return: user input (Str | Int | Float)
        :raises ValueToReturnEmptyError: if the value to return is empty
        """
        try:
            return self.value_to_return
        except AttributeError:
            raise ValueToReturnEmptyError("Value to return is empty")



def SimpleConsoleMenu(menuName:str,menuItems:list,inputQuestion = "What do you want to do:",menuSize = 76,autoAddQuit = False,onlyReturnNumber = True, allowedCharacters = '', acceptedQuitCharacters = '', suppress_deprecation_warning = False) -> int | str:
    if not suppress_deprecation_warning:
        print("The SimpleConsoleMenu is deprecated, if you wish to continue using it, import it from the old module: 'from simple_console_menu import Menu_old'")
    return Menu_old.SimpleConsoleMenu(menuName,menuItems,inputQuestion,menuSize,autoAddQuit,onlyReturnNumber,allowedCharacters,acceptedQuitCharacters)
    
    # raise DeprecationWarning("The SimpleConsoleMenu function is deprecated, if you wish to continue using it, import it from the old module: 'from simple_console_menu import Menu_old'")

def SimpleConsoleMenuBlock(menuName:str,menuItems:list,inputQuestion = "What do you want to do:",menuSize = 76,autoAddQuit = False,onlyReturnNumber = True, allowedCharacters = '', acceptedQuitCharacters = '', suppress_deprecation_warning = False) -> int | str:
    if not suppress_deprecation_warning:
        print("The SimpleConsoleMenuBlock is deprecated, if you wish to continue using it, import it from the old module: 'from simple_console_menu import Menu_old'")
    return Menu_old.SimpleConsoleMenuBlock(menuName,menuItems,inputQuestion,menuSize,autoAddQuit,onlyReturnNumber,allowedCharacters,acceptedQuitCharacters)
    # raise DeprecationWarning("The SimpleConsoleMenuBlock function is deprecated, if you wish to continue using it, import it from the old module: 'from simple_console_menu import Menu_old'")