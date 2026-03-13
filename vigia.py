import requests
import time

# --- CONFIGURAÇÃO ---
TOKEN_TELEGRAM = "8710482509:AAFIqDYVg00TZYJ5ydrLPzeVehXoPS28t_Q"
CHAT_ID = "982976668"

# Lista completa da Mendeshop
LINKS_PARA_VIGIAR = {
    "Lápis de Cor - ML": "https://tinyurl.com/mendes-lapis",
    "Samsung A56": "https://tinyurl.com/mendes-samsung-a56",
    "Ventilador de mesa 40cm": "https://tinyurl.com/mendes-vent-mesa",
    "Projetor 4k": "https://tinyurl.com/mendes-projetor-4k",
    "Ventilador coluna 40cm": "https://tinyurl.com/mendes-vent-coluna",
    "Play 5": "https://tinyurl.com/mendes-ps5",
    "Echo Dot 5": "https://tinyurl.com/mendes-alexa-5",
    "Wave Buds 2 Branco": "https://tinyurl.com/mendes-buds-branco",
    "Caixa Waiua": "https://tinyurl.com/mendes-caixa-waiua",
    "Wave Buds 2 Preto": "https://tinyurl.com/mendes-buds-preto",
    "Boombox 4": "https://tinyurl.com/mendes-boombox-4",
    "Parafusadeira Black Tools": "https://tinyurl.com/mendes-parafusadeira",
    "Motorola Moto G15": "https://tinyurl.com/mendes-moto-g15",
    "Lavadora Vonder": "https://tinyurl.com/mendes-lavadora-vonder",
    "Prateleira de Canto": "https://tinyurl.com/mendes-prateleira",
    "Espelho Sala de Estar": "https://tinyurl.com/mendes-espelho",
    "Gloss Franciny Chaveiro": "https://tinyurl.com/mendes-gloss-chaveiro",
    "Teste Visualização Gloss": "https://tinyurl.com/mendes-teste-gloss"
}

def enviar_aviso(nome, link, silencioso=False):
    mensagem = f"🚩 **STATUS MENDESHOP**\n\n📦 Item: **{nome}**\n🔗 Link: {link}"
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensagem,
        "parse_mode": "Markdown",
        "disable_notification": silencioso
    }
    try:
        requests.post(url, data=payload)
    except:
        print("Erro no Telegram.")

print("🔍 Monitor Mendeshop Ativo!")

while True:
    for nome, link in LINKS_PARA_VIGIAR.items():
        try:
            # Engana o bloqueio fingindo ser um navegador real
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            # 'allow_redirects=True' resolve o problema do link cair no TinyURL
            resposta = requests.get(link, headers=headers, timeout=30, allow_redirects=True)
            
            if resposta.status_code == 200:
                print(f"✅ OK: {nome}")
            else:
                print(f"🚩 Status {resposta.status_code} em: {nome}")
                enviar_aviso(f"CAIU: {nome}", link)
        except:
            print(f"❌ Erro de conexão em {nome}")
    
    enviar_aviso("RONDA CONCLUÍDA", "Tudo checado!", silencioso=True)
    time.sleep(120) # Espera 2 minutos para evitar novos bloqueios
    
    enviar_aviso("RONDA CONCLUÍDA", "Todos os itens foram checados e estão OK.", silencioso=True)
    print("⏳ Tudo conferido. Aguardando 1 minuto...")
    time.sleep(60)
