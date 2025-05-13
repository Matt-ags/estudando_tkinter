from tkinter import *
from tkinter import messagebox 
import tkinter as tk
import json

candidatos = []
votacao_ativa = False

janela = tk.Tk()
janela.title("Sistema de Votação")

def mostra_menu():
    janela.geometry("400x300")
    janela.configure(padx=20, pady=20)

    label_menu = tk.Label(janela, text="Escolha uma opção:")
    label_menu.pack(pady=10)

    botao_cadastro = tk.Button(janela, text="Cadastro de Candidato", command=cadastra_candidato)
    botao_cadastro.pack(pady=5)

    botao_votacao = tk.Button(janela, text="Iniciar Votação", command=iniciar_votacao)
    botao_votacao.pack(pady=5)

    botao_encerrar = tk.Button(janela, text="Encerrar Votação", command=encerrar_votacao)
    botao_encerrar.pack(pady=5)


def cadastra_candidato():
    janela_cadastro = tk.Toplevel(janela)
    janela_cadastro.title("Cadastro de Candidato")
    janela_cadastro.geometry("400x300")

    tk.Label(janela_cadastro, text="Número do Candidato:").pack(pady=5)
    entrada_numero = tk.Entry(janela_cadastro)
    entrada_numero.pack(pady=5)

    tk.Label(janela_cadastro, text="Nome do Candidato:").pack(pady=5)
    entrada_nome = tk.Entry(janela_cadastro)
    entrada_nome.pack(pady=5)

    tk.Label(janela_cadastro, text="Partido do Candidato:").pack(pady=5)
    entrada_partido = tk.Entry(janela_cadastro)
    entrada_partido.pack(pady=5)

    def salvar_candidato():
        numero = entrada_numero.get()
        nome = entrada_nome.get()
        partido = entrada_partido.get()
        candidatos.append({"numero": numero, "nome": nome, "partido": partido, "votos": 0})
        messagebox.showinfo("Sucesso", "Candidato cadastrado com sucesso!")
        janela_cadastro.destroy()

    botao_salvar = tk.Button(janela_cadastro, text="Salvar", command=salvar_candidato)
    botao_salvar.pack(pady=5)


def iniciar_votacao():
    global votacao_ativa
    votacao_ativa = True
    registrar_voto()

def registrar_voto():
    if votacao_ativa:
        janela_votacao = tk.Toplevel(janela)
        janela_votacao.title("Votação")
        janela_votacao.geometry("400x300")

        tk.Label(janela_votacao, text=f"NOME CANDIDATO | NÚMERO CANDIDATO").pack(pady=5)

        for candidato in candidatos:
            tk.Label(janela_votacao, text=f"{candidato['nome']} | {candidato['partido']}").pack(pady=5)

        tk.Label(janela_votacao, text="Digite sua matrícula:").pack(pady=5)
        entrada_matricula = tk.Entry(janela_votacao)
        entrada_matricula.pack(pady=5)

        tk.Label(janela_votacao, text="Digite o número do candidato:").pack(pady=5)
        entrada_voto = tk.Entry(janela_votacao)
        entrada_voto.pack(pady=5)

        def confirmar_voto():
            matricula = entrada_matricula.get()
            voto = entrada_voto.get()

            if not matricula:
                messagebox.showwarning("Erro", "Matrícula não pode ser vazia.")
                return

            candidato_escolhido = next((c for c in candidatos if c["numero"] == voto), None)

            if candidato_escolhido:
                confirmar = messagebox.askyesno("Confirmação", f"Confirmar voto para {candidato_escolhido['nome']} ({candidato_escolhido['partido']})?")
                if confirmar:
                    candidato_escolhido["votos"] += 1
                    messagebox.showinfo("Sucesso", "Voto registrado com sucesso!")
                    janela_votacao.destroy()
                    registrar_voto()
            else:
                confirmar = messagebox.askyesno("Confirmação", "Candidato inexistente. Confirmar voto nulo?")
                if confirmar:
                    messagebox.showinfo("Sucesso", "Voto nulo registrado!")
                    janela_votacao.destroy()
                    registrar_voto()

        botao_votar = tk.Button(janela_votacao, text="Votar", command=confirmar_voto)
        botao_encerrar = tk.Button(janela_votacao, text="Cancelar", command=janela_votacao.destroy)
        
        botao_votar.pack(pady=5)
        botao_encerrar.pack(pady=0)

def imprime_relatorio():
    janela_relatorio = tk.Toplevel(janela)
    janela_relatorio.title("Resultados")
    janela_relatorio.geometry("400x300")

    total_votos = sum(c["votos"] for c in candidatos)

    if total_votos > 0:
        for candidato in candidatos:
            tk.Label(janela_relatorio, text=f"{candidato['nome']} ({candidato['partido']}): {candidato['votos']} votos").pack(pady=5)
    else:
        tk.Label(janela_relatorio, text="Não houve votos válidos.").pack(pady=5)

    botao_fechar = tk.Button(janela_relatorio, text="Fechar", command=janela_relatorio.destroy)
    botao_fechar.pack(pady=5)

def encerrar_votacao():
    global votacao_ativa
    votacao_ativa = False
    print(candidatos)
    # Método 1: Iterando e escrevendo no arquivo
    with open("dicionarios.txt", "w") as arquivo:
        arquivo.write("Número | Nome | Partido | Votos\n")
        for dicionario in candidatos:
            arquivo.write(str(dicionario["numero"]) + " | " + str(dicionario["nome"]) + " | " + str(dicionario["partido"]) + " | " + str(dicionario["votos"]) + "\n")
    imprime_relatorio()

mostra_menu()
janela.mainloop()
