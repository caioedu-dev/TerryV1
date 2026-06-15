from colorama import Fore, Back, Style
from difflib import get_close_matches
titulo = "C H A T  T E R R Y  V 1"

print("╔════════════════════════════╗")
print(Fore.WHITE + Back.BLUE + "║" + titulo.center(28) + "║" + Style.RESET_ALL)
print("╚════════════════════════════╝" )
respostas = {}
with open('respostas.txt','r', encoding='utf-8') as arquivo:
    for linha in arquivo:
        linha = linha.strip()

        if not linha:
            continue

        if '|' not in linha:
            continue

        pergunta, resposta = linha.split('|', 1)
        respostas[pergunta.lower()] = resposta

print('Olá, eu sou o Terry v1. Posso responder perguntas sobre programação e tecnologia, escreva suas perguntas corretamente para que eu possa responder, sou uma agente direta.')     
while True:
    m=str(input(Fore.RED + 'Você: ' + Style.RESET_ALL).lower())
    pergunta_parecida = get_close_matches(m, respostas.keys(), n=1, cutoff=0.6)
    if m.lower() in respostas:
        print(Fore.BLUE + 'Terry: ' +  Style.RESET_ALL + respostas[m] )
    elif pergunta_parecida:
       chave = pergunta_parecida[0]
       print(Fore.BLUE + "Terry: "+ Style.RESET_ALL + respostas[chave])
    elif m.lower() == 'sair':
        print(Fore.BLUE + 'Terry: ' +  Style.RESET_ALL + 'Até logo!' )
        break
    else:
        print(Fore.BLUE + 'Terry: ' + Style.RESET_ALL + 'Não sei responder isso.')    
        