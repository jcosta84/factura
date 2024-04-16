import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


st.set_page_config(page_title="Projecto Facturação",
                   page_icon=":bar_chart:",
                   layout="wide")





#memoria cache
@st.cache_data
def carregar_unidade():
    unidade = pd.read_excel(upload_file, engine="openpyxl")
    return unidade

@st.cache_data
def carregar_tipocliente():
    tip = pd.read_excel(upload_file, engine="openpyxl")
    return tip

@st.cache_data
def carregar_produto():
    produto = pd.read_excel(upload_file, engine="openpyxl")
    return produto

@st.cache_data
def carregar_estfact():
    estfact = pd.read_excel(upload_file, engine="openpyxl")
    return estfact

@st.cache_data
def carregar_factura():
    factura = pd.read_excel(upload_file, engine="openpyxl")
    return factura

@st.cache_data
def carregar_contactos():
    contacto = pd.read_excel(upload_file, engine="openpyxl")
    return contacto

@st.cache_data
def carregar_contratos():
    contrato = pd.read_excel(upload_file, engine="openpyxl")
    return contrato

st.subheader("IMPORTAR DADOS:")




# Importar facturas contabilistico
upload_file = st.file_uploader("Importar Facturação", type="xlsx")
if upload_file:
    st.markdown("---")
    factura = carregar_factura()
    factura.head()

upload_file = st.file_uploader("Importar Contratos", type="xlsx")
if upload_file:
    st.markdown("---")
    contrato = carregar_contratos()
    factrato = pd.merge(factura, contrato, on='CIL', how='left')
    factrato.head()

upload_file = st.file_uploader("Importar Contactos", type="xlsx")
if upload_file:
    st.markdown("---")
    contacto = carregar_contactos()
    factacto = pd.merge(factrato, contacto, on='CIL', how='left')
    factacto.head()

upload_file = st.file_uploader("Importar Unidade", type="xlsx")
if upload_file:
    st.markdown("---")
    unidade = carregar_unidade()
    factun = pd.merge(factacto, unidade, on='UC', how='left')
    factun.head()

upload_file = st.file_uploader("Importar Tipo Cliente", type="xlsx")
if upload_file:
    st.markdown("---")
    tip = carregar_tipocliente()
    factip = pd.merge(factun, tip, on='Tp Client', how='left')
    factip.head()

upload_file = st.file_uploader("Importar Produto", type="xlsx")
if upload_file:
    st.markdown("---")
    produto = carregar_produto()
    factpro = pd.merge(factip, produto, on='Prod', how='left')
    factpro.head()

upload_file = st.file_uploader("Importar Estado Factura", type="xlsx")
if upload_file:
    st.markdown("---")
    estfact = carregar_estfact()
    factto = pd.merge(factpro, estfact, on='Est Fact', how='left')
    factto.head()


    # apresentar dados com informação filtrada no x30 onde existe consumo e valor facturado
    tabela_geral = factto.loc[factto['Conse'] == 'X30']
    # organizar
    tabela_geral2 = tabela_geral.loc[:,
                        ['Unidade', 'CIL', 'Cliente', 'NOME', 'LOCALIDADE', 'MORADA', 'Tip Cliente', 'Produtos',
                         'Dat Emi',
                         'Dat Fact',
                         'Nº Doc', 'Descrição', 'Quant (Kwh)', 'Val Total (ECV)', 'Email', 'Email 2', 'Fixo 1',
                         'Fixo 2',
                         'Movel 1', 'Movel 2', 'Movel 3', 'Movel 4']]
    tabela_geral2.head()

    st.sidebar.header("Filtar Por Unidade, Tipo Cliente, Produto:")
    un = st.sidebar.multiselect(
        "Filtar Unidade",
        options=tabela_geral2['Unidade'].unique(),
    )

    cliente = st.sidebar.multiselect(
        "Filtar Tipo Cliente",
        options=tabela_geral2["Tip Cliente"].unique(),

    )

    prod = st.sidebar.multiselect(
        "Filtar Produto",
        options=tabela_geral2["Produtos"].unique(),

    )
    geral_selection = tabela_geral.query(
        "`Unidade` == @un & `Tip Cliente` == @cliente & `Produtos` == @prod"
    )

    st.subheader("DASHBOARD")

    # informação resumida parte superior
    quantidade_de_clientes = int(geral_selection["CIL"].count())
    quantidade_facturado = int(geral_selection["Quant (Kwh)"].sum())
    valor_facturado = int(geral_selection["Val Total (ECV)"].sum())

    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        st.subheader("Quantidade de Clientes")
        st.subheader(f"Locais {quantidade_de_clientes:,}")
    with middle_column:
        st.subheader("Quantidade Facturado")
        st.subheader(f" Kwh {quantidade_facturado:,}")
    with right_column:
        st.subheader("Valor Facturado")
        st.subheader(f" ECV {valor_facturado:,}")

    st.markdown("---")

    #tabela dinamica
    unidfact = pd.pivot_table(geral_selection, index='Unidade', values='Val Total (ECV)', aggfunc=np.sum)
    uniquan = pd.pivot_table(geral_selection, index='Unidade', values='Quant (Kwh)', aggfunc=np.sum)
    factquant = pd.merge(unidfact, uniquan, on='Unidade', how='left')

    # grafico valor facturado
    fig_val = px.bar(
        factquant,
        x=factquant.index,
        y=['Val Total (ECV)'],
        orientation="v",
        title="<b>Grafico Valor Facturado (ECV)</b>",
        color_discrete_sequence=["#5F9EA0"],
        template="plotly_white",
    )
    fig_val.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )

    # grafico quantidade consumido
    fig_quant = px.bar(
        factquant,
        x=['Quant (Kwh)'],
        y=factquant.index,
        orientation="h",
        title="<b>Grafico Valor Consumido</b>",
        color_discrete_sequence=["#B22222"],
        template="plotly_white",
    )
    fig_quant.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )

    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_val, use_container_width=True)
    right_column.plotly_chart(fig_quant, use_container_width=True)

    #download facturação geral
    @st.cache_data
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')


    csv = convert_df(geral_selection)

    st.download_button(
        label="Download Facturação Geral",
        data=csv,
        file_name='facturação.csv',
        mime='text/csv',
    )

    st.markdown("---")

    st.sidebar.header("Filtar Cliente, CIL:")
    client = st.sidebar.multiselect(
        "Filtar Cliente",
        options=tabela_geral2["Cliente"].unique(),
    )

    geral_selection2 = tabela_geral2.query(
        "`Cliente` == @client"
    )
    st.subheader("Tabela Cliente")
    st.dataframe(geral_selection2)


    # download facturação cliente
    @st.cache_data
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')


    csv = convert_df(geral_selection2)

    st.download_button(
        label="Download Facturação Cliente",
        data=csv,
        file_name='facturação cliente.csv',
        mime='text/csv',
    )

    cil = st.sidebar.multiselect(
        "Filtrar CIL",
        options=tabela_geral2["CIL"].unique(),
    )
    st.subheader("Tabela CIL")
    geral_selection3 = tabela_geral2.query(
        "`CIL` == @cil"
    )
    st.dataframe(geral_selection3)


    @st.cache_data
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')


    csv = convert_df(geral_selection3)

    st.download_button(
        label="Download Facturação CIL",
        data=csv,
        file_name='facturação cil.csv',
        mime='text/csv',
    )


hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </styke>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)

