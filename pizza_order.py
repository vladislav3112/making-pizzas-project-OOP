from time import sleep
import click
from random import randint
import sys
from typing import Union, Callable


def str_to_class(str: str):
    """Функция для перевода из строкового названия пиццы в консоли в объект класса"""
    return getattr(sys.modules[__name__], str.title())


def log(msg: str):
    """Выводит время выполниния функции, принимая соответствующий шаблон"""

    def _log(func: Callable):
        def wrapper(pizza: Pizza):
            attr = func.__name__ + "time"
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
    """Выводит меню"""
    print(
        "— Margherita 🧀 : tomato sauce, mozzarella, tomatoes\n— Pepperoni 🍕 : tomato sauce, mozzarella, pepperoni\n— Hawaiian 🍍 : tomato sauce, mozzarella, chicken, pineapples"
    )


class Recipe:
    """Класс для описания рецептов
    — метод dict() выводит рецепт в виде словаря
    """

    pizza_name: str
    recipe: list

    def __init__(self, pizza_name, recipe_list) -> None:
        self.pizza_name = pizza_name
        self.recipe_list = recipe_list


class Pizza:
    """Класс для описания пицц:
    - bake_time, delivery_time и pickup_time определяют время готовки, доставки, самовывоза
    - При задании размера XL пицца готовится на 2 сек дольше
    - Рецепт пиццы передается в формате: название пиццы, список ингридиентов
    """

    name: str
    size: str
    emoji: str
    recipe: Recipe
    recipe_list: list

    bake_time = randint(1, 5)
    delivery_time = randint(1, 4)
    pickup_time = randint(1, 4)

    def __init__(self, size="L") -> None:
        self.size = size
        if size == "XL":
            self.bake_time += 2
        name = type(self).__name__ + " " + self.emoji
        self.recipe = Recipe(name, self.recipe_list)


class Margherita(Pizza):
    recipe_list = ["tomato sauce", "mozzarella", "tomatoes"]
    emoji = "🧀"


class Pepperoni(Pizza):
    recipe_list = ["tomato sauce", "mozzarella", "pepperoni"]
    emoji = "🍕"


class Hawaiian(Pizza):
    recipe_list = ["tomato sauce", "mozzarella", "chicken", "pineapples"]
    emoji = "🍍"


@log("󰳏 Приготовили за {}с!")
def bake_(pizza: Pizza):
    """Готовит пиццу"""
    pass


@log("🛵 Доставили за {}с!")
def delivery_(pizza: Pizza):
    """Доставляет пиццу"""
    pass


@log("🏠 Забрали за {}с!")
def pickup_(pizza: Pizza):
    """Самовывоз"""
    pass


@cli.command()
@click.option("--delivery", default=False, is_flag=True)
@click.option("--pickup", default=False, is_flag=True)
@click.argument("pizza", nargs=1)
def order(pizza: Union[str, Pizza], delivery: bool, pickup: bool):
    """Готовит и доставляет пиццу"""
    if isinstance(pizza, str):
        pizza_obj = str_to_class(pizza.title())
    else:
        pizza_obj = pizza
    bake_(pizza_obj)
    if delivery:
        delivery_(pizza_obj)
    if pickup:
        pickup_(pizza_obj)


if __name__ == "__main__":
    cli()
