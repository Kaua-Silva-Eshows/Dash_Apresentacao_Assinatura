import streamlit as st
from st_aggrid import GridUpdateMode, JsCode, StAggridTheme
from st_aggrid import AgGrid, GridOptionsBuilder
from streamlit_echarts import st_echarts
import pandas as pd

def component_hide_sidebar():
    st.markdown(""" 
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
                display: none;
                }
    </style>
    """, unsafe_allow_html=True)

def component_fix_tab_echarts():
    streamlit_style = """
    <style>
    iframe[title="streamlit_echarts.st_echarts"]{ height: 450px; width: 750px;} 
   </style>
    """

    return st.markdown(streamlit_style, unsafe_allow_html=True)

def component_effect_underline():
    if st.session_state.get("base_theme") == "dark":
        color = "#ffffff"
    else:
        color = "#000000" 
    st.markdown(
    f"""<style>.full-width-line-white {{width: 100%;border-bottom: 1px solid {color};margin-bottom: 0.5em;}}</style>""",unsafe_allow_html=True)

def component_plotDataframe(df, name, num_columns=[], percent_columns=[], df_details=None, coluns_merge_details=None, coluns_name_details=None, key="default"):


    st.markdown(f"<h5 style='text-align: center; background-color: #ffb131; padding: 0.1em;'>{name}</h5>",unsafe_allow_html=True)
    # Converter colunas selecionadas para float com limpeza de texto
    for col in num_columns:
        if col in df.columns:
            df[f"{col}_NUM"] = (
                df[col]
                .astype(str)
                .str.upper()
                .str.replace(r'[A-Z$R\s]', '', regex=True)
                .str.replace('.', '', regex=False)
                .str.replace(',', '.', regex=False)
            )
            df[f"{col}_NUM"] = pd.to_numeric(df[f"{col}_NUM"], errors='coerce')

            # Formatar a coluna original como string BR
            df[col] = df[f"{col}_NUM"].apply(
                lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if pd.notnull(x) else ""
            )

    for col in percent_columns:
        if col in df.columns:
            df[f"{col}_NUM"] = (
                df[col]
                .astype(str)
                .str.replace('%', '', regex=False)
                .str.replace(',', '.', regex=False)
                .str.replace('−', '-', regex=False)
                .str.replace('–', '-', regex=False)
                .str.replace(r'[^\d\.\-]', '', regex=True)
            )
            df[f"{col}_NUM"] = pd.to_numeric(df[f"{col}_NUM"], errors='coerce')

            # Formatar a coluna original como string percentual
            df[col] = df[f"{col}_NUM"].apply(
                lambda x: f"{x:.2f}%".replace('.', ',') if pd.notnull(x) else ""
            )

    # Definir cellStyle para pintar valores negativos/positivos
    cellstyle_code = JsCode("""
    function(params) {
        const value = params.data[params.colDef.field + '_NUM'];
        if (value === null || value === undefined || isNaN(value)) {
            return {};
        }
        if (value < 0) {
            return {
                color: '#ff7b7b',
                fontWeight: 'bold'
            };
        }
        if (value > 0) {
            return {
                color: '#90ee90',
                fontWeight: 'bold'
            };
        }
        return {};
    }
    """)

    # Construir grid options builder
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(filter=True)

    # Esconder colunas _NUM e detail
    for col in num_columns + percent_columns:
        if f"{col}_NUM" in df.columns:
            gb.configure_column(f"{col}_NUM", hide=True, type=["numericColumn"])
    if "detail" in df.columns:
        gb.configure_column("detail", hide=True)

    grid_options = gb.build()

    if df_details is not None:
        df['detail'] = df[coluns_merge_details].apply(
            lambda i: df_details[df_details[coluns_merge_details] == i].to_dict('records')
        )

        special_column = {
            "field": coluns_name_details,
            "cellRenderer": "agGroupCellRenderer",
            "checkboxSelection": False,
        }

        other_columns = []
        for col in df.columns:
            if col in [coluns_name_details, "detail"]:
                continue
            col_def = {"field": col}
            if col in num_columns + percent_columns:
                col_def["cellStyle"] = cellstyle_code
            other_columns.append(col_def)

        columnDefs = [special_column] + other_columns

        detail_columnDefs = [{"field": c} for c in df_details.columns]

        grid_options.update({
            "masterDetail": True,
            "columnDefs": columnDefs,
            "detailCellRendererParams": {
                "detailGridOptions": {
                    "columnDefs": detail_columnDefs,
                },
                "getDetailRowData": JsCode("function(params) {params.successCallback(params.data.detail);}"),
            },
            "rowData": df.to_dict('records'),
            "enableRangeSelection": True,
            "suppressRowClickSelection": True,
            "cellSelection": True,
            "rowHeight": 40,
            "defaultColDef": {
                "flex": 1,
                "minWidth": 100,
                "autoHeight": False,
                "filter": True,
            }
        })

    else:
        grid_options.update({
            "enableRangeSelection": True,
            "suppressRowClickSelection": False,
            "cellSelection": False,
            "rowHeight": 40,
            "defaultColDef": {
                "flex": 1,
                "minWidth": 100,
                "autoHeight": False,
                "filter": True,
            }
        })

    # Criar DataFrame sem colunas técnicas
    cols_to_drop = [col for col in df.columns if col.endswith('_NUM') or col == 'detail']
    df_to_show = df.drop(columns=cols_to_drop, errors='ignore')

    # Ajustar columnDefs se não for masterDetail
    if "masterDetail" not in grid_options:
        grid_options["columnDefs"] = [{"field": col} for col in df_to_show.columns]

    # Adicionar efeito zebra (linhas alternadas)
    if st.session_state.get("base_theme") == "dark":
        custom_theme = (StAggridTheme(base="balham").withParams().withParts('colorSchemeDark'))
    # Zebra escura
        grid_options["getRowStyle"] = JsCode('''
        function(params) {
            if (params.node.rowIndex % 2 === 0) {
                return { background: '#222', color: '#fff' };
            } else {
                return { background: '#333', color: '#fff' };
            }
        }
        ''')
    else:
    # Zebra clara (padrão)
        custom_theme = (StAggridTheme(base="balham").withParams())
        grid_options["getRowStyle"] = JsCode('''
        function(params) {
            if (params.node.rowIndex % 2 === 0) {
                return { background: '#fff', color: '#111' };
            } else {
                return { background: '#e0e0e0', color: '#111' };
            }
        }
        ''')

    # Mostrar AgGrid
    grid_response = AgGrid(
        df_to_show,
        gridOptions=grid_options,
        enable_enterprise_modules=True,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,
        key=f"aggrid_{name}_{key}",
        theme=custom_theme
    )

    filtered_df = grid_response['data']
    filtered_df = filtered_df.drop(columns=[col for col in filtered_df.columns if col.endswith('_NUM')], errors='ignore')
    return filtered_df, len(filtered_df)

def component_plot_Stacked_Line_Chart(df, x_col, y_cols, name, key):
        st.markdown(
            f"<h5 style='text-align: center; background-color: #ffb131; padding: 0.1em;'>{name}</h5>",
            unsafe_allow_html=True
        )

        df_sorted = df.copy()

        try:
            df_sorted[x_col] = pd.to_datetime(df_sorted[x_col], format='%m/%Y')
            df_sorted = df_sorted.sort_values(by=x_col)
            # Formata para mês/ano novamente (string) para o eixo X
            df_sorted[x_col] = df_sorted[x_col].dt.strftime('%m/%Y')
        except Exception as e:
            st.error(f"Erro ao converter datas: {e}")
            return

        options = {
            "title": None,
            "tooltip": {
    "trigger": "axis",
    "axisPointer": {
        "type": "cross",
        "label": {"backgroundColor": "#6a7985"}
    },
    "formatter": None
},
            "legend": {
                "data": y_cols,
                "top": 30,
                "selectedMode": "multiple",  # Permite selecionar/desselecionar séries
                "textStyle": {"color": "#555"}
            },
            "grid": {"left": "3%", "right": "4%", "bottom": "5%", "containLabel": True},
            "toolbox": {
                "feature": {
                    "saveAsImage": {},
                    "dataZoom": {
                        "yAxisIndex": "none"
                    },
                    "restore": {}
                }
            },
            "dataZoom": [
                {
                    "type": "slider",
                    "start": 0,
                    "end": 100,
                    "bottom": 0,
                    "height": 20,
                    "handleSize": "100%",
                    "handleStyle": {"color": "#ffb131"},
                    "backgroundColor": "#f2f2f2",
                    "borderColor": "#ddd"
                },
                {
                    "type": "inside",
                    "start": 0,
                    "end": 100
                }
            ],
            "xAxis": {
                "type": "category",
                "boundaryGap": True,
                "data": df_sorted[x_col].tolist(),
                "axisLine": {"lineStyle": {"color": "#999"}},
                "axisLabel": {"rotate": 45, "formatter": "{value}"}
            },
            "yAxis": [
                {
                    "type": "value",
                    "name": "Total",
                    "position": "left",
                    "axisLine": {"lineStyle": {"color": "#999"}},
                    "splitLine": {"lineStyle": {"type": "dashed", "color": "#eee"}}
                }
            ],
            "series": [
                {
                    "name": col,
                    "type": "line",
                    "stack": "Total",
                    "smooth": True,
                    "lineStyle": {"width": 3},
                    "areaStyle": {},  # Preenche área sob a curva para efeito empilhado visual
                    "data": [float(x) for x in df_sorted[col].fillna(0)]
                }
                for col in y_cols
            ]
        }
        st_echarts(options=options, height="500px", key=key)

def component_plot_DualAxis_Chart(df, x_col, y_col_bar, y_col_line, name, key):
    st.markdown(f"<h5 style='text-align: center; background-color: #ffb131; padding: 0.1em;'>{name}</h5>",unsafe_allow_html=True)

    df_sorted = df.copy()
    try:
        df_sorted[x_col] = pd.to_datetime(df_sorted[x_col], format='%m/%Y')
        df_sorted = df_sorted.sort_values(by=x_col)
        # Não converter para string para manter o datetime (melhor para ordenação)
    except Exception as e:
        st.error(f"Erro ao converter datas: {e}")
        return

    # Para o eixo x como strings formatadas:
    x_labels = df_sorted[x_col].dt.strftime('%m/%Y').tolist()

    options = {
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "cross"}},
        "toolbox": {"feature": {"saveAsImage": {}, "restore": {}, "dataView": {"readOnly": True}}},
        "legend": {"data": [y_col_bar, y_col_line], "top": 30},
        "xAxis": {"type": "category", "data": x_labels, "axisLabel": {"rotate": 45}},
        "yAxis": [
            {"type": "value", "name": y_col_bar, "position": "left", "axisLabel": {"formatter": "{value}"}},
            {"type": "value", "name": y_col_line, "position": "right", "axisLabel": {"formatter": "{value} dias"}}
        ],
        "series": [
            {"name": y_col_bar, "type": "bar", "yAxisIndex": 0, "data": df_sorted[y_col_bar].fillna(0).tolist(), "barWidth": "40%"},
            {"name": y_col_line, "type": "line", "yAxisIndex": 1, "smooth": True, "lineStyle": {"width": 3}, "data": df_sorted[y_col_line].fillna(0).tolist()}
        ]
    }

    # Use chave dinâmica para forçar atualização
    st_echarts(options=options, height="500px", key=key)

def component_plot_dual_axis_line_chart(df, x_col, y_col1, y_col2, y_label1, y_label2, name, key):
    st.markdown(f"<h5 style='text-align: center; background-color: #ffb131; padding: 0.1em;'>{name}</h5>",unsafe_allow_html=True)

    df_sorted = df.copy()
    categorias = df_sorted[x_col].tolist()
    dados1 = df_sorted[y_col1].apply(float).tolist()
    dados2 = df_sorted[y_col2].apply(float).tolist()

    # Cores derivadas do laranja #ffb131, com variações para distinguir as duas linhas
    cor1 = "#ffb131"        # laranja principal
    cor2 = "#4200db"        # azul mais escuro para contraste

    options = {
        "tooltip": {"trigger": "axis"},
        "legend": {"data": [y_label1, y_label2], "top": 30},
        "grid": {"left": "5%", "right": "5%", "bottom": "10%", "containLabel": True},
        "xAxis": {
            "type": "category",
            "data": categorias,
            "axisLine": {"lineStyle": {"color": "#999"}},
            "axisLabel": {"rotate": 0}
        },
        "yAxis": [
            {
                "type": "value",
                "name": y_label1,
                "position": "left",
                "axisLine": {"lineStyle": {"color": cor1}},
                "splitLine": {"lineStyle": {"type": "dashed", "color": "#eee"}}
            },
            {
                "type": "value",
                "name": y_label2,
                "position": "right",
                "axisLine": {"lineStyle": {"color": cor2}},
                "splitLine": {"show": False}
            }
        ],
        "series": [
            {
                "name": y_label1,
                "type": "line",
                "data": dados1,
                "yAxisIndex": 0,
                "smooth": True,
                "lineStyle": {"color": cor1, "width": 3},
                "symbol": "circle",
                "symbolSize": 8,
                "itemStyle": {"color": cor1}
            },
            {
                "name": y_label2,
                "type": "line",
                "data": dados2,
                "yAxisIndex": 1,
                "smooth": True,
                "lineStyle": {"color": cor2, "width": 3},
                "symbol": "circle",
                "symbolSize": 8,
                "itemStyle": {"color": cor2}
            }
        ]
    }

    st_echarts(options=options, height="500px", key=key)

def component_plot_dual_axis_bar_line(df, x_col, y_col_bar, y_col_line, name, key):
    st.markdown(f"<h5 style='text-align: center; background-color: #ffb131; padding: 0.1em;'>{name}</h5>",unsafe_allow_html=True)

    # Converter colunas para float (evita problemas com Decimal)
    df_sorted = df.copy()
    df_sorted.loc[:, y_col_bar] = df_sorted[y_col_bar].astype(float)
    df_sorted.loc[:, y_col_line] = df_sorted[y_col_line].astype(float)

    options = {
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "cross"}
        },
        "toolbox": {
            "feature": {"saveAsImage": {}, "restore": {}, "dataView": {"readOnly": True}}
        },
        "legend": {"data": [y_col_bar, y_col_line], "top": 30},
        "xAxis": {
            "type": "category",
            "data": df_sorted[x_col].tolist(),
            "axisLabel": {"rotate": 0}
        },
        "yAxis": [
            {
                "type": "value",
                "name": y_col_bar,
                "position": "left",
                "axisLabel": {"formatter": "{value}"}
            },
            {
                "type": "value",
                "name": y_col_line,
                "position": "right",
                "axisLabel": {"formatter": f"R$ {{value}}"}
            }
        ],
        "series": [
            {
                "name": y_col_bar,
                "type": "bar",
                "yAxisIndex": 0,
                "data": df_sorted[y_col_bar].tolist(),
                "barWidth": "40%",
                "itemStyle": {"color": "#ffb131"}
            },
            {
                "name": y_col_line,
                "type": "line",
                "yAxisIndex": 1,
                "smooth": True,
                "lineStyle": {"width": 3, "color": "#4200db"},
                "data": df_sorted[y_col_line].tolist(),
                "symbol": "circle",
                "symbolSize": 8,
                "itemStyle": {"color": "#4200db"}
            }
        ]
    }

    st_echarts(options=options, height="500px", key=key)

def component_custom_card(title, value, subtitle=""):
        card_html = f"""<div style="
    background: #ffb131;
    padding: 15px;
    border-radius: 5px;
    width: 230px;
    height: 130px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    color: white;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 10px auto;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
">
    <h3 style="margin: 0; font-weight: 600; font-size: 1.2rem; text-align: left; margin-left: 25px;">{title}</h3>
    <p style="margin: 0; font-size: 1.8rem; font-weight: 700; line-height: 1.8rem;">{value}</p>
    <small style="opacity: 0.85; font-size: 0.85rem; margin-top: 4px;">{subtitle}</small>
</div>
"""
        st.markdown(card_html, unsafe_allow_html=True)