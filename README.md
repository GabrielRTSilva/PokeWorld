# 🌍 PokeWorld - ETL de Dados da PokeAPI

Este projeto Python tem como objetivo consumir dados da [PokeAPI](https://pokeapi.co/), realizar um pipeline de ETL (Extração, Transformação e Carga) e armazenar os dados estruturados em um banco de dados SQLite. O projeto foca na organização dos Pokémon por regiões, com tabelas relacionais otimizadas para consultas futuras.

---

## 📁 Estrutura do Projeto

script-pokeworld/
|— pipeline_pokeworld.py  # Script com funções ETL para coleta e transformação dos dados
|— main.py                # Script principal responsável por criar o banco de dados SQLite e popular as tabelas
⌊ pokeworld.db           # Arquivo gerado contendo o banco de dados populado (após execução).


---

## 🧠 Funcionalidades

- 📦 Criação da tabela de Regiões Pokémon com descrição, imagem e referência à Pokédex
- 🔎 Extração dos Pokémon de cada região via API, incluindo casos especiais como Kalos
- 📊 Geração de tabela de Pokémon únicos, com dados como tipo(s), altura, peso, imagem e som
- 🧬 Geração de uma tabela intermediária Pokedex, que relaciona Pokémon e Regiões
- 🗃️ Criação e persistência do banco de dados SQLite com suporte a chaves estrangeiras

---

## ⚙️ Como Executar

1. Clone o repositório:

    git clone https://github.com/GabrielRTSilva/PokeWorld
    cd PokeWorld

2. Instale as dependências:

    pip install pandas

3. Execute o script principal:

    python main.py

Isso criará o arquivo pokeworld.db com as seguintes tabelas populadas:
- REGIOES
- POKEMONS
- POKEDEX

---

## 🧾 Estrutura das Tabelas

REGIOES:
- ID_REGIAO: INTEGER – ID primário da região
- NOME_REGIAO: TEXT – Nome da região (ex: Kanto)
- DESCRICAO_REGIAO: TEXT – Texto descritivo
- IMAGEM_REGIAO: TEXT – URL da imagem da região
- ID_POKEDEX: TEXT – ID lógico da Pokédex associada

POKEMONS:
- ID_POKEMON: INTEGER – ID do Pokémon (da API)
- NOME_POKEMON: TEXT – Nome do Pokémon
- TIPOS: TEXT – Tipo(s) do Pokémon (ex: fire, flying)
- ALTURA: INTEGER – Altura (em decímetros)
- PESO: INTEGER – Peso (em hectogramas)
- IMAGEM: TEXT – URL do sprite padrão
- SOM_POKEMON: TEXT – URL do som (cries) do Pokémon

POKEDEX:
- ID_POKEDEX: INTEGER
- ID_REGIAO: INTEGER – FK para REGIOES(ID_REGIAO)
- ID_POKEMON: INTEGER – FK para POKEMONS(ID_POKEMON)

---

## 💡 Observações Técnicas

- As requisições à API são feitas com time.sleep para respeitar limites e evitar bloqueios.
- A região de Kalos possui três Pokédex diferentes (Central, Coastal e Mountain), sendo tratada separadamente.
- Os dados são extraídos diretamente da PokeAPI, uma API pública e gratuita.
- Após a execução, os dados são salvos no banco de dados pokeworld.db.

---

## 💡 Possíveis Extensões Futuras

- Interface web com Flask ou Django
- Dashboard com gráficos interativos
- Integração com React, Next.js ou Streamlit
- Filtros por tipo, peso ou região
- Sistema de recomendação de Pokémon

---

## 🧑‍💻 Autor

Desenvolvido por Gabriel Rosemberg
Contato: grtsilva00@gmail.com
LinkedIn: [https://linkedin.com/in/seu-perfil](https://www.linkedin.com/in/gabrielrtsilva/)
