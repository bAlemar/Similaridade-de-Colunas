import pandas as pd
import difflib

class Bot_Semelhanca():
    """
        Objetivo desse bot é padronizar/preencher valores de uma tabela, quando se tem uma tabela de referência...
    
    """
    def __init__(self,df,df_consulta):
        """
        Argumentos:
        
        df = DataFrame a ser padronizada

        df_consulta = DataFrame que servirá como consulta
        
        """


        self.df = df
        self.df_consulta = df_consulta
    
    def limpeza_na(self,lista):
        lista = list(filter(lambda x: pd.notna(x),lista))
        return lista
        


    def semelhanca(self,palavra_chave:str,coluna,cutoff=0.7):
        """
        
        Essa função busca a semelhança da palavra chave, vinda de uma coluna x do df, com as palavras vindas de uma coluna x do df_consulta.
        Exemplo: Busca semelhança da palavra "Carro" do df na Coluna "Itens" com as palavras contidas no df_consulta na coluna "Itens".
        
        
        Argumentos:

        palavra_chave = Palavra que será buscada seus semelhantes

        coluna = Coluna da palavra_chave

        cutoff = Nível de similaridade 

        """
        

        if pd.isna(palavra_chave):
            return None
        
        #Palavras únicas do df_consulta
        lista_palavras_unicas = self.df_consulta[coluna].dropna().unique()
        
        # #Limpeza para valores np.nan
        # lista_palavras_unicas = self.limpeza_na(lista_palavras_unicas)

        if pd.isna(any(lista_palavras_unicas)):
            return None

        #Buscando palavras semelhantes:

        #Verificando semelhança entre as palavras
        palavras_semelhantes = difflib.get_close_matches(palavra_chave,lista_palavras_unicas,cutoff=cutoff)

        #Limpeza de valores np.nan
        palavras_semelhantes = self.limpeza_na(palavras_semelhantes)
        
            
        return palavras_semelhantes

    def semelhanca_condiconada(self,
                               coluna_condicao,
                               palavra_condicao,
                               palavra_chave,
                               coluna,
                               cutoff
                               ):
        """
        Essa função funciona praticamente como função semelhanca, entretanto teremos uma condição na lista de valores unicos.
        
        Essa condição é referente ao filtro da semelhança da outra coluna...

        Argumentos
        
        coluna_condicao: Coluna que filtrará os resultados

        palavra_condicao: Palavra que filtrará os resultados

        palavra_chave: Palavra a buscar a similaridade

        coluna: Coluna da palavra_chave

        cutoff: Nivel de similaridade

        """
        lista_palavras_unicas = self.df_consulta[self.df_consulta[coluna_condicao]==palavra_condicao][coluna].dropna().unique()

        if pd.isna(any(lista_palavras_unicas)):
            return None

        #Buscando palavras semelhantes:

        #Verificando semelhança entre as palavras
        palavras_semelhantes = difflib.get_close_matches(palavra_chave,lista_palavras_unicas,cutoff=cutoff)

        #Limpeza de valores np.nan
        palavras_semelhantes = self.limpeza_na(palavras_semelhantes)
        
            
        return palavras_semelhantes


    def looping_semelhanca(self,
                           coluna1:str,
                           coluna2:str,
                           cutoff1:float,
                           cutoff2:float,
                           coluna_objetivo:str
                           ):
        """
        Essa função irá ver se além da semelhança na coluna1 há semelhança com a coluna2 , deixando resultado ainda mais preciso
        Nota-se que podemos acrescentar quantas colunas quisermos...
        
        A recomendação é de utilizar o Nivel de hierarquia do mais específico para o mais generalista...
        
        
        
        Argumentos:

        palavra_chave1: Palavra Chave referente Coluna1

        coluna1: Coluna1

        cutoff1: Nível de Similaridade para palavra_chave1
        
        palavra_chave2: Palavra Chave referente Coluna2

        coluna2: Coluna2

        cutoff2: Nivel de Similaridade para palavra_chave2
        
        coluna_objetivo: Coluna que você quer a resposta
                
        """
        df = self.df
        for i in range(len(self.df)):  
            lista_semelhanca = []
            lista_palavra_objetivo = []

            palavra_chave1 = self.df.loc[i,coluna1]

            resultado_1 = self.semelhanca(palavra_chave=palavra_chave1,
                                          coluna=coluna1,
                                          cutoff=cutoff1)
            
            if resultado_1:
                # Verificando se há semelhança TAMBÉM com coluna2
                # Para isso será feito um looping
                for palavra_chave1_semelhante in resultado_1:   
                    # A partir das palavras_semelhantes da coluna 1 com df_consulta, iremos consultar quais são valores únicos dela para coluna2
                
                    palavra_chave2 = self.df.loc[i,coluna2]
                    
                    
                    resultado_2 = self.semelhanca_condiconada(coluna_condicao=coluna1,
                                                              palavra_condicao=palavra_chave1_semelhante,
                                                              palavra_chave=palavra_chave2,
                                                              coluna=coluna2,
                                                              cutoff=cutoff2)
                    
                    if resultado_2: #Tem semelhança com coluna1 e coluna2
                        for palvara_chave2_semelhante in resultado_2: 
                            
                            df_semelhante = self.df_consulta[(self.df_consulta[coluna1]==palavra_chave1_semelhante)&
                                                                (self.df_consulta[coluna2]==palvara_chave2_semelhante)] 
                            
                            palavra_objetivo = list(df_semelhante[coluna_objetivo].unique())

                            semelhanca = f'Semelhante {coluna1} e {coluna2}'

                            lista_palavra_objetivo.append(palavra_objetivo)
                            lista_semelhanca.append(semelhanca)


                    else: #Não tem semelhança com coluna 2 mas tem com coluna1
                        
                        df_semelhante = self.df_consulta[self.df_consulta[coluna1]==palavra_chave1_semelhante] 
                        
                        palavra_objetivo = list(df_semelhante[coluna_objetivo].unique())

                        semelhanca = f'Semelhante {coluna1}'

                        lista_palavra_objetivo.append(palavra_objetivo)
                        lista_semelhanca.append(semelhanca)

            
            else: # Não há semelhança com coluna1
                palavra_chave2 = self.df.loc[i,coluna2]
    
                resultado_2 = self.semelhanca(palavra_chave=palavra_chave2,
                                              coluna=coluna2,
                                              cutoff=cutoff2)
                
                if resultado_2: #Não semelhança com coluna 1 mas tem com coluna2
                    for palvara_chave2_semelhante in resultado_2:
                        
                        df_semelhante = self.df_consulta[self.df_consulta[coluna2]==palvara_chave2_semelhante] 
                        
                        palavra_objetivo = list(df_semelhante[coluna_objetivo].unique())

                        semelhanca = f'Semelhante {coluna2}'

                        lista_palavra_objetivo.append(palavra_objetivo)
                        lista_semelhanca.append(semelhanca)


                else: # Não semelhança nem com coluna1 nem com coluna2
        
                    palavra_objetivo = 'Não Encontrada'

                    semelhanca = f'Nenhuma Semelhança'

                    lista_palavra_objetivo.append(palavra_objetivo)
                    lista_semelhanca.append(semelhanca)


            df.at[i,'Semelhança'] = lista_semelhanca
            df.at[i,f'{coluna_objetivo}_Sugerida'] = lista_palavra_objetivo
            
        return   df



