#  Desafio Webscraping
O objetivo do projeto de Data Engineering é coletar e organizar dados. Isso mesmo, você precisa ser capaz de acessar fontes distintas de dados, coletar essas informações e armazenar em um local de fácil acesso e que seja escalável.

##  Os Dados do desafio
Os dados para serem coletados e armazenados, estão disponíveis neste site. http://books.toscrape.com/. O trabalho será  será coletar e armazenar os seguintes dados:
1.  O nome do livro.
2.  A categoria do livro.
3.  O número de estrelas que o livro recebeu.
4.  O preço do livro.
5.  Se o livro está em Estoque ou não.

## Roteiro para Resolução
1. web scraper, necessariamente, utilizando a linguagem Python.
2. Utiliza a biblioteca Selenium do Python para navegar entre os links das categorias e as páginas.
3. Utiliza a biblioteca BeautifulSoup do Python para coletar os dados das páginas HTML.
4. Instale no seu computador e configure um banco de dados Postgres.
5. Crie uma tabela para armazenar os dados.
6. Crie sua solução modularizada. O Script em Python deve salvar um arquivo csv em alguma pasta da sua máquina e então outro script em bash, deve fazer a inserção dos dados no banco de dados.

## sugestão
Faça o gerenciamento desses jobs utilizando o Airflow ( Framework de gerenciamento de Jobs ). Um script só pode rodar, quando o outro terminar.
