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
        print("Erro ao enviar para o Telegram.")

print("🔍 Monitor Mendeshop Ativo!")

while True:
    for nome, link in LINKS_PARA_VIGIAR.items():
        try:
            # Identificação de navegador real para evitar bloqueios
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
            }
            # allow_redirects=True é fundamental para links encurtados (tinyurl)
            resposta = requests.get(link, headers=headers, timeout=30, allow_redirects=True)
            
            if resposta.status_code != 200:
                print(f"🚩 Status {resposta.status_code} em: {nome}")
                enviar_aviso(f"VERIFICAR: {nome}", link, silencioso=False)
            else:
                print(f"✅ OK: {nome}")
        except Exception as e:
            print(f"❌ Erro de Conexão em {nome}")
            
    # Mensagem de ronda concluída (silenciosa)
    enviar_aviso("RONDA CONCLUÍDA", "Todos os links verificados.", silencioso=True)
    
    print("⏳ Tudo conferido. Aguardando 2 minutos...")
    time.sleep(120) # Intervalo de 2 minutos para não sobrecarregar
    
    enviar_aviso("RONDA CONCLUÍDA", "Todos os itens foram checados e estão OK.", silencioso=True)
    print("⏳ Tudo conferido. Aguardando 1 minuto...")
    time.sleep(60)
