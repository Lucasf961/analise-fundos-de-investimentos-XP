import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep

# abrindo o link no google chrome com selenium
s = Service('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
navegador = webdriver.Chrome(service=s)
navegador.get('https://www.xpi.com.br/investimentos/fundos-de-investimento/lista/')
sleep(15)

# número de fundos disponíveis
n = navegador.find_element(By.XPATH, '//article/section[1]/div/div[1]').get_attribute('innerText')
n = int(n.split()[0])

# Clique em "Ver mais" para expandir todos os fundos
click = navegador.find_element(By.XPATH, "//div/div[2]/div/div/div[3]/div/div")
click.click()
sleep(10)

# Extraindo informações sobre os fundos
nome_fundo = []
tipo_fundo = []
aplicacao_min = []
taxa_adm = []
cotizacao_resgate = []
liquidacao_resgate = []
taxa_risco = []
rentabilidade_12_meses = []
rentabilidade_24_meses = []
rentabilidade_36_meses = []
for item in range(-1,n*2,2):
    nome_fundo0 = navegador.find_element(By.XPATH, f'//article/section[2]/div[{item+2}]/div[1]/div').get_attribute('innerText')
    nome_fundo.append(nome_fundo0)
    
    tipo_fundo0 = navegador.find_element(By.XPATH, f'//section/div[{item+2}]/div/p').get_attribute('innerText')
    tipo_fundo.append(tipo_fundo0)
    
    aplicacao_min0 = navegador.find_element(By.XPATH,f'//article/section[2]/div[{item+2}]/div[2]').get_attribute('innerText')
    aplicacao_min.append(aplicacao_min0)

    taxa_adm0 = navegador.find_element(By.XPATH,f'//article/section[2]/div[{item+2}]/div[3]').get_attribute('innerText')
    taxa_adm.append(taxa_adm0)
    
    cotizacao_resgate0 = navegador.find_element(By.XPATH,f'//article/section[2]/div[{item+2}]/div[4]/div').get_attribute('innerText')
    cotizacao_resgate.append(cotizacao_resgate0)
    
    liquidacao_resgate0 = navegador.find_element(By.XPATH,f'//article/section[2]/div[{item+2}]/div[5]/div').get_attribute('innerText')
    liquidacao_resgate.append(liquidacao_resgate0)
    
    taxa_risco0 = navegador.find_element(By.XPATH,f'//article/section[2]/div[{item+2}]/div[6]/span').get_attribute('innerText')
    taxa_risco.append(taxa_risco0)
    
    rentabilidade_12_meses0 = navegador.find_element(By.XPATH,f'//article/section[2]/div[{item+2}]/div[7]/div[2]/div[3]').get_attribute('innerText')
    rentabilidade_12_meses.append(rentabilidade_12_meses0)
    
    rentabilidade_24_meses0 = navegador.find_element(By.XPATH,f'//article/section[2]/div[{item+2}]/div[7]/div[2]/div[4]').get_attribute('innerText')
    rentabilidade_24_meses.append(rentabilidade_24_meses0)
    
    rentabilidade_36_meses0 = navegador.find_element(By.XPATH,f'//article/section[2]/div[{item+2}]/div[7]/div[2]/div[5]').get_attribute('innerText')
    rentabilidade_36_meses.append(rentabilidade_36_meses0)


# extraindo informações adicionais sobre os fundos
data_de_inicio = []
benchmark = []
taxa_performance = []
link = []
for item in range(0, n*2, 2):
    try:
        navegador.find_element(By.XPATH,f'//article/section[2]/div[{item+1}]').click()
        sleep(5)

        datelist0 = navegador.find_element(By.XPATH, f'//article/section[2]/div[{item+2}]/section/section/section[1]/div[4]/div[2]').get_attribute('innerText')
        data_de_inicio.append(datelist0)

        benchmark0 = navegador.find_element(By.XPATH, f'//article/section[2]/div[{item+2}]/section/section/section[1]/div[6]/div[2]').get_attribute('innerText')
        benchmark.append(benchmark0)

        taxa_performance0= navegador.find_element(By.XPATH, f'//article/section[2]/div[{item+2}]/section/section/section[1]/div[10]/div[2]').get_attribute('innerText')
        taxa_performance.append(taxa_performance0)

        link0 = navegador.find_element(By.XPATH, f'//article/section[2]/div[{item+2}]/section/section/section[1]/div[13]/div/a').get_attribute('href')
        link.append(link0)
    except:
        data_de_inicio.append(None)
        benchmark.append(None)
        taxa_performance.append(None)
        link.append(None)


# DataFrame
df = pd.DataFrame({'nome_fundo':nome_fundo, 'tipo_fundo':tipo_fundo, 'aplicacao_min':aplicacao_min, 'taxa_adm':taxa_adm, 'cot_resgate':cotizacao_resgate, 'liq_resgate':liquidacao_resgate,'taxa_risco':taxa_risco,'rent_12_meses':rentabilidade_12_meses, 'rent_24_meses':rentabilidade_24_meses, 'rent_36_meses':rentabilidade_36_meses, 'data_inicio':data_de_inicio, 'benchmark':benchmark, 'taxa_performance':taxa_performance, 'link':link})

#df.to_excel('Downloads\FundosXP.xlsx',index=False)
#df = pd.read_excel('Downloads\FundosXP.xlsx')

# Tratamento dos dados
for col in range(0,len(df.columns)):
    for row in range(0,len(df)):
        if df.iloc[row,col] == '-':
            df.iloc[row,col] = np.nan 
        elif df.iloc[row,col] == 'N/D':
            df.iloc[row,col] = np.nan

df['cot_resgate'] = [str(x).replace('\n\n',' ') for x in df['cot_resgate']]
df['liq_resgate'] = [str(x).replace('\n\n',' ') for x in df['liq_resgate']]

# Convertendo tipos dos dados
df['taxa_adm'] = df['taxa_adm'].astype(float)
df['taxa_risco'] = df['taxa_risco'].astype(int)
df['rent_12_meses'] = df['rent_12_meses'].astype(float)
df['rent_24_meses'] = df['rent_24_meses'].astype(float)
df['rent_36_meses'] = df['rent_36_meses'].astype(float)
df['taxa_performance'] = df['taxa_performance'].astype(float)
df['data_inicio'] = pd.to_datetime(df['data_inicio'])

df.head()

#df.to_excel('FundosXPv2.xlsx', index=False)

