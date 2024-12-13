# Sistema de Extração de Eventos - CCBB RJ

## Descrição

Este projeto é um sistema para extrair informações sobre os eventos do **Centro Cultural Banco do Brasil (CCBB)** no Rio de Janeiro. O sistema coleta dados do site oficial do CCBB, armazena essas informações em um banco de dados SQLite e permite a consulta de eventos com base em diferentes critérios. A solução foi implementada em **Python**, utilizando bibliotecas para **web scraping** (BeautifulSoup) e manipulação de banco de dados (SQLite).

## Introdução

Este sistema foi desenvolvido para coletar dados sobre os eventos realizados no **CCBB Rio de Janeiro** a partir do seu site oficial. O código realiza um processo de **web scraping** para extrair informações sobre os eventos, como nome, tipo, data, local de realização e metadados, e armazena esses dados em um banco de dados **SQLite**.

## Objetivos

- **Coletar informações** sobre os eventos no CCBB RJ a partir da página de programação do site.
- **Armazenar** essas informações em um banco de dados SQLite.
- **Gerar relatórios** sobre os eventos, permitindo consultas detalhadas com base em critérios como localização, tipo e proximidade de início.

## Metodologia

### Tecnologias Utilizadas

- **Python**: Linguagem de programação utilizada para o desenvolvimento do sistema.
- **SQLite**: Banco de dados para armazenar as informações extraídas.
- **BeautifulSoup**: Biblioteca de **web scraping** usada para fazer a extração dos dados do site.
- **Urllib**: Biblioteca para realizar as requisições HTTP e manipulação de URLs.

### Estrutura do Código

O código foi estruturado em funções que realizam tarefas específicas:

1. **`criar_tabelas(conn)`**: Cria as tabelas no banco de dados SQLite para armazenar os dados dos eventos, informações adicionais e metadados.
2. **`inserir_eventos(conn)`**: Realiza o processo de **web scraping**, extrai os eventos do site e os insere no banco de dados, evitando duplicações.
3. **`consultar_eventos(conn)`**: Realiza consultas no banco de dados para exibir diferentes relatórios, como:
   - Todos os eventos com suas datas, localizações e tipos.
   - Os dois eventos mais próximos de iniciar.
   - Eventos no Rio de Janeiro.
   - Eventos ao ar livre (caso existam).
   - Eventos do tipo "cinema".
4. **`gerar_relatorio(eventos_extraidos, eventos_inseridos, erros)`**: Gera um relatório final, exibindo a quantidade de eventos extraídos, inseridos e eventuais erros encontrados durante a execução.
5. **`main()`**: Função principal que executa todas as etapas: criação das tabelas, inserção dos dados, consulta dos eventos e geração do relatório.

### Dados Manipulados

Os dados extraídos e armazenados incluem:

- **Nome do evento**
- **Tipo de evento** (teatro, cinema, música, etc.)
- **Data e horário**
- **Localização** (sempre "Rio de Janeiro" neste projeto)
- **Imagem** (URL da imagem do evento, se disponível)

### Consultas Realizadas

O sistema permite realizar as seguintes consultas:

1. **Todos os eventos com suas datas, localização e tipo**:
   Exibe todos os eventos armazenados no banco de dados.

2. **Dois eventos mais próximos de iniciar**:
   Exibe os dois eventos mais próximos de ocorrer, ordenados pela data.

3. **Eventos que acontecem no Rio de Janeiro**:
   Exibe todos os eventos que estão localizados no Rio de Janeiro.

4. **Eventos que são ao ar livre**:
   (Não há eventos ao ar livre neste momento, mas a consulta está preparada para retornar dados caso existam.)

5. **Eventos do tipo cinema**:
   Exibe os eventos que estão relacionados a cinema.

6. **Metadados por evento**:
   Exibe os metadados associados a cada evento, como URL da imagem.

## Gestão de Exceções e Relatório Final

O código implementa uma gestão de exceções para lidar com problemas durante a execução, como falhas de conexão com a internet ou erros ao inserir dados no banco. Ao final do processo, é gerado um relatório detalhado com as informações sobre o número de eventos extraídos, inseridos no banco de dados e quaisquer erros encontrados.

## Referências

- [Documentação do Python](https://docs.python.org/3/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [SQLite](https://www.sqlite.org/index.html)
