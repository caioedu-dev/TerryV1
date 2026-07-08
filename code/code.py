import tkinter as tk
from tkinter import font as tkfont
from difflib import get_close_matches
import os

# ---------- Cores e estilo (tema escuro) ----------
COR_FUNDO = "#0d0d0d"
COR_CHAT_FUNDO = "#000000"
COR_TEXTO = "#e0e0e0"
COR_USUARIO = "#ff5c8a"
COR_TERRY = "#5c9dff"
COR_SISTEMA = "#5cff9d"
COR_ENTRADA_FUNDO = "#1a1a1a"
COR_BOTAO = "#5c9dff"
COR_BOTAO_TEXTO = "#0d0d0d"

RESPOSTAS_ARQUIVO = "respostas.txt"
NIVEL_ARQUIVO = "nivel.txt"


class TerryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Terry V1")
        self.root.geometry("520x640")
        self.root.configure(bg=COR_FUNDO)
        self.root.minsize(420, 480)

        self.respostas = self.carregar_respostas()
        self.nivel = self.carregar_nivel()

        self._montar_interface()
        self._mensagem_boas_vindas()

    # ---------- Carregamento de dados ----------
    def carregar_respostas(self):
        respostas = {}
        if os.path.exists(RESPOSTAS_ARQUIVO):
            with open(RESPOSTAS_ARQUIVO, "r", encoding="utf-8") as arquivo:
                for linha in arquivo:
                    linha = linha.strip()
                    if not linha or "|" not in linha:
                        continue
                    pergunta, resposta = linha.split("|", 1)
                    respostas[pergunta.lower()] = resposta
        return respostas

    def carregar_nivel(self):
        if os.path.exists(NIVEL_ARQUIVO):
            with open(NIVEL_ARQUIVO, "r") as arquivo:
                linha = arquivo.read().strip()
            if linha and "|" in linha:
                nivel_atual, xp_atual = linha.split("|")
                return {"xp": int(xp_atual), "nivel": int(nivel_atual)}
        return {"xp": 0, "nivel": 1}

    def salvar_nivel(self):
        with open(NIVEL_ARQUIVO, "w") as arquivo:
            arquivo.write(f"{self.nivel['nivel']}|{self.nivel['xp']}")

    # ---------- Interface ----------
    def _montar_interface(self):
        fonte_titulo = tkfont.Font(family="Segoe UI", size=16, weight="bold")
        fonte_chat = tkfont.Font(family="Segoe UI", size=11)
        fonte_entrada = tkfont.Font(family="Segoe UI", size=11)

        # Cabeçalho
        cabecalho = tk.Frame(self.root, bg=COR_TERRY, height=60)
        cabecalho.pack(fill="x", side="top")
        tk.Label(
            cabecalho,
            text="C H A T   T E R R Y   V 1",
            bg=COR_TERRY,
            fg=COR_BOTAO_TEXTO,
            font=fonte_titulo,
            pady=15,
        ).pack()

        # Área do chat
        area_chat = tk.Frame(self.root, bg=COR_CHAT_FUNDO)
        area_chat.pack(fill="both", expand=True, padx=12, pady=(12, 6))

        scrollbar = tk.Scrollbar(area_chat)
        scrollbar.pack(side="right", fill="y")

        self.texto_chat = tk.Text(
            area_chat,
            bg=COR_CHAT_FUNDO,
            fg=COR_TEXTO,
            font=fonte_chat,
            wrap="word",
            bd=0,
            padx=10,
            pady=10,
            state="disabled",
            yscrollcommand=scrollbar.set,
        )
        self.texto_chat.pack(fill="both", expand=True)
        scrollbar.config(command=self.texto_chat.yview)

        # Tags de cor para cada remetente
        self.texto_chat.tag_config("usuario", foreground=COR_USUARIO, font=(fonte_chat.actual("family"), 11, "bold"))
        self.texto_chat.tag_config("terry", foreground=COR_TERRY, font=(fonte_chat.actual("family"), 11, "bold"))
        self.texto_chat.tag_config("sistema", foreground=COR_SISTEMA, font=(fonte_chat.actual("family"), 10, "italic"))
        self.texto_chat.tag_config("corpo", foreground=COR_TEXTO)

        # Área de entrada
        area_entrada = tk.Frame(self.root, bg=COR_FUNDO)
        area_entrada.pack(fill="x", padx=12, pady=(0, 12))

        self.entrada = tk.Entry(
            area_entrada,
            bg=COR_ENTRADA_FUNDO,
            fg=COR_TEXTO,
            insertbackground=COR_TEXTO,
            font=fonte_entrada,
            bd=0,
            relief="flat",
        )
        self.entrada.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 8))
        self.entrada.bind("<Return>", lambda evento: self.enviar_mensagem())
        self.entrada.focus()

        botao_enviar = tk.Button(
            area_entrada,
            text="Enviar",
            command=self.enviar_mensagem,
            bg=COR_BOTAO,
            fg=COR_BOTAO_TEXTO,
            font=tkfont.Font(family="Segoe UI", size=10, weight="bold"),
            bd=0,
            relief="flat",
            padx=18,
            cursor="hand2",
            activebackground="#74a8f5",
            activeforeground=COR_BOTAO_TEXTO,
        )
        botao_enviar.pack(side="right", ipady=8)

    # ---------- Lógica de chat ----------
    def _mensagem_boas_vindas(self):
        self._adicionar_mensagem(
            "Terry",
            "Olá. Eu sou Terry V1, uma IA direta criada para responder perguntas de forma "
            "rápida. Posso ajudar com programação, tecnologia, estudos e conhecimentos gerais. "
            "Faça sua pergunta de forma clara.",
            "terry",
        )
        self._adicionar_mensagem(
            "Dica", 'Quer acompanhar sua evolução? Digite "nivel" para ver seu nível atual.', "sistema"
        )

    def _adicionar_mensagem(self, remetente, texto, tag):
        self.texto_chat.config(state="normal")
        self.texto_chat.insert("end", f"{remetente}: ", tag)
        self.texto_chat.insert("end", f"{texto}\n\n", "corpo")
        self.texto_chat.config(state="disabled")
        self.texto_chat.see("end")

    def _ganhar_xp(self):
        self.nivel["xp"] += 100
        if self.nivel["xp"] >= 1000:
            self.nivel["nivel"] += 1
            self.nivel["xp"] = 0
            self._adicionar_mensagem("Terry", "Parabéns! Você subiu de nível!", "sistema")
        self.salvar_nivel()

    def enviar_mensagem(self):
        mensagem = self.entrada.get().strip()
        if not mensagem:
            return
        self.entrada.delete(0, "end")
        self._adicionar_mensagem("Você", mensagem, "usuario")

        m = mensagem.lower()
        pergunta_parecida = get_close_matches(m, self.respostas.keys(), n=1, cutoff=0.6)

        if m in self.respostas:
            self._adicionar_mensagem("Terry", self.respostas[m], "terry")
            self._ganhar_xp()
        elif pergunta_parecida:
            chave = pergunta_parecida[0]
            self._adicionar_mensagem("Terry", self.respostas[chave], "terry")
            self._ganhar_xp()
        elif m == "sair":
            self._adicionar_mensagem("Terry", "Até logo!", "terry")
            self.root.after(1200, self.root.destroy)
        elif m == "nivel":
            self._adicionar_mensagem(
                "Terry", f"Nível {self.nivel['nivel']} — XP: {self.nivel['xp']}/1000", "terry"
            )
        else:
            self._adicionar_mensagem("Terry", "Não sei responder isso.", "terry")


if __name__ == "__main__":
    janela = tk.Tk()
    app = TerryApp(janela)
    janela.mainloop()