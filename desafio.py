import requests
from bs4 import BeautifulSoup
import datetime


# URL da página de pesquisa de vagas no LinkedIn
url = 'https://www.linkedin.com/jobs/search/?currentJobId=3539292514&f_I=80&f_JT=F%2CI&geoId=106057199&location=Brasil&refresh=true&sortBy=R'

# Faz a requisição HTTP para obter o conteúdo da página
response = requests.get(url)
print(response.status_code)

def vaga_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    exp = soup.find_all('span', class_='description__job-criteria-text')[0].text.strip()
    print(exp)
    tipo_de_contratacao = soup.find_all('span', class_='description__job-criteria-text')[1].text.strip()
    print(tipo_de_contratacao)
    '''
    n_de_candidatos = soup.find_all('span', class_='num-applicants__caption topcard__flavor--metadata topcard__flavor--bullet')[0].text.strip()
    print(n_de_candidatos)
    '''
    return response.status_code

def empresa_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    local =soup.find_all('dd')[2].text.strip()
    print(local)
    return url

soup = BeautifulSoup(response.text, 'html.parser')

# Encontra todos os resultados da pesquisa de vagas na página
#results = soup.find_all('li', class_='jobs-search-results__list-item')
results = soup.find_all('div', class_='base-card')
#print(results[0])


for result in results:
    vaga = result.find('span', class_='sr-only').text.strip()
    vaga_url = result.find('a', class_='base-card__full-link').get("href")
    empresa = result.find('a', class_='hidden-nested-link').text.strip()
    empresa_url= result.find('a', class_='hidden-nested-link').get("href")
    data_de_postagem = soup.find('time').get("datetime")
    data_scraping = datetime.datetime.now()
    
    print(empresa.encode("utf-8"))
    print(empresa_url)
    print(vaga.encode("utf-8"))
    print(vaga_url)
    vaga_data(vaga_url)
    print(data_de_postagem)
    print(data_scraping)
    #empresa_data(empresa_url)
    print("\n")
    