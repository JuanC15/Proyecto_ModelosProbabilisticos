import streamlit as st
import numpy as np
import pandas as pd
from markov_absorbente import procesar_markov, graficar_matriz
from funciones_colas import calcular_mm1, calcular_mmc, grafica_L_vs_lambda
import base64

st.sidebar.info("Proyecto final - Modelos Probabilísticos y Simulación\nAutor: Juan Aroca")
st.markdown(
    "<h2 style='text-align:center;color:#4CAF50;'>Simulador de Cadenas de Márkov (Absorbentes) y Modelos de Colas M/M/1 - M/M/c</h2>",
    unsafe_allow_html=True
)
st.set_page_config(page_title="Simulador de Márkov y Colas", layout="wide")
st.title("📊 Simulador de Cadenas de Márkov y Teoría de Colas")

tabs = st.tabs(["Cadenas de Márkov", "Teoría de Colas"])

# --- TAB 1: Cadenas de Márkov ---
with tabs[0]:
    st.header("Cadenas de Márkov (Estados Absorbentes)")
    n = st.number_input("Número de estados:", min_value=2, max_value=10, value=3)
    st.write("Introduce la matriz de transición:")
    
    P = []
    for i in range(n):
        fila = st.text_input(f"Fila {i+1} (separada por comas):", ",".join(["0"] * n))
        P.append([float(x) for x in fila.split(",")])
    
    if st.button("Calcular Márkov"):
        try:
            Q, R, N, B, absorb, no_absorb = procesar_markov(P)
            st.subheader("Resultados:")
            st.write(f"**Estados absorbentes:** {absorb}")
            st.write(f"**Estados no absorbentes:** {no_absorb}")
            st.write("**Matriz fundamental (N):**")
            st.dataframe(pd.DataFrame(N))
            st.write("**Probabilidades de absorción (B):**")
            st.dataframe(pd.DataFrame(B))
            
            img_b64 = graficar_matriz(np.array(P))
            st.image(base64.b64decode(img_b64))
        except Exception as e:
            st.error(f"Error: {e}")

# --- TAB 2: Teoría de Colas ---
with tabs[1]:
    st.header("Modelos de Colas")
    modelo = st.radio("Selecciona el modelo:", ["M/M/1", "M/M/c"])
    lam = st.number_input("Tasa de llegada (λ):", min_value=0.1, value=2.0)
    mu = st.number_input("Tasa de servicio (μ):", min_value=0.1, value=5.0)
    c = 1
    if modelo == "M/M/c":
        c = st.number_input("Número de servidores (c):", min_value=1, value=2)

    if st.button("Calcular Colas"):
        if modelo == "M/M/1":
            res = calcular_mm1(lam, mu)
        else:
            res = calcular_mmc(lam, mu, c)
        
        if "error" in res:
            st.error(res["error"])
        else:
            st.subheader("Resultados")
            st.json(res)
            img_b64 = grafica_L_vs_lambda(mu, modelo, c)
            st.image(base64.b64decode(img_b64))