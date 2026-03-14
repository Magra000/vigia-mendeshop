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

# Links para o Robô vigiar e gerar posts
LINKS_PARA_VIGIAR = {
    "Projetor 4k Magcubic": "https://www.mercadolivre.com.br/projetor-magcubic-hy320-android-11-4k-780-ansi-wifi-6-bt50/p/MLB1039420015",
    "Samsung Galaxy A56": "https://www.mercadolivre.com.br/samsung-galaxy-a56-5g-256gb-8gb-ram/p/MLB1039433241",
    "Console PlayStation 5": "https://www.mercadolivre.com.br/console-playstation-5-sony-ps5-825gb-standard-cor-branco-e-preto/p/MLB16157155"
}

# --- SERVIDOR PARA MANTER O RENDER VIVO ---
def run_dummy_server():
    server_address = ('', 10000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()

# --- GERADOR DE IMAGEM (CARD MENDESSHOP) ---
def gerar_card_visual(url_foto, nome, preco):
    try:
        # 1. Fundo Rosa MendesShop
        fundo = Image.new('RGB', (1080, 1080), color=(255, 20, 147))
        draw = ImageDraw.Draw(fundo)

        # 2. Baixar e colar a foto do produto
        res = requests.get(url_foto, timeout=20)
        img_prod = Image.open(BytesIO(res.content)).convert("RGBA")
        img_prod = img_prod.resize((750, 750))
        fundo.paste(img_prod, (165, 80), img_prod)

        # 3. Rodapé Branco para o Texto
        draw.rectangle([0, 850, 1080, 1080], fill="white")
        
        # 4. Selo OFERTA RELÂMPAGO
        draw.ellipse([820, 30, 1050, 260], fill="yellow", outline="black")
        draw.text((850, 110), "OFERTA\n⚡️AGORA", fill="black")

        # 5. Nome e Marca
        draw.text((50, 870), "MendesShop - OFERTA DO DIA", fill=(255, 20, 147))
        draw.text((50, 930), f"{nome[:30]}...", fill="black")
        draw.text((50, 980), f"R$ {preco}", fill=(255, 20, 147))

        bio = BytesIO()
        fundo.save(bio, 'PNG')
        bio.seek(0)
        return bio
    except Exception as e:
        print(f"Erro ao criar card: {e}")
        return None

# --- ENVIO PARA TELEGRAM ---
def enviar_ao_telegram(imagem_bio, legenda):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendPhoto"
    files = {'photo': ('post.png', imagem_bio, 'image/png')}
    data = {'chat_id': CHAT_ID, 'caption': legenda, 'parse_mode': 'Markdown'}
    requests.post(url, files=files, data=data)

# --- INICIALIZAÇÃO ---
threading.Thread(target=run_dummy_server, daemon=True).start()

print("🚀 MendesShop Engine: VISUAL ATIVO!")

while True:
    agora = datetime.now().strftime("%H:%M")
    print(f"📸 Iniciando ronda de fotos às {agora}")

    for nome, link in LINKS_PARA_VIGIAR.items():
        # Foto de teste (No futuro o robô pega a do link automaticamente)
        foto_exemplo = "https://m.media-amazon.com/images/I/518v96f-pHL._AC_SL1000_.jpg"
        
        card = gerar_card_visual(foto_exemplo, nome, "CONSULTAR VALOR")
        
        if card:
            legenda = f"💎 **ACHADINHO MENDESSHOP**\n\n🔥 {nome}\n\n✅ Link direto na Bio ou nos Comentários!\n🚀 Siga para mais ofertas."
            enviar_ao_telegram(card, legenda)
            print(f"✅ Post enviado: {nome}")
        
        time.sleep(15) # Pausa para o Render não travar

    print("⏳ Tudo enviado! Próxima ronda em 1 hora.")
    time.sleep(3600)
