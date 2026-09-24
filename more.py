import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Ranking & Estatísticas da Equipe", page_icon="🏆", layout="wide")

ARQUIVO_DADOS = "pontuacoes_equipe.csv"

# Função para carregar os dados
def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        return pd.read_csv(ARQUIVO_DADOS)
    else:
        return pd.DataFrame(columns=["Data", "Integrante", "Pontos", "Observação"])

df_pontos = carregar_dados()

st.title("🏆 Ranking & Estatísticas de Desempenho da Equipe")
st.markdown("Insira sua pontuação diária para atualizar os cálculos e o ranking em tempo real!")
st.markdown("---")

# --- FORMULÁRIO DE LANÇAMENTO ---
with st.container():
    st.subheader("📝 Lançamento de Pontuação do Dia")
    with st.form("form_pontuacao", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            integrantes_padrao = ["Carolina Rodrigues Bruno", "Saruete Stabile", "Benedito", "Outro"]
            integrante = st.selectbox("Selecione o Integrante:", integrantes_padrao)
            if integrante == "Outro":
                integrante = st.text_input("Digite o nome do Integrante:")

        with col2:
            data_lancamento = st.date_input("Data da Pontuação:", value=datetime.today())
            
        with col3:
            pontos = st.number_input("Pontos / Meta Realizada:", min_value=0.0, step=1.0, format="%.1f")

        observacao = st.text_input("Observação / Comentário (Opcional):")
        enviado = st.form_submit_button("🚀 Salvar Pontuação")

        if enviado:
            if not integrante:
                st.warning("Por favor, informe o nome do integrante.")
            else:
                nova_linha = pd.DataFrame([{
                    "Data": data_lancamento.strftime("%Y-%m-%d"),
                    "Integrante": integrante,
                    "Pontos": pontos,
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

    # Cálculos estatísticos
    total_pontos_geral = df_pontos["Pontos"].sum()
    media_geral = df_pontos["Pontos"].mean()
    total_lancamentos = len(df_pontos)
    maior_pontuacao_dia = df_pontos["Pontos"].max()

    # Cards de Métricas no Topo
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Acumulado (Equipe)", f"{total_pontos_geral:.1f} pts")
    c2.metric("Média por Lançamento", f"{media_geral:.1f} pts")
    c3.metric("Total de Registros", f"{total_lancamentos}")
    c4.metric("Recorde Diário (Individual)", f"{maior_pontuacao_dia:.1f} pts")

    st.markdown("---")

    # Agrupamentos para o Ranking
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
        st.dataframe(tabela_exibic, use_container_width=True) if 'tabela_exibic' in locals() else st.dataframe(tabela_exibrio := tabela_exib, use_container_width=True)

    with col_b:
        st.markdown("### 📈 Comparativo de Pontuação Acumulada")
        st.bar_chart(ranking_geral.set_index("Integrante")["Total_Pontos"])

    st.markdown("---")
    
    # Histórico detalhado
    st.subheader("📋 Histórico Completo de Lançamentos")
    st.dataframe(df_pontos.sort_values(by="Data", ascending=False), use_container_width=True)
    
    # Botão de download
    csv = df_pontos.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 Baixar Histórico Completo em CSV", data=csv, file_name="historico_pontuacoes.csv", mime="text/csv")

else:
    st.info("Nenhuma pontuação registrada ainda. Faça o primeiro lançamento acima para gerar as estatísticas!")
