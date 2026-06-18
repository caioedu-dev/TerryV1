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
with open('nivel.txt','r') as arquivo:
    linha = arquivo.read()
nivel_atual,xp_atual = linha.split('|')
nivel = {'xp': int(xp_atual),
         'nivel': int(nivel_atual)        }

print('Olá. Eu sou Terry V1, uma IA direta criada para responder perguntas de forma rápida. Posso ajudar com programação, tecnologia, estudos e conhecimentos gerais. Faça sua pergunta de forma clara.')
print(Fore.GREEN + 'Dica: Quer acompanhar sua evolução? Digite "nivel" para ver seu nível atual e experiência.' + Style.RESET_ALL)     
while True:
    m=str(input(Fore.RED + 'Você: ' + Style.RESET_ALL).lower())
    pergunta_parecida = get_close_matches(m, respostas.keys(), n=1, cutoff=0.6)
    if m.lower() in respostas:
        print(Fore.BLUE + 'Terry: ' +  Style.RESET_ALL + respostas[m] )
        nivel['xp'] += 100
        if nivel['xp'] >= 1000:
           nivel['nivel'] += 1
           nivel['xp'] = 0
           print(Fore.BLUE + 'Terry: ' + Style.RESET_ALL + 'Parabéns! você subiu de nível!')
        with open ('nivel.txt', 'w') as arquivo:
            arquivo.write(f"{nivel['nivel']}|{nivel['xp']}")
    elif pergunta_parecida:
       chave = pergunta_parecida[0]
       print(Fore.BLUE + "Terry: "+ Style.RESET_ALL + respostas[chave])
       nivel['xp'] += 100
       if nivel['xp'] >= 1000:
            nivel['nivel'] += 1
            nivel['xp'] = 0
            print(Fore.BLUE + 'Terry: ' + Style.RESET_ALL + Fore.GREEN + 'Parabéns! você subiu de nível!' + Style.RESET_ALL)
       with open ('nivel.txt', 'w') as arquivo:
            arquivo.write(f"{nivel['nivel']}|{nivel['xp']}")
    elif m.lower() == 'sair':
        print(Fore.BLUE + 'Terry: ' +  Style.RESET_ALL + 'Até logo!' )
        break
    elif m.lower() == 'nivel':
        print(Fore.BLUE + 'Terry: ' + Style.RESET_ALL + f"{nivel['nivel']}")
    else:
        print(Fore.BLUE + 'Terry: ' + Style.RESET_ALL + 'Não sei responder isso.')    
