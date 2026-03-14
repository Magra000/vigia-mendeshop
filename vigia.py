import requests
import time
from datetime import datetime
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# --- CONFIGURAÇÃO ---
TOKEN_TELEGRAM = "8710482509:AAFIqDYVg00TZYJ5ydrLPzeVehXoPS28t_Q"
CHAT_ID = "982976668"

LINKS_PARA_VIGIAR = {
    "Samsung A56": "https://www.mercadolivre.com.br/samsung-galaxy-a56-5g-256gb-8gb-ram/p/MLB1039433241",
    "Projetor 4k": "https://www.mercadolivre.com.br/projetor-magcubic-hy320-android-11-4k-780-ansi-wifi-6-bt50/p/MLB1039420015",
    "Play 5": "https://www.mercadolivre.com.br/console-playstation-5-sony-ps5-825gb-standard-cor-branco-e-preto/p/MLB16157155",
    "Echo Dot 5": "https://www.amazon.com.br/echo-dot-5a-geracao-preta/dp/B09B8VGMSY",
}

# --- FUNÇÃO PARA CRIAR O CARD VISUAL ---
def gerar_card_mendesshop(url_foto, nome, preco):
    try:
        # 1. Cria o fundo rosa vibrante da MendesShop
        fundo = Image.new('RGB', (1080, 1080), color=(255, 20, 147))
        draw = ImageDraw.Draw(fundo)

        # 2. Tenta baixar a foto do produto
        res = requests.get(url_foto)
        img_prod = Image.open(BytesIO(res.content)).convert("RGBA")
        img_prod = img_prod.resize((700, 700))
        
        # Colar produto (centralizado)
        fundo.paste(img_prod, (190, 100), img_prod)

        # 3. Faixa de preço e textos
        draw.rectangle([0, 820, 1080, 1080], fill="white")
        
        # Selo Oferta Relâmpago (Círculo amarelo no canto)
        draw.ellipse([800, 50, 1030, 280], fill="yellow", outline="black")
        draw.text((825, 120), "OFERTA\n⚡️AGORA", fill="black")

        # Texto MendesShop e Preço
        draw.text((50, 840), "MendesShop - ACHADINHO!", fill=(255, 20, 147))
        draw.text((50, 900), f"{nome[:25]}...", fill="black")
        draw.text((50, 960), f"R$ {preco}", fill=(255, 20, 147))

        # Salvar na memória para enviar
        bio = BytesIO()
        fundo.save(bio, 'PNG')
        bio.seek(0)
        return bio
    except Exception as e:
        print(f"Erro ao criar card: {e}")
        return None

# --- FUNÇÃO ENVIO TELEGRAM (FOTO) ---
def enviar_foto_telegram(bio_imagem, legenda):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendPhoto"
    files = {'photo': ('post.png', bio_imagem, 'image/png')}
    data = {'chat_id': CHAT_ID, 'caption': legenda, 'parse_mode': 'Markdown'}
    requests.post(url, files=files, data=data)

# --- SERVIDOR MANTÉM-VIVO ---
def run_dummy_server():
    server_address = ('', 10000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

print("🔍 MendesShop Engine Ativa!")

while True:
    for nome, link in LINKS_PARA_VIGIAR.items():
        # Simulando uma busca de preço e foto (no futuro pegaremos automático)
        # Por enquanto, ele gera o card para você testar o visual
        print(f"📸 Gerando post para: {nome}")
        
        # URL da foto (O robô precisa da URL direta da imagem)
        # Exemplo genérico para teste:
        foto_teste = "https://a-static.mlcdn.com.br/618x463/projetor-magcubic-hy320-android-11-4k-780-ansi-wifi-6-bt50/magcubic/hy320/004a6e8b7c7c4e5e8e8e8e8e8e8e8e8e.jpg"
        
        card = gerar_card_mendesshop(foto_teste, nome, "VER NA LOJA")
        
        if card:
            legenda = f"💎 **ACHADINHO MENDESSHOP**\n\n🔥 {nome}\n\n✅ Link Seguro nos Comentários!\n🚀 Siga para não perder as ofertas."
            enviar_foto_telegram(card, legenda)
        
        time.sleep(10) # Pausa entre cada geração

    print("⏳ Ronda finalizada. Próxima em 1 hora.")
    time.sleep(3600)
    time.sleep(3600)
