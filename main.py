import tkinter as tk
import math
import re

cor_fundo = "#ffe6f0"
cor_botao = "#ffb6c1"
cor_texto = "#880e4f"
cor_botaoFuncao = "#f06292"
janela = tk.Tk()
janela.title("Calculadora Python!")
janela.geometry("340x460")
janela.configure(bg=cor_fundo)
janela.iconbitmap("recursos/icone (2).ico")
entrada = tk.Entry(janela, width=17, font=("Arial", 24), borderwidth=2, relief="flat", justify='right', fg=cor_texto, bg="#fff0f5")
entrada.grid(row=0, column=0, columnspan=4, padx=(10, 20), pady=20)

rodape = tk.Label(
    janela,
    text="Bons Cálculos!",
    font=("Comic Sans MS", 16, "italic"),
    fg=cor_texto,
    bg=cor_fundo
)
rodape.place(relx=0.5, rely=1.0, anchor='s', y=-10)

def clicar(valor):
    entrada.insert(tk.END, valor)

def apagar_ultimo():
    texto = entrada.get()
    entrada.delete(0, tk.END)
    entrada.insert(0, texto[:-1])

def calcular():
    try:
        expressao = entrada.get()
        expressao = expressao.replace('^', '**')
        expressao = re.sub(r'√(\d+(\.\d+)?)', r'math.sqrt(\1)', expressao)
        expressao = re.sub(r'(\d)(\()', r'\1*\2', expressao)  
        expressao = re.sub(r'(\))(\d)', r'\1*\2', expressao)  
        resultado = eval(expressao, {"__builtins__": None}, {"math": math})
        entrada.delete(0, tk.END)
        entrada.insert(0, str(resultado))
    except:
        entrada.delete(0, tk.END)
        entrada.insert(0, "Erro")

def pressionar_tecla(evento):
    if not evento.char: 
        return
    tecla = evento.char
    if tecla in '0123456789.+-*/^()':
        clicar(tecla)
    elif evento.keysym == 'Return':
        calcular()
    elif evento.keysym in ['BackSpace', 'Delete']:
        apagar_ultimo()

def inserir_parenteses():
    texto = entrada.get()
    abre = texto.count('(')
    fecha = texto.count(')')
    if abre <= fecha:
        entrada.insert(tk.END, '(')
    else:
        entrada.insert(tk.END, ')')

janela.bind("<Key>", pressionar_tecla)
botoes = [
    ('Del', 1, 0), ('√', 1, 1), ('^', 1, 2), ('()', 1, 3),
    ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
    ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
    ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
    ('0', 5, 0), ('.', 5, 1), ('=', 5, 2), ('+', 5, 3)
]

for (texto, linha, coluna) in botoes:
    cor = cor_botaoFuncao if texto in ['Del', '√', '^', '()'] else cor_botao
    if texto == '=':
        funcao = calcular
    elif texto == 'Del':
        funcao = apagar_ultimo
    elif texto == '()':
        funcao = inserir_parenteses
    else:
        funcao = lambda x=texto: clicar(x)
    botao = tk.Button(janela, text=texto, width=5, height=2, font=("Arial", 14), bg=cor, fg=cor_texto, bd=0, activebackground="#ffc1cc", command=funcao)
    def on_enter(e, btn=botao):
        btn.configure(bg="#ffd6e8")  

    def on_leave(e, btn=botao, original=cor):
        btn.configure(bg=original)  
    botao.bind("<Enter>", on_enter)
    botao.bind("<Leave>", on_leave)
    botao.grid(row=linha, column=coluna, padx=5, pady=5)

janela.mainloop()