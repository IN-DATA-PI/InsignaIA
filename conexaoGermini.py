import mysql.connector
import requests

# Configuração do banco
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='25117195',
    database='Insigna',
)
cursor = conexao.cursor()


# Função para buscar dados no banco
def verDadosPrompt1():
    comando = 'SELECT SUM(agosto) FROM dados WHERE ano = 2024 AND natureza = "ROUBO - OUTROS";'
    cursor.execute(comando)
    resultado = cursor.fetchall()  # Lê o banco de dados (SELECT)
    return resultado

def chamar_gemini(prompt):
    url = "https://api.gemini.google.com/v1/models/text-bison:generateText"
    api_key = "AIzaSyAzWexuaPI9XnO6DpBz8n-u0aTDWxl67dM" # Obtém a chave da variável de ambiente
    print(api_key)
    if not api_key:
        raise ValueError("Chave da API Gemini não encontrada. Defina a variável de ambiente.")

    headers = {"Authorization": f"Bearer {api_key}"}
    data = {"prompt": prompt}
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Função para inserir recomendações no banco
def inserirRecomendacao(recomendacao):
    comando = 'INSERT INTO ia (recomendacoes) VALUES (%s)'
    cursor.execute(comando, (recomendacao,))
    conexao.commit()  # Grava no banco

# Lógica principal
try:
    # Buscar dados
    resultadoPrompt1 = verDadosPrompt1()
    print(f"Resultado da consulta: {resultadoPrompt1}")

    # Preparar a frase para a API
    prompt1 = f"Avalie a qualidade literária da seguinte frase: {resultadoPrompt1}"
    resposta_gemini = chamar_gemini(prompt1)

    # Extrair texto relevante da resposta da API
    texto_recomendacao = resposta_gemini.get("text", "Nenhuma recomendação encontrada.")
    print(f"Recomendação gerada: {texto_recomendacao}")

    # Inserir recomendação no banco
    inserirRecomendacao(texto_recomendacao)

except Exception as e:
    print(f"Erro: {e}")

finally:
    # Fechar conexão
    cursor.close()
    conexao.close()
