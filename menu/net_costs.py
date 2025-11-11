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
        📅 Selecione Qualquer Dia do Mês para pegar o Mês fechado
         <span style="font-size: 20px; color: #ffb131;">
    </div>
    """,
    unsafe_allow_html=True
)
    
    #st.write(liquidValuePerTraining)
    # row_cards = st.columns(2)
    # with row_cards[0]:
    #     component_custom_card(
    #         title="Valor Médio por Formação",
    #         value=f"R$ {liquidValuePerTraining['MEDIA POR FORMACAO'].mean():,.2f}",
    #         subtitle="Média de valor por formação"
    #     )
    
    date_axis_bar, date_axis_bar2 = function_date_select_structure("row_date", 6, "Selecione um Mês", "Selecione um Mês")

    liquidValuePerTraining = liquid_value_per_training(date_axis_bar)
    liquidValuePerTraining = liquidValuePerTraining[~liquidValuePerTraining['INTEGRANTES'].isin(['5 pessoas', '6 pessoas'])]
    liquidValuePerTraining = liquidValuePerTraining.copy()
    liquidValuePerTraining['MEDIA POR FORMACAO'] = liquidValuePerTraining['MEDIA POR FORMACAO'].astype(float)
    liquidValuePerTraining['Media de horas por show'] = liquidValuePerTraining['Media de horas por show'].astype(float)
    
    liquidValuePerTraining2 = liquid_value_per_training(date_axis_bar2)
    liquidValuePerTraining2 = liquidValuePerTraining2[~liquidValuePerTraining2['INTEGRANTES'].isin(['5 pessoas', '6 pessoas'])]
    liquidValuePerTraining2 = liquidValuePerTraining2.copy()
    liquidValuePerTraining2['MEDIA POR FORMACAO'] = liquidValuePerTraining2['MEDIA POR FORMACAO'].astype(float)
    liquidValuePerTraining2['Media de horas por show'] = liquidValuePerTraining2['Media de horas por show'].astype(float)
    

    row_axis_bar_line = st.columns(2)
    with row_axis_bar_line[0]:
        component_plot_dual_axis_bar_line(liquidValuePerTraining,x_col='FORMAÇÃO',y_col_bar='OPORTUNIDADES',y_col_line='Valor por H', name='Oportunidades e Méd. Valor por Hora')
    
    with row_axis_bar_line[1]:
        component_plot_dual_axis_bar_line(liquidValuePerTraining2,x_col='FORMAÇÃO',y_col_bar='OPORTUNIDADES',y_col_line='Valor por H',name='Oportunidades e Méd. Valor por Hora')

    st.write('---')
    
    date_dual_axis, date_dual_axis2 = function_date_select_structure("row_date", 6, "Selecione um Mês", "Selecione um Mês")
    liquidValuePerTraining = liquid_value_per_training(date_dual_axis)
    liquidValuePerTraining2 = liquid_value_per_training(date_dual_axis2)
    row_dual_axis_line = st.columns(2)
    with row_dual_axis_line[0]:
        component_plot_dual_axis_line_chart(liquidValuePerTraining,x_col='FORMAÇÃO',y_col1='MEDIA POR FORMACAO',y_col2='Media de horas por show',y_label1='Valor Médio (R$)',y_label2='Horas Médias',name='Horas Méd. por Show e Valor Médio por Formação')
    with row_dual_axis_line[1]:    
        component_plot_dual_axis_line_chart(liquidValuePerTraining2,x_col='FORMAÇÃO',y_col1='MEDIA POR FORMACAO',y_col2='Media de horas por show',y_label1='Valor Médio (R$)',y_label2='Horas Médias',name='Horas Méd. por Show e Valor Médio por Formação')   

    st.write('---')

    date_dual_axis_bar, date_dual_axis_bar2 = function_date_select_structure("row_date", 6, "Selecione um Mês", "Selecione um Mês")

    liquidValuerPerStyle = liquid_valuer_per_style(date_dual_axis_bar)
    liquidValuerPerStyle2 = liquid_valuer_per_style(date_dual_axis_bar2)

    row_filter_style = st.columns(3)
    with row_filter_style[1]:
        style_selector = sorted(list(set(
            liquidValuerPerStyle['Estilo'].unique().tolist() +
            liquidValuerPerStyle2['Estilo'].unique().tolist()
        )))  
        options = ["Todos"] + style_selector

        style_filter = st.multiselect("Selecione o Estilo", options, default=["Todos"])

        if "Todos" in style_filter:
            style_filter = style_selector  
        else:
            style_filter = style_filter

    liquidValuerPerStyle_filtered = liquidValuerPerStyle[liquidValuerPerStyle['Estilo'].isin(style_filter)]
    liquidValuerPerStyle_filtered2 = liquidValuerPerStyle2[liquidValuerPerStyle2['Estilo'].isin(style_filter)]

    row_dual_axis_bar = st.columns(2)
    with row_dual_axis_bar[0]:
        component_plot_dual_axis_bar_chart(liquidValuerPerStyle_filtered,"Estilo", "Oportunidades", "Valor Total","Oportunidades", "Valor Total (R$)", "Oportunidades e Valor Total Por Estilo")

    with row_dual_axis_bar[1]:
        component_plot_dual_axis_bar_chart(liquidValuerPerStyle_filtered2,"Estilo", "Oportunidades", "Valor Total","Oportunidades", "Valor Total (R$)", "Oportunidades e Valor Total Por Estilo")
        
    st.write('---')

    date_line_chart, date_line_chart2 = function_date_select_structure("row_date", 6, "Selecione um Mês", "Selecione um Mês")
    liquidValuerPerStyle_filtered = liquid_valuer_per_style(date_line_chart)
    liquidValuerPerStyle_filtered2 = liquid_valuer_per_style(date_line_chart2)
    row_line_chart = st.columns(2)
    with row_line_chart[0]:
        liquidValuerPerStyle_filtered = liquidValuerPerStyle_filtered[liquidValuerPerStyle_filtered['Estilo'].isin(style_filter)]
        component_plot_line_chart(liquidValuerPerStyle_filtered, "Estilo", "Media por Show", "Media por Show", "Valor Méd. Por Show e Estilo")
    
    with row_line_chart[1]:
        liquidValuerPerStyle_filtered2 = liquidValuerPerStyle_filtered2[liquidValuerPerStyle_filtered2['Estilo'].isin(style_filter)]
        component_plot_line_chart(liquidValuerPerStyle_filtered2, "Estilo", "Media por Show", "Media por Show", "Valor Méd. Por Show e Estilo")

class NetCost(Page):
    def render(self):
        self.data = {}
        self.data['liquidValuePerTraining'] = liquid_value_per_training(date='2025-01')
        self.data['liquidValuerPerStyle'] = liquid_valuer_per_style(date='2025-01')
        self.data['liquidValuePerTraining2'] = liquid_value_per_training(date='2024-01')
        self.data['liquidValuerPerStyle2'] = liquid_valuer_per_style(date='2024-01')
        
        BuildNetCost(self.data['liquidValuePerTraining'],
                     self.data['liquidValuerPerStyle'],
                     self.data['liquidValuePerTraining2'],
                     self.data['liquidValuerPerStyle2'])