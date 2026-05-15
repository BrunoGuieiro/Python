from flask import Flask

app = Flask(__name__)

@app.route('/')
def curriculo():
    return """
    <!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Currículo - Bruno Guieiro Lessa</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 20px auto;
            padding: 20px;
            border: 1px solid #eee;
            border-radius: 8px;
            background-color: #f9f9f9;
        }
        h1 {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 5px;
        }
        .contact-info {
            text-align: center;
            font-size: 0.9em;
            color: #7f8c8d;
            margin-bottom: 20px;
        }
        h2 {
            border-bottom: 2px solid #3498db;
            color: #3498db;
            padding-bottom: 5px;
            margin-top: 25px;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            margin-bottom: 8px;
        }
        strong {
            color: #2c3e50;
        }
    </style>
</head>
<body>

    <h1>Bruno Guieiro Lessa</h1>
    <p class="contact-info">
        lessabrunoguieiro@gmail.com | (31) 997836247
    </p>

    <h2>Formação Tecnica</h2>
    <ul>
        <li><strong>Colégio Cotemig:</strong> Ensino Médio Técnico</li>
        <li><strong>Cargo:</strong> Estudante</li>
        <li><strong>Período:</strong> Jan 2024 - Presente</li>
    </ul>

</body>
</html>
    """

if __name__ == '__main__':
    # Executa a aplicação
    app.run(debug=True)