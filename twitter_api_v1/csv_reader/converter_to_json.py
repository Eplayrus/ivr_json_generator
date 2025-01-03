text = """

"Цена клика": 3.22,
"Яндекс.Плюс": 2.33
"""

# Преобразуем текст в словарь
import ast

# Текст можно преобразовать в словарь, если правильно оформить строки
data = ast.literal_eval("{" + text + "}")

# Выводим данные
for issue, score in data.items():
    print(f"               \"{issue}\": {score},")
