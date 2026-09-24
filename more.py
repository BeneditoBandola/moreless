import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import json
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Multitemas de Terror - Ranking & Patentes", page_icon="🦇", layout="centered")

ARQUIVO_DADOS = "pontuacoes_equipe.csv"
ARQUIVO_INTEGRANTES = "integrantes_equipe.csv"
ARQUIVO_HISTORICO_JSON = "historico_semanas.json"

# --- CONFIGURAÇÃO DOS TEMAS (TODOS COM PEGADA DE TERROR, ADAPTADOS) ---
TEMAS = {
    "💀 Cemitério Gótico": {
        "bg_app": "#09090B",
        "card_bg": "linear-gradient(135deg, #120A2A, #09090B)",
        "border_color": "#4C1D95",
        "text_color": "#E4E4E7",
        "accent_color": "#A855F7",
        "icone": "💀",
        "patentes": {100: "💀 Necromante Supremo", 75: "🦇 Senhor(a) da Noite", 50: "⚰️ Zumbi Insaciável", 25: "🕯️ Alma Penada", 0: "🦴 Ossinho Frágil"},
        "mensagens": [
            "As catacumbas guardam os segredos daqueles que não entregaram as metas...",
            "O roxo da meia-noite cobre os corredores enquanto o sistema aguarda.",
            "Cuidado com os passos falsos... o coveiro está sempre de olho nos relatórios."
        ]
    },
    "👰 Noiva Fantasma": {
        "bg_app": "#18181B",
        "card_bg": "linear-gradient(135deg, #27272A, #09090B)",
        "border_color": "#F472B6",
        "text_color": "#F4F4F5",
        "accent_color": "#FB7185",
        "icone": "👰",
        "patentes": {100: "💍 Noiva Espectral", 75: "💐 Dama do Véu Sangrento", 50: "🕊️ Assombração Romântica", 25: "💌 Aparição Solitária", 0: "🎀 Alma Abandonada no Altar"},
        "mensagens": [
            "Até que o erro do sistema nos separe para todo o sempre...",
            "Um véu rasgado, passos no altar vazio e prazos que nunca morrem.",
            "A promessa era eterna, assim como a pilha de pendências na sua mesa."
        ]
    },
    "💖 Meninas Sombrias": {
        "bg_app": "#1A0A1C",
        "card_bg": "linear-gradient(135deg, #3B0764, #18181B)",
        "border_color": "#EC4899",
        "text_color": "#FCE7F3",
        "accent_color": "#F43F5E",
        "icone": "💖",
        "patentes": {100: "👑 Rainha Vampira do Poder", 75: "💅 Ícone Gótico Chic", 50: "✨ Boneca Possuída de Ouro", 25: "🌸 Fada das Trevas", 0: "☕ Garota do Café Amaldiçoado"},
        "mensagens": [
            "Garotas estilosas conquistam qualquer meta... mesmo que precisem morder alguém.",
            "Brilhe na escuridão e mostre o seu poder com muito charme.",
            "Foco, café frio, batom escuro e metas batidas nas sombras!"
        ]
    },
    "🌈 Alegria Macabra": {
        "bg_app": "#0A1F1C",
        "card_bg": "linear-gradient(135deg, #064E3B, #09090B)",
        "border_color": "#34D399",
        "text_color": "#ECFDF5",
        "accent_color": "#10B981",
        "icone": "🌈",
        "patentes": {100: "🌟 Unicórnio Zumbi Radiante", 75: "🦄 Criatura Mágica do Pântano", 50: "🌻 Girassol Carnívoro", 25: "🎈 Palhaço Sinistro Feliz", 0: "🌱 Sementinha Assombrada"},
        "mensagens": [
            "Sorria! Cada pontinho de hoje atrai um raio de sol... ou um raio laser mortal!",
            "A alegria contagiante (literalmente um vírus zumbi) vai te ajudar a bater metas!",
            "Espalhe energia positiva e fuja correndo dos monstros do escritório!"
        ]
    },
    "💻 Cyber Terror": {
        "bg_app": "#030712",
        "card_bg": "linear-gradient(135deg, #0F172A, #030712)",
        "border_color": "#06B6D4",
        "text_color": "#E2E8F0",
        "accent_color": "#22D3EE",
        "icone": "💻",
        "patentes": {100: "🤖 IA Assassina da Matrix", 75: "⚡ Hacker do Além-Túmulo", 50: "💻 Programador(a) zumbi", 25: "⌨️ Fantasma na Máquina", 0: "🔌 Desconectado(a) no Vazio"},
        "mensagens": [
            "Executando rotina de abdução de dados... 100% concluído.",
            "O código está assombrado, o servidor caiu, que comece o pânico.",
            "Cuidado com os bugs mutantes na matrix corporativa."
        ]
    },
    "☕ Terror no Escritório": {
        "bg_app": "#0F0F13",
        "card_bg": "linear-gradient(135deg, #1E1B4B, #09090B)",
        "border_color": "#6366F1",
        "text_color": "#E0E7FF",
        "accent_color": "#818CF8",
        "icone": "☕",
        "patentes": {100: "👔 CEO dos Pesadelos", 75: "📊 Diretor(a) das Almas Perdidas", 50: "💼 Gerente Espectral", 25: "📋 Estagiário(a) Zumbi", 0: "☕ Viciado(a) em Café Frio"},
        "mensagens": [
            "Reunião que podia ser um e-mail? Não, esta é uma maldição sem fim!",
            "O café acabou, a planilha travou e o prazo venceu à meia-noite.",
            "Organização corporativa e terror administrativo caminham juntos."
        ]
    }
}

# --- BARRA LATERAL (CONFIGURAÇÕES E TEMAS) ---
st.sidebar.title("🎨 Personalização")
tema_escolhido = st.sidebar.selectbox("Escolha o Tema Sombrio:", list(TEMAS.keys()))
t = TEMAS[tema_escolhido]

st.sidebar.markdown("---")
st.sidebar.title("⚙️ Exibição")
ocultar_boas_vindas = st.sidebar.checkbox("Ocultar mensagem de boas-vindas", value=False)

# --- APLICAR CSS DINÂMICO CONFORME O TEMA (Chaves duplicadas para evitar conflito com f-string) ---
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
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    }}
    @media (max-width: 768px) {{
        h1 {{ font-size: 22px !important; }}
        h2 {{ font-size: 18px !important; }}
        h3 {{ font-size: 16px !important; }}
    }}
    </style>
""", unsafe_allow_html=True)

CORES_PADRAO = {
    "Benedito": "#2563EB",
    "Bárbara": "#DB2777",
    "Vinícius": "#059669",
    "Samuel": "#D97706",
    "Gabrielle": "#8B5CF6"
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
            <h3 style="margin: 0; color: {t["accent_color"]};">{t["icone"]} Painel Sombrio - {tema_escolhido}</h3>
            <p style="font-size: 13px; opacity: 0.7; margin-top: 2px;">📅 Data do Ritual: <b>{datetime.today().strftime('%d/%m/%Y')}</b></p>
            <hr style="border: 0.5px solid {t["border_color"]}; margin: 8px 0;">
            <p style="font-size: 14px; margin: 0; font-style: italic;">"{mensagem_dia}"</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.title(f"{t['icone']} Ranking & Patentes das Trevas")
st.markdown("---")

# --- ABAS OTIMIZADAS PARA CELULAR ---
aba_lancamento, aba_ranking, aba_admin = st.tabs(["📝 Registrar", "🏆 Ranking", "⚙️ Gestão"])

with aba_lancamento:
    st.subheader("Registrar Oferenda de Pontos")
    with st.form("form_pontuacao", clear_on_submit=True):
        lista_nomes = list(carregar_integrantes().keys())
        integrante = st.selectbox("Escolha o Adepto:", lista_nomes)
        data_lancamento = st.date_input("Data do Sacrifício:", value=datetime.today())
        pontos = st.number_input("Pontos (Máximo 25):", min_value=0, max_value=25, step=1, format="%d")
        observacao = st.text_input("Sussurro / Observação (Opcional):")
        enviado = st.form_submit_button("🔥 Consagrar Pontuação", use_container_width=True)

        if enviado:
            if not integrante:
                st.warning("Selecione o adepto.")
            else:
                nova_linha = pd.DataFrame([{
                    "Data": data_lancamento.strftime("%Y-%m-%d"),
                    "Integrante": integrante,
                    "Pontos": int(pontos),
                    "Observação": observacao if observacao else ""
                }])
                df_pontos = pd.concat([df_pontos, nova_linha], ignore_index=True)
                df_pontos.to_csv(ARQUIVO_DADOS, index=False)
                st.success("Pontuação registrada nas sombras com sucesso!")
                st.rerun()

with aba_ranking:
    if not df_pontos.empty:
        st.subheader("📊 Estatísticas do Além")
        total_pontos_geral = df_pontos["Pontos"].sum()
        maior_pontuacao_dia = df_pontos["Pontos"].max()

        c1, c2 = st.columns(2)
        c1.metric("Almas Acumuladas", f"{int(total_pontos_geral)} pts")
        c2.metric("Pico de Terror Diário", f"{int(maior_pontuacao_dia)} pts")

        st.markdown("---")
        st.subheader("🥇 Hierarquia Sombria")

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

        st.markdown("### 📈 Gráfico de Almas Coletadas")
        st.bar_chart(ranking_geral.set_index("Integrante")["Total_Pontos"])

        st.markdown("---")
        st.subheader("📋 Livro de Registros Recentes")
        st.dataframe(df_exibicao.sort_values(by="Data", ascending=False), use_container_width=True)
    else:
        st.info("Nenhum ritual registrado nas catacumbas ainda.")

with aba_admin:
    st.subheader("➕ Despertar Novo Integrante")
    with st.form("form_novo_integrante", clear_on_submit=True):
        novo_nome = st.text_input("Nome do Adepto:")
        nova_cor = st.color_picker("Cor Sombria de Destaque:", t["accent_color"])
        cadastrar_btn = st.form_submit_button("Consagrar Adepto", use_container_width=True)
        
        if cadastrar_btn:
            if novo_nome.strip():
                if novo_nome.strip() in integrantes_cores:
                    st.warning("Este espírito já habita o cemitério!")
                else:
                    salvar_integrante(novo_nome.strip(), nova_cor)
                    st.success(f"{novo_nome.strip()} foi despertado com sucesso!")
                    st.rerun()
            else:
                st.warning("Digite um nome válido.")

    st.markdown("---")
    if st.button("🎉 Julgar e Apurar Campeão da Semana", use_container_width=True):
        if df_pontos.empty:
            st.warning("Sem pontuações para realizar o julgamento!")
        else:
            df_pontos['Data_Parsed'] = pd.to_datetime(df_pontos['Data'], errors='coerce')
            hoje = datetime.today()
            ano_atual, semana_atual, _ = hoje.isocalendar()
            chave_semana = f"Ano {ano_atual} - Semana {semana_atual}"
            
            df_pontos['Ano_Semana'] = df_pontos['Data_Parsed'].apply(lambda x: f"Ano {x.isocalendar()[0]} - Semana {x.isocalendar()[1]}" if pd.notnull(x) else "")
            df_semana_atual = df_pontos[df_pontos['Ano_Semana'] == chave_semana]
            
            if df_semana_atual.empty:
                st.warning(f"Nenhum ritual encontrado na semana ({chave_semana}).")
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
                st.success(f"🦇 O(A) Senhor(a) Supremo(a) da Semana é {campeao} com {int(pontos_campeao)} pts!")
