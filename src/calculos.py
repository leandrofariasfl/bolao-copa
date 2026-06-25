import pandas as pd

def calcular_ranking(df):
    """
    Processa os palpites comparando com o GABARITO.
    
    Retornos esperados (sempre 3 elementos):
        - df_ranking (pd.DataFrame): Classificação dos jogadores.
        - df_palpites (pd.DataFrame): Matriz comparativa de palpites.
        - status (str): Mensagem de sucesso ou erro amigável.
    """
    # 1. Separação de escopo
    df_gabarito = df[df['Quem é você?'].str.upper() == 'GABARITO']
    df_jogadores = df[df['Quem é você?'].str.upper() != 'GABARITO']
    
    if df_gabarito.empty:
        df_vazio = pd.DataFrame()
        return df_vazio, df_vazio, "⚠️ Nenhum palpite com o nome 'GABARITO' foi encontrado na planilha."
        
    gabarito_linha = df_gabarito.iloc[0]
    colunas_jogos = df.columns[3:]
    
    ranking = []
    palpites_geral = []
    
    # 2. Construção da linha de referência (Gabarito) na matriz de palpites
    dicionario_gabarito = {"Participante": "🏆 RESULTADO REAL (GABARITO)"}
    for i in range(0, len(colunas_jogos) - 1, 2):
        col_casa = colunas_jogos[i]
        col_fora = colunas_jogos[i+1]
        
        nome_jogo = col_casa.replace("Gols de ", "").replace("Gols do ", "").replace(" [Gols]", "").strip() + " x " + \
                    col_fora.replace("Gols de ", "").replace("Gols do ", "").replace(" [Gols]", "").strip()
        
        r_casa = gabarito_linha[col_casa]
        r_fora = gabarito_linha[col_fora]
        
        dicionario_gabarito[nome_jogo] = "Não jogado" if pd.isna(r_casa) or pd.isna(r_fora) else f"{int(r_casa)} x {int(r_fora)}"
        
    palpites_geral.append(dicionario_gabarito)
    
    # 3. Processamento dos palpites dos jogadores
    for _, jg in df_jogadores.iterrows():
        nome = jg['Quem é você?']
        if pd.isna(nome) or str(nome).strip() == "":
            continue
            
        pontos = 0
        dicionario_palpites = {"Participante": nome}
        
        for i in range(0, len(colunas_jogos) - 1, 2):
            col_casa = colunas_jogos[i]
            col_fora = colunas_jogos[i+1]
            
            nome_jogo = col_casa.replace("Gols de ", "").replace("Gols do ", "").replace(" [Gols]", "").strip() + " x " + \
                        col_fora.replace("Gols de ", "").replace("Gols do ", "").replace(" [Gols]", "").strip()
            
            p_casa, p_fora = jg[col_casa], jg[col_fora]
            r_casa, r_fora = gabarito_linha[col_casa], gabarito_linha[col_fora]
            
            dicionario_palpites[nome_jogo] = "-" if pd.isna(p_casa) or pd.isna(p_fora) else f"{int(p_casa)} x {int(p_fora)}"
            
            if pd.isna(r_casa) or pd.isna(r_fora):
                continue
                
            try:
                p_casa, p_fora = int(p_casa), int(p_fora)
                r_casa, r_fora = int(r_casa), int(r_fora)
                
                if p_casa == r_casa and p_fora == r_fora:
                    pontos += 3
                elif (p_casa > p_fora and r_casa > r_fora) or \
                     (p_casa < p_fora and r_casa < r_fora) or \
                     (p_casa == p_fora and r_casa == r_fora):
                    pontos += 1
            except (ValueError, TypeError):
                continue
                
        ranking.append({"Participante": nome, "Pontos": pontos})
        palpites_geral.append(dicionario_palpites)
        
    # 4. Estruturação dos DataFrames finais para retorno
    df_palpites = pd.DataFrame(palpites_geral).set_index("Participante")
    
    if not ranking:
        df_ranking = pd.DataFrame(columns=["Participante", "Pontos"])
        return df_ranking, df_palpites, "Sucesso"
        
    df_ranking = pd.DataFrame(ranking).sort_values(by="Pontos", ascending=False).reset_index(drop=True)
    df_ranking.index += 1
    
    return df_ranking, df_palpites, "Sucesso"