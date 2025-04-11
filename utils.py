import streamlit as st
import pandas as pd

def calcular_parcela(valor_financiado, taxa_juros_anual, total_parcelas):
    taxa_mensal = taxa_juros_anual / 100 / 12
    n = total_parcelas

    if taxa_mensal == 0:
        parcela = valor_financiado / n
    else:
        parcela = valor_financiado * (taxa_mensal * (1 + taxa_mensal)**n) / ((1 + taxa_mensal)**n - 1)
    
    return parcela

def gerar_tabela_amortizacao(valor_financiado, taxa_juros_anual, total_parcelas):
    taxa_mensal = taxa_juros_anual / 100 / 12
    saldo_devedor = valor_financiado
    parcela = calcular_parcela(valor_financiado, taxa_juros_anual, total_parcelas)
    
    tabela = []
    for i in range(1, total_parcelas + 1):
        juros = saldo_devedor * taxa_mensal
        amortizacao = parcela - juros
        saldo_devedor -= amortizacao
        tabela.append({
            "Parcela": i,
            "Amortização (R$)": round(amortizacao, 2),
            "Juros (R$)": round(juros, 2),
            "Parcela (R$)": round(parcela, 2),
            "Saldo Devedor (R$)": round(max(saldo_devedor, 0), 2)
        })

    return pd.DataFrame(tabela)

# Interface do usuário
st.title("Simulador de Parcelas de Financiamento Imobiliário")

valor_total = st.number_input("Valor total do imóvel (R$)", min_value=1000.0, step=1000.0, format="%.2f")
entrada = st.number_input("Valor da entrada (R$)", min_value=0.0, step=1000.0, format="%.2f")
taxa_juros = st.number_input("Taxa de juros anual (%)", min_value=0.0, step=0.1, format="%.2f")
total_parcelas = st.number_input("Total de parcelas (ex: 360)", min_value=1, step=1)

# Cálculo do subsídio e valor a financiar
caixa_20 = valor_total * 0.20
valor_financiado = valor_total - entrada - caixa_20

st.write(f"**Subsídio (20% Caixa):** R$ {caixa_20:,.2f}")
st.write(f"**Valor a ser financiado:** R$ {valor_financiado:,.2f}")

if valor_financiado <= 0:
    st.warning("O valor financiado está zerado ou negativo. Verifique os valores informados.")
else:
    parcela_mensal = calcular_parcela(valor_financiado, taxa_juros, total_parcelas)
    st.success(f"**Parcela mensal aproximada:** R$ {parcela_mensal:,.2f}")
    
    st.subheader("Tabela de Amortização")
    tabela = gerar_tabela_amortizacao(valor_financiado, taxa_juros, total_parcelas)
    st.dataframe(tabela, use_container_width=True)

    # Exportar como CSV
    csv = tabela.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Baixar simulação em CSV",
        data=csv,
        file_name="simulacao_financiamento.csv",
        mime="text/csv"
    )
