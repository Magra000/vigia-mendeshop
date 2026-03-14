import requests
import time
from datetime import datetime
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

# --- CONFIGURAÇÃO ---
TOKEN_TELEGRAM = "8710482509:AAFIqDYVg00TZYJ5ydrLPzeVehXoPS28t_Q"
CHAT_ID = "982976668"

# Função para enganar o Render (Servidor Fantasma)
def run_dummy_server():
    server_address = ('', 10000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("🚀 Servidor de suporte ativo na porta 10000")
    httpd.serve_forever()

def testar_envio():
    print("🚀 Iniciando teste de envio...")
    url_texto = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": "🔔 MENDESSHOP: Teste de Conexão OK!"}
    
    try:
        r = requests.post(url_texto, data=payload)
        print(f"Status: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"Erro: {e}")

# Inicia o servidor em segundo plano para o Render ficar feliz
threading.Thread(target=run_dummy_server, daemon=True).start()

# Executa o teste de envio
testar_envio()

# Mantém o script vivo
while True:
    print(f"Vigia ativo - {datetime.now().strftime('%H:%M:%S')}")
    time.sleep(60)
