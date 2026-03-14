import requests
import time
from datetime import datetime
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import re

# --- CONFIGURAÇÃO ---
TOKEN_TELEGRAM = "8710482509:AAFIqDYVg00TZYJ5ydrLPzeVehXoPS28t_Q"
CHAT_ID = "982976668"

LINKS_PARA_VIGIAR = {
    "Projetor 4k Magcubic": "https://www.mercadolivre.com.br/projetor-magcubic-hy320-android-11-4k-780-ansi-wifi-6-bt50/p/MLB1039420015",
    "Samsung Galaxy A56": "https://www.mercadolivre.com.br/samsung-galaxy-a56-5g-256gb-8gb-ram/p/MLB1039433241"
}

def run_dummy_server():
    server_address = ('', 10000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()

def gerar_card_visual(url_foto, nome, preco):
    try:
        print(f"🎨 Desenhando card para: {nome}")
        fundo = Image.new('RGB', (1080, 1080), color=(255, 20, 147))
        draw = ImageDraw.Draw(fundo)

        # Download da foto com User-Agent para não ser bloqueado
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url_foto, headers=headers, timeout=20)
        img_prod = Image.open(BytesIO(res.content)).convert("RGBA")
        img_prod = img_prod.resize((750, 750))
        fundo.paste(img_prod, (165, 80), img_prod)

        draw.rectangle([0, 850, 1080, 1080], fill="white")
        draw.ellipse([820, 30, 1050, 260], fill="yellow", outline="black")
        draw.text((850, 110), "OFERTA\n⚡️AGORA", fill="black")

        draw.text((50, 870), "MendesShop - OFERTA DO DIA", fill=(255, 20, 147))
        draw.text((50, 930), f"{nome[:30]}...", fill="black")
        draw.text((50, 980), f"PRECO: {preco}", fill=(255, 20, 147))

        bio = BytesIO()
        fundo.save(bio, 'PNG')
        bio.seek(0)
        return bio
    except Exception as e:
        print(f"❌ Erro ao criar card: {e}")
        return None

def enviar_ao_telegram(imagem_bio, legenda):
    try:
        url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendPhoto"
        files = {'photo': ('post.png', imagem_bio, 'image/png')}
        data = {'chat_id': CHAT_ID, 'caption': legenda, 'parse_mode': 'Markdown'}
        r = requests.post(url, files=files, data=data)
        print(f"📤 Status Envio: {r.status_code}")
    except Exception as e:
        print(f"❌ Erro no POST do Telegram: {e}")

threading.Thread(target=run_dummy_server, daemon=True).start()

print("🚀 MendesShop Engine Iniciada!")

while True:
    for nome, link in LINKS_PARA_VIGIAR.items():
        print(f"🧐 Processando: {nome}")
        
        # Foto padrão de segurança caso a busca falhe
        foto_url = "https://http2.mlstatic.com/D_NQ_NP_612735-MLA74320499251_022024-O.webp"
        
        card = gerar_card_visual(foto_url, nome, "VER NA LOJA")
        
        if card:
            legenda = f"💎 **ACHADINHO MENDESSHOP**\n\n🔥 {nome}\n\n✅ Link na Bio!\n🚀 Siga para mais."
            enviar_ao_telegram(card, legenda)
        
        time.sleep(10)

    print("⏳ Aguardando 1 hora...")
    time.sleep(3600)
