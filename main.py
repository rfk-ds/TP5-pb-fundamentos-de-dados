import urllib.request
from bs4 import BeautifulSoup
import sqlite3
import time

url = 'https://ccbb.com.br/rio-de-janeiro/programacao/'

def criar_tabelas(conn):
    """
    Cria as tabelas no banco de dados para armazenar eventos, dados dos eventos e metadados.

    Args:
        conn (sqlite3.Connection): Conexão com o banco de dados SQLite.
    """
    cursor = conn.cursor()
    
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            tipo TEXT NOT NULL
        )
    ''')
    
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS dados_eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_evento INTEGER UNIQUE,
            data TEXT NOT NULL,
            localizacao TEXT NOT NULL,
            FOREIGN KEY (id_evento) REFERENCES eventos(id)
        )
    ''')
    
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS metadados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_evento INTEGER,
            metadado TEXT NOT NULL,
            FOREIGN KEY (id_evento) REFERENCES eventos(id)
        )
    ''')
    
    conn.commit()

def inserir_eventos(conn):
    """
    Extrai eventos do site e insere no banco de dados, evitando duplicatas.

    Args:
        conn (sqlite3.Connection): Conexão com o banco de dados.

    Returns:
        tuple: (eventos extraídos, eventos inseridos, lista de erros)
    """
    eventos_extraidos = 0
    eventos_inseridos = 0
    erros = []
    
    try:
        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                raise Exception(f"Erro ao acessar o site: Status {response.status}")
            soup = BeautifulSoup(response.read(), 'html.parser')
    except urllib.error.URLError as e:
        erros.append(f"Erro de rede: {e}")
        return eventos_extraidos, eventos_inseridos, erros
    except Exception as e:
        erros.append(f"Erro ao fazer a requisição: {e}")
        return eventos_extraidos, eventos_inseridos, erros

    cursor = conn.cursor()
    
    for evento in soup.find_all('div', class_='card-evento__content'):  
        try:
            titulo = evento.find('h4', class_='titulo')
            data = evento.find('p', class_='data')
            localizacao = 'Rio de Janeiro'
            
            tipo_elemento = evento.find_previous('div', class_='tipo')
            tipo_evento = tipo_elemento.find('p')
            tipo = tipo_evento.text.strip() if tipo_evento else "Desconhecido"
            
            imagem_elemento = evento.find_previous('img', class_='attachment-medium_large size-medium_large wp-post-image')
            imagem_url = imagem_elemento['src'] if imagem_elemento else "Sem imagem"

            if titulo and data:
                nome = titulo.text.strip()
                data_text = data.text.strip()

                try:
                    cursor.execute('INSERT OR IGNORE INTO eventos (nome, tipo) VALUES (?, ?)', (nome, tipo))
                    evento_id = cursor.lastrowid or cursor.execute('SELECT id FROM eventos WHERE nome = ?', (nome,)).fetchone()[0]
                    cursor.execute('INSERT OR IGNORE INTO dados_eventos (id_evento, data, localizacao) VALUES (?, ?, ?)', (evento_id, data_text, localizacao))
                    cursor.execute('INSERT OR IGNORE INTO metadados (id_evento, metadado) VALUES (?, ?)', (evento_id, imagem_url))

                    eventos_extraidos += 1
                    eventos_inseridos += 1
                except sqlite3.IntegrityError as e:
                    erros.append(f"Erro ao inserir evento {nome}: {e}")
        except Exception as e:
            erros.append(f"Erro ao processar evento: {e}")
            
    conn.commit()
    return eventos_extraidos, eventos_inseridos, erros


def gerar_relatorio(eventos_extraidos, eventos_inseridos, erros):
    """
    Exibe um relatório sobre a extração de eventos, incluindo erros encontrados.

    Args:
        eventos_extraidos (int): Número de eventos extraídos.
        eventos_inseridos (int): Número de eventos inseridos no banco de dados.
        erros (list): Lista de erros encontrados durante o processo.
    """
    print("\nRelatório Final:")
    print(f"Eventos extraídos: {eventos_extraidos}")
    print(f"Eventos inseridos no banco: {eventos_inseridos}")
    if erros:
        print("\nErros encontrados:")
        for erro in erros:
            print(f" - {erro}")
    else:
        print("\nNenhum erro encontrado.")
    
def consultar_eventos(conn):
    """
    Consulta e exibe eventos armazenados no banco de dados.

    Args:
        conn (sqlite3.Connection): Conexão com o banco de dados SQLite.
    """
    cursor = conn.cursor()

    print("\nTodos os eventos com suas datas, localização e tipo:\n")
    cursor.execute(''' 
        SELECT e.nome, d.data, d.localizacao, e.tipo
        FROM eventos e
        JOIN dados_eventos d ON e.id = d.id_evento
    ''')
    for row in cursor.fetchall():
        print(row)

    print("\nDois eventos mais próximos de iniciar:\n")
    cursor.execute(''' 
        SELECT e.nome, d.data, d.localizacao, e.tipo
        FROM eventos e
        JOIN dados_eventos d ON e.id = d.id_evento
        ORDER BY d.data ASC
        LIMIT 2
    ''')
    for row in cursor.fetchall():
        print(row)

    print("\nEventos que acontecem no Rio de Janeiro:\n")
    cursor.execute(''' 
        SELECT e.nome, d.data, d.localizacao, e.tipo
        FROM eventos e
        JOIN dados_eventos d ON e.id = d.id_evento
        WHERE d.localizacao = 'Rio de Janeiro'
    ''')
    for row in cursor.fetchall():
        print(row)

    print("\nEventos que são ao ar livre (não há nenhum):\n")
    cursor.execute(''' 
        SELECT e.nome, d.data, d.localizacao, e.tipo
        FROM eventos e
        JOIN dados_eventos d ON e.id = d.id_evento
        WHERE e.tipo LIKE '%ao ar livre%'
    ''')
    for row in cursor.fetchall():
        print(row)
        
    print("\nEventos do tipo cinema (consulta alternativa):\n")
    cursor.execute(''' 
        SELECT e.nome, d.data, d.localizacao, e.tipo
        FROM eventos e
        JOIN dados_eventos d ON e.id = d.id_evento
        WHERE e.tipo LIKE '%cinema%'
    ''')
    for row in cursor.fetchall():
        print(row)

    print("\nMetadados por evento:\n")
    cursor.execute(''' 
        SELECT e.nome, m.metadado
        FROM eventos e
        JOIN metadados m ON e.id = m.id_evento
    ''')
    for row in cursor.fetchall():
        print(row)

def main():
    """
    Executa a extração de eventos, inserção no banco e gera um relatório.
    """
    conn = sqlite3.connect('eventos_ccbb.db')
    criar_tabelas(conn)

    start_time = time.time()

    eventos_extraidos, eventos_inseridos, erros = inserir_eventos(conn)

    consultar_eventos(conn)

    gerar_relatorio(eventos_extraidos, eventos_inseridos, erros)
    
    end_time = time.time()
    print(f"\nTempo total de execução: {end_time - start_time:.2f} segundos.")
    
    conn.close()

main()