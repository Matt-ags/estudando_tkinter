from tkinter import *
from tkinter import messagebox 
import tkinter as tk

"""
um sistema simples de converter moedas

2 campos:

(insirir valor em reais)

(Selecionar moeda para conversão)

--- 

(botão converter)

(ao clicar, exibir o valor convertido)

"""

taxas = {
    "dólar": 5.00,
    "euro": 5.40,
    "libra": 6.20,
}

# prierio, vamos estudar a logica

# def coverter():
#    valor_reais = float(input("Digite o valor em reais: "))
 #   moeda = input("Digite a moeda para conversão (dólar, euro, libra): ").lower()
   # if moeda in taxas:
    #    valor_convertido = valor_reais / taxas[moeda]
     #   print(f"Valor convertido: {valor_convertido:.2f} {moeda}")
   # else:
   #     print("Moeda inválida.")

#coverter()

# Agora, vamos criar uma interface gráfica simples usando tkinter
janela = tk.Tk()
janela.title("Conversor de Moedas")
janela.geometry("400x300")
janela.configure(padx=20, pady=20) # adiciona um "padding"

# Função para converter o valor
def converter():
    valor_reais = float(entrada_valor.get())
    moeda = combo_moeda.get().lower()
    if moeda in taxas:
        valor_convertido = valor_reais / taxas[moeda]
        messagebox.showinfo("Resultado", f"Valor convertido: {valor_convertido:.2f} {moeda}")
    else:
        messagebox.showerror("Erro", "Moeda inválida.")

# Label e entrada para o valor em reais
label_valor = tk.Label(janela, text="Valor em Reais:")
label_valor.pack(pady=5)
entrada_valor = tk.Entry(janela)
entrada_valor.pack(pady=5)
# Label e combo box para selecionar a moeda

label_moeda = tk.Label(janela, text="Selecione a Moeda:")
label_moeda.pack(pady=5)
moedas = list(taxas.keys())
combo_moeda = tk.StringVar()
combo_moeda.set(moedas[0])  # valor padrão
combo = tk.OptionMenu(janela, combo_moeda, *moedas)
combo.pack(pady=5)

# Botão para converter
botao_converter = tk.Button(janela, text="Converter", command=converter)
botao_converter.pack(pady=10)
# Inicia o loop principal da interface
janela.mainloop()
