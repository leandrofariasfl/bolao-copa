import pandas as pd
import streamlit as st

def carregar_dados(url_planilha):
    """
    Lê a planilha do Google Forms convertida em CSV e limpa os dados básicos.
    """
    try:
        # Lê o CSV direto da URL
        df = pd.read_csv(url_planilha)
        
        # Remove espaços em branco extras que possam vir nos nomes das colunas
        df.columns = df.columns.str.strip()
        
        return df
    except Exception as e:
        st.error("Erro ao conectar com a Google Planilha. Verifique se o link está público.")
        return None