from datetime import datetime
import os
from pathlib import Path
import random
import altair as alt
import pandas as pd
import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Multitemas - Ranking & Patentes",
    page_icon="✨",
    layout="centered",
)

PASTA_SCRIPT = Path(__file__).resolve().parent
ARQUIVO_INTEGRANTES = PASTA_SCRIPT / "integrantes_equipe.csv"
ARQUIVO_DADOS_CSV = PASTA_SCRIPT / "banco_dados.csv"
PASTA_FOTOS = PASTA_SCRIPT / "fotos_integrantes"

if not PASTA_FOTOS.exists():
    PASTA_FOTOS.mkdir(parents=True, exist_ok=True)

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
    },
}

# --- BARRA LATERAL ---
st.sidebar.title("🎨 Personalização")
tema_escolhido = st.sidebar.selectbox("Escolha o Tema Visual:", list(TEMAS.keys()))
t = TEMAS[tema_escolhido]

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
    "Bárbara": {"Cor": "#DB2777", "Foto": str(PASTA_FOTOS / "Barbara.jpg")},
    "Benedito": {"Cor": "#2563EB", "Foto": str(PASTA_FOTOS / "Benedito.jpg")},
    "Samuel": {"Cor": "#D97706", "Foto": str(PASTA_FOTOS / "Samuel.jpg")},
    "Vinícius": {"Cor": "#059669", "Foto": str(PASTA_FOTOS / "Vinicius.jpg")},
    "Gabrielle": {"Cor": "#8B5CF6", "Foto": str(PASTA_FOTOS / "Gabrielle.jpg")},
}

def carregar_integrantes():
    if ARQUIVO_INTEGRANTES.exists():
        df_int = pd.read_csv(ARQUIVO_INTEGRANTES)
        if "Avatar" in df_int.columns and "Foto" not in df_int.columns:
            df_int = df_int.rename(columns={"Avatar": "Foto"})
        if "Foto" not in df_int.columns:
            df_int["Foto"] = ""
        if "Cor" not in df_int.columns:
            df_int["Cor"] = "#2563EB"
        return df_int.set_index("Nome").to_dict(orient="index")
    else:
        dados_lista = []
        for nome, info in INTEGRANTES_PADRAO.items():
            dados_lista.append({"Nome": nome, "Cor": info["Cor"], "Foto": info["Foto"]})
        df_int = pd.DataFrame(dados_lista)
        df_int.to_csv(ARQUIVO_INTEGRANTES, index=False)
        return df_int.set_index("Nome").to_dict(orient="index")

def salvar_integrante(nome, cor, caminho_foto):
    integrantes_dict = carregar_integrantes()
    integrantes_dict[nome] = {"Cor": cor, "Foto": caminho_foto}
    dados_lista = []
    for n, info in integrantes_dict.items():
        dados_lista.append({"Nome": n, "Cor": info.get("Cor", "#2563EB"), "Foto": info.get("Foto", "")})
    df_int = pd.DataFrame(dados_lista)
    df_int.to_csv(ARQUIVO_INTEGRANTES, index=False)

# --- SISTEMA DE DADOS SIMPLES (CSV LOCAL) ---
def carregar_dados_local():
    if ARQUIVO_DADOS_CSV.exists():
        try:
            df = pd.read_csv(ARQUIVO_DADOS_CSV)
            if df.empty or not all(col in df.columns for col in ["Data", "Integrante", "Pontos", "Observação"]):
                return pd.DataFrame(columns=["Data", "Integrante", "Pontos", "Observação"])
            df["Pontos"] = pd.to_numeric(df["Pontos"], errors="coerce").fillna(0).astype(int)
            df["Observação"] = df["Observação"].fillna("").astype(str)
            df["Data"] = pd.to_datetime(df["Data"], errors="coerce").dt.strftime("%Y-%m-%d")
            return df.dropna(subset=["Data", "Integrante"])
        except Exception as e:
            return pd.DataFrame(columns=["Data", "Integrante", "Pontos", "Observação"])
    else:
        df_inicial = pd.DataFrame(columns=["Data", "Integrante", "Pontos", "Observação"])
        df_inicial.to_csv(ARQUIVO_DADOS_CSV, index=False)
        return df_inicial

def salvar_registro_local(data_str, integrante, pontos, observacao):
    try:
        df = carregar_dados_local()
        novo_df = pd.DataFrame([{
            "Data": str(data_str),
            "Integrante": str(integrante),
            "Pontos": int(pontos),
            "Observação": str(observacao)
        }])
        df = pd.concat([df, novo_df], ignore_index=True)
        df.to_csv(ARQUIVO_DADOS_CSV, index=False)
        return True
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")
        return False

def obter_classificacao(pontos, patentes):
    for limite in sorted(patentes.keys(), reverse=True):
        if pontos >= limite:
            return patentes[limite]
    return list(patentes.values())[-1]

integrantes_info = carregar_integrantes()
df_pontos = carregar_dados_local()

st.title(f"{t['icone']} Ranking & Patentes")
st.markdown("---")

aba_lancamento, aba_ranking, aba_podio, aba_admin = st.tabs(["📝 Registrar", "🏆 Ranking", "🥇 Pódio", "⚙ Gestão"])

with aba_lancamento:
    st.subheader("Registrar Pontuação por Data")
    with st.form("form_pontuacao", clear_on_submit=True):
        lista_nomes = list(integrantes_info.keys())
        integrante = st.selectbox("Escolha o Integrante:", lista_nomes)
        
        if integrante in integrantes_info and integrantes_info[integrante].get("Foto"):
            foto_path = integrantes_info[integrante]["Foto"]
            if foto_path and Path(foto_path).exists():
                st.image(foto_path, width=80)

        data_lancamento = st.date_input("Data:", value=datetime.today())
        pontos = st.number_input("Pontos (Máximo 25):", min_value=0, max_value=25, step=1, format="%d")
        observacao = st.text_input("Observação (Opcional):")
        enviado = st.form_submit_button("🔥 Registrar Pontuação", use_container_width=True)

        if enviado:
            if not integrante:
                st.warning("Selecione o integrante.")
            else:
                data_str = data_lancamento.strftime("%Y-%m-%d")
                sucesso = salvar_registro_local(data_str, integrante, pontos, observacao)
                if sucesso:
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
        st.subheader("🥇 Ranking Atual")

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
        ranking_geral["Patente"] = ranking_geral["Total_Pontos"].apply(
            lambda x: obter_classificacao(x, t["patentes"])
        )
        ranking_geral["Cor"] = ranking_geral["Integrante"].apply(
            lambda x: integrantes_info.get(x, {}).get("Cor", t["accent_color"])
        )

        for idx, row in ranking_geral.iterrows():
            nome_int = row["Integrante"]
            total_pts = row["Total_Pontos"]
            patente = row["Patente"]
            pos = row["Posição"]
            
            info_int = integrantes_info.get(nome_int, {})
            foto = info_int.get("Foto", "")
            cor_int = info_int.get("Cor", t["accent_color"])

            col_foto, col_info, col_pts = st.columns([1, 4, 2])
            with col_foto:
                if foto and Path(foto).exists():
                    st.image(foto, width=70)
                else:
                    st.markdown("👤")
            with col_info:
                st.markdown(f"<h3 style='color: {cor_int}; margin: 0;'>#{pos} - {nome_int}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size: 15px; margin: 2px 0;'>Patente: <b>{patente}</b></p>", unsafe_allow_html=True)
            with col_pts:
                st.markdown(f"<h2 style='margin: 0; text-align: right;'>{int(total_pts)} pts</h2>", unsafe_allow_html=True)
            st.divider()

        st.markdown("### 📈 Gráfico de Pontuação Personalizado")
        chart = alt.Chart(ranking_geral).mark_bar().encode(
            x=alt.X('Integrante:N', sort='-y', title='Integrante'),
            y=alt.Y('Total_Pontos:Q', title='Pontos Totais'),
            color=alt.Color('Integrante:N', scale=alt.Scale(domain=list(ranking_geral['Integrante']), range=list(ranking_geral['Cor'])), legend=None),
            tooltip=['Integrante', 'Total_Pontos', 'Patente']
        ).properties(height=300)
        
        st.altair_chart(chart, use_container_width=True)

        st.markdown("---")
        st.subheader("📋 Livro de Registros Recentes")
        df_exibicao = df_pontos.copy()
        df_exibicao["Data"] = pd.to_datetime(df_exibicao["Data"]).dt.strftime("%d/%m/%Y")
        st.dataframe(df_exibicao.sort_values(by="Data", ascending=False).reset_index(drop=True), use_container_width=True)
    else:
        st.info("Nenhum registo encontrado. Use a aba 'Registrar' para adicionar pontuações.")

with aba_podio:
    st.subheader("🏆 Ranking Atual - Pódio")
    if not df_pontos.empty:
        ranking_podio = (
            df_pontos.groupby("Integrante")["Pontos"].sum().reset_index()
            .sort_values(by="Pontos", ascending=False)
            .reset_index(drop=True)
        )

        p = {}
        for idx, row in ranking_podio.head(5).iterrows():
            p[idx + 1] = {
                "nome": row["Integrante"],
                "pontos": int(row["Pontos"]),
                "foto": integrantes_info.get(row["Integrante"], {}).get("Foto", ""),
                "cor": integrantes_info.get(row["Integrante"], {}).get("Cor", t["accent_color"])
            }

        titulos_colunas = {1: "🥇 1º Lugar", 2: "🥈 2º Lugar", 3: "🥉 3º Lugar", 4: "4º Lugar", 5: "5º Lugar"}

        for i in range(1, len(p) + 1):
            dados = p[i]
            col_pos, col_foto, col_nome, col_pts = st.columns([1.5, 1, 3, 2])
            
            with col_pos:
                st.markdown(f"<h4 style='color: #FFD700; margin-top: 15px;'>{titulos_colunas[i]}</h4>", unsafe_allow_html=True)
            with col_foto:
                if dados["foto"] and Path(dados["foto"]).exists():
                    st.image(dados["foto"], width=65)
                else:
                    st.markdown("<div style='font-size: 35px;'>👤</div>", unsafe_allow_html=True)
            with col_nome:
                st.markdown(f"<h3 style='color: {dados['cor']}; margin-top: 15px;'>{dados['nome']}</h3>", unsafe_allow_html=True)
            with col_pts:
                st.markdown(f"<h3 style='margin-top: 15px; text-align: right;'>{dados['pontos']} pts</h3>", unsafe_allow_html=True)
            st.divider()
    else:
        st.info("Nenhum dado disponível para montar o pódio.")

with aba_admin:
    st.subheader("⚙ Configuração, Gestão e Exclusão de Registros")
    
    st.markdown("### 🗑️ Apagar Lançamento Incorreto")
    if not df_pontos.empty:
        df_excluir = df_pontos.copy().reset_index().rename(columns={"index": "Indice_Original"})
        df_excluir["Exibicao"] = df_excluir.index.astype(str) + " - " + df_excluir["Data"] + " | " + df_excluir["Integrante"] + " | " + df_excluir["Pontos"].astype(str) + " pts (" + df_excluir["Observação"] + ")"
        
        linha_selecionada = st.selectbox("Selecione o registo que deseja apagar:", df_excluir["Exibicao"])
        
        if st.button("❌ Apagar Registo Selecionado", use_container_width=True):
            idx_escolhido = int(linha_selecionada.split(" - ")[0])
            df_novo = df_pontos.drop(df_pontos.index[idx_escolhido]).reset_index(drop=True)
            df_novo.to_csv(ARQUIVO_DADOS_CSV, index=False)
            st.success("Registo apagado com sucesso!")
            st.rerun()
    else:
        st.info("Não há registos para apagar.")

    st.markdown("---")
    
    st.markdown("### 💾 Gestão de Ficheiro de Dados (Backup)")
    col_dl, col_ul = st.columns(2)
    
    with col_dl:
        st.write("Guardar dados atuais no PC:")
        if ARQUIVO_DADOS_CSV.exists():
            with open(ARQUIVO_DADOS_CSV, "rb") as f:
                st.download_button(
                    label="📥 Baixar Backup (CSV)",
                    data=f,
                    file_name="banco_dados.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        else:
            st.info("Ainda sem dados para baixar.")
            
    with col_ul:
        st.write("Restaurar / Enviar dados anteriores:")
        arquivo_upload = st.file_uploader("Carregar 'banco_dados.csv':", type=["csv"])
        if arquivo_upload is not None:
            try:
                df_up = pd.read_csv(arquivo_upload)
                df_up.to_csv(ARQUIVO_DADOS_CSV, index=False)
                st.success("Dados restaurados com sucesso! Recarregue a página.")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao carregar ficheiro: {e}")

    st.markdown("---")
    st.subheader("🖼️ Gerenciar Fotos dos Integrantes")
    integrante_foto_sel = st.selectbox("Selecione o Integrante para Upar/Trocar a Foto:", list(integrantes_info.keys()))
    
    if integrante_foto_sel:
        info_sel = integrantes_info[integrante_foto_sel]
        col_atual, col_up = st.columns([1, 2])
        
        with col_atual:
            st.write("Foto Atual:")
            if info_sel.get("Foto") and Path(info_sel["Foto"]).exists():
                st.image(info_sel["Foto"], width=100)
            else:
                st.markdown("Nenhuma foto cadastrada.")
                
        with col_up:
            with st.form(f"form_foto_{integrante_foto_sel}"):
                nova_foto_file = st.file_uploader("Enviar Nova Foto (JPG/PNG):", type=["png", "jpg", "jpeg"])
                nova_cor_picker = st.color_picker("Cor de Destaque:", info_sel.get("Cor", "#2563EB"))
                btn_salvar_foto = st.form_submit_button("Salvar Alterações", use_container_width=True)
                
                if btn_salvar_foto:
                    caminho_salvo = info_sel.get("Foto", "")
                    if nova_foto_file is not None:
                        caminho_salvo = str(PASTA_FOTOS / f"{integrante_foto_sel}.jpg")
                        with open(caminho_salvo, "wb") as f:
                            f.write(nova_foto_file.getbuffer())
                    
                    salvar_integrante(integrante_foto_sel, nova_cor_picker, caminho_salvo)
                    st.success(f"Configurações de {integrante_foto_sel} atualizadas com sucesso!")
                    st.rerun()

    st.markdown("---")
    st.subheader("➕ Adicionar Novo Integrante")
    with st.form("form_novo_integrante", clear_on_submit=True):
        novo_nome = st.text_input("Nome:")
        nova_cor = st.color_picker("Cor de Destaque:", t["accent_color"])
        arquivo_foto = st.file_uploader("Carregar Foto (PNG/JPG):", type=["png", "jpg", "jpeg"])
        cadastrar_btn = st.form_submit_button("Cadastrar Integrante", use_container_width=True)

        if cadastrar_btn:
            if novo_nome.strip():
                if novo_nome.strip() in integrantes_info:
                    st.warning("Este integrante já existe!")
                else:
                    caminho_foto_salva = ""
                    if arquivo_foto is not None:
                        caminho_foto_salva = str(PASTA_FOTOS / f"{novo_nome.strip()}.jpg")
                        with open(caminho_foto_salva, "wb") as f:
                            f.write(arquivo_foto.getbuffer())
                    
                    salvar_integrante(novo_nome.strip(), nova_cor, caminho_foto_salva)
                    st.success(f"{novo_nome.strip()} cadastrado com sucesso!")
                    st.rerun()
            else:
                st.warning("Digite um nome válido.")
