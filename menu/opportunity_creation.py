from datetime import date, datetime, timedelta
from decimal import Decimal
import streamlit as st
from data.querys_eshows import *
from menu.page import Page
from utils.components import *
from utils.functions import *


def BuildOpportunityCreation(avaregeOpportunityCreatedMonth, avaregeOpportunityCreatedYear):

    row_card = st.columns(4)

    with row_card[1]:
        AvaregeOpportunityCreated_2024 = avaregeOpportunityCreatedYear.loc[avaregeOpportunityCreatedYear['Ano'] == 2024, 'Media em DIAS'].iloc[0]
        OpportunityCreated_2024 = avaregeOpportunityCreatedYear.loc[avaregeOpportunityCreatedYear['Ano'] == 2024, 'Oportunidades'].iloc[0]

        component_custom_card("Med. Criação 2024", f"{AvaregeOpportunityCreated_2024:.2f} Dias", f"Oportunidades: {OpportunityCreated_2024}")

    with row_card[2]:
        AvaregeOpportunityCreated_2025 = avaregeOpportunityCreatedYear.loc[avaregeOpportunityCreatedYear['Ano'] == 2025, 'Media em DIAS'].iloc[0]
        OpportunityCreated_2025 = avaregeOpportunityCreatedYear.loc[avaregeOpportunityCreatedYear['Ano'] == 2025, 'Oportunidades'].iloc[0]

        component_custom_card("Med. Criação 2025", f"{AvaregeOpportunityCreated_2025:.2f} Dias", f"Oportunidades: {OpportunityCreated_2025}")

    
    for col in avaregeOpportunityCreatedMonth.columns:avaregeOpportunityCreatedMonth[col] = avaregeOpportunityCreatedMonth[col].map(lambda x: float(x) if isinstance(x, Decimal) else x)
    component_plot_DualAxis_Chart(avaregeOpportunityCreatedMonth, x_col='Mes/Ano', y_col_bar='Oportunidades', y_col_line='Media em DIAS', name='Total de Oportunidades vs Média de Criação', key="avaregeOpportunityCreatedMonth_key")



class OpportunityCreation(Page):
    def render(self):
        self.data = {}
        self.data['avaregeOpportunityCreatedMonth'] = avarege_opportunity_created_month()
        self.data['avaregeOpportunityCreatedYear'] = avarege_opportunity_created_year()


    
        BuildOpportunityCreation(self.data['avaregeOpportunityCreatedMonth'],
                                 self.data['avaregeOpportunityCreatedYear'])