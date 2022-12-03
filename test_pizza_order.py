import pytest
from pizza_order import *
from click.testing import CliRunner

PIZZA_OBJ_LIST = [Pepperoni(), Margherita(), Hawaiian()]
PIZZA_FUNCS_LIST = [pizza_pickup, pizza_delivery, pizza_bake]


@pytest.mark.parametrize("test_pizza_obj", PIZZA_OBJ_LIST)
@pytest.mark.parametrize("test_func", PIZZA_FUNCS_LIST)
def test_log_output(capsys, test_pizza_obj, test_func):
    """Тест для всех типов пицц для всех основных методов (кроме order)"""
    function_name = test_func.__name__
    attr_name = function_name + "_time"
    test_func(test_pizza_obj)
    captured = capsys.readouterr()
    match function_name:
        case "pizza_pickup":
            expected_out = "🏠 Забрали за {}с!"
        case "pizza_delivery":
            expected_out = "🛵 Доставили за {}с!"
        case "pizza_bake":
            expected_out = "👨‍🍳 Приготовили за {}с!"
    expected_str = expected_out.format(getattr(test_pizza_obj, attr_name))

    assert captured.out.startswith(expected_str)


@pytest.mark.parametrize("test_pizza_obj", PIZZA_OBJ_LIST)
def test_dict_result(test_pizza_obj):
    """Тест для проверки результата метода __dict__ для рецепта пиццы"""
    match test_pizza_obj:
        case Pepperoni():
            expected_res = {
                "pizza_name": "Pepperoni 🍕",
                "recipe_list": ["tomato sauce",
                                "mozzarella",
                                "pepperoni"],
            }
        case Margherita():
            expected_res = {
                "pizza_name": "Margherita 🧀",
                "recipe_list": ["tomato sauce",
                                "mozzarella",
                                "tomatoes"],
            }
        case Hawaiian():
            expected_res = {
                "pizza_name": "Hawaiian 🍍",
                "recipe_list": ["tomato sauce",
                                "mozzarella",
                                "chicken",
                                "pineapples"],
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
        large_pizza_time += test_pizza_obj.pizza_bake_time
        extra_large_pizza_time += test_pizza_obj_big.pizza_bake_time

    assert extra_large_pizza_time / OBJ_NUM > large_pizza_time / OBJ_NUM


@pytest.mark.parametrize("test_pizza_obj", ["pepperoni", "margherita", "hawaiian"])
def test_order_output(test_pizza_obj):
    """Тест для всех типов пицц метода order"""
    runner = CliRunner()
    expected_out = "👨‍🍳 Приготовили за {}с!"

    result = runner.invoke(order, [test_pizza_obj])
    test_pizza_obj = str_to_class(test_pizza_obj)
    expected_str = expected_out.format(test_pizza_obj.pizza_bake_time)
    assert result.exit_code == 0
    assert expected_str in result.output  # check what function prints


@pytest.mark.parametrize("test_pizza_obj", ["pepperoni", "margherita", "hawaiian"])
def test_order_output_with_delivery(test_pizza_obj):
    """Тест для всех типов пицц метода order c флагом --delivery"""
    runner = CliRunner()
    expected_out = "👨‍🍳 Приготовили за {}с!"
    expected_delivery_out = "🛵 Доставили за {}с!"

    result = runner.invoke(order, [test_pizza_obj, "--delivery"])
    test_pizza_obj = str_to_class(test_pizza_obj)
    expected_str = expected_out.format(test_pizza_obj.pizza_bake_time)
    assert result.exit_code == 0
    assert expected_str in result.output
    assert (
        expected_delivery_out.format(test_pizza_obj.pizza_delivery_time)
        in result.output
    ), "No delivery data in output{}: ".format(result.output)


@pytest.mark.parametrize("test_pizza_obj", ["pepperoni", "margherita", "hawaiian"])
def test_order_output_with_pickup(test_pizza_obj):
    """Тест для всех типов пицц для метода order с флагом --pickup"""
    runner = CliRunner()
    expected_out = "👨‍🍳 Приготовили за {}с!"
    expected_pickup_out = "🏠 Забрали за {}с!"

    result = runner.invoke(order, [test_pizza_obj, "--pickup"])
    test_pizza_obj = str_to_class(test_pizza_obj)
    expected_str = expected_out.format(test_pizza_obj.pizza_bake_time)
    assert result.exit_code == 0
    assert expected_str in result.output
    assert (
        expected_pickup_out.format(test_pizza_obj.pizza_pickup_time) in result.output
    ), "No pickup data in output{}: ".format(result.output)
