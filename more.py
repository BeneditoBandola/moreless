from datetime import datetime
import json
import os
import random
import pandas as pd
import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Multitemas - Ranking & Patentes",
    page_icon="✨",
    layout="centered",
)

ARQUIVO_DADOS_JSON = "dados_diarios.json"
ARQUIVO_INTEGRANTES = "integrantes_equipe.csv"
ARQUIVO_HISTORICO_JSON = "historico_semanas.json"

# --- LISTA EXTENSA DE AVATARES DIVERTIDOS ---
LISTA_AVATARES = [
    "👰 Noivinha Clássica",
    "🤵 Noivo Elegante",
    "💍 Aliança de Ouro",
    "💐 Bouquet de Flores",
    "💒 Capela dos Sonhos",
    "👽 ET Cinzento",
    "🛸 Disco Voador",
    "🤖 Robô Cibernético",
    "🪐 Planeta Anelado",
    "🚀 Foguete Espacial",
    "🌌 Mestre Jedi",
    "⚔️ Cavaleiro Sith",
    "🛡️ Caçador de Recompensas",
    "🪐 Piloto Estelar",
    "🔮 Mago Supremo",
    "🧞 Gênio da Lâmpada",
    "🧞‍♂️ Espírito Mágico",
    "🧚 Fada Madrinha",
    "🧙 Mago das Fórmulas",
    "🦄 Unicórnio Mágico",
    "🍌 Minion Maluco",
    "👾 Monstrinho Pixel",
    "👻 Fantasminha Camarada",
    "🦸 Super-Herói",
    "🦹 Super-Vilão",
    "🐐 Cabrito Sagrado",
    "🐎 Égua Veloz",
    "🐴 Mula Carinhosa",
    "🦁 Leão Corajoso",
    "🦊 Raposa Astuta",
    "👑 Rei do Trono",
    "💼 Diretor Executivo",
    "☕ Xícara de Café",
    "💻 Hacker da Madrugada",
    "💀 Caveira Estilosa",
]

PATENTES_ORIGINAIS = {
    100: "👑 Deus Supremo",
    75: "🐐 Cabrito Sagrado",
    50: "🐎 Égua Satânica",
    25: "🐴 Mula Juvenil",
    0: "🎒 Mochila de Criança",
}

TEMAS = {
    "💀 Cemitério": {
        "bg_app": "#09090B",
        "card_bg": "linear-gradient(135deg, #120A2A, #09090B)",
        "border_color": "#4C1D95",
        "text_color": "#E4E4E7",
        "accent_color": "#A855F7",
        "input_bg": "#18181B",
        "input_text": "#FFFFFF",
        "icone": "💀",
        "patentes": PATENTES_ORIGINAIS,
        "mensagens": [
            "As catacumbas guardam os segredos daqueles que não entregaram as metas...",
            "O roxo da meia-noite cobre os corredores enquanto o sistema aguarda.",
            "Cuidado com os passos falsos... o coveiro está sempre de olho nos relatórios.",
        ],
    },
    "👰 Noiva e Casamentos": {
        "bg_app": "#FDF2F8",
        "card_bg": "linear-gradient(135deg, #FCE7F3, #FFF1F2)",
        "border_color": "#F472B6",
        "text_color": "#831843",
        "accent_color": "#DB2777",
        "input_bg": "#FFFFFF",
        "input_text": "#831843",
        "icone": "👰",
        "patentes": PATENTES_ORIGINAIS,
        "mensagens": [
            "Planejando cada detalhe com amor, elegância e foco total nas metas do grande dia.",
            "Até que o fecho da folha de cálculo nos uma para sempre no altar!",
            "Um casamento perfeito exige um bouquet lindo, convidados felizes e metas batidas.",
        ],
    },
    "💖 Meninas e Estilo": {
        "bg_app": "#FFF1F2",
        "card_bg": "linear-gradient(135deg, #FFE4E6, #FCE7F3)",
        "border_color": "#FB7185",
        "text_color": "#4C0519",
        "accent_color": "#E11D48",
        "input_bg": "#FFFFFF",
        "input_text": "#4C0519",
        "icone": "💖",
        "patentes": PATENTES_ORIGINAIS,
        "mensagens": [
            "Garotas inteligentes conquistam qualquer meta com charme, salto alto e atitude!",
            "Brilhe muito hoje, coloque o batom favorito e arrase nos resultados.",
            "Foco, café, look do dia impecável e metas batidas com sucesso!",
        ],
    },
    "💻 Tecnologia e Cyber": {
        "bg_app": "#030712",
        "card_bg": "linear-gradient(135deg, #0F172A, #030712)",
        "border_color": "#06B6D4",
        "text_color": "#E2E8F0",
        "accent_color": "#22D3EE",
        "input_bg": "#0F172A",
        "input_text": "#FFFFFF",
        "icone": "💻",
        "patentes": PATENTES_ORIGINAIS,
        "mensagens": [
            "A executar rotina de otimização de dados... 100% de eficiência concluída.",
            "O código está limpo, o deploy foi feito com sucesso e o sistema voa.",
            "Conectado na matrix corporativa, a processar cada desafio com inovação.",
        ],
    },
    "☕ Escritório Corporativo": {
        "bg_app": "#F8FAFC",
        "card_bg": "linear-gradient(135deg, #F1F5F9, #E2E8F0)",
        "border_color": "#CBD5E1",
        "text_color": "#1E293B",
        "accent_color": "#2563EB",
        "input_bg": "#FFFFFF",
        "input_text": "#1E293B",
        "icone": "☕",
        "patentes": PATENTES_ORIGINAIS,
        "mensagens": [
            "Reunião que podia ser um e-mail? Aqui o foco é produtividade real!",
            "O café quentinho está na chávena e a folha de cálculo aberta para começar o dia.",
            "Organização, networking e foco nas entregas definem o sucesso de hoje.",
        ],
    },
}

# --- BARRA LATERAL ---
st.sidebar.title("🎨 Personalização")
tema_escolhido = st.sidebar.selectbox("Escolha o Tema Visual:", list(TEMAS.keys()))
t = TEMAS[tema_escolhido]

st.sidebar.markdown("---")
st.sidebar.title("⚙️ Exibição")
ocultar_boas_vindas = st.sidebar.checkbox("Ocultar mensagem de boas-vindas", value=False)

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {t["bg_app"]};
        color: {t["text_color"]};
    }}
    .custom-card {{
        background: {t["card_bg"]};
        border: 1px solid {t["border_color"]};
        padding: 16px;
        border-radius: 14px;
        color: {t["text_color"]};
        margin-bottom: 15px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    }}
    .stTextInput label, .stSelectbox label, .stDateInput label, .stNumberInput label {{
        color: {t["text_color"]} !important;
        font-weight: 600;
    }}
    input, select, textarea {{
        background-color: {t["input_bg"]} !important;
        color: {t["input_text"]} !important;
    }}
    </style>
""",
    unsafe_allow_html=True,
)

INTEGRANTES_PADRAO = {
    "Benedito": {"Cor": "#2563EB", "Avatar": "👑 Rei do Trono"},
    "Bárbara": {"Cor": "#DB2777", "Avatar": "👰 Noivinha Clássica"},
    "Vinícius": {"Cor": "#059669", "Avatar": "👽 ET Cinzento"},
    "Samuel": {"Cor": "#D97706", "Avatar": "🌌 Mestre Jedi"},
    "Gabrielle": {"Cor": "#8B5CF6", "Avatar": "🧞 Gênio da Lâmpada"},
    "Tuane": {"Cor": "#0891B2", "Avatar": "🍌 Minion Maluco"},
}


def carregar_integrantes():
    if os.path.exists(ARQUIVO_INTEGRANTES):
        df_int = pd.read_csv(ARQUIVO_INTEGRANTES)
        if "Avatar" not in df_int.columns:
            df_int["Avatar"] = "👤 Participante"
        return df_int.set_index("Nome").to_dict(orient="index")
    else:
        dados_lista = []
        for nome, info in INTEGRANTES_PADRAO.items():
            dados_lista.append({"Nome": nome, "Cor": info["Cor"], "Avatar": info["Avatar"]})
        df_int = pd.DataFrame(dados_lista)
        df_int.to_csv(ARQUIVO_INTEGRANTES, index=False)
        return df_int.set_index("Nome").to_dict(orient="index")


def salvar_integrante(nome, cor, avatar):
    integrantes_dict = carregar_integrantes()
    integrantes_dict[nome] = {"Cor": cor, "Avatar": avatar}
    dados_lista = []
    for n, info in integrantes_dict.items():
        dados_lista.append({"Nome": n, "Cor": info["Cor"], "Avatar": info["Avatar"]})
    df_int = pd.DataFrame(dados_lista)
    df_int.to_csv(ARQUIVO_INTEGRANTES, index=False)


def carregar_dados_json():
    if os.path.exists(ARQUIVO_DADOS_JSON):
        with open(ARQUIVO_DADOS_JSON, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}


def salvar_dados_json(dados):
    with open(ARQUIVO_DADOS_JSON, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)


def converter_json_para_dataframe(dados_json):
    linhas = []
    for data_str, registros in dados_json.items():
        for integrante, info in registros.items():
            linhas.append({
                "Data": data_str,
                "Integrante": integrante,
                "Pontos": info.get("Pontos", 0),
                "Observação": info.get("Observação", ""),
            })
    if not linhas:
        return pd.DataFrame(columns=["Data", "Integrante", "Pontos", "Observação"])
    return pd.DataFrame(linhas)


def carregar_historico_json():
    if os.path.exists(ARQUIVO_HISTORICO_JSON):
        with open(ARQUIVO_HISTORICO_JSON, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}


def salvar_historico_json(historico):
    with open(ARQUIVO_HISTORICO_JSON, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=4)


def obter_classificacao(pontos, patentes):
    for limite in sorted(patentes.keys(), reverse=True):
        if pontos >= limite:
            return patentes[limite]
    return list(patentes.values())[-1]


integrantes_info = carregar_integrantes()
dados_diarios = carregar_dados_json()
df_pontos = converter_json_para_dataframe(dados_diarios)

# --- BOAS-VINDAS ---
if not ocultar_boas_vindas:
    mensagem_dia = random.choice(t["mensagens"])
    st.markdown(
        f"""
        <div class="custom-card">
            <h3 style="margin: 0; color: {t["accent_color"]};">{t["icone"]} Painel Interativo - {tema_escolhido}</h3>
            <p style="font-size: 13px; opacity: 0.8; margin-top: 2px;">📅 Data: <b>{datetime.today().strftime('%d/%m/%Y')}</b></p>
            <hr style="border: 0.5px solid {t["border_color"]}; margin: 8px 0;">
            <p style="font-size: 14px; margin: 0; font-style: italic;">"{mensagem_dia}"</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.title(f"{t['icone']} Ranking & Patentes")
st.markdown("---")

aba_lancamento, aba_ranking, aba_admin = st.tabs(["📝 Registrar", "🏆 Ranking", "⚙️ Gestão"])

with aba_lancamento:
    st.subheader("Registrar Pontuação por Data")
    with st.form("form_pontuacao", clear_on_submit=True):
        lista_nomes = list(integrantes_info.keys())
        integrante = st.selectbox("Escolha o Integrante:", lista_nomes)
        data_lancamento = st.date_input("Data:", value=datetime.today(), format="DD/MM/YYYY")
        pontos = st.number_input("Pontos (Máximo 25):", min_value=0, max_value=25, step=1, format="%d")
        observacao = st.text_input("Observação (Opcional):")
        enviado = st.form_submit_button("🔥 Registrar Pontuação", use_container_width=True)

        if enviado:
            if not integrante:
                st.warning("Selecione o integrante.")
            else:
                data_str = data_lancamento.strftime("%Y-%m-%d")
                if data_str not in dados_diarios:
                    dados_diarios[data_str] = {}
                dados_diarios[data_str][integrante] = {
                    "Pontos": int(pontos),
                    "Observação": observacao if observacao else ""
                }
                salvar_dados_json(dados_diarios)
                st.success(f"Pontuação de {integrante} salva com sucesso para o dia {data_lancamento.strftime('%d/%m/%Y')}!")
                st.rerun()

with aba_ranking:
    if not df_pontos.empty:
        st.subheader("📊 Estatísticas Gerais")
        total_pontos_geral = df_pontos["Pontos"].sum()
        maior_pontuacao_dia = df_pontos["Pontos"].max()

        c1, c2 = st.columns(2)
        c1.metric("Pontos Acumulados", f"{int(total_pontos_geral)} pts")
        c2.metric("Recorde Diário", f"{int(maior_pontuacao_dia)} pts")

        st.markdown("---")
        st.subheader("🥇 Hierarquia Atual")

        ranking_geral = (
            df_pontos.groupby("Integrante")
            .agg(
                Total_Pontos=("Pontos", "sum"),
                Dias_Trabalhados=("Data", "nunique"),
            )
            .reset_index()
        )

        ranking_geral = ranking_geral.sort_values(by="Total_Pontos", ascending=False).reset_index(drop=True)
        ranking_geral["Posição"] = ranking_geral.index + 1

        ranking_geral["Avatar"] = ranking_geral["Integrante"].apply(
            lambda x: integrantes_info.get(x, {}).get("Avatar", "👤 Participante")
        )
        ranking_geral["Patente"] = ranking_geral["Total_Pontos"].apply(
            lambda x: obter_classificacao(x, t["patentes"])
        )

        df_exibicao = df_pontos.copy()
        df_exibicao["Data"] = pd.to_datetime(df_exibicao["Data"]).dt.strftime("%d/%m/%Y")

        tabela_exib = ranking_geral[["Posição", "Avatar", "Integrante", "Total_Pontos", "Patente"]].rename(columns={"Total_Pontos": "Total"})
        st.dataframe(tabela_exib, use_container_width=True, index=False)

        st.markdown("### 📈 Gráfico de Pontuação")
        chart_data = ranking_geral.set_index("Integrante")["Total_Pontos"]
        st.bar_chart(chart_data)

        st.markdown("---")
        st.subheader("📋 Livro de Registros Recentes")
        st.dataframe(df_exibicao.sort_values(by="Data", ascending=False), use_container_width=True, index=False)
    else:
        st.info("Nenhum registo encontrado ainda.")

with aba_admin:
    st.subheader("➕ Adicionar Novo Integrante")
    with st.form("form_novo_integrante", clear_on_submit=True):
        novo_nome = st.text_input("Nome:")
        novo_avatar = st.selectbox("Escolha o Avatar:", LISTA_AVATARES)
        nova_cor = st.color_picker("Cor de Destaque da Barra:", t["accent_color"])
        cadastrar_btn = st.form_submit_button("Cadastrar Integrante", use_container_width=True)

        if cadastrar_btn:
            if novo_nome.strip():
                if novo_nome.strip() in integrantes_info:
                    st.warning("Este integrante já existe!")
                else:
                    salvar_integrante(novo_nome.strip(), nova_cor, novo_avatar)
                    st.success(f"{novo_nome.strip()} cadastrado com sucesso!")
                    st.rerun()
            else:
                st.warning("Digite um nome válido.")

    st.markdown("---")
    st.subheader("🏆 Apuração e Resumo Diário da Semana")
    
    if not df_pontos.empty:
        df_temp = df_pontos.copy()
        df_temp["Data_Parsed"] = pd.to_datetime(df_temp["Data"], errors="coerce")
        df_temp["Ano_Semana"] = df_temp["Data_Parsed"].apply(
            lambda x: f"Ano {x.isocalendar()[0]} - Semana {x.isocalendar()[1]}" if pd.notnull(x) else ""
        )
        semanas_disponiveis = sorted(df_temp["Ano_Semana"].unique(), reverse=True)
    else:
        semanas_disponiveis = []

    hoje = datetime.today()
    ano_atual, semana_atual, _ = hoje.isocalendar()
    semana_padrao_str = f"Ano {ano_atual} - Semana {semana_atual}"

    if semana_padrao_str not in semanas_disponiveis and semanas_disponiveis:
        semana_selecionada = st.selectbox("Escolha a Semana para Apuração:", semanas_disponiveis)
    elif semanas_disponiveis:
        semana_selecionada = st.selectbox("Escolha a Semana para Apuração:", semanas_disponiveis, index=semanas_disponiveis.index(semana_padrao_str))
    else:
        semana_selecionada = semana_padrao_str

    if st.button("📊 Gerar Relatório Detalhado da Semana", use_container_width=True):
        if df_pontos.empty:
            st.warning("Sem pontuações para exibir!")
        else:
            df_pontos["Data_Parsed"] = pd.to_datetime(df_pontos["Data"], errors="coerce")
            df_pontos["Ano_Semana"] = df_pontos["Data_Parsed"].apply(
                lambda x: f"Ano {x.isocalendar()[0]} - Semana {x.isocalendar()[1]}" if pd.notnull(x) else ""
            )
            df_semana = df_pontos[df_pontos["Ano_Semana"] == semana_selecionada].copy()

            if df_semana.empty:
                st.warning(f"Nenhum lançamento encontrado na semana ({semana_selecionada}).")
            else:
                df_semana["Data_Formatada"] = df_semana["Data_Parsed"].dt.strftime("%d/%m (%a)")

                tabela_detalhada = df_semana.pivot_table(
                    index="Integrante", 
                    columns="Data_Formatada", 
                    values="Pontos", 
                    aggfunc="sum", 
                    fill_value=0
                )

                tabela_detalhada["Total Semana"] = tabela_detalhada.sum(axis=1)
                tabela_detalhada = tabela_detalhada.sort_values(by="Total Semana", ascending=False)

                st.markdown(f"### Detalhe por Dia - {semana_selecionada}")
                st.dataframe(tabela_detalhada, use_container_width=True)

                campeao = tabela_detalhada.index[0]
                pontos_campeao = tabela_detalhada.iloc[0]["Total Semana"]

                st.success(f"👑 **Vencedor(a) da Semana:** {campeao} com um total de **{int(pontos_campeao)} pts**!")

    st.markdown("---")
    if st.button("🎉 Salvar Campeão da Semana no Histórico", use_container_width=True):
        if not df_pontos.empty:
            df_temp = df_pontos.copy()
            df_temp["Data_Parsed"] = pd.to_datetime(df_temp["Data"], errors="coerce")
            df_temp["Ano_Semana"] = df_temp["Data_Parsed"].apply(
                lambda x: f"Ano {x.isocalendar()[0]} - Semana {x.isocalendar()[1]}" if pd.notnull(x) else ""
            )
            df_semana_atual = df_temp[df_temp["Ano_Semana"] == semana_selecionada]

            if not df_semana_atual.empty:
                ranking_semana = df_semana_atual.groupby("Integrante")["Pontos"].sum().reset_index()
                ranking_semana = ranking_semana.sort_values(by="Pontos", ascending=False).reset_index(drop=True)
                campeao = ranking_semana.iloc[0]["Integrante"]
                pontos_campeao = ranking_semana.iloc[0]["Pontos"]

                historico = carregar_historico_json()
                historico[semana_selecionada] = {
                    "campeao": campeao,
                    "pontos": int(pontos_campeao),
                    "ranking_completo": ranking_semana.to_dict(orient="records"),
                    "data_apuracao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                }
                salvar_historico_json(historico)
                st.balloons()
                st.success(f"Campeão da {semana_selecionada} guardado com sucesso no histórico!")
