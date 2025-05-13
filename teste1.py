import streamlit as st

# Inicialização dos dados
if "pagina" not in st.session_state:
    st.session_state.pagina = "menu"
if "candidatos" not in st.session_state:
    st.session_state.candidatos = []
if "votacao_ativa" not in st.session_state:
    st.session_state.votacao_ativa = False

def mostra_menu():
    st.title("Sistema de Votação")
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

def cadastra_candidato():
    st.title("Cadastro de Candidato")
    numero = st.text_input("Número do Candidato")
    nome = st.text_input("Nome do Candidato")
    partido = st.text_input("Partido do Candidato")

    if st.button("Salvar Candidato"):
        if numero and nome and partido:
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

def registrar_voto():
    st.title("Votação")

    for c in st.session_state.candidatos:
        st.markdown(f"**{c['nome']}** ({c['partido']}) - Número: `{c['numero']}`")

    matricula = st.text_input("Digite sua matrícula")
    voto = st.text_input("Digite o número do candidato")

    if st.button("Votar"):
        if not matricula:
            st.warning("Matrícula não pode ser vazia.")
            return

        candidato = next((c for c in st.session_state.candidatos if c["numero"] == voto), None)

        if candidato:
            st.radio("Confirmar voto?", ["Sim", "Não"], key="confirmar_voto")
            if st.session_state.confirmar_voto == "Sim":
                candidato["votos"] += 1
                st.success("Voto registrado com sucesso!")
            else:
                st.info("Voto cancelado.")
        else:
            st.error("Número de candidato inválido.")

    if st.button("Voltar"):
        st.session_state.pagina = "menu"

def mostra_resultado():
    st.title("Resultado da Votação")

    all_users = [c["nome"] for c in st.session_state.candidatos]

    with st.container(border=True):
        users = st.multiselect("Candidatos", all_users, default=all_users)
        # rolling_average = st.toggle("Rolling average")

    if st.session_state.candidatos:
        for c in st.session_state.candidatos:
            st.write(f"{c['nome']} ({c['partido']}) - {c['votos']} votos")
    else:
        st.write("Nenhum candidato cadastrado.")

    if st.button("Voltar ao Menu"):
        st.session_state.pagina = "menu"

# Roteador principal
if st.session_state.pagina == "menu":
    mostra_menu()
elif st.session_state.pagina == "cadastro":
    cadastra_candidato()
elif st.session_state.pagina == "votacao":
    registrar_voto()
elif st.session_state.pagina == "resultado":
    mostra_resultado()
