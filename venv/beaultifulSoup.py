import requests
import urllib.parse
from bs4 import BeautifulSoup
from bs4 import SoupStrainer


def getNomeCurso(codigo=None):
    urlcursos = 'https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo2019/cursos.html'
    response = requests.get(urlcursos)
    conteudo = response.content.decode(response.apparent_encoding).splitlines()
    linestart = '<span>' + codigo + ' </span>'
    nomecurso = None
    for linha in conteudo:
        if linha.startswith(linestart):
            start = linha.find('html\'>') + 6
            end = linha.find('</a>')
            nomecurso = linha[start:end]
            break
    return nomecurso


codigo = input('Código do curso: ')
try:
    nome = getNomeCurso(codigo)
    if nome is not None:
        urlbase = 'https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo2019/proposta/'
        urlproposta = urlbase + 'sug' + codigo + '.html'
        response = requests.get(urlproposta)
        strainer = SoupStrainer(name='div', attrs={'class': 'div100'})
        soup = BeautifulSoup(response.content.decode(response.apparent_encoding), 'html.parser', parse_only=strainer)
        links = soup.find_all('a')
        filename = 'Disciplinas' + codigo + '.csv'
        f = open(filename, 'w', encoding='utf-8')
        f.write('Código,Nome,Créditos\n')
        for link in links:
            disccode = link.string[0:link.string.find('(')]
            disccred = link.string[link.string.find('(') + 1:link.string.find(')')]
            url = urllib.parse.urljoin(urlbase, link['href'])
            disc = requests.get(url)
            discnames = BeautifulSoup(disc.content.decode(disc.apparent_encoding), 'html.parser')
            discsoup = discnames.find(attrs={'name': disccode})
            codname = discsoup.string
            discname = codname[codname.find('-') + 2:-1]
            f.write(disccode + ',' + discname + ',' + disccred +'\n')
            print('.', end='')
        print(f'\nDisciplinas obrigatórias do curso \'{nome}\' salvas em \'{filename}\'')
        f.close()
    else:
        print(f'Nenhum curso com código {codigo} foi encontrado')
except Exception as e:
    print(f'Exceção ocorrida: {e}')