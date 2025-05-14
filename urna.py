import streamlit as st
import pandas as pd
import numpy as np

# Inicialização dos dados
# aqui, de forma simples, meio que cria as variaveis necessárias, no momento que for pedido
# pois se colocar aqui, tipo "candidatos = []", ao voltar na pagina inicial, ele zera a lista
if "pagina" not in st.session_state:
    st.session_state.pagina = "menu"
if "candidatos" not in st.session_state:
    st.session_state.candidatos = []
if "votacao_ativa" not in st.session_state:
    st.session_state.votacao_ativa = False

# abaixo, mostra o menu inicial
def mostra_menu():
    st.header("***Sistema de Votação***", divider=True)
    st.image("https://www.justicaeleitoral.jus.br/imagens/fotos/saiba-mais-sobre-a-seguranca-da-urna-eletronica/@@streaming/image/2023-09-12-seguran%C3%A7a-urna.jpg", caption="Urna Eletrônica")
    st.markdown("""### Selecione uma das opções abaixo:
                
                """)

    if st.button("Cadastro de Candidato"):
        st.session_state.pagina = "cadastro"

    if st.button("Iniciar Votação"):
        if not st.session_state.candidatos:
            st.warning("Cadastre pelo menos um candidato antes de iniciar a votação.")
        else:
            st.session_state.votacao_ativa = True
            st.session_state.pagina = "votacao"

    if st.button("Encerrar Votação"):
        st.session_state.votacao_ativa = False
        st.session_state.pagina = "resultado"

# abaixo, mostra a tela de cadastro de candidatos
def cadastra_candidato():
    st.title("Cadastro de Candidato")

    st.image("https://habitacional.com.br/wp-content/uploads/2023/08/Cadastro-de-condominos_por-que-ele-e-extremamente-importante.webp", caption="Cadastro de Candidatos")
    # função de formulario, pra deixa bunitin
    with st.form("form_candidato"):
        numero = st.text_input("Número do Candidato")
        nome = st.text_input("Nome do Candidato")
        partido = st.text_input("Partido do Candidato")
        enviado = st.form_submit_button("Salvar Candidato")

        if enviado:
            if numero and nome and partido:
                # lembra la em cima que criei as "variaveis"?
                # então, aqui eu chamo e adiciono os dados!
                st.session_state.candidatos.append({
                    "numero": numero,
                    "nome": nome,
                    "partido": partido,
                    "votos": 0
                })
                st.success("Candidato cadastrado com sucesso!")
            else:
                st.error("Preencha todos os campos.")

    if st.button("Voltar"):
        st.session_state.pagina = "menu"

# abaixo, mostra a tela de votação
def registrar_voto():
    st.title("Votação")
        
    df_candidatos = pd.DataFrame(st.session_state.candidatos, columns=["nome", "partido", "numero"])
    df_candidatos.rename(columns={"nome": "Nome", "partido": "Partido", "numero": "Número"}, inplace=True)

    st.dataframe(df_candidatos, height=250, use_container_width=True)

    with st.form("form_voto"):
        matricula = st.text_input("Digite sua matrícula")
        voto = st.text_input("Digite o número do candidato")
        enviado = st.form_submit_button("Registrar Voto")

        if enviado:
            if not matricula:
                st.warning("Matrícula não pode ser vazia.")
                return
            
            candidato = next((c for c in st.session_state.candidatos if c["numero"] == voto), None) # isso pode parecer feio, mas é assim, "c" em "c", esse ultimo c é o candidato, e o primeiro c é a lista de candidatos, então ele vai pegar o candidato que tem o mesmo numero que o voto
            # se o candidato for encontrado, ele adiciona 1 voto

            if candidato:
                candidato["votos"] += 1
                st.success("Voto registrado com sucesso!") # mensagens de sucesso
            else:
                st.error("Número de candidato inválido.")
    

    if st.button("Voltar"):
        st.session_state.pagina = "menu"

# função que mostra o resultado da votação
def mostra_resultado():

    st.title("Resultado da Votação")

    all_users = [c["nome"] for c in st.session_state.candidatos]



    if st.session_state.candidatos:

        with st.container(border=True):
            users = st.multiselect("Candidatos", all_users, default=all_users)
        # rolling_average = st.toggle("Rolling average")

        data = pd.DataFrame({
            "Candidatos": users,
            "Votos": [c["votos"] for c in st.session_state.candidatos if c["nome"] in users]
        })

        tab1, tab2 = st.tabs(["Grafico de Barras", "Tabela"])
        tab1.bar_chart(data.set_index("Candidatos"))
        tab2.dataframe(data, height=250, use_container_width=True)

        df = pd.DataFrame(st.session_state.candidatos)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Baixar resultados em CSV", data=csv, file_name="resultado_votacao.csv", mime="text/csv") # fazer o download do csv
    else:
        st.image("https://media.tenor.com/OA8KFcZxPjsAAAAm/sad-emoji.webp", caption="Opa! Parece que não temos candidatos cadastrados ainda!")


    if st.button("Voltar ao Menu"):
        st.session_state.pagina = "menu"

# Roteador principal
# aqui, é pra poder mudar de pagina, de acordo com o que o usuario clicar
if st.session_state.pagina == "menu":
    mostra_menu()
elif st.session_state.pagina == "cadastro":
    cadastra_candidato()
elif st.session_state.pagina == "votacao":
    registrar_voto()
elif st.session_state.pagina == "resultado":
    mostra_resultado()
