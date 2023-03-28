import requests
from bs4 import BeautifulSoup
import datetime
import csv


# URL da página de pesquisa de vagas no LinkedIn
url = 'https://www.linkedin.com/jobs/search/?currentJobId=3539292514&f_I=80&f_JT=F%2CI&geoId=106057199&location=Brasil&refresh=true&sortBy=R'

list =[]
# Faz a requisição HTTP para obter o conteúdo da página

try:
    with open('./scraping-Roberto.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile,  delimiter=' ', quotechar='|')
        for s in spamreader:
            list.append(s)
    del list[0]
except:
    print('arquivo sendo criado')

response = requests.get(url)

def vaga_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    exp = soup.find_all('span', class_='description__job-criteria-text')
    tipo_de_contratacao = soup.find_all('span', class_='description__job-criteria-text')
    n_de_candidatos = soup.find_all('span', class_='num-applicants__caption topcard__flavor--metadata topcard__flavor--bullet')
    link_empresa = soup.find('a', class_='topcard__org-name-link').get("href")


    if(len(n_de_candidatos) < 1):
        if(len(soup.find_all('figcaption', class_='num-applicants__caption')) > 1):
            n_de_candidatos = soup.find_all('figcaption', class_='num-applicants__caption')[0].text.strip()
        else:
            n_de_candidatos = 'Não informado'
    else:
        n_de_candidatos = soup.find_all('span', class_='num-applicants__caption topcard__flavor--metadata topcard__flavor--bullet')[0].text.strip()

    if(len(exp) < 1):
        exp = "Não informado"
    else:
        exp = soup.find_all('span', class_='description__job-criteria-text')[0].text.strip()
    
    if(len(tipo_de_contratacao) < 1):
        tipo_de_contratacao = "Não informado"
    else:
        tipo_de_contratacao = soup.find_all('span', class_='description__job-criteria-text')[1].text.strip()

    return [n_de_candidatos, exp, tipo_de_contratacao, link_empresa]

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
    vaga_info = vaga_data(vaga_url)

    response_empresa = requests.get(vaga_info[3])
    soup_empresa = BeautifulSoup(response_empresa.text, 'html.parser')
    local_empresa = soup_empresa.find_all('span')

    print(vaga_info[3])
    print('\n')
    list.append([vaga_url, vaga.encode("utf-8"), empresa.encode("utf-8"), empresa_url,'...', vaga_info[2], vaga_info[1], vaga_info[0], data_de_postagem, data_scraping])
    
print(len(list[0]))
with open('./scraping-Roberto.csv', 'w') as csvfile:
    csv.writer(csvfile).writerow(['URL da vaga', 'Nome da vaga', 'Nome da empresa', 'URL da Empresa', 'Modelo de contratação', 'Tipo de contratação', 'Nível de experiência', 'Número de candidaturas da vaga', 'Data da postagem da vaga', 'Horario do scraping','Numero de funcionarios da empresa', 'Número de seguidores da empresa', 'Local sede', 'URL da candidatura'])
    for l in list:
        csv.writer(csvfile).writerow(l)
