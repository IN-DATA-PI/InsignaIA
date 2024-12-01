import mysql.connector
import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyDg5PGIiXl6Yp16Bsg-MsheM11T0QqY3e0"
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

contexto = """O Centro de São Paulo enfrenta uma crise significativa de criminalidade, com um roubo a cada 30 minutos, conforme dados da Secretaria Estadual da Segurança Pública (SSP). Entre janeiro e julho de 2023, foram registradas 13.478 ocorrências de roubo nas oito delegacias da região central, o maior número desde 2001. A presença da Cracolândia e a falta de policiamento adequado têm agravado a situação, impactando diretamente a população e o comércio local, como relatado por Daniel Bernardini, que fechou sua loja após quatro invasões. 

O nosso projeto consiste em um sistema que irá ajudar a polícia a tomar decisões mais rápidas em relação ao combate a roubos na cidade de São Paulo. Podendo assim, fazer policiamentos mais estratégicos e eficazes para combater estes crimes em São Paulo.
Utilizando a base de dados da Secretaria Estadual da Segurança Pública (SSP) pegamos os seguintes dados:
Roubos em geral
Roubos de carga
Roubos de veículos 
O ano que estes crimes acima foram registrados.
O mês que estes crimes acima foram registrados.
E por fim, a área/zona de São Paulo que ele ocorreu, podendo ser Leste, Sul, Norte, Oeste ou Centro.

Sendo estes alguns dados desta base citada:

A zona Sul é a mais perigosa 
Os roubos em geral estão em constante crescimento na zona Sul
O ano com mais crimes é 2023
Roubo de carga é muito comum no Centro 
Roubo de veículos são muito comuns na zona leste
O mês de janeiro de 2023 é o mês que acontecem mais Roubos em geral
O mês de janeiro de 2023 é o mês que acontecem mais Roubos de carga
O mês de fevereiro de 2023 é o mês que acontecem mais Roubos de veículos
O mês de janeiro se torna o mais perigoso por ter os roubos em geral e de carga.

Diante desse cenário, propomos o desenvolvimento de um sistema de análise de dados sobre os roubos na cidade de São Paulo, que será uma ferramenta estratégica para apoiar as autoridades na tomada de decisões e aumentar a eficácia das operações policiais. Esse sistema incluirá: 

Dashboard informativa: Apresentando estatísticas atualizadas dos roubos, com gráficos de tendências e comparações entre diferentes períodos. 

Cadastro de operações: Investigadores poderão registrar operações planejadas, as quais serão avaliadas por delegados cadastrados, permitindo um controle mais rigoroso e transparente sobre a continuidade e necessidade de cada ação.

Com isso responda a seguinte pergunta:
"""

def inserirRecomendacao(recomendacao):
    try:
        cursor = conexao.cursor()
        comando = "INSERT INTO ia (recomendacoes) VALUES (%s)"
        cursor.execute(comando, (recomendacao,))
        conexao.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

# Configuração do banco
conexao = mysql.connector.connect(
    host='23.23.154.244',
    user='root',
    password='urubu100',
    database='Insigna',
)

perguntas = [
    f"{contexto} Analisando a área/zona com mais roubos ou seja a mais perigosa, qual o crime que está em constante crescimento nela?",
    f"{contexto} Analisando o ano e o mês com mais roubos e crimes, qual seria o mês mais perigoso para assim poder aumentar as operações para que ele possa diminuir? ",
    f"{contexto} Visando os roubos de veículos e de carga, em qual área/zona de São Paulo eles são muito comum?"
]

for pergunta in perguntas:
    response = model.generate_content(pergunta)
    inserirRecomendacao(response.text)

conexao.close()
