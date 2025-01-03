from flask import Flask, request, render_template, jsonify
import pandas as pd
from csv_reader import examples

app = Flask(__name__)

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Обработка данных после загрузки файла
@app.route('/process', methods=['POST'])
def process_data():
    # Загружаем файл CSV из запроса
    file = request.files['file']
    if not file:
        return jsonify({'error': 'Файл не загружен'}), 400

    # Читаем файл в DataFrame
    df = pd.read_csv(file, sep='\t', encoding='cp1251')
    data_dict = df.to_dict(orient='records')  # Преобразуем DataFrame в список словарей

    # Получаем словарь из модуля examples
    issues_dict = examples.issues_dict
    themes_to_process = set(issues_dict.keys())  # Получаем ключи (темы), которые нужно обработать

    # Преобразуем data_dict в словарь для быстрого поиска
    data_theme_values = {}
    for items in data_dict:
        theme = items.get("theme,value", "")
        if theme:
            theme_parts = theme.split(",")  # Разделяем строку по запятой
            if len(theme_parts) >= 3:
                try:
                    # Форматируем строку как число
                    value = float(f"{theme_parts[1][1]}.{theme_parts[2][0:2]}")
                    data_theme_values[theme_parts[0]] = {"value": value, "is_changed": True}
                except ValueError:
                    # Если не удаётся привести к числу, сохраняем строкой
                    data_theme_values[theme_parts[0]] = {"value": theme_parts[1][1] + "." + theme_parts[2][0:2], "is_changed": True}

    # Формируем результат
    output = {}
    for theme in themes_to_process:
        if theme in data_theme_values:
            value = data_theme_values[theme]["value"]
        else:
            value = issues_dict[theme]

        # Форматируем значение с 15 пробелами перед строкой
        formatted_value = f'               "{value}"' if isinstance(value, str) else f'{value}'
        output[theme] = {
            "value": formatted_value,
            "is_changed": theme in data_theme_values
        }

    # Возвращаем результат
    return jsonify(output)

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)
