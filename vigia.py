import requests
import time

# --- CONFIGURAÇÃO ---
TOKEN_TELEGRAM = "8710482509:AAFIqDYVg00TZYJ5ydrLPzeVehXoPS28t_Q"
CHAT_ID = "982976668"

# Lista completa da Mendeshop (17 itens)
LINKS_PARA_VIGIAR = {
    "Lápis de Cor - ML": "https://www.mercadolivre.com.br/social/mendeshop?matt_word=pinterest&matt_tool=42893323&forceInApp=true&ref=BOiejnazCwnp%2BP5avEqP70ywBWSiSGyjiEzKomhEUsEXePNMcZsEhEV2Hnl0ZFZdb8fmziZr44y8ETGPmN56R8utyp0ypJapZlhtjGNMcUP9LZ1gpF7IpPH8262BBVwTlkxcTHjeAfOqkL5oS2pgX0bGIeAAe4KMHju8ZT6PPKdWFiaGOaXAAwrBcBD%2F%2FiKy6wFXh18%3D",
    "Samsung A56": "https://www.mercadolivre.com.br/social/mendeshop?matt_word=pinterest&matt_tool=42893323&forceInApp=true&ref=BClDSSEgSC7N4CxCB5VNy4E%2BhljPqTyhszvnMjZLnxRN%2FYx01xmYv2gml5wRzJ8w%2Bjw%2BJjZdnxuEbXeculuPpTLLltpBguCItegGhmrZVoAyJ8HGimL3iJT1HwPQj4VN9O28%2Bg%2FFPkWGdRPoKtByynKijH%2Fys1FKicLueUQeLq8oVBVWBbXBwskVFT%2FD6KLbb98G08I%3D",
    "Ventilador de mesa 40cm": "https://www.mercadolivre.com.br/social/mendeshop?matt_word=pinterest&matt_tool=42893323&forceInApp=true&ref=BL0HjrS86kXqoUx1JOxpmMFjtX%2BP74MM6yX%2BfcUyylU9XDk%2FuIFk7g6QxuFV%2Fg2m5qrkP863S1uhf5R3DshbTz1X0bNVsa9BafmizwF33liUgXp7M6sHq8ZJ2UwXSiDVzV30qlFWo6Kx7VyEJzgSqs9dNf6vjkNdQvmnQiBJ0TsWxO%2BK19H7A5cYek8K1jVM8L%2Bba4o%3D",
    "Projetor 4k": "https://www.mercadolivre.com.br/social/mendeshop?matt_word=pinterest&matt_tool=42893323&forceInApp=true&ref=BLIsnRkmlF7MwFUFRBR2DxiDdx2FyipDEej86zUHAE%2FnpWmTOlmM2cd5pUwPe1SnhRexalaa5sV4VL9za%2BYJt8cmt4ExOIPn5LNgW9KX%2BaKYhV0jPxmZgAZUORT2hSM4V%2ByMdhl1RZN5ohaHD15Wo5WOrrq8QNkjQuVQUELSeBGhOVD%2BXEY5qyfX00Zl34kEyAIsvg%3D%3D",
    "Ventilador coluna 40cm": "https://www.mercadolivre.com.br/social/mendeshop?matt_word=pinterest&matt_tool=42893323&forceInApp=true&ref=BGbBrrag0qjINEpHL3xn3OvcMoOrYtqQbff19AfVFoUWHH0hYKwdkx%2FkvmW4JFrnZawZoJstbCjjUWnwoT%2F7x7VVwFT8tswnMBfGLHrD4jubzdrXJRDKfXSojzA3N5Lq1SZJ8CovX8VLI9GjQ3XGvKnkc%2Bf6yf6csSxsZVT7nit1rrzZNPjLdKYmrMFXqzijWrguKNQ%3D",
    "Play 5": "https://www.mercadolivre.com.br/social/mendeshop?matt_word=pinterest&matt_tool=42893323&forceInApp=true&ref=BN5LR2fqwG25j3WUGiyPChMSIfstOncvy9rWlRr4o0gIMaN5TPnkEmW5VdYoqFG4j093RI1qkm4PuCJoF1au1o%2F6qLHPd645Fwu%2BBH0EtJ9Qa5W0TQ%2Fz%2FksWWufdfh4yqTHSf7sOGLD1TmAfpYQLmANnP5GpoDubHOV8rlHXIea29FJWThjn4yDIsWfMChAECbqtkm0%3D",
    "Echo Dot 5": "https://www.mercadolivre.com.br/social/mendeshop?matt_word=pinterest&matt_tool=42893323&forceInApp=true&ref=BHy1bp8F3K287LfZOyaejkYfCy51%2FS%2FBa7wPlQTGlpSF1drQ8ISRh9bNAmvgGKFdcgwF0VZRgLayzNhfgfUkg%2BlHUvWNMx3pBS5mfXdQJZTbEK0NBMh%2BsDzL2B01gsYL4w5bVfyZLNg5qAffCewT3ugk0jB571GxmD9%2BWDGNR2%2F6MS3hOIDLR6GJMRJO2OsZf44niuc%3D",
    "Wave Buds 2 Branco": "https://www.mercadolivre.com.br/social/mendeshop?matt_word=pinterest&matt_tool=42893323&forceInApp=true&ref=BOMwLwGTxdbFxpPh1ChVPAYQ9oP%2BPnYIZkjtue2PB%2FYOPKshn%2Fr7OxZfFc82yNpOEkXz1pm1uT3ajAMkFSF1quAt8B030HrKOYRO9YNcPEJoGbmQqEHAEYknvhCqkWZY%2FFFchA7dfpl2mEXUl%2BXQ5Agh%2F%2Bx1wSn88x1je8fE5GX5SaMAJQoo5D4Vcu%2BL8yTNTGEIINU%3D",
    "Caixa Waiua": "https://www.mercadolivre.com.br/social/mendeshop?matt_word=pinterest&matt_tool=42893323&forceInApp=true&ref=BMnCUzL7ip9Ra%2F1UgP9teBbX46N9Dc4UkDrmR8ju4gDLIC%2Fndh10n2wQ8DBfJa8E9dp3IuDS0n4bFqKFaYYwf2pbLBqxLxcZJJK%2B6x0gF90NisGZ%2BjW0VebM79Zua2lGLoOhgUFleVCPjLdmo9ZWLxeR824La1t4%2FYaTiGfL%2Flg0JOI2bFnuoZXV4UqZ%2BevJPhg7%2FAk%3D",
    "Wave Buds 2 Preto": "https://www.mercadolivre.com.br/social/mendeshop?matt_word=pinterest&matt_tool=42893323&forceInApp=true&ref=BOMwLwGTxdbFxpPh1ChVPAYQ9oP%2BPnYIZkjtue2PB%2FYOPKshn%2Fr7OxZfFc82yNpOEkXz1pm1uT3ajAMkFSF1quAt8B030HrKOYRO9YNcPEJoGbmQqEHAEYknvhCqkWZY%2FFFchA7dfpl2mEXUl%2BXQ5Agh%2F%2Bx1wSn88x1je8fE5GX5SaMAJQoo5D4Vcu%2BL8yTNTGEIINU%3D",
    "Boombox 4": "https://www.mercadolivre.com.br/social/mendeshop?matt_word=pinterest&matt_tool=42893323&forceInApp=true&ref=BPkOKp5ihsvJq0ZX1QMMcuMRQb30JnMMfbkbVUVm8um%2F%2BEoKUkKXqQ2ow7xMQPr1nc6j4xzMtneJjf0kHxQLEHk7AAluQcBsG8MLHRdRk9CG9JZj16Y4JdD%2F0oOUj8qcfX0M%2BSCN14QHX79LYGLmuyWUEzvNVj8BYzhM43dgG%2FuMS8tca5lrS7%2BX53IJtKWMPBUGn%2BY%3D",
    "Parafusadeira Black Tools": "https://www.mercadolivre.com.br/social/mendeshop?matt_word=pinterest&matt_tool=42893323&forceInApp=true&ref=BEZeFXGXlZMKj1jSONNasP7Jyy%2BwS3QqHD9EkG%2BufbiOo26c7txOro7zioeVFHtGNaZQBgowbBf8O97z0K1pAMMdQsq%2Bw%2FL63kB65SPtqV%2F%2B1erc5w28w9x0PXY7cSDAaxOYBWMv2Pp%2BtwOGsSE4KYJKXwQBHlXf0vYh27%2FR7uhCiue5auyO5KOxyUV%2B6Tvc%2B2TjPYI%3D",
    "Motorola Moto G15": "https://www.mercadolivre.com.br/social/mendeshop?matt_word=pinterest&matt_tool=42893323&forceInApp=true&ref=BKy6mYNZqr4UlYb66%2ByGMd94c3z5IMQ1jNmo4OaU0dFbrZ3%2B%2Bd10dn1Ptd9l715TUvBrzFJWqOMOhuunltJ%2FDagSkuKJA%2BWuLk3yrdlyPyih8N%2Bygeoauvj2ibJTSKD80lAVz%2F%2BPSwZh2lU1b1yPp1Pw74M5IsqNl3KuM%2FlVhkXte%2FPxL1%2BGxU0wUVaPU2m3gj3UM3o%3D",
    "Lavadora Vonder": "https://www.mercadolivre.com.br/social/mendeshop?matt_word=pinterest&matt_tool=42893323&forceInApp=true&ref=BMMWGCki8nnEIX27Ag1PY54AZGSHqjgA%2F5H0j0mxignbFLzSb06sfgE4jeHw%2FwEUn5OKjvV4pKVWHykmenCRwvl%2F5ujYnhB8tTzLft0cpLvZBcaXftiY%2Bp7HySQFZAJE4qIimtsgrA%2BibmwUM%2F%2F7qFOVJaa0cSU1hUCiCRxh2jFYSGUMx2ThPCwAhNEHCQz0hTv770c%3D",
    "Prateleira de Canto": "https://www.mercadolivre.com.br/social/mendeshop?matt_word=pinterest&matt_tool=42893323&forceInApp=true&ref=BDhS5K%2FrYaAUVQJ6EWNgEf4P2ZelxEAq1W2yrTJoMSBcmfvhh0SDU8gVhdlzTO0qfrc6Ho3OQCCujJxZWh0Nv74yZbjoC5UhIivcZj6%2F2pd1jheM3c1QzMgwxW4c8rr%2Flrlc4BMbT1quP4iRJp5gqdkrBgjfDn7S6VWReJ2pEeyRrlS6KQC3eZln1SIS5tauTMj5Ow%3D%3D",
    "Espelho Sala de Estar": "https://www.mercadolivre.com.br/social/mendeshop?matt_word=pinterest&matt_tool=42893323&forceInApp=true&ref=BBG5I%2BXGG9n17kQToKSvJNJe%2BWRQ2Q3c39i0Sem5%2Bszre8WX0bv4NmRSux9q3reLmkfcsq%2FGCCNnj%2FqpGp1VTG6htuneY4cKOGWcS6xddJ0cDRBZD9DFMHlW%2FyiC1SENVuWQcgccYMJgKwdJf0K1377RNReJEqUXwqarZyb3d%2F8ca75RKo8jhPCa1i0ntPluegevmQ%3D%3D",
    "Gloss Franciny Chaveiro": "https://www.mercadolivre.com.br/social/mendeshop?matt_word=pinterest&matt_tool=42893323&forceInApp=true&ref=BLqFHNMjAizFpuA%2Fp2rClq7zOr8XbmvEj%2BohqqivKpZJl7nTVEYOZK3jbezyio87QCCg1krAajI6QBoMjuHpbDRPX5mQDbLkpTuSc0H3BnVGmK6m9HcBCFUR7mpCZcaFTXPYPrJpwCYWyLbdepbZ2660NkSzU%2FoW7YvP1REBIcd8hy7c07zJx6LbkNPFIZiMD5Wx8Q%3D%3D&utm_source=Pinterest&utm_medium=organic"
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

print("🔍 Monitor MendeShop Ativo - Ronda a cada 6 horas")

while True:
    for nome, link in LINKS_PARA_VIGIAR.items():
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
            # allow_redirects=True permite ver se o ML te jogou para a vitrine geral
            resposta = requests.get(link, headers=headers, timeout=25, allow_redirects=True)
            
            # Checa status ou se a palavra 'ref=' sumiu da URL final (indica desvio)
            if resposta.status_code != 200 or "ref=" not in resposta.url:
                print(f"🚩 Link furado detectado: {nome}")
                enviar_aviso(f"🚨 ALERTA: {nome} (Link Quebrado ou Desviado)", link, silencioso=False)
            else:
                print(f"✅ OK: {nome}")
                
        except Exception as e:
            print(f"❌ Erro de Conexão em {nome}: {e}")
            enviar_aviso(f"🔥 ERRO TÉCNICO: {nome}", link, silencioso=False)
        
        # Pausa de 5 segundos entre links para não ser bloqueado
        time.sleep(5) 
    
    # Envia aviso de que a checagem terminou (modo silencioso)
    enviar_aviso("RONDA CONCLUÍDA", "Todos os itens foram checados e estão operacionais.", silencioso=True)
    
    print("⏳ Tudo conferido. Próxima ronda em 6 horas...")
    # 21600 segundos = 6 horas
    time.sleep(21600)
