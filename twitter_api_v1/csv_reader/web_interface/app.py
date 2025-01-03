from flask import Flask, request, render_template, jsonify
import pandas as pd

app = Flask(__name__)

# Переменная для хранения словаря из формы "Text Processing"
text_dict = {}

# Главная страница с вкладками для обработки текста и загрузки файла CSV
@app.route('/')
def index():
    return render_template('index.html')

# Обработка текста из формы
@app.route('/process_text', methods=['POST'])
def process_text():
    global text_dict
    text = request.form.get('text', '')

    if not text.strip():
        return jsonify({"error": "Input text is empty!"}), 400

    # Удаляем запятые и преобразуем текст в словарь
    try:
        new_text = text.replace(",", "")
        text_dict = {}
        for line in new_text.strip().split("\n"):
            if line.strip():
                key, value = line.split(":", 1)
                key = key.strip().strip('"')  # Удаляем пробелы и кавычки
                value = float(value.strip())  # Преобразуем значение в float
                text_dict[key] = value
    except Exception as e:
        return jsonify({"error": f"Failed to process text. Error: {str(e)}"}), 400

    return jsonify(text_dict)

# Обработка данных после загрузки файла CSV
@app.route('/process_csv', methods=['POST'])
def process_data():
    global text_dict
    # Загружаем файл CSV из запроса
    file = request.files['file']
    if not file:
        return jsonify({'error': 'Файл не загружен'}), 400

    # Читаем файл в DataFrame
    df = pd.read_csv(file, sep='\t', encoding='cp1251')
    data_dict = df.to_dict(orient='records')  # Преобразуем DataFrame в список словарей

    if not text_dict:
        return jsonify({'error': 'Сначала загрузите и обработайте текст!'}), 400

    # Получаем ключи (темы), которые нужно обработать из text_dict
    themes_to_process = set(text_dict.keys())  # Ключи из словаря, полученного в "Text Processing"

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

    # Формируем результат, используя text_dict вместо examples
    output = {}
    for theme in themes_to_process:
        if theme in data_theme_values:
            value = data_theme_values[theme]["value"]
        else:
            value = text_dict.get(theme, "Не найдено")  # Используем значение из text_dict

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
