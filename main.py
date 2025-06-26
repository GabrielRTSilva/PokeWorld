import sqlite3
from pipeline_pokeworld import gerar_tabelas  # importa as tabelas do pipeline 

# Gera os DataFrames
t1_regiao, t2_pokemons, t3_pokedex = gerar_tabelas()

print(' # ===== Iniciando o banco de dados ===== #')

# Conecta ao banco e ativa suporte a FOREIGN KEY
print('Criando a conexão...')
conn = sqlite3.connect("pokeworld.db")  # Instancia a conexão
cursor = conn.cursor()  # Instancia o objeto para realizar as modificações.
cursor.execute("PRAGMA foreign_keys = ON;")

# Cria a tabela REGIOES
print('Criando a tabela REGIOES...')
cursor.execute("""
CREATE TABLE IF NOT EXISTS REGIOES (
    ID_REGIAO INTEGER PRIMARY KEY,
    NOME_REGIAO TEXT NOT NULL,
    DESCRICAO_REGIAO TEXT,
    IMAGEM_REGIAO TEXT,
    ID_POKEDEX TEXT
);
""")

# Cria a tabela POKEMONS
print('Criando a tabela POKEMONS')
cursor.execute("""
CREATE TABLE IF NOT EXISTS POKEMONS (
    ID_POKEMON INTEGER PRIMARY KEY,
    NOME_POKEMON TEXT NOT NULL,
    TIPOS TEXT,
    ALTURA INTEGER,
    PESO INTEGER,
    IMAGEM TEXT,
    SOM_POKEMON TEXT
);
""")

# Cria a tabela POKEDEX com chaves estrangeiras
print('Criando a tabela POKEDEX...')
cursor.execute("""
CREATE TABLE IF NOT EXISTS POKEDEX (
    ID_POKEDEX INTEGER,
    ID_REGIAO INTEGER,
    ID_POKEMON INTEGER,
    FOREIGN KEY (ID_REGIAO) REFERENCES REGIOES(ID_REGIAO),
    FOREIGN KEY (ID_POKEMON) REFERENCES POKEMONS(ID_POKEMON)
);
""")

# Insere os dados nas tabelas criadas
print('Populando as tabelas criadas.')
t1_regiao.to_sql("REGIOES", conn, if_exists="append", index=False)
t2_pokemons.to_sql("POKEMONS", conn, if_exists="append", index=False)
t3_pokedex.to_sql("POKEDEX", conn, if_exists="append", index=False)

# Sobe as modificações e fecha a conexão
conn.commit()
conn.close()

print("Banco de dados criado e populado com sucesso.")
