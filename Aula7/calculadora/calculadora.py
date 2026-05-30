import math

from flask import render_template, request


def calcular():
    num1 = float(request.form["num1"])
    operacao = request.form["operacao"]

    if operacao == "sqrt":

        if num1 < 0:
            resultado = "Erro"
            etapas = f"Não existe raiz real de {num1}"

        else:
            resultado = math.sqrt(num1)
            etapas = f"√{num1} = {resultado}"

    elif operacao == "bhaskara":

        a = float(request.form["a"])
        b = float(request.form["b"])
        c = float(request.form["c"])

        delta = b**2 - 4*a*c

        if delta < 0:
            resultado = "Sem raízes reais"
            etapas = f"Δ = {delta}"

        else:
            x1 = (-b + math.sqrt(delta)) / (2*a)
            x2 = (-b - math.sqrt(delta)) / (2*a)

            resultado = f"x1 = {x1}, x2 = {x2}"

            etapas = (
                f"Δ = {delta}<br>"
                f"x1 = {x1}<br>"
                f"x2 = {x2}"
            )

    else:

        num2_valor = request.form.get("num2", "").strip()

        if not num2_valor:
            return render_template(
                "calculadora.html",
                etapas="Informe o segundo número",
                resultados=""
            )

        num2 = float(num2_valor)

        if operacao == "+":
            resultado = num1 + num2
            etapas = f"{num1} + {num2} = {resultado}"

        elif operacao == "-":
            resultado = num1 - num2
            etapas = f"{num1} - {num2} = {resultado}"

        elif operacao == "*":
            resultado = num1 * num2
            etapas = f"{num1} * {num2} = {resultado}"

        elif operacao == "/":

            if num2 == 0:
                resultado = ""
                etapas = "Erro: divisão por zero"

            else:
                resultado = num1 / num2
                etapas = f"{num1} / {num2} = {resultado}"

        elif operacao == "**":
            resultado = num1 ** num2
            etapas = f"{num1} ^ {num2} = {resultado}"

    return render_template(
        "calculadora.html",
        etapas=etapas,
        resultados=resultado
    )