import streamlit as st
import pandas as pd
from datetime import datetime
import os
import json

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Ranking & Campeão da Semana", page_icon="🏆", layout="wide")

ARQUIVO_DADOS = "pontuacoes_equipe.csv"
ARQUIVO_INTEGRANTES = "integrantes_equipe.csv"
ARQUIVO_HISTORICO_JSON = "historico_semanas.json"

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

integrantes_cores = carregar_integrantes()
df_pontos = carregar_dados()

st.title("🏆 Ranking & Apuração do Campeão da Semana")
st.markdown("Registre sua pontuação diária (máximo de 25 pontos) e acompanhe o histórico semanal guardado em JSON!")
st.markdown("---")

# --- APURAÇÃO E TRAVA DA SEMANA ATUAL ---
if st.button("🎉 APURAR E SALVAR CAMPEÃO DA SEMANA ATUAL!", use_container_width=True):
    if df_pontos.empty:
        st.warning("Ainda não há pontuações cadastradas para apurar o campeão!")
    else:
        df_pontos['Data_Parsed'] = pd.to_datetime(df_pontos['Data'], errors='coerce')
        
        # Obter o Ano e o Número da Semana ISO atual
        hoje = datetime.today()
        ano_atual, semana_atual, _ = hoje.isocalendar()
        chave_semana = f"Ano {ano_atual} - Semana {semana_atual}"
        
        # Filtrar dados da semana atual
        df_pontos['Ano_Semana'] = df_pontos['Data_Parsed'].apply(lambda x: f"Ano {x.isocalendar()[0]} - Semana {x.isocalendar()[1]}" if pd.notnull(x) else "")
        df_semana_atual = df_pontos[df_pontos['Ano_Semana'] == chave_semana]
        
        if df_semana_atual.empty:
            st.warning(f"Nenhum lançamento encontrado para a semana atual ({chave_semana}).")
        else:
            ranking_semana = df_semana_atual.groupby("Integrante")["Pontos"].sum().reset_index()
            ranking_semana = ranking_semana.sort_values(by="Pontos", ascending=False).reset_index(drop=True)
            
            campeao = ranking_semana.iloc[0]["Integrante"]
            pontos_campeao = ranking_semana.iloc[0]["Pontos"]
            
            # Salvar no JSON histórico (Trava da Semana)
            historico = carregar_historico_json()
            historico[chave_semana] = {
                "campeao": campeao,
                "pontos": int(pontos_campeao),
                "ranking_completo": ranking_semana.to_dict(orient="records"),
                "data_apuracao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            salvar_historico_json(historico)
            
            cor_campeao = integrantes_cores.get(campeao, "#2563EB")
            
            st.balloons()
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, {cor_campeao}, #F59E0B); padding: 30px; border-radius: 15px; text-align: center; color: white; box-shadow: 0px 4px 15px rgba(0,0,0,0.2);">
                    <h1 style="margin: 0; font-size: 38px;">👑 CAMPEÃO(A) DA {chave_semana.upper()}! 👑</h1>
                    <h2 style="margin: 10px 0; font-size: 32px; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">{campeao}</h2>
                    <p style="font-size: 20px; margin: 0;">Pontuação acumulada: <b>{int(pontos_campeao)} pontos</b></p>
                    <h3 style="margin-top: 15px; font-style: italic;">Resultado travado e salvo com sucesso no histórico JSON! 🔒🚀</h3>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown("<br>", unsafe_allow_html=True)

# --- EXIBIR HISTÓRICO DE CAMPEÕES SALVOS NO JSON ---
historico_salvo = carregar_historico_json()
if historico_salvo:
    with st.expander("📜 Ver Histórico de Campeões Salvos (JSON)"):
        for sem, dados in sorted(historico_salvo.items(), reverse=True):
            st.markdown(f"### 🏆 {sem}")
            st.write(f"**Campeão:** {dados['campeao']} ({dados['pontos']} pts) | *Apurado em:* {dados['data_apuracao']}")
            df_rank_hist = pd.DataFrame(dados['ranking_completo'])
            st.dataframe(df_rank_hist, use_container_width=True)
            st.markdown("---")

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
