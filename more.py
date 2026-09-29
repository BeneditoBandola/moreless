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
                # Formata a data para exibir bonito na tabela (ex: Seg, 28/09)
                df_semana["Data_Formatada"] = df_semana["Data_Parsed"].dt.strftime("%d/%m (%a)")

                # Cria uma tabela pivot: Linhas = Integrantes, Colunas = Dias da Semana, Valores = Pontos
                tabela_detalhada = df_semana.pivot_table(
                    index="Integrante", 
                    columns="Data_Formatada", 
                    values="Pontos", 
                    aggfunc="sum", 
                    fill_value=0
                )

                # Adiciona a coluna com a somatória total da semana
                tabela_detalhada["Total Semana"] = tabela_detalhada.sum(axis=1)

                # Ordena do maior para o menor total
                tabela_detalhada = tabela_detalhada.sort_values(by="Total Semana", ascending=False)

                st.markdown(f"### Detalhe por Dia - {semana_selecionada}")
                st.dataframe(tabela_detalhada, use_container_width=True)

                # Identifica o campeão com base na somatória da tabela
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
