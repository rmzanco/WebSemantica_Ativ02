import requests
from lxml import html

response = requests.get('https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo2019/cursos.html')
tree = html.fromstring(response.content)

cursos = tree.xpath('/html/body/div/div/div[1]/div[3]/div/a/text()')
for curso in cursos:
    print(curso)