from flask import Flask


app = Flask(__name__) # inicio o flask

@app.route('/') # Isso é o decorator, ele é usado para mapear a função abaixo para a rota '/'
def ola_mundo():
    return 'Olá, Mundo!' # Isso é o que será retornado quando a rota '/' for acessada

@app.route('/decorator') # Isso é outro decorator, mapeando a função abaixo para a rota '/hello'
def decorator():
   return "<h1>Decorator</h1><p>O que e: Um padrao que modifica o comportamento de uma funcao sem mudar seu codigo.</p><p>Para que serve: Adicionar funcoes extras e reutilizar codigo.</p><p>No Flask: O @app.route conecta uma URL a uma funcao.</p>" \

if __name__ == '__main__':
    app.run(debug=True) # Isso inicia o servidor Flask em modo de depuração, o que é útil para desenvolvimento
