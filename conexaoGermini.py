import mysql.connector
import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyDg5PGIiXl6Yp16Bsg-MsheM11T0QqY3e0"
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

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
    host='localhost',
    user='root',
    password='25117195',
    database='Insigna',
)

perguntas = [
    "Como fazer um tiramissu?",
    "Quais os números primos de 1 até 100?",
    "Em quais anos o Corinthians foi campeão mundial?"
]

for pergunta in perguntas:
    response = model.generate_content(pergunta)
    inserirRecomendacao(response.text)

conexao.close()
