import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Ranking & Campeão da Semana", page_icon="🏆", layout="wide")

ARQUIVO_DADOS = "pontuacoes_equipe.csv"
ARQUIVO_INTEGRANTES = "integrantes_equipe.csv"

# Cores padrão para os integrantes iniciais
CORES_PADRAO = {
    "Benedito": "#1E3A8A",      # Azul Escuro
    "Bárbara": "#DB2777",      # Rosa / Magenta
    "Vinícius": "#059669",     # Verde Esmeralda
    "Samuel": "#D97706"        # Laranja / Âmbar
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

integrantes_cores = carregar_integrantes()
df_pontos = carregar_dados()

st.title("🏆 Ranking & Apuração do Campeão da Semana")
st.markdown("Registre sua pontuação diária (máximo de 25 pontos) e descubra quem é o campeão da semana!")
st.markdown("---")

# --- BOTÃO DE VERIFICAR CLASSIFICAÇÃO / CAMPEÃO DA SEMANA ---
if st.button("🎉 VERIFICAR CLASSIFICAÇÃO & CAMPEÃO DA SEMANA!", use_container_width=True):
    if df_pontos.empty:
        st.warning("Ainda não há pontuações cadastradas para apurar o campeão!")
    else:
        df_pontos['Data_Parsed'] = pd.to_datetime(df_pontos['Data'], errors='coerce')
        hoje = pd.to_datetime(datetime.today().date())
        inicio_semana = hoje - timedelta(days=7)
        
        # Filtrar dados dos últimos 7 dias
        df_semana = df_pontos[df_pontos['Data_Parsed'] >= inicio_semana]
        
        if df_semana.empty:
            st.info("Nenhum lançamento registrado nos últimos 7 dias. Mostrando campeão do histórico geral:")
            df_semana = df_pontos.copy()
            
        ranking_semana = df_semana.groupby("Integrante")["Pontos"].sum().reset_index()
        ranking_semana = ranking_semana.sort_values(by="Pontos", ascending=False).reset_index(drop=True)
        
        campeao = ranking_semana.iloc[0]["Integrante"]
        pontos_campeao = ranking_semana.iloc[0]["Pontos"]
        cor_campeao = integrantes_cores.get(campeao, "#2563EB")
        
        # --- QUADRO ALEGRE DE PREMIAÇÃO ---
        st.balloons()
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, {cor_campeao}, #F59E0B); padding: 30px; border-radius: 15px; text-align: center; color: white; box-shadow: 0px 4px 15px rgba(0,0,0,0.2);">
                <h1 style="margin: 0; font-size: 40px;">👑 CAMPEÃO(A) DA SEMANA! 👑</h1>
                <h2 style="margin: 10px 0; font-size: 32px; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">{campeao}</h2>
                <p style="font-size: 20px; margin: 0;">Com uma pontuação espetacular de <b>{int(pontos_campeao)} pontos</b> nos últimos 7 dias!</p>
                <h3 style="margin-top: 15px; font-style: italic;">Parabéns pelo excelente desempenho e dedicação! 🚀🌟</h3>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)

st.markdown("---")

# --- CADASTRO DE NOVO INTEGRANTE ---
with st.expander("➕ Cadastrar Novo Integrante"):
    with st.form("form_novo_integrante", clear_on_submit=True):
        novo_nome = st.text_input("Nome do Integrante:")
        nova_cor = st.color_picker("Escolha a Cor de Destaque:", "#2563EB")
        cadastrar_btn = st.form_submit_button("Salvar Integrante")
        
        if cadastrar_btn:
            if novo_nome.strip():
                if novo_nome.strip() in integrantes_cores:
                    st.warning("Este integrante já está cadastrado!")
                else:
                    salvar_integrante(novo_nome.strip(), nova_cor)
                    st.success(f"Integrante {novo_nome.strip()} cadastrado com sucesso!")
                    st.rerun()
            else:
                st.warning("Digite um nome válido.")

# --- FORMULÁRIO DE LANÇAMENTO ---
with st.container():
    st.subheader("📝 Lançamento de Pontuação do Dia")
    with st.form("form_pontuacao", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            lista_nomes = list(carregar_integrantes().keys())
            integrante = st.selectbox("Selecione o Integrante:", lista_nomes)

        with col2:
            data_lancamento = st.date_input("Data da Pontuação:", value=datetime.today())
            
        with col3:
            pontos = st.number_input("Pontos do Dia (Máximo 25):", min_value=0, max_value=25, step=1, format="%d")

        observacao = st.text_input("Observação / Comentário (Opcional):")
        enviado = st.form_submit_button("🚀 Salvar Pontuação")

        if enviado:
            if not integrante:
                st.warning("Por favor, selecione o integrante.")
            else:
                nova_linha = pd.DataFrame([{
                    "Data": data_lancamento.strftime("%Y-%m-%d"),
                    "Integrante": integrante,
                    "Pontos": int(pontos),
                    "Observação": observacao if observacao else ""
                }])
                
                df_pontos = pd.concat([df_pontos, nova_linha], ignore_index=True)
                df_pontos.to_csv(ARQUIVO_DADOS, index=False)
                st.success(f"Pontuação de {integrante} registrada com sucesso!")
                st.rerun()

st.markdown("---")

# --- PAINEL DE ESTATÍSTICAS E RANKING ---
if not df_pontos.empty:
    st.subheader("📊 Painel de Estatísticas da Equipe")

    total_pontos_geral = df_pontos["Pontos"].sum()
    media_geral = df_pontos["Pontos"].mean()
    total_lancamentos = len(df_pontos)
    maior_pontuacao_dia = df_pontos["Pontos"].max()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Acumulado (Equipe)", f"{int(total_pontos_geral)} pts")
    c2.metric("Média por Lançamento", f"{media_geral:.1f} pts")
    c3.metric("Total de Registros", f"{total_lancamentos}")
    c4.metric("Recorde Diário", f"{int(maior_pontuacao_dia)} pts")

    st.markdown("---")

    ranking_geral = df_pontos.groupby("Integrante").agg(
        Total_Pontos=("Pontos", "sum"),
        Media_Diaria=("Pontos", "mean"),
        Dias_Trabalhados=("Pontos", "count")
    ).reset_index()

    ranking_geral = ranking_geral.sort_values(by="Total_Pontos", ascending=False).reset_index(drop=True)
    ranking_geral.index = ranking_geral.index + 1
    ranking_geral.index.name = "Posição"
    ranking_geral = ranking_geral.reset_index()

    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("### 🥇 Tabela de Classificação & Estatísticas")
        tabela_exib = ranking_geral.rename(columns={
            "Integrante": "Integrantes",
            "Total_Pontos": "Total (Pts)",
            "Media_Diaria": "Média (Pts/Dia)",
            "Dias_Trabalhados": "Lançamentos"
        })
        st.dataframe(tabela_exib, use_container_width=True)

    with col_b:
        st.markdown("### 📈 Comparativo de Pontuação Acumulada")
        st.bar_chart(ranking_geral.set_index("Integrante")["Total_Pontos"])

    st.markdown("---")
    st.subheader("📋 Histórico Completo de Lançamentos")
    st.dataframe(df_pontos.sort_values(by="Data", ascending=False), use_container_width=True)
    
    csv = df_pontos.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 Baixar Histórico Completo em CSV", data=csv, file_name="historico_pontuacoes.csv", mime="text/csv")

else:
    st.info("Nenhuma pontuação registrada ainda. Faça o primeiro lançamento acima para gerar as estatísticas!")
