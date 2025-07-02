import requests

def obter_localizacao_por_ip(ip):
    try:
        resposta = requests.get(f"https://ipapi.co/{ip}/json/")
        if resposta.status_code == 200:
            return resposta.json()
        return None
    except Exception as e:
        print("Erro ao buscar localização:", e)
        return None
