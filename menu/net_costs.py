from datetime import date, datetime, timedelta
import streamlit as st
from data.querys_eshows import *
from menu.page import Page
from utils.components import *
from utils.functions import *


def BuildNetCost(liquidValuePerTraining):
    #st.write(liquidValuePerTraining)

    liquidValuePerTraining = liquidValuePerTraining[~liquidValuePerTraining['INTEGRANTES'].isin(['5 pessoas', '6 pessoas'])]
    liquidValuePerTraining = liquidValuePerTraining.copy()
    liquidValuePerTraining['MEDIA POR FORMACAO'] = liquidValuePerTraining['MEDIA POR FORMACAO'].astype(float)
    liquidValuePerTraining['Media de horas por show'] = liquidValuePerTraining['Media de horas por show'].astype(float)
    #st.write(liquidValuePerTraining)
    row_training = st.columns(2)
    with row_training[0]:
        component_plot_dual_axis_bar_line(liquidValuePerTraining,x_col='FORMAÇÃO',y_col_bar='OPORTUNIDADES',y_col_line='Valor por H',name='Oportunidade e Valor por Hora por Formação')
    with row_training[1]:
        component_plot_dual_axis_line_chart(liquidValuePerTraining,x_col='FORMAÇÃO',y_col1='MEDIA POR FORMACAO',y_col2='Media de horas por show',y_label1='Valor Médio (R$)',y_label2='Horas Médias',name='Comparação de Valor Médio e Horas Médias por Formação')
class NetCost(Page):
    def render(self):
        self.data = {}
        self.data['liquidValuePerTraining'] = liquid_value_per_training()
        
        
        BuildNetCost(self.data['liquidValuePerTraining'])