import requests

URL_FRASE = "https://api.adviceslip.com/advice"


def buscar_frase():
    try:
        resposta = requests.get(URL_FRASE, timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()
        return dados["slip"]["advice"]
    except Exception:
        return "Foco em uma tarefa por vez. Você consegue!"
