import streamlit as st
from src.dados import carregar_dados
from src.calculos import calcular_ranking

st.set_page_config(page_title="🏆 Bolão da Copa", page_icon="⚽", layout="wide")

st.title("🏆 Bolão da Copa")
st.write("Acompanhe a classificação e os palpites da rodada em tempo real!")
st.markdown("---")

URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1tv0rlRREvdFhZgBdxRlhhoCGeHPFMItlsUHcRkPu3LU/export?format=csv&gid=1735885906"

if URL_PLANILHA == "COLE_AQUI_O_LINK_DO_SEU_CSV":
    st.info("💡 **Aviso ao Administrador:** Insira o link correto da sua planilha.")
else:
    df_bruto = carregar_dados(URL_PLANILHA)
    
    if df_bruto is not None:
        # Contrato fixo: Sempre espera 3 elementos estruturados do backend
        df_ranking, df_palpites, status = calcular_ranking(df_bruto)
        
        if df_ranking.empty and status != "Sucesso":
            st.warning(status)
        else:
            aba_ranking, aba_palpites = st.tabs(["📊 Classificação", "👁️ Ver Palpites"])
            
            with aba_ranking:
                if not df_ranking.empty:
                    lider = df_ranking.iloc[0]['Participante']
                    pontos_lider = df_ranking.iloc[0]['Pontos']
                    st.success(f"👑 **{lider}** está na liderança com **{pontos_lider} pontos**!")
                
                st.markdown("### 📊 Tabela de Classificação")
                st.dataframe(df_ranking, use_container_width=True)
            
            with aba_palpites:
                st.markdown("### 👁️ Palpites Cadastrados")
                st.write("Veja abaixo o que cada participante apostou comparado ao gabarito oficial:")
                st.dataframe(df_palpites, use_container_width=True)
            
            st.markdown("---")
            st.caption("ℹ️ Em caso de empate na pontuação, o prêmio será dividido entre os líderes.")