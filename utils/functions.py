import hashlib
import numpy as np
import pandas as pd
import streamlit.components.v1 as components
import streamlit as st

def function_copy_dataframe_as_tsv(df):
    # Converte o DataFrame para uma string TSV
    df_tsv = df.to_csv(index=False, sep='\t')
    
    # Gera código HTML e JavaScript para copiar o conteúdo para a área de transferência
    components.html(
        f"""
        <style>
            .custom-copy-btn {{
                background: linear-gradient(90deg, #ffb131 0%, #ff7f50 100%);
                color: #fff;
                border: none;
                padding: 12px 28px 12px 18px;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                display: inline-flex;
                align-items: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.10);
                transition: background 0.3s, color 0.3s;
                position: relative;
                gap: 8px;
            }}
            .custom-copy-btn:hover {{
                background: linear-gradient(90deg, #ff7f50 0%, #ffb131 100%);
                color: #222;
            }}
            .copy-icon {{
                width: 20px;
                height: 20px;
                vertical-align: middle;
                fill: currentColor;
            }}
        </style>
        <textarea id="clipboard-textarea" style="position: absolute; left: -10000px;">{df_tsv}</textarea>
        <button class="custom-copy-btn" id="copy-btn" onclick="copyDF()">
            <svg class='copy-icon' viewBox='0 0 24 24'><path d='M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z'/></svg>
            <span id="copy-btn-text">Copiar DataFrame</span>
        </button>
        <script>
        function copyDF() {{
            var textarea = document.getElementById('clipboard-textarea');
            textarea.select();
            document.execCommand('copy');
            var btn = document.getElementById('copy-btn');
            var btnText = document.getElementById('copy-btn-text');
            btnText.innerText = 'Copiado!';
            btn.style.background = 'linear-gradient(90deg, #4BB543 0%, #43e97b 100%)';
            setTimeout(function() {{
                btnText.innerText = 'Copiar DataFrame';
                btn.style.background = 'linear-gradient(90deg, #ffb131 0%, #ff7f50 100%)';
            }}, 1500);
        }}
        </script>
        """,
        height=110
    )

def function_box_lenDf(len_df,df,y='', x='', box_id='', item=''):
    len_df = len(df)
    st.markdown(
        """
        <style>
        .small-box {
            border: 1px solid #ffb131; /* Cor da borda */
            border-radius: 5px; /* Cantos arredondados */
            padding: 10px; /* Espaçamento interno */
            background-color: transparent; /* Cor de fundo da caixa */
            box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.1); /* Sombra */
            font-size: 14px; /* Tamanho da fonte */
            font-weight: bold; /* Negrito */
            text-align: center; /* Alinhamento do texto */
            width: 150px; /* Largura da caixinha */
            z-index: 1; /* Garantir que a caixa fique acima de outros elementos */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # CSS para o posicionamento específico via ID
    st.markdown(
        f"""
        <style>
        #{box_id} {{
            position: absolute; /* Posicionamento absoluto */
            top: {y}px; /* Distância do topo da página */
            left: {x}px; /* Distância da borda esquerda da página */
        }}
        </style>
        <div id="{box_id}" class="small-box">
            O DataFrame contém <span style="color: #ffb131;">{len_df}</span> {item}.
        </div>
        """,
        unsafe_allow_html=True
    )

def function_format_number_columns(df=None, columns=[], valor=None):
    if valor is not None:
        try:
            valor = float(valor)
            return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except (ValueError, TypeError):
            return ""

    # Formatando colunas de DataFrame
    if df is not None and columns:
        for column in columns:
            if column in df.columns:
                try:
                    df[column] = pd.to_numeric(df[column], errors='coerce')
                    df[column] = df[column].apply(
                        lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                        if pd.notnull(x) else ''
                    )
                except Exception:
                    continue
        return df

def function_total_line(df, column_values, column_total):
    if isinstance(column_values, str):
        column_values = [column_values]

    total_values = {}
    for col in column_values:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        total_values[col] = df[col].sum()

    new_row = {col: total_values.get(col, np.nan) for col in column_values}
    new_row[column_total] = "Total:"

    for col in df.columns:
        if col not in new_row:
            new_row[col] = np.nan  # Use np.nan, não ""

    new_row_df = pd.DataFrame([new_row])
    df = pd.concat([df, new_row_df], ignore_index=True)

    return df

def function_generate_chart_key(*args):
    return hashlib.md5("_".join(map(str, args)).encode()).hexdigest()

def function_format_number(value):
    s = f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    # Remove ",00" no final
    if s.endswith(",00"):
        s = s[:-3]
    return s