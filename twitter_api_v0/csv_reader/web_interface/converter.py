from flask import Flask, request, render_template, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('converter_index.html')


@app.route('/process', methods=['POST'])
def process_text():
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


if __name__ == '__main__':
    app.run(debug=True)
