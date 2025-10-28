from datetime import date, datetime, timedelta
import streamlit as st
from data.querys_eshows import *
from menu.page import Page
from utils.components import *
from utils.functions import *


def BuildNetCost(liquidValuePerTraining, liquidValuerPerStyle, liquidValuePerTraining2, liquidValuerPerStyle2):
    #st.write(liquidValuePerTraining)
    if st.session_state.get("base_theme") == "dark":
        text_color = "#ffffff"
    else:
        text_color = "#000000"
    st.markdown(f"""<div style="text-align: center; font-weight: bold; font-size: 20px; color: #ffb131; margin: 20px 0;">
        📅 Dados Referentes ao Período de 
        <span style="font-size: 20px; color: {text_color};">20/08/2025</span> <span style="font-size: 20px; color: #ffb131;">até</span> <span style="font-size: 20px; color: {text_color};"> 20/09/2025</span>
    </div>
    """,
    unsafe_allow_html=True
)
    liquidValuePerTraining = liquidValuePerTraining[~liquidValuePerTraining['INTEGRANTES'].isin(['5 pessoas', '6 pessoas'])]
    liquidValuePerTraining = liquidValuePerTraining.copy()
    liquidValuePerTraining['MEDIA POR FORMACAO'] = liquidValuePerTraining['MEDIA POR FORMACAO'].astype(float)
    liquidValuePerTraining['Media de horas por show'] = liquidValuePerTraining['Media de horas por show'].astype(float)
    
    liquidValuePerTraining2 = liquidValuePerTraining2[~liquidValuePerTraining2['INTEGRANTES'].isin(['5 pessoas', '6 pessoas'])]
    liquidValuePerTraining2 = liquidValuePerTraining2.copy()
    liquidValuePerTraining2['MEDIA POR FORMACAO'] = liquidValuePerTraining2['MEDIA POR FORMACAO'].astype(float)
    liquidValuePerTraining2['Media de horas por show'] = liquidValuePerTraining2['Media de horas por show'].astype(float)
    
    #st.write(liquidValuePerTraining)
    # row_cards = st.columns(2)
    # with row_cards[0]:
    #     component_custom_card(
    #         title="Valor Médio por Formação",
    #         value=f"R$ {liquidValuePerTraining['MEDIA POR FORMACAO'].mean():,.2f}",
    #         subtitle="Média de valor por formação"
    #     )
    row_training = st.columns(2)
    with row_training[0]:
        component_plot_dual_axis_bar_line(liquidValuePerTraining,x_col='FORMAÇÃO',y_col_bar='OPORTUNIDADES',y_col_line='Valor por H',name='Oportunidades e Méd. Valor por Hora 20/08 a 20/09')
        component_plot_dual_axis_line_chart(liquidValuePerTraining,x_col='FORMAÇÃO',y_col1='MEDIA POR FORMACAO',y_col2='Media de horas por show',y_label1='Valor Médio (R$)',y_label2='Horas Médias',name='Horas Méd. por Show e Valor Médio por Formação 20/08 a 20/09')   
    with row_training[1]:
        component_plot_dual_axis_bar_line2(liquidValuePerTraining2,x_col='FORMAÇÃO',y_col_bar='OPORTUNIDADES',y_col_line='Valor por H',name='Oportunidades e Méd. Valor por Hora 20/09 a 20/10')
        component_plot_dual_axis_line_chart2(liquidValuePerTraining2,x_col='FORMAÇÃO',y_col1='MEDIA POR FORMACAO',y_col2='Media de horas por show',y_label1='Valor Médio (R$)',y_label2='Horas Médias',name='Horas Méd. por Show e Valor Médio por Formação 20/09 a 20/10')
    st.write('---')

    row_filter_style = st.columns(3)
    with row_filter_style[1]:
        style_selector = liquidValuerPerStyle['Estilo'].unique().tolist()
        options = ["Todos"] + style_selector

        style_filter = st.multiselect("Selecione o Estilo", options, default=["Todos"])

        # Interpretar seleção:
        if "Todos" in style_filter:
            style_filter = style_selector  # seleciona todos os estilos
        else:
            style_filter = style_filter

    row_style = st.columns(2)
    with row_style[0]:
        liquidValuerPerStyle_filtered = liquidValuerPerStyle[liquidValuerPerStyle['Estilo'].isin(style_filter)]
        component_plot_dual_axis_bar_chart(liquidValuerPerStyle_filtered, "Estilo", "Oportunidades", "Valor Total", "Oportunidades", "Valor Total (R$)", "Oportunidades e Valor Total Por Estilo 20/08 a 20/09")
        liquidValuerPerStyle_filtered = liquidValuerPerStyle[liquidValuerPerStyle['Estilo'].isin(style_filter)]
        component_plot_line_chart(liquidValuerPerStyle_filtered, "Estilo", "Media por Show", "Media por Show", "Valor Méd. Por Show e Estilo 20/08 a 20/09")
    
    with row_style[1]:
        liquidValuerPerStyle_filtered2 = liquidValuerPerStyle2[liquidValuerPerStyle2['Estilo'].isin(style_filter)]
        component_plot_dual_axis_bar_chart2(liquidValuerPerStyle_filtered2, "Estilo", "Oportunidades", "Valor Total", "Oportunidades", "Valor Total (R$)", "Oportunidades e Valor Total Por Estilo 20/09 a 20/10")
        liquidValuerPerStyle_filtered2 = liquidValuerPerStyle2[liquidValuerPerStyle2['Estilo'].isin(style_filter)]
        component_plot_line_chart2(liquidValuerPerStyle_filtered2, "Estilo", "Media por Show", "Media por Show", "Valor Méd. Por Show e Estilo 20/09 a 20/10")

class NetCost(Page):
    def render(self):
        self.data = {}
        self.data['liquidValuePerTraining'] = liquid_value_per_training(day1='2025-08-20', day2='2025-09-20')
        self.data['liquidValuerPerStyle'] = liquid_valuer_per_style(day1='2025-08-20', day2='2025-09-20')
        self.data['liquidValuePerTraining2'] = liquid_value_per_training(day1='2025-09-20', day2='2025-10-21')
        self.data['liquidValuerPerStyle2'] = liquid_valuer_per_style(day1='2025-09-20', day2='2025-10-21')
        
        BuildNetCost(self.data['liquidValuePerTraining'],
                     self.data['liquidValuerPerStyle'],
                     self.data['liquidValuePerTraining2'],
                     self.data['liquidValuerPerStyle2'])