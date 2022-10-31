from unittest import expectedFailure
from pizza_order import *
import builtins
import pytest
from unittest.mock import Mock
import contextlib, io


@pytest.mark.parametrize("test_pizza_obj", [Pepperoni(), Margherita(), Hawaiian()])
@pytest.mark.parametrize("test_func", [pickup_, delivery_, bake_])
def test_log_output(test_pizza_obj, test_func):
    """Тест для всех типов пицц для всех основных методов"""
    mock = Mock()
    mock.side_effect = print  # ensure actual print is called to capture its txt
    print_original = print
    builtins.print = mock
    expected_out = ""
    try:
        str_io = io.StringIO()
        with contextlib.redirect_stdout(str_io):
            test_func(test_pizza_obj)
        output = str_io.getvalue()
        match test_func.__name__:
            case "pickup_":
                expected_out = "🏠 Забрали за {}с!"
            case "delivery_":
                expected_out = "🛵 Доставили за {}с!"
            case "bake_":
                expected_out = "󰳏 Приготовили за {}с!"
        expected_str = expected_out.format(test_pizza_obj.pickup_time)
        assert print.called  # `called` is a Mock attribute
        assert output.startswith(expected_str)  # check what function prints
    finally:
        builtins.print = print_original  # ensure print is "unmocked"


@pytest.mark.parametrize("test_pizza_obj", [Pepperoni(), Margherita(), Hawaiian()])
def test_dict_result(test_pizza_obj):
    """Тест для проверки результата метода __dict__ для рецепта пиццы"""
    match test_pizza_obj:
        case Pepperoni():
            expected_res = {
                "pizza_name": "Pepperoni 🍕",
                "recipe_list": ["tomato sauce", "mozzarella", "pepperoni"],
            }
        case Margherita():
            expected_res = {
                "pizza_name": "Margherita 🧀",
                "recipe_list": ["tomato sauce", "mozzarella", "tomatoes"],
            }
        case Hawaiian():
            expected_res = {
                "pizza_name": "Hawaiian 🍍",
                "recipe_list": ["tomato sauce", "mozzarella", "chicken", "pineapples"],
            }
    assert test_pizza_obj.recipe.__dict__ == expected_res


@pytest.mark.parametrize(
    "test_pizza_obj, test_pizza_obj_big",
    [
        (Pepperoni(), Pepperoni(size="XL")),
        (Margherita(), Margherita(size="XL")),
        (Hawaiian(), Hawaiian(size="XL")),
    ],
)
def test_avg_time(test_pizza_obj, test_pizza_obj_big):
    """Тест для проверки среднего времени готовки пиццы в зависимости от размера"""
    OBJ_NUM = 50

    large_pizza_time = 0
    extra_large_pizza_time = 0
    for _ in range(OBJ_NUM):
        large_pizza_time += test_pizza_obj.bake_time
        extra_large_pizza_time += test_pizza_obj_big.bake_time

    assert extra_large_pizza_time / OBJ_NUM > large_pizza_time / OBJ_NUM


@pytest.mark.parametrize("test_pizza_obj", [Pepperoni(), Margherita(), Hawaiian()])
@pytest.mark.parametrize("delivery", [True, False])
@pytest.mark.parametrize("pickup", [True, False])
def test_order_output(test_pizza_obj):
    """Тест для всех типов пицц для всех метода order"""
    mock = Mock()
    mock.side_effect = print  # ensure actual print is called to capture its txt
    print_original = print
    builtins.print = mock
    expected_out = ""
    try:
        str_io = io.StringIO()
        with contextlib.redirect_stdout(str_io):
            order(test_pizza_obj)
        output = str_io.getvalue()

        expected_str = expected_out.format(test_pizza_obj.bake_time)
        assert print.called  # `called` is a Mock attribute
        assert output.startswith(expected_str)  # check what function prints
    finally:
        builtins.print = print_original  # ensure print is "unmocked"
