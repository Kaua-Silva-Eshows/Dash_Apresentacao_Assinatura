from datetime import date, datetime, timedelta
from decimal import Decimal
import streamlit as st
from data.querys_eshows import *
from menu.page import Page
from utils.components import *
from utils.functions import *


def BuildOpportunityCreation(avaregeOpportunityCreatedMonth, avaregeOpportunityCreatedYear, recusedOpportunities, canceledOpportunities):

    row_card = st.columns(4)

    with row_card[0]:
        AvaregeOpportunityCreated_2024 = avaregeOpportunityCreatedYear.loc[avaregeOpportunityCreatedYear['Ano'] == 2024, 'Media em DIAS'].iloc[0]
        OpportunityCreated_2024 = avaregeOpportunityCreatedYear.loc[avaregeOpportunityCreatedYear['Ano'] == 2024, 'Oportunidades'].iloc[0]

        component_custom_card("Med. Criação 2024", f"{AvaregeOpportunityCreated_2024:.2f} Dias", f"Oportunidades: {OpportunityCreated_2024}")

    with row_card[1]:
        AvaregeOpportunityCreated_2025 = avaregeOpportunityCreatedYear.loc[avaregeOpportunityCreatedYear['Ano'] == 2025, 'Media em DIAS'].iloc[0]
        OpportunityCreated_2025 = avaregeOpportunityCreatedYear.loc[avaregeOpportunityCreatedYear['Ano'] == 2025, 'Oportunidades'].iloc[0]

        component_custom_card("Med. Criação 2025", f"{AvaregeOpportunityCreated_2025:.2f} Dias", f"Oportunidades: {OpportunityCreated_2025}")
    
    with row_card[2]:
        recusedOpportunities_2024 = recusedOpportunities[recusedOpportunities['Mes/Ano'].str.contains('2024')]['QUANTIDADE RECUSA'].mean()
        component_custom_card("Med. Recusas 2024", f"{recusedOpportunities_2024:.2f}", f"Recusas: {recusedOpportunities[recusedOpportunities['Mes/Ano'].str.contains('2024')]['QUANTIDADE RECUSA'].sum()}")

    with row_card[3]:
        recusedOpportunities_2025 = recusedOpportunities[recusedOpportunities['Mes/Ano'].str.contains('2025')]['QUANTIDADE RECUSA'].mean()
        component_custom_card("Med. Recusas 2025", f"{recusedOpportunities_2025:.2f}", f"Recusas: {recusedOpportunities[recusedOpportunities['Mes/Ano'].str.contains('2025')]['QUANTIDADE RECUSA'].sum()}")

    for col in avaregeOpportunityCreatedMonth.columns:avaregeOpportunityCreatedMonth[col] = avaregeOpportunityCreatedMonth[col].map(lambda x: float(x) if isinstance(x, Decimal) else x)
    opportunity_graph_merge = recusedOpportunities.merge(avaregeOpportunityCreatedMonth, on='Mes/Ano', how='right')
    component_plot_DualAxis_Chart(opportunity_graph_merge, x_col='Mes/Ano', y_col_bar='Oportunidades', y_col_bar2='QUANTIDADE RECUSA', y_col_line='Media em DIAS', y_col_line2= 'Media até Candidatura H', y_col_line3='Media até Aceite D', name='Total de Oportunidades com Média de Criação')
    st.markdown("---")
    component_plot_stacked_chart(canceledOpportunities, mes_col= 'Mes/Ano', motivo_col= 'MOTIVO', qtd_col= 'CANCELAMENTOS', name='Oportunidades Canceladas por Motivo')   
class OpportunityCreation(Page):
    def render(self):
        
        self.data = {}
        self.data['avaregeOpportunityCreatedMonth'] = avarege_opportunity_created_month()
        self.data['avaregeOpportunityCreatedYear'] = avarege_opportunity_created_year()
        self.data['recusedOpportunities'] = recused_opportunities()
        self.data['canceledOpportunities'] = canceled_opportunities()


    
        BuildOpportunityCreation(self.data['avaregeOpportunityCreatedMonth'],
                                 self.data['avaregeOpportunityCreatedYear'],
                                 self.data['recusedOpportunities'],
                                 self.data['canceledOpportunities'])