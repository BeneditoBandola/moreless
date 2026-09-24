import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import json
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Ranking & Patentes das Trevas", page_icon="🦇", layout="wide")

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

# --- FUNÇÃO PARA DEFINIR A CLASSIFICAÇÃO BASEADA NA PONTUAÇÃO ---
def obter_classificacao(pontos):
    if pontos >= 100:
        return "👑 Deus Supremo"
    elif pontos >= 75:
        return "🐐 Cabrito Sagrado"
    elif pontos >= 50:
        return "🐎 Égua Satânica"
    elif pontos >= 25:
        return "🐴 Mula Juvenil"
    else:
        return "🎒 Mochila de Criança"

# --- GERADOR DE 900+ MENSAGENS COM VIÉS DE TERROR E O SOMBRIO ---
@st.cache_data
def gerar_banco_mensagens_terror():
    citacoes_sombrias = [
        "Até mesmo o homem mais puro de coração e que reza em suas preces diárias, pode se tornar um monstro quando a meta não é batida.",
        "Nas sombras da noite corporativa, os erros do passado nunca morrem... eles apenas esperam o próximo fechamento.",
        "Cuidado com os passos que você dá nos corredores escuros; o fracasso espreita logo após a curva.",
        "O relógio bate as doze badaladas, e o tempo para o fechamento se esvai como areia ensanguentada entre os dedos.",
        "Há monstros piores do que aqueles que habitam os pesadelos: os prazos fatais que se aproximam.",
        "Ninguém escapa das consequências de um relatório incompleto. A auditoria das trevas sempre cobra o seu preço.",
        "O eco de metas não alcançadas ressoa eternamente nas catacumbas do esquecimento."
    ]
    
    charadas_macabras = [
        ("O que é, o que é: quanto mais se alimenta, mais cresce, mas se beber água, morre?", "O fogo... ou a ambição desmedida."),
        ("O que é, o que é: tem asas mas não voa, tem olhos mas não vê, e habita a escuridão?", "Um morcego faminto nas torres do castelo."),
        ("O que é, o что é: caminha de quatro pela manhã, de duas ao meio-dia e de três à noite?", "A criatura que rasteja pelas planícies da perdição."),
        ("O que é, o que é: corta sem lâmina, fere sem punhal e silencia para sempre?", "O peso do remorso por deixar pontos para trás."),
        ("O que é, o que é: quanto mais você tira dele, maior se torna o vazio?", "O abismo insondável dos números vermelhos.")
    ]
    
    avisos_malignos = [
        "Aviso das trevas: Se ouvir passos atrás de você na sala vazia, não olhe para trás... apenas acelere os lançamentos.",
        "Profecia macabra: Aquele que hesitar em registrar os pontos de hoje será assombrado por planilhas infinitas na madrugada.",
        "A maldição do sistema: Quem ousa zerar a pontuação por três dias consecutivos atrai a ira das forças ocultas da gerência.",
        "Olhe bem para a tela: os pixels ao seu redor estão frios porque a ausência de metas cumpridas gela a alma.",
        "Cuidado com o sussurro na penumbra: ele diz que a concorrência está vindo te buscar..."
    ]
    
    lista_completa = []
    
    for i in range(150):
        for c in citacoes_sombrias:
            lista_completa.append(("🌑 Decreto das Sombras", f"{c} *(Sussurro #{i+1} da cripta)*"))
        for a in avisos_malignos:
            lista_completa.append(("⚰️ Alerta Macabro", f"{a} *(Aviso ritualístico #{i+1} de perigo)*"))
        for p, r in charadas_macabras:
            lista_completa.append(("🦇 Enigma do Abismo", f"**Enigma:** {p}<br>*(Decifre se tiver coragem...)*<br>💀 **Resposta Oculta:** {r} *(Registro #{i+1})*"))
            
    return lista_completa

integrantes_cores = carregar_integrantes()
df_pontos = carregar_dados()

# --- TELA DE BOAS-VINDAS SOMBRIA (DIÁRIA) ---
banco_msgs = gerar_banco_mensagens_terror()
hoje_str = datetime.today().strftime("%Y-%m-%d")
indice_diario = abs(hash(hoje_str)) % len(banco_msgs)
tipo_msg, texto_msg = banco_msgs[indice_diario]

st.markdown(
    f"""
    <div style="background: linear-gradient(135deg, #09090B, #18181B); border: 1px solid #27272A; padding: 25px; border-radius: 12px; color: #F4F4F5; margin-bottom: 20px; box-shadow: 0px 4px 20px rgba(0,0,0,0.8);">
        <h2 style="margin: 0; font-size: 26px; color: #EF4444; font-family: serif;">🕯️ Bem-vindo(a) às Trevas do Expediente</h2>
        <p style="font-size: 14px; opacity: 0.7; margin-top: 5px;">📅 Data da maldição: <b>{datetime.today().strftime('%d/%m/%Y')}</b></p>
        <hr style="border: 0.5px solid rgba(239, 68, 68, 0.3); margin: 12px 0;">
        <h4 style="margin: 0 0 5px 0; color: #F87171;">{tipo_msg}:</h4>
        <p style="font-size: 16px; margin: 0; line-height: 1.6; font-style: italic;">"{texto_msg}"</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.title("🏆 Ranking, Patentes & Apuração do Campeão")
st.markdown("Registre sua pontuação diária (máximo de 25 pontos) e conquiste sua patente nas trevas!")
st.markdown("---")

# --- APURAÇÃO E TRAVA DA SEMANA ATUAL ---
if st.button("🎉 APURAR E SALVAR CAMPEÃO DA SEMANA ATUAL!", use_container_width=True):
    if df_pontos.empty:
        st.warning("Ainda não há pontuações cadastradas para apurar o campeão!")
    else:
        df_pontos['Data_Parsed'] = pd.to_datetime(df_pontos['Data'], errors='coerce')
        
        hoje = datetime.today()
        ano_atual, semana_atual, _ = hoje.isocalendar()
        chave_semana = f"Ano {ano_atual} - Semana {semana_atual}"
        
        df_pontos['Ano_Semana'] = df_pontos['Data_Parsed'].apply(lambda x: f"Ano {x.isocalendar()[0]} - Semana {x.isocalendar()[1]}" if pd.notnull(x) else "")
        df_semana_atual = df_pontos[df_pontos['Ano_Semana'] == chave_semana]
        
        if df_semana_atual.empty:
            st.warning(f"Nenhum lançamento encontrado para a semana atual ({chave_semana}).")
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
                "data_apuracao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            salvar_historico_json(historico)
            
            cor_campeao = integrantes_cores.get(campeao, "#7F1D1D")
            
            st.balloons()
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, {cor_campeao}, #09090B); border: 2px solid #EF4444; padding: 30px; border-radius: 15px; text-align: center; color: white; box-shadow: 0px 0px 25px rgba(239,68,68,0.5);">
                    <h1 style="margin: 0; font-size: 38px; color: #FCA5A5;">👑 SENHOR(A) DAS SOMBRAS DA {chave_semana.upper()} 👑</h1>
                    <h2 style="margin: 10px 0; font-size: 32px; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.9);">{campeao}</h2>
                    <p style="font-size: 20px; margin: 0;">Almas/Pontos colhidos: <b>{int(pontos_campeao)} pontos</b></p>
                    <h3 style="margin-top: 15px; font-style: italic; color: #FCA5A5;">O trono sombrio foi conquistado! Salvo no grimório JSON. 🦇🔥</h3>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown("<br>", unsafe_allow_html=True)

# --- EXIBIR HISTÓRICO DE CAMPEÕES SALVOS NO JSON ---
historico_salvo = carregar_historico_json()
if historico_salvo:
    with st.expander("📜 Ver Grimório Histórico de Campeões (JSON)"):
        for sem, dados in sorted(historico_salvo.items(), reverse=True):
            st.markdown(f"### 🦇 {sem}")
            st.write(f"**Senhor(a) das Sombras:** {dados['campeao']} ({dados['pontos']} pts) | *Rito de apuração:* {dados['data_apuracao']}")
            df_rank_hist = pd.DataFrame(dados['ranking_completo'])
            st.dataframe(df_rank_hist, use_container_width=True)
            st.markdown("---")

st.markdown("---")

# --- CADASTRO DE NOVO INTEGRANTE ---
with st.expander("➕ Iniciar Novo Adepto / Integrante"):
    with st.form("form_novo_integrante", clear_on_submit=True):
        novo_nome = st.text_input("Nome do Integrante:")
        nova_cor = st.color_picker("Escolha a Cor Sombria de Destaque:", "#7F1D1D")
        cadastrar_btn = st.form_submit_button("Consagrar Integrante")
        
        if cadastrar_btn:
            if novo_nome.strip():
                if novo_nome.strip() in integrantes_cores:
                    st.warning("Este adepto já habita as trevas!")
                else:
                    salvar_integrante(novo_nome.strip(), nova_cor)
                    st.success(f"Integrante {novo_nome.strip()} consagrado com sucesso!")
                    st.rerun()
            else:
                st.warning("Digite um nome válido.")

# --- FORMULÁRIO DE LANÇAMENTO ---
with st.container():
    st.subheader("📝 Oferenda Diária de Pontuação")
    with st.form("form_pontuacao", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            lista_nomes = list(carregar_integrantes().keys())
            integrante = st.selectbox("Selecione o Integrante:", lista_nomes)

        with col2:
            data_lancamento = st.date_input("Data do Sacrifício / Lançamento:", value=datetime.today())
            
        with col3:
            pontos = st.number_input("Pontos do Dia (Máximo 25):", min_value=0, max_value=25, step=1, format="%d")

        observacao = st.text_input("Sussurro / Observação (Opcional):")
        enviado = st.form_submit_button("🔥 Consagrar Pontuação")

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
                st.success(f"Pontuação de {integrante} registrada nas sombras!")
                st.rerun()

st.markdown("---")

# --- PAINEL DE ESTATÍSTICAS E RANKING COM CLASSIFICAÇÕES ---
if not df_pontos.empty:
    st.subheader("📊 Painel de Profecias & Estatísticas")

    total_pontos_geral = df_pontos["Pontos"].sum()
    media_geral = df_pontos["Pontos"].mean()
    total_lancamentos = len(df_pontos)
    maior_pontuacao_dia = df_pontos["Pontos"].max()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Almas Acumuladas (Equipe)", f"{int(total_pontos_geral)} pts")
    c2.metric("Média por Sacrifício", f"{media_geral:.1f} pts")
    c3.metric("Total de Rituais", f"{total_lancamentos}")
    c4.metric("Recorde das Trevas", f"{int(maior_pontuacao_dia)} pts")

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

    # Adicionar a coluna de classificação temática
    ranking_geral["Patente / Classificação"] = ranking_geral["Total_Pontos"].apply(obter_classificacao)

    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("### 🥇 Hierarquia das Sombras (Ranking & Patentes)")
        tabela_exib = ranking_geral[["Posição", "Integrante", "Total_Pontos", "Patente / Classificação", "Dias_Trabalhados"]].rename(columns={
            "Integrante": "Integrantes",
            "Total_Pontos": "Total (Pts)",
            "Dias_Trabalhados": "Rituais"
        })
        st.dataframe(tabela_exib, use_container_width=True)

    with col_b:
        st.markdown("### 📈 Panorama das Almas Colhidas")
        st.bar_chart(ranking_geral.set_index("Integrante")["Total_Pontos"])

    st.markdown("---")
    st.subheader("📋 Livro de Registros das Trevas")
    st.dataframe(df_pontos.sort_values(by="Data", ascending=False), use_container_width=True)
    
    csv = df_pontos.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 Baixar Grimório em CSV", data=csv, file_name="historico_pontuacoes.csv", mime="text/csv")

else:
    st.info("Nenhum ritual registrado ainda. Faça a primeira oferenda de pontos acima!")
