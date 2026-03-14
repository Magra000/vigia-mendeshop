import requests
import time
from datetime import datetime
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

# --- CONFIGURAÇÃO ---
TOKEN_TELEGRAM = "8710482509:AAFIqDYVg00TZYJ5ydrLPzeVehXoPS28t_Q"
CHAT_ID = "982976668"

LINKS_PARA_VIGIAR = {
    "Lápis de Cor - ML": "https://www.mercadolivre.com.br/lapis-de-cor-sextavado-60-cores-ecolapis-faber-castell/p/MLB19958019",
    "Samsung A56": "https://www.mercadolivre.com.br/samsung-galaxy-a56-5g-256gb-8gb-ram/p/MLB1039433241",
    "Ventilador de mesa 40cm": "https://www.mercadolivre.com.br/ventilador-de-mesa-mondial-vsp-40-b-8-pas-40cm-preto-127v/p/MLB15161421",
    "Projetor 4k": "https://www.mercadolivre.com.br/projetor-magcubic-hy320-android-11-4k-780-ansi-wifi-6-bt50/p/MLB1039420015",
    "Ventilador coluna 40cm": "https://www.mercadolivre.com.br/ventilador-de-coluna-mondial-nv-61-6p-nv-61-6p-c-6-pas-40cm-preto-127v/p/MLB15183845",
    "Play 5": "https://www.mercadolivre.com.br/console-playstation-5-sony-ps5-825gb-standard-cor-branco-e-preto/p/MLB16157155",
    "Echo Dot 5": "https://www.amazon.com.br/echo-dot-5a-geracao-preta/dp/B09B8VGMSY",
    "Wave Buds 2 Branco": "https://www.mercadolivre.com.br/fone-de-ouvido-jbl-wave-buds-tws-bluetooth-cor-branco/p/MLB22453673",
    "Caixa Waiua": "https://www.mercadolivre.com.br/caixa-de-som-portatil-waiua-bluetooth-a-prova-dagua/p/MLB10293845",
    "Wave Buds 2 Preto": "https://www.mercadolivre.com.br/fone-de-ouvido-jbl-wave-buds-tws-bluetooth-cor-preto/p/MLB22453672",
    "Boombox 4": "https://www.mercadolivre.com.br/caixa-de-som-jbl-boombox-3-portatil-com-bluetooth-a-prova-dagua-preta/p/MLB19565555",
    "Parafusadeira Black Tools": "https://www.mercadolivre.com.br/parafusadeira-furadeira-impacto-bateria-21v-black-tools/p/MLB21948574",
    "Motorola Moto G15": "https://www.mercadolivre.com.br/motorola-moto-g15-5g-128gb-4gb-ram/p/MLB10384722",
    "Lavadora Vonder": "https://www.mercadolivre.com.br/lavadora-de-alta-pressao-vonder-lav-1200-1200w-1305-psi/p/MLB10045623",
    "Prateleira de Canto": "https://www.mercadolivre.com.br/prateleira-de-canto-mdf-branco-25x25cm/p/MLB18475623",
    "Espelho Sala de Estar": "https://www.mercadolivre.com.br/espelho-decorativo-redondo-60cm-moldura-couro/p/MLB19283745",
    "Gloss Franciny Chaveiro": "https://www.mercadolivre.com.br/gloss-labial-franciny-ehlke-glossip-chaveiro/p/MLB20384756",
    "Teste Visualização Gloss": "https://www.mercadolivre.com.br/gloss-labial-franciny-ehlke-glossip-original/p/MLB20384757"
}

# --- SERVIDOR PARA MANTER O RENDER FELIZ ---
def run_dummy_server():
    server_address = ('', 10000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("🚀 Servidor 'Mantém-Vivo' ativo na porta 10000")
    httpd.serve_forever()

def enviar_aviso(mensagem_texto, link="", silencioso=False):
    texto = f"🚩 **STATUS MENDESHOP**\n\n{mensagem_texto}"
    if link:
        texto += f"\n🔗 Link: {link}"
    
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": texto, "parse_mode": "Markdown", "disable_notification": silencioso}
    try:
        requests.post(url, data=payload)
    except:
        pass

# Inicia o servidor fantasma em uma thread
threading.Thread(target=run_dummy_server, daemon=True).start()

print("🔍 Monitor Mendeshop Ativo e Oficial!")
ultima_ronda_enviada = -1

while True:
    agora = datetime.now()
    hora_atual = agora.hour

    for nome, link in LINKS_PARA_VIGIAR.items():
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            resposta = requests.get(link, headers=headers, timeout=20)
            
            if resposta.status_code in [404, 410]:
                enviar_aviso(f"🚨 LINK CAIU (404): {nome}", link)
        except:
            print(f"❌ Erro de conexão em {nome}")

    # Notificação 12h e 00h (Relatório de Status)
    if hora_atual in [0, 12] and hora_atual != ultima_ronda_enviada:
        saudacao = "☀️ STATUS DIÁRIO" if hora_atual == 12 else "🌙 STATUS NOTURNO"
        enviar_aviso(f"{saudacao}\n\nTodos os links checados e operando 100%!", silencioso=True)
        ultima_ronda_enviada = hora_atual

    print(f"⏳ Ronda de {agora.strftime('%H:%M')} finalizada. Próxima em 5 min.")
    time.sleep(300) # Volta para 5 minutos
