import click
import sys
from random import randint
from time import sleep
from typing import Union, Callable
from functools import wraps
from click_option_group import optgroup, MutuallyExclusiveOptionGroup


def str_to_class(str: str):
    """Функция для перевода из строкового названия пиццы в консоли в объект класса"""
    try:
        return getattr(sys.modules[__name__], str.title())
    except (AttributeError):
        print("Wrong pizza name, order again")
        return


def log(msg: str):
    """Выводит время выполниния функции, принимая соответствующий шаблон"""

    @wraps(msg)
    def inner_log_func(func: Callable):
        @wraps(func)
        def wrapper(pizza: Pizza):
            attr = func.__name__ + "_time"
            f_time = getattr(pizza, attr)
            sleep(f_time)
            print(msg.format(f_time))

        return wrapper

    return inner_log_func


@click.group()
def cli():
    pass


@cli.command()
def menu():
    """Выводит меню"""
    print(
        "— Margherita 🧀 : tomato sauce, mozzarella, tomatoes\n"
        "— Pepperoni 🍕 : tomato sauce, mozzarella, pepperoni\n"
        "— Hawaiian 🍍 : tomato sauce, mozzarella, chicken, pineapples"
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
    - pizza_bake_time, pizza_delivery_time и pizza_pickup_time
      определяют время готовки, доставки, самовывоза
    - При задании размера XL пицца готовится на 2 сек дольше
    - Рецепт пиццы передается в формате: название пиццы, список ингридиентов
    """

    name: str
    size: str
    emoji: str
    recipe: Recipe
    recipe_list: list

    pizza_bake_time = randint(1, 5)
    pizza_delivery_time = randint(1, 4)
    pizza_pickup_time = randint(1, 4)

    def __init__(self, size="L") -> None:
        self.size = size
        if size == "XL":
            self.pizza_bake_time += 2
        name = type(self).__name__ + " {}".format(self.emoji)
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


@log("👨‍🍳 Приготовили за {}с!")
def pizza_bake(pizza: Pizza):
    """Готовит пиццу"""
    pass


@log("🛵 Доставили за {}с!")
def pizza_delivery(pizza: Pizza):
    """Доставляет пиццу"""
    pass


@log("🏠 Забрали за {}с!")
def pizza_pickup(pizza: Pizza):
    """Самовывоз"""
    pass


@cli.command()
@optgroup.group("Mutally exclusive flags", cls=MutuallyExclusiveOptionGroup)
@optgroup.option("--delivery", default=False, is_flag=True)
@optgroup.option("--pickup", default=False, is_flag=True)
@click.argument("pizza", nargs=1)
def order(pizza: Union[str, Pizza], delivery: bool, pickup: bool):
    """Готовит и доставляет пиццу"""
    if isinstance(pizza, str):
        pizza_obj = str_to_class(pizza.title())
        if not pizza_obj:
            return
    else:
        pizza_obj = pizza
    pizza_bake(pizza_obj)
    if delivery:
        pizza_delivery(pizza_obj)
    if pickup:
        pizza_pickup(pizza_obj)


if __name__ == "__main__":
    cli()
