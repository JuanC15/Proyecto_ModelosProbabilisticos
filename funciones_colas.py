import numpy as np
import io
import base64
import matplotlib.pyplot as plt
import math

# --- Modelo M/M/1 ---
def calcular_mm1(lam, mu):
    if lam >= mu:
        return {"error": "El sistema es inestable (λ ≥ μ)"}

    rho = lam / mu
    L = rho / (1 - rho)
    Lq = rho**2 / (1 - rho)
    W = 1 / (mu - lam)
    Wq = lam / (mu * (mu - lam))

    return {
        "ρ (Utilización)": rho,
        "L (Número promedio en el sistema)": L,
        "Lq (Número promedio en cola)": Lq,
        "W (Tiempo promedio en el sistema)": W,
        "Wq (Tiempo promedio en cola)": Wq,
    }

# --- Modelo M/M/c ---
def calcular_mmc(lam, mu, c):
    rho = lam / (c * mu)
    if rho >= 1:
        return {"error": "El sistema es inestable (ρ ≥ 1)"}

    # Cálculo de P0
    suma = sum([(c * rho) ** n / math.factorial(n) for n in range(c)])
    P0 = 1 / (suma + ((c * rho) ** c / (math.factorial(c) * (1 - rho))))

    # Lq y L
    Lq = (P0 * ((c * rho) ** c) * rho) / (math.factorial(c) * (1 - rho) ** 2)
    L = Lq + (lam / mu)
    Wq = Lq / lam
    W = Wq + (1 / mu)

    return {
        "ρ (Utilización)": rho,
        "P0 (Probabilidad de 0 clientes)": P0,
        "Lq (Número promedio en cola)": Lq,
        "L (Número promedio en el sistema)": L,
        "Wq (Tiempo promedio en cola)": Wq,
        "W (Tiempo promedio en el sistema)": W,
    }

# --- Gráfica L vs λ ---
def grafica_L_vs_lambda(mu, modelo="M/M/1", c=1):
    lambdas = np.linspace(0.1, mu - 0.1, 50)
    Ls = []

    for lam in lambdas:
        if modelo == "M/M/1":
            res = calcular_mm1(lam, mu)
        else:
            res = calcular_mmc(lam, mu, c)
        Ls.append(res.get("L (Número promedio en el sistema)", np.nan))

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(lambdas, Ls, marker="o", color="#007ACC", linewidth=2)
    ax.fill_between(lambdas, Ls, alpha=0.1, color="#007ACC")
    ax.set_xlabel("Tasa de llegada (λ)", fontsize=12)
    ax.set_ylabel("L (número promedio en el sistema)", fontsize=12)
    ax.set_title(f"Comportamiento de L en el modelo {modelo}", fontsize=14, fontweight="bold")
    ax.grid(alpha=0.3)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", dpi=200)
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()

    return img_b64