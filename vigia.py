import requests
import time
from datetime import datetime

# --- CONFIGURAÇÃO (Verifique se os números estão exatos) ---
TOKEN_TELEGRAM = "8710482509:AAFIqDYVg00TZYJ5ydrLPzeVehXoPS28t_Q"
CHAT_ID = "982976668"

def testar_envio():
    print("🚀 Iniciando teste de envio...")
    
    # 1. Teste de Texto
    url_texto = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": "🔔 TESTE MENDESSHOP: O robô está online!"}
    
    try:
        r = requests.post(url_texto, data=payload)
        print(f"Status Texto: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"Erro no envio de texto: {e}")

    # 2. Teste de Imagem (Link direto da internet)
    url_foto = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendPhoto"
    foto_url = "https://m.media-amazon.com/images/I/518v96f-pHL._AC_SL1000_.jpg"
    
    try:
        r = requests.post(url_foto, data={"chat_id": CHAT_ID, "photo": foto_url, "caption": "🖼️ Teste de Imagem MendesShop"})
        print(f"Status Foto: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"Erro no envio de foto: {e}")

# Executa o teste
testar_envio()

# Mantém o script vivo para o Render não fechar
while True:
    print(f"Vigia ativo em {datetime.now()}")
    time.sleep(60)
