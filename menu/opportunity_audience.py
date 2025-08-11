from datetime import date, datetime, timedelta
import streamlit as st
from data.querys_eshows import *
from menu.page import Page
from utils.components import *
from utils.functions import *

def BuildOpportunityAudience(avaregeCandidatesOpportunityMonth, avaregeCandidatesOpportunityWeek, avaregeCandidatesByArtist):

    with st.expander("Candidaturas Mensais"): 
        avaregeCandidatesOpportunityMonth_graph, len_df = component_plotDataframe(avaregeCandidatesOpportunityMonth, "Media de Candidatos por Oportunidade Mensal", key="avaregeCandidatesOpportunityMonth_key")

    component_plot_Stacked_Line_Chart(avaregeCandidatesOpportunityMonth_graph, "Data", ["Media por Vaga", "Total de Oportunidades", "Total de Candidaturas"], "Candidaturas Mensais", height="440px", width="100%")

    with st.expander("Candidaturas Semanais"):
        df_copy, len_df = component_plotDataframe(avaregeCandidatesOpportunityWeek, "Media de Candidatos por Oportunidade Semanal", key="avaregeCandidatesOpportunityWeek_key")
    
    st.write('---')

    row_date = st.columns([2,1,2])
    with row_date[1]:
        day_range = st.date_input("Selecione o intervalo de datas",value=(date(2025, 1, 1), date(2025, 7, 31)),key="date_range",label_visibility="visible")

        if isinstance(day_range, tuple) and len(day_range) == 2:
            day, day2 = day_range
        else:
            st.error("Selecione o intervalo de datas corretamente.")
            return

    avaregeCandidatesByArtist = avarege_candidates_by_artist(day, day2)

    row_card = st.columns([1,2,2,2,1])
    with row_card[1]:
        applications_artist = function_format_number(avaregeCandidatesByArtist['Candidaturas do Artista'].sum())
        component_custom_card("Total de Candidaturas", applications_artist, "Candidaturas")
    with row_card[2]:
        applications_greater_35 = function_format_number(avaregeCandidatesByArtist['Candidatos Ativos'].unique()[0])
        component_custom_card("Artistas com Mais de 35 Candidaturas", applications_greater_35, "01/2025 a 07/2025")
    with row_card[3]:
        component_custom_card("Artistas Distintos", avaregeCandidatesByArtist['ARTISTA'].nunique(), "Artistas Distintos")

    avaregeCandidatesByArtist.drop(columns=['Candidatos Ativos'], inplace=True)
    component_plotDataframe(avaregeCandidatesByArtist, "Media de Candidaturas por Artista", key="avaregeCandidatesByArtist")

    row = st.columns(2)
    with row[0]:
        with st.expander("Top Maior Candidaturas e Menor Aceite"):
            filtro = ((avaregeCandidatesByArtist['Média de Candidaturas por Mês'] >= 70) &(avaregeCandidatesByArtist['Média Aceite por Mês'] <= 8))

            top_few_high_accept = avaregeCandidatesByArtist.loc[filtro].sort_values(by=['Média de Candidaturas por Mês', 'Média Aceite por Mês'],ascending=[False, True]).head(10)

            top_few_high_accept = top_few_high_accept[['ARTISTA', 'Média de Candidaturas por Mês', 'Média Aceite por Mês']]
            component_plotDataframe(top_few_high_accept, "Artistas com maior Med. Candidaturas e menor Med. Aceite", key="top_few_high_accept")
    
    with row[1]:
        with st.expander("Top Menor Candidaturas e Maior Aceite"):
            filtro = ((avaregeCandidatesByArtist['Média de Candidaturas por Mês'] <= 40) &(avaregeCandidatesByArtist['Média Aceite por Mês'] >= 6))
            
            low_candidates_top_accepts = avaregeCandidatesByArtist.loc[filtro].sort_values(by=['Média de Candidaturas por Mês', 'Média Aceite por Mês'],ascending=[False, True]).head(10)

            low_candidates_top_accepts = low_candidates_top_accepts[['ARTISTA', 'Média de Candidaturas por Mês', 'Média Aceite por Mês']]
            component_plotDataframe(low_candidates_top_accepts, "Artistas com menor Med. Candidaturas e maior Med. Aceite")

    #Artistas com menor Media de Candidaturas e maior Media de Aceite

class OpportunityAudience(Page):
    def render(self):
        self.data = {}
        day = '2025-01-01' 
        day2 = '2025-07-31'
        self.data['avaregeCandidatesOpportunityMonth'] = avarege_candidates_by_opportunity_month()
        self.data['avaregeCandidatesOpportunityWeek'] = avarege_candidates_by_opportunity_week()
        self.data['avaregeCandidatesByArtist'] = avarege_candidates_by_artist(day, day2)
        
        BuildOpportunityAudience(self.data['avaregeCandidatesOpportunityMonth'],
                   self.data['avaregeCandidatesOpportunityWeek'],
                   self.data['avaregeCandidatesByArtist'])