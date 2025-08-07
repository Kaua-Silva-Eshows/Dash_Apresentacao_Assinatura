from datetime import date, datetime, timedelta
import streamlit as st
from data.querys_eshows import *
from menu.page import Page
from utils.components import *
from utils.functions import *


def BuildNetCost():
    st.write("NetCost")


class NetCost(Page):
    def render(self):
        self.data = {}
        
        
        
        BuildNetCost()