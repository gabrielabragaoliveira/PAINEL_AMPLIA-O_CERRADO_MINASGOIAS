import pandas as pd
import numpy as np

def estruturar_planilha_engenharia(caminho_arquivo):
    """
    Função para ler e planificar dados orçamentários/quantitativos
    do arquivo BI - AMPLIAÇÃO, transformando a estrutura visual em uma tabela plana (flat table).
    """
    try:
        # Carrega a aba principal. Se precisar pular linhas de cabeçalho do relatório, adicione skiprows=2
        df = pd.read_excel(caminho_arquivo)
        
        # ⚠️ IMPORTANTE: Ajuste estes nomes para o cabeçalho exato que está no seu arquivo Excel!
        col_desc = 'Descrição'   # Coluna onde fica o texto do item/grupo
        col_un = 'Un'            # Coluna de Unidade de Medida
        col_quant = 'Quantidade' # Coluna do Quantitativo
        
        # 1. Identificar linhas de "Macro-serviço"
        # Naquelas planilhas paginadas, as linhas de grupo têm a descrição, 
        # mas as colunas de Unidade e Quantidade ficam vazias (NaN).
        df['Macro_Servico'] = np.where(df[col_un].isna(), df[col_desc], np.nan)
        
        # 2. Propagar os grupos para baixo (Forward Fill)
        # O pandas vai copiar o nome do grupo para todos os subitens abaixo dele
        df['Macro_Servico'] = df['Macro_Servico'].ffill()
        
        # (Opcional) Limpar linhas de quebra de página se o arquivo foi exportado de PDF/Software
        # Exemplo: removendo linhas onde a descrição contenha "Página"
        df = df[~df[col_desc].astype(str).str.contains("Página", na=False)]
        
        # 3. Remover as linhas que eram apenas os títulos dos grupos
        # Ficamos estritamente com os itens de execução (que possuem a unidade preenchida)
        df_plano = df.dropna(subset=[col_un]).copy()
        
        # 4. Reorganizar as colunas para o dashboard
        cols_atuais = df_plano.columns.tolist()
        cols_atuais.remove('Macro_Servico')
        df_plano = ['Macro_Servico'] + cols_atuais
        
        return df_plano
        
    except Exception as e:
        print(f"Erro ao processar a planilha: {e}")
        return pd.DataFrame()

# Testando localmente
# df_limpo = estruturar_planilha_engenharia("BI - AMPLIAÇÃO.xlsx")
# print(df_limpo.head())
