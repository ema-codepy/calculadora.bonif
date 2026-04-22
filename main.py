import streamlit as st

# Configuração da página
st.set_page_config(page_title="CALCULADORA BONIF", layout="centered")

# Estilo para esconder menus e deixar com cara de App
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #28a745;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. Base de Preços
precos = {
    'RS': {'Dunhill': 114.72, 'Kent': 71.12, 'Rothmans (BASE)': 82.60},
    'SC': {'Dunhill': 135.04, 'Kent': 70.95, 'Rothmans (BASE)': 96.13}
}

# --- Cabeçalho ---
st.markdown(f"""
    <div style="background-color: #002d72; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
        <h1 style="color: white; margin: 0; font-family: sans-serif; letter-spacing: 2px; font-size: 24px;">CALCULADORA BONIF</h1>
    </div>
""", unsafe_allow_html=True)

# --- Entrada de Dados ---
estado = st.selectbox("Estado:", ["RS", "SC"])
obj_100 = st.number_input("Objetivo (100%):", value=120, step=1)

planos = {
    'Prime Light (100%)': 1.0,
    'Varejo Normal (120%)': 1.2,
    'Prime Boost (130%)': 1.3,
    'Prime Offenders (150%)': 1.5
}
plano_sel = st.selectbox("Plano Varejo:", list(planos.keys()), index=2)

# Cálculo automático do Objetivo Máximo
obj_max_auto = int(obj_100 * planos[plano_sel])
obj_max = st.number_input("Objetivo Máximo:", value=obj_max_auto, step=1)

faixa = st.selectbox("Faixa:", list(range(1, 9)), index=4)

lista_p = [0] + list(range(11, 37)) + [39, 40, 44, 45, 47, 48, 53, 54, 64, 71, 72, 95, 96]
perc_sel = st.selectbox("% Bonificação:", lista_p, index=len(lista_p)-1) / 100

marca = st.selectbox("Marca Prêmio:", ["Rothmans", "Kent", "Dunhill"])

# --- Botão e Lógica ---
if st.button("CALCULAR RESULTADO"):
    if perc_sel < 0.8 and perc_sel != 0:
        st.error("Bonificação não atingida: O varejo não atingiu o mínimo de 80% do objetivo.")
    else:
        diferenca = obj_max - obj_100
        bonif_adicional = diferenca * perc_sel
        qtd_fixa = 2 if faixa <= 4 else 3
        
        p_base = precos[estado]['Rothmans (BASE)']
        if marca == 'Rothmans':
            res_bruto = bonif_adicional + qtd_fixa
        else:
            p_prem = precos[estado][marca]
            res_bruto = (bonif_adicional * (p_base / p_prem)) + qtd_fixa

        resultado_final = round(res_bruto)

        st.markdown(f"""
            <div style="border: 2px solid #28a745; padding: 20px; border-radius: 10px; background-color: white; text-align: center; margin-top: 20px;">
                <p style="margin: 0; color: #666; font-size: 14px; text-transform: uppercase;">Quantidade Final</p>
                <h1 style="margin: 10px 0; color: #28a745; font-size: 40px;">{resultado_final} Pacotes</h1>
                <p style="font-size: 12px; color: #888;">MARCA: {marca.upper()} | OBJ MAX: {obj_max}</p>
            </div>
        """, unsafe_allow_html=True)