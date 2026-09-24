import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import json
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Multitemas - Ranking & Patentes", page_icon="✨", layout="centered")

ARQUIVO_DADOS = "pontuacoes_equipe.csv"
ARQUIVO_INTEGRANTES = "integrantes_equipe.csv"
ARQUIVO_HISTORICO_JSON = "historico_semanas.json"

# --- PATENTES ORIGINAIS (APLICADAS A TODOS OS TEMAS) ---
PATENTES_ORIGINAIS = {
    100: "👑 Deus Supremo",
    75: "🐐 Cabrito Sagrado",
    50: "🐎 Égua Satânica",
    25: "🐴 Mula Juvenil",
    0: "🎒 Mochila de Criança"
}

# --- CONFIGURAÇÃO DOS TEMAS COM CORES E ESTILOS CORRIGIDOS ---
TEMAS = {
    "💀 Cemitério Gótico": {
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
            "Cuidado com os passos falsos... o coveiro está sempre de olho nos relatórios."
        ]
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
            "Até que o fechamento da planilha nos una para sempre no altar!",
            "Um casamento perfeito exige buquê lindo, convidados felizes e metas batidas."
        ]
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
            "Foco, café, look do dia impecável e metas batidas com sucesso!"
        ]
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
            "Executando rotina de otimização de dados... 100% de eficiência concluída.",
            "O código está limpo, o deploy foi feito com sucesso e o sistema voa.",
            "Conectado na matrix corporativa, processando cada desafio com inovação."
        ]
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
            "O café quentinho está na xícara e a planilha aberta para começar o dia.",
            "Organização, networking e foco nas entregas definem o sucesso de hoje."
        ]
    }
}

# --- BARRA LATERAL (CONFIGURAÇÕES E TEMAS) ---
st.sidebar.title("🎨 Personalização")
tema_escolhido = st.sidebar.selectbox("Escolha o Tema Visual:", list(TEMAS.keys()))
t = TEMAS[tema_escolhido]

st.sidebar.markdown("---")
st.sidebar.title("⚙️ Exibição")
ocultar_boas_vindas = st.sidebar.checkbox("Ocultar mensagem de boas-vindas", value=False)

# --- APLICAR CSS CORRIGIDO PARA EVITAR TEXTO INVISÍVEL ---
st.markdown(f"""
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
    @media (max-width: 768px) {{
        h1 {{ font-size: 22px !important; }}
        h2 {{ font-size: 18px !important; }}
        h3 {{ font-size: 16px !important; }}
    }}
    </style>
""", unsafe_allow_html=True)

# Cores padrão incluindo a Tuane e a Gabrielle
CORES_PADRAO = {
    "Benedito": "#2563EB",
    "Bárbara": "#DB2777",
    "Vinícius": "#059669",
    "Samuel": "#D97706",
    "Gabrielle": "#8B5CF6",
    "Tuane": "#0891B2"  # Azul-petróleo elegante
}

def carregar_integrantes():
    if os.path.exists(ARQUIVO_INTEGRANTES):
        df_int = pd.read_csv(ARQUIVO_INTEGRANTES)
        return dict(zip(df_int["Nome"], df_int["Cor"]))
    else:
        df_int = pd.DataFrame(list(CORES_PADRAO.items()), columns=["Nome", "Cor"])
        df_int.to_csv(ARQUIVO_INTEGRANTES, index=False)
        return CORES_PADRAO

def salvar_integrante(nome, cor):
    df_int = pd.DataFrame(list(carregar_integrantes().items()), columns=["Nome", "Cor"])
    if nome not in df_int["Nome"].values:
        nova_linha = pd.DataFrame([{"Nome": nome, "Cor": cor}])
        df_int = pd.concat([df_int, nova_linha], ignore_index=True)
        df_int.to_csv(ARQUIVO_INTEGRANTES, index=False)

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        return pd.read_csv(ARQUIVO_DADOS)
    else:
        return pd.DataFrame(columns=["Data", "Integrante", "Pontos", "Observação"])

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

integrantes_cores = carregar_integrantes()
df_pontos = carregar_dados()

# --- TELA DE BOAS-VINDAS CONDICIONAL ---
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
        unsafe_allow_html=True
    )

st.title(f"{t['icone']} Ranking & Patentes")
st.markdown("---")

# --- ABAS OTIMIZADAS PARA CELULAR ---
aba_lancamento, aba_ranking, aba_admin = st.tabs(["📝 Registrar", "🏆 Ranking", "⚙️ Gestão"])

with aba_lancamento:
    st.subheader("Registrar Pontuação")
    with st.form("form_pontuacao", clear_on_submit=True):
        lista_nomes = list(carregar_integrantes().keys())
        integrante = st.selectbox("Escolha o Integrante:", lista_nomes)
        data_lancamento = st.date_input("Data:", value=datetime.today())
        pontos = st.number_input("Pontos (Máximo 25):", min_value=0, max_value=25, step=1, format="%d")
        observacao = st.text_input("Observação (Opcional):")
        enviado = st.form_submit_button("🔥 Registrar Pontuação", use_container_width=True)

        if enviado:
            if not integrante:
                st.warning("Selecione o integrante.")
            else:
                nova_linha = pd.DataFrame([{
                    "Data": data_lancamento.strftime("%Y-%m-%d"),
                    "Integrante": integrante,
                    "Pontos": int(pontos),
                    "Observação": observacao if observacao else ""
                }])
                df_pontos = pd.concat([df_pontos, nova_linha], ignore_index=True)
                df_pontos.to_csv(ARQUIVO_DADOS, index=False)
                st.success("Pontuação registrada com sucesso!")
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

        ranking_geral = df_pontos.groupby("Integrante").agg(
            Total_Pontos=("Pontos", "sum"),
            Dias_Trabalhados=("Pontos", "count")
        ).reset_index()

        ranking_geral = ranking_geral.sort_values(by="Total_Pontos", ascending=False).reset_index(drop=True)
        ranking_geral.index = ranking_geral.index + 1
        ranking_geral.index.name = "Posição"
        ranking_geral = ranking_geral.reset_index()
        
        ranking_geral["Patente"] = ranking_geral["Total_Pontos"].apply(lambda x: obter_classificacao(x, t["patentes"]))

        df_exibicao = df_pontos.copy()
        df_exibicao['Data'] = pd.to_datetime(df_exibicao['Data']).dt.strftime('%d/%m/%Y')

        tabela_exib = ranking_geral[["Posição", "Integrante", "Total_Pontos", "Patente"]].rename(columns={
            "Total_Pontos": "Total"
        })
        st.dataframe(tabela_exib, use_container_width=True)

        st.markdown("### 📈 Gráfico de Pontuação")
        st.bar_chart(ranking_geral.set_index("Integrante")["Total_Pontos"])

        st.markdown("---")
        st.subheader("📋 Livro de Registros Recentes")
        st.dataframe(df_exibicao.sort_values(by="Data", ascending=False), use_container_width=True)
    else:
        st.info("Nenhum registro encontrado ainda.")

with aba_admin:
    st.subheader("➕ Adicionar Novo Integrante")
    with st.form("form_novo_integrante", clear_on_submit=True):
        novo_nome = st.text_input("Nome:")
        nova_cor = st.color_picker("Cor de Destaque:", t["accent_color"])
        cadastrar_btn = st.form_submit_button("Cadastrar Integrante", use_container_width=True)
        
        if cadastrar_btn:
            if novo_nome.strip():
                if novo_nome.strip() in integrantes_cores:
                    st.warning("Este integrante já existe!")
                else:
                    salvar_integrante(novo_nome.strip(), nova_cor)
                    st.success(f"{novo_nome.strip()} cadastrado com sucesso!")
                    st.rerun()
            else:
                st.warning("Digite um nome válido.")

    st.markdown("---")
    if st.button("🎉 Apurar Campeão da Semana", use_container_width=True):
        if df_pontos.empty:
            st.warning("Sem pontuações para apurar!")
        else:
            df_pontos['Data_Parsed'] = pd.to_datetime(df_pontos['Data'], errors='coerce')
            hoje = datetime.today()
            ano_atual, semana_atual, _ = hoje.isocalendar()
            chave_semana = f"Ano {ano_atual} - Semana {semana_atual}"
            
            df_pontos['Ano_Semana'] = df_pontos['Data_Parsed'].apply(lambda x: f"Ano {x.isocalendar()[0]} - Semana {x.isocalendar()[1]}" if pd.notnull(x) else "")
            df_semana_atual = df_pontos[df_pontos['Ano_Semana'] == chave_semana]
            
            if df_semana_atual.empty:
                st.warning(f"Nenhum lançamento encontrado na semana ({chave_semana}).")
            else:
                ranking_semana = df_semana_atual.groupby("Integrante")["Pontos"].sum().reset_index()
                ranking_semana = ranking_semana.sort_values(by="Pontos", ascending=False).reset_index(drop=True)
                campeao = ranking_semana.iloc[0]["Integrante"]
                pontos_campeao = ranking_semana.iloc[0]["Pontos"]
                
                historico = carregar_historico_json()
                historico[chave_semana] = {
                    "campeao": campeao,
                    "pontos": int(pontos_campeao),
                    "ranking_completo": ranking_semana.to_dict(orient="records"),
                    "data_apuracao": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                }
                salvar_historico_json(historico)
                st.balloons()
                st.success(f"👑 O(A) grande campeão(ã) da semana é {campeao} com {int(pontos_campeao)} pts!")
