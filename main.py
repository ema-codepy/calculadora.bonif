import ipywidgets as widgets
from IPython.display import display, clear_output

# 1. Base de Preços
precos = {
    'RS': {'Dunhill': 114.72, 'Kent': 71.12, 'Rothmans (BASE)': 82.60},
    'SC': {'Dunhill': 135.04, 'Kent': 70.95, 'Rothmans (BASE)': 96.13}
}

# --- Interface ---
style = {'description_width': 'initial'}
layout = widgets.Layout(width='460px')

# Widgets
dropdown_estado = widgets.Dropdown(options=['RS', 'SC'], description='Estado:', style=style, layout=layout)
input_obj_100 = widgets.IntText(value=120, description='Objetivo (100%):', style=style, layout=layout)

# Seleção de Plano (Multiplicadores)
planos_opcoes = [
    ('Prime Light (100%)', 1.0),
    ('Varejo Normal (120%)', 1.2),
    ('Prime Boost (130%)', 1.3),
    ('Prime Offenders (150%)', 1.5)
]
dropdown_plano = widgets.Dropdown(options=planos_opcoes, value=1.3, description='Plano do Varejo:', style=style, layout=layout)

input_obj_max = widgets.IntText(value=156, description='Objetivo Máximo (Ajustável):', style=style, layout=layout)

dropdown_faixa = widgets.Dropdown(options=[(f'Faixa {i}', i) for i in range(1, 9)], value=5, description='Faixa de Premiação:', style=style, layout=layout)

lista_perc = [0] + list(range(11, 37)) + [39, 40, 44, 45, 47, 48, 53, 54, 64, 71, 72, 95, 96]
dropdown_percentual = widgets.Dropdown(options=[(f'{p}%', p/100) for p in lista_perc], value=0.96, description='% Bonificação:', style=style, layout=layout)

dropdown_marca = widgets.Dropdown(options=['Rothmans', 'Kent', 'Dunhill'], description='Marca Bonificação:', style=style, layout=layout)

btn_calcular = widgets.Button(description='CALCULAR BONIFICAÇÃO', button_style='success', layout={'width': '460px', 'height': '40px'})
output_painel = widgets.Output()

# Lógica para atualizar o Objetivo Máximo automaticamente ao mudar o plano ou objetivo 100%
def atualizar_objetivo_max(*args):
    input_obj_max.value = int(input_obj_100.value * dropdown_plano.value)

input_obj_100.observe(atualizar_objetivo_max, 'value')
dropdown_plano.observe(atualizar_objetivo_max, 'value')

def realizar_calculo(b):
    with output_painel:
        clear_output()
        
        est = dropdown_estado.value
        obj_100 = input_obj_100.value
        obj_max = input_obj_max.value
        perc = dropdown_percentual.value
        faixa = dropdown_faixa.value
        marca = dropdown_marca.value
        
        # 1. Trava de 80% (Baseado no percentual atingido informado)
        if perc < 0.8 and perc != 0:
            display(widgets.HTML("<b style='color:red;'>⚠️ Bonificação não atingida: O varejo não atingiu o mínimo de 80% do objetivo.</b>"))
            return

        # 2. Diferença de Pacotes (Excedente)
        diferenca = obj_max - obj_100
        
        # 3. Bonificação Adicional (Sobre o excedente)
        bonif_adicional = diferenca * perc
        
        # 4. Bonificação Fixa (Faixas)
        qtd_fixa = 2 if faixa <= 4 else 3
        
        # 5. Lógica de Conversão Financeira
        p_base = precos[est]['Rothmans (BASE)']
        if marca == 'Rothmans':
            res_bruto = bonif_adicional + qtd_fixa
        else:
            p_prem = precos[est][marca]
            # Converte o valor financeiro de Rothmans para a marca Premium
            res_bruto = (bonif_adicional * (p_base / p_prem)) + qtd_fixa

        resultado_final = round(res_bruto)

        # --- Saída Visual ---
        print("="*50)
        print(f"        RESULTADO FINAL ({est})")
        print("="*50)
        print(f"PLANO SELECIONADO: {next(k for k, v in planos_opcoes if v == dropdown_plano.value)}")
        print(f"Diferença (Máx - 100%): {diferenca} pct")
        print(f"Bonif. Adicional: {bonif_adicional:.2f} | Fixa: {qtd_fixa}")
        print("-" * 50)
        display(widgets.HTML(f"<h2 style='color:#28a745;'>✅ TOTAL: {resultado_final} PACOTES ({marca})</h2>"))
        print(f"(Cálculo exato: {res_bruto:.4f})")
        print("="*50)

btn_calcular.on_click(realizar_calculo)

display(widgets.HTML("<h2>🧮 Calculadora BAT - Completa</h2>"))
display(widgets.VBox([
    dropdown_estado, 
    input_obj_100, 
    dropdown_plano, 
    input_obj_max, 
    dropdown_faixa, 
    dropdown_percentual, 
    dropdown_marca, 
    btn_calcular
]))
display(output_painel)