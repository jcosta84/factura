import pandas as pd
import streamlit as  st
import io
from io import StringIO


st.set_page_config(page_title="Converção de dados Script Facturação",
                   layout="wide",
                   page_icon=":bar_chart:")

#criar cabeçalho
colunas = ['BOA IND', 'EMP ID', 'UNIDADE', 'PRODUTO', 'DT PROC', 'DT FACT', 'NR FACT', 'CLI ID', 'CLI CONTA', 'CIL',
           'TP FACT', 'TP CLI', 'COD TARIFA', 'VAL TOT', 'CONCEITO', 'QTDE', 'VALOR']

#tabela Unidade
dados = [['10201000', 'Praia'],
         ['10202000', 'São Domingos'],
         ['10203000', 'Santa Catarina'],
         ['10204000', 'Tarrafal'],
         ['10205000', 'Calheta'],
         ['10206000', 'Santa Cruz'],
         ['10701000', 'Mosteiros'],
         ['10702000', 'São Filipe'],
         ['10801000', 'Maio'],
         ['10901000', 'Brava'],
         ['10101000', 'Mindelo'],
         ['10301000', 'SAL'],
         ['10401000', 'BOAVISTA'],
         ['10501000', 'VILA DA RIBEIRA BRAVA'],
         ['10601000', 'R.GRANDE - N.S.Rosário'],
         ['10602000', 'PORTO NOVO - S.João Baptista'],
         ['10603000', 'PAUL - S.António das Pombas'],
         ['10502000', 'Tarrafal S.Nicolau'],
         ['10000000', 'Electra SUL']
         ]
unidade = pd.DataFrame(dados, columns=['UNIDADE', 'Unidade'])
unidade['UNIDADE'] = unidade['UNIDADE'].astype(int)
unidade.set_index('UNIDADE', inplace=True)

#tabela de regão
dados2 = [['Praia', 'SUL'],
        ['São Domingos', 'SUL'],
        ['Santa Catarina', 'SUL'],
        ['Tarrafal', 'SUL'],
        ['Calheta', 'SUL'],
        ['Santa Cruz', 'SUL'],
        ['Mosteiros', 'SUL'],
        ['São Filipe', 'SUL'],
        ['Maio', 'SUL'],
        ['Brava', 'SUL'],
        ['Mindelo', 'NORTE'],
        ['SAL', 'NORTE'],
        ['BOAVISTA', 'NORTE'],
        ['VILA DA RIBEIRA BRAVA', 'NORTE'],
        ['R.GRANDE - N.S.Rosário', 'NORTE'],
        ['PORTO NOVO - S.João Baptista', 'NORTE'],
        ['PAUL - S.António das Pombas', 'NORTE'],
        ['Tarrafal S.Nicolau', 'NORTE']
         ]
regiao = pd.DataFrame(dados2, columns=['Unidade', 'Região'])

#tabela de produto
dados2 = [['EB', 'Baixa Tensão'],
          ['EE', 'Baixa Tensão Especial'],
          ['EM', 'Media Tensão'],
          ['AG', 'Agua']
          ]
produto = pd.DataFrame(dados2, columns=['PRODUTO', 'Produto'])
produto.set_index('PRODUTO', inplace=True)

#tabela tipo Cliente
dados4 = [['72', 'Empresa Publica'],
          ['82', 'Colectivos'],
          ['93', 'Industriais'],
          ['94', 'Construção'],
          ['73', 'Estado-Patrimonio'],
          ['91', 'Domésticos'],
          ['92', 'Comércio, Industria, Agricul.'],
          ['21', 'Consumos Próprios'],
          ['31', 'Autarquias'],
          ['51', 'Instituições'],
          ['71', 'Estado-Tesouro'],
          ['XX', 'Clientes Senhas de Água'],
          ]
tip_client = pd.DataFrame(dados4, columns=['TP CLI', 'Tipo_Cliente'])
tip_client['TP CLI'] = tip_client['TP CLI'].astype(str)
tip_client.set_index('TP CLI', inplace=True)

#tabela Tipo Factura
dados3 = [['11', 'Em Ciclo Leitura'],
          ['12', 'Em Ciclo Estimativa'],
          ['22', 'Baixa Voluntária'],
          ['23', 'Baixa por Dívida'],
          ['24', 'Alterações Contratuais'],
          ['28', 'Baixa Forçada'],
          ['29', 'Substit. Modif.'],
          ['30', 'Substituição'],
          ['33', 'Acerto de Cobrança'],
          ['39', 'Facturação Diversa'],
          ['99', 'Lig Relig CompPg']
          ]
tp_fact = pd.DataFrame(dados3, columns=['TP FACT', 'Tipo_Factura'])
tp_fact['TP FACT'] = tp_fact['TP FACT'].astype(int)
tp_fact.set_index('TP FACT', inplace=True)

#tabela Tarifa
dados5 = [['A1', 'Tarifa Água I'],
            ['A2', 'Tarifa Água II'],
            ['A3', 'Tarifa Água III B'],
            ['A4', 'Tarifa Água III A'],
            ['A5', 'Tarifa Água II (Turismo)'],
            ['AD', 'ADA'],
            ['AP', 'Água Praia'],
            ['B4', 'Autotanques II'],
            ['CD', 'Central Dessalinizadora'],
            ['CP', 'Consumos Proprios'],
            ['R4', 'Autotanques I (Social)'],
            ['SA', 'Senhas de Água'],
            ['XX', 'Venda de Água Avulso'],
            ['AV', 'Avença'],
            ['CE', 'Caixa de Escada'],
            ['CP', 'Consumos Proprios'],
            ['D1', 'Tarifa D'],
            ['D11', 'Tarifa D'],
            ['D2', 'Tarifa D-S. Nicolau'],
            ['D3', 'Tarifa D-Social-S. Nicolau'],
            ['D4', 'Tarifa D - Maio'],
            ['D5', 'Tarifa D - Social - Maio'],
            ['DS', 'Tarifa D - Social'],
            ['IP', 'Iluminação Publica'],
            ['LM', 'Ligação Provisória - MONO'],
            ['LP', 'Ligação Provisória'],
            ['LT', 'Ligação Provisória - TRI'],
            ['LU', 'Ligação Provisória - MONO URG'],
            ['S1', 'Tarifa Social'],
            ['SF', 'Semáfores'],
            ['T1', 'Trabalhador Electra-S. Nicolau'],
            ['T2', 'Trab. Electra Is.RTC-S.Nicolau'],
            ['T3', 'Trabalhador Electra - Maio'],
            ['T4', 'Trab. Electra Is. RTC - Maio'],
            ['TB', 'Trabalhador Electra'],
            ['TI', 'Trab. Electra Isento RTC'],
            ['TU', 'Ligação Provisória - TRI URG'],
            ['AV', 'Tarifa Avença'],
            ['E1', 'Tarifa BTE 1'],
            ['E2', 'Tarifa BTE'],
            ['S1', 'Tarifa Social'],
            ['M1', 'Tarifa MT 1'],
            ['M2', 'Tarifa MT'],
            ['M3', 'Tarifa MT'],
            ['S1', 'Tarifa Social'],
            ['TBP', 'Trabalhador Partilhado'],
            ['TBB', 'Trab. Beneficiário']
          ]
tarifa = pd.DataFrame(dados5, columns=['COD TARIFA', 'Tarifa'])
tarifa['COD TARIFA'] = tarifa['COD TARIFA'].astype(str)
tarifa.set_index('COD TARIFA', inplace=True)

uploaded_file = st.file_uploader("Escolha um arquivo", type=["txt"])

if uploaded_file is not None:
    # Lê o conteúdo como string e converte para DataFrame
    content = uploaded_file.read().decode("utf-8")
    factura = pd.read_csv(io.StringIO(content), sep='\t', names=colunas)
    factura = factura.loc[factura['CONCEITO'] == 'X30']
    fact = pd.merge(factura, unidade, on='UNIDADE', how='left')
    fact1 = pd.merge(fact, regiao, on='Unidade', how='left')
    fact2 = pd.merge(fact1, produto, on='PRODUTO', how='left')
    fact2['TP CLI'] = fact2['TP CLI'].astype(str)
    fact3 = pd.merge(fact2, tip_client, on='TP CLI', how='left')
    fact4 = pd.merge(fact3, tp_fact, on='TP FACT', how='left')
    fact5 = pd.merge(fact4, tarifa, on='COD TARIFA', how='left')

    fact5 = fact5[['EMP ID', 'Unidade', 'Região', 'Produto', 'DT PROC', 'DT FACT', 'NR FACT', 'CLI ID', 'CLI CONTA',
               'CIL', 'Tipo_Factura', 'Tipo_Cliente', 'Tarifa', 'VAL TOT', 'CONCEITO', 'QTDE', 'VALOR']]
    fact5['DT PROC'] = pd.to_datetime(fact5['DT PROC'], format='%Y%m%d')
    fact5['DT PROC'] = fact5['DT PROC'].dt.strftime('%d-%m-%Y')
    fact5['DT FACT'] = pd.to_datetime(fact5['DT FACT'], format='%Y%m%d')
    fact5['DT FACT'] = fact5['DT FACT'].dt.strftime('%d-%m-%Y')
    fact5['NR FACT'] = fact5['NR FACT'].astype(str)
    #fact3['VAL TOT'] = fact3['VAL TOT'].astype(str)
    # Aplica a conversão para cada valor da coluna
    #fact3['VAL TOT'] = fact3['VAL TOT'].str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)
    #fact3['VAL TOT'] = fact3['VAL TOT'].apply(lambda x: f"{x:,.0f}".replace(",", "X").replace(".", ",").replace("X", "."))
    #fact3['VAL TOT'] = fact3['VAL TOT'].astype(str)
    #fact3['VAL TOT'] = fact3['VAL TOT'].astype(str).str.replace(',', '.', regex=False)
    #fact3['VAL TOT'] = fact3['VAL TOT'].astype(str).str.replace('.', ',', regex=False)
    st.markdown("---")
    # Ajuste de altura com CSS personalizado
    
    # definir campos de pesquisa
    st.sidebar.header("Filtrar Região:")
    reg = st.sidebar.multiselect(
        "Filtrar Região",
        options=fact5['Região'].unique(),
    )
    geral_selection2 = fact5.query(
        "`Região` == @reg"
    )
    geral_selection2.set_index('EMP ID', inplace=True)
    st.dataframe(geral_selection2, use_container_width=True)
    #fact3.to_excel("C:\Temp\precos_formatados.xlsx", index=False)
    
    # converção do ficheiro para o formato csv e baixar o mesmo
    @st.cache_data
    def convert_df2(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv(sep=';', decimal=',').encode('utf-8-sig')
    
    csv = convert_df2(geral_selection2)

    st.download_button(
        label="Download Facturação",
        data=csv,
        file_name='Facturação.csv',
        mime='text/csv',

    )
