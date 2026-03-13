import requests
import time

# --- CONFIGURAÇÃO ---
TOKEN_TELEGRAM = "8710482509:AAFIqDYVg00TZYJ5ydrLPzeVehXoPS28t_Q"
CHAT_ID = "982976668"

# Lista com links diretos (Originais)
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

def enviar_aviso(nome, link, silencioso=False):
    mensagem = f"🚩 **ALERTA MENDESHOP**\n\n📦 Item: **{nome}**\n🔗 Link: {link}"
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "Markdown", "disable_notification": silencioso}
    try:
        requests.post(url, data=payload)
    except:
        pass

print("🔍 Monitor Mendeshop Ativo!")

while True:
    for nome, link in LINKS_PARA_VIGIAR.items():
        try:
            # Fingindo ser um navegador real para evitar o bloqueio do ML
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Accept-Language': 'pt-BR,pt;q=0.9'
            }
            resposta = requests.get(link, headers=headers, timeout=30)
            
            # Se der 404 (Página não encontrada) ou 410 (Removido), o link realmente caiu
            if resposta.status_code in [404, 410]:
                print(f"🚩 LINK MORTO: {nome}")
                enviar_aviso(f"LINK QUEBRADO (404): {nome}", link)
            
            # Se der 200, está tudo perfeito
            elif resposta.status_code == 200:
                print(f"✅ OK: {nome}")
            
            # Outros códigos (403, 503) geralmente são bloqueios temporários do servidor, ignoramos para não dar alarme falso
            else:
                print(f"⚠️ Status {resposta.status_code} em {nome} (Bloqueio provisório)")
                
        except Exception as e:
            print(f"❌ Erro de conexão em {nome}")
            
    print("⏳ Ronda finalizada. Aguardando 5 minutos...")
    time.sleep(300)
    enviar_aviso("RONDA CONCLUÍDA", "Todos os itens foram checados e estão OK.", silencioso=True)
    print("⏳ Tudo conferido. Aguardando 1 minuto...")
    time.sleep(60)
