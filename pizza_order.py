from time import sleep
import click
from random import randint
import sys
from typing import Union, Callable

def str_to_class(str):
    return getattr(sys.modules[__name__], str.title() + "()")


def log(msg:str):
    def _log(func:Callable):
        def wrapper(pizza:Pizza):
            attr = func.__name__ +"_time"
            f_time = getattr(pizza, attr)
            sleep(f_time)
            print(msg.format(f_time))
        return wrapper
    return _log

@click.group()
def cli():
    pass


@cli.command()
def menu():
    print("- Margherita 🧀 : tomato sauce, mozzarella, tomatoes\n — Pepperoni 🍕 : tomato sauce, mozzarella, pepperoni\n — Hawaiian 🍍 : tomato sauce, mozzarella, chicken, pineapples")


        
class Pizza():
    name: str
    size = 'L'
    emoji: str
    recipe:  str
    order_time = randint(1,5)
    bake_time = randint(1,5)
    delivery_time = randint(1,5)
    pickup_time = randint(1,5)
    
    def __dict__(self):
        print({self.__name__ + " " + self.emoji : self.recipe})
        

        
class Margherita(Pizza):

    def __init__(self,size='L'):
        self.size = size
        self.recipe = 'tomato sauce, mozzarella, tomatoes'
        self.emoji = '🧀'

class Pepperoni(Pizza):
    
    def __init__(self,size='L'):
        self.size = size
        self.recipe = 'tomato sauce, mozzarella, pepperoni'
        self.emoji = '🍕'
        
class Hawaiian(Pizza):
    
    def __init__(self,size='L'):
        self.size = size
        self.recipe = 'tomato sauce, mozzarella, chicken, pineapples'
        self.emoji = '🍍'


    

@log("󰳏 Приготовили за {}с!")
def bake(pizza: Pizza):
    pass

@log('🛵 Доставили за {}с!')
def delivery(pizza: Pizza):
    pass

@log("🏠 Забрали за {}с!")
def pickup(pizza: Pizza):
    pass
    
@cli.command()
@click.option('--delivery', default=False, is_flag=True)
@click.option('--pickup', default=False, is_flag=True)
@click.argument('pizza', nargs=1)
def order(pizza: Union[str,Pizza], delivery_: bool, pickup_: bool):
    if(type(pizza) == 'str'):
        pizza = str_to_class(pizza.title())
    bake(pizza)
    if(delivery_):
        delivery(pizza)
    if(pickup_):
        pickup(pizza)

        
if __name__ == '__main__' :
    m = Margherita()
    bake(m)
    cli()