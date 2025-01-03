import pandas as pd
import examples

# Указать правильную кодировку для файла
df = pd.read_csv('DataExport_2024-12-27_16-13-15.csv', sep='\t', encoding='cp1251')

# Преобразование данных в список словарей
data_dict = df.to_dict(orient='records')

# Получаем словарь из модуля examples
issues_dict = examples.issues_dict

# Темы, которые нужно обработать
themes_to_process = set(issues_dict.keys())

# Преобразуем data_dict в словарь для быстрого поиска
data_theme_values = {}
for items in data_dict:
    theme = items.get("theme,value", "")
    if theme:
        theme_parts = theme.split(",")
        if len(theme_parts) >= 3:
            data_theme_values[theme_parts[0]] = f"{theme_parts[1][1]}.{theme_parts[2][0:2]}"

# Итоговый вывод
for theme in themes_to_process:
    if theme in data_theme_values:
        # print(theme)
        # Используем значение из data_dict
        value = data_theme_values[theme]
    else:
        # Используем значение из issues_dict
        value = issues_dict[theme]
    print(f'        "{theme}": {value},')

print('        "default": 0.00')

print("")


print("Was changed:")
for theme in themes_to_process:
    if theme in data_theme_values:
        print(theme)