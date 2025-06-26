
# Script para gerar as tabelas do PokeWorld.
import pandas as pd
import requests
import time


# ======== Funções ETL ======== #

def criar_tabela_regioes():
    '''
    Essa função gera o dataframe tabela_regioes.
    - Argumento:
        - Não recebe nenhum argumento, pois, os dados foram previamente analisados na API e estruturados na função.
    - Saída:
        - Um objeto dataframe contendo 5 colunas: ID_REGIAO, NOME_REGIAO, DESCRICAO_REGIAO e ID_POKEDEX. 
    '''
    id_regioes = [1, 2, 3, 4, 5, 6]

    lista_nome_regiao = ['Kanto', 'Johto', 'Hoenn', 'Sinnoh', 'Unova', 'Kalos']
    
    lista_descricoes = [
        "A primeira e mais icônica região do mundo Pokémon! Lar dos 151 Pokémon originais, Kanto é repleta de nostalgia, cidades clássicas e aventuras inesquecíveis. Comece sua jornada onde tudo começou!",

        "Com rica herança cultural e laços profundos com Kanto, Johto apresenta Pokémon místicos, tradições antigas e novas mecânicas como a criação e os ovos. Uma região que une passado e inovação!",

        "Repleta de natureza exuberante, mares vastos e ilhas tropicais, Hoenn traz desafios aquáticos e climáticos. Aqui surgem batalhas em dupla, competições de beleza e um Pokédex diversificado!",

        "Montanhas geladas, mitos ancestrais e lendas de criação do universo Pokémon fazem de Sinnoh uma das regiões mais enigmáticas. Um lugar onde a ciência e a espiritualidade se encontram.",

        "Inspirada em grandes metrópoles, Unova marca uma nova era com Pokémon inéditos e uma narrativa envolvente. A região traz uma experiência urbana cheia de inovação e diversidade!",

        "Estilo e elegância definem Kalos! Com paisagens deslumbrantes inspiradas na França, Kalos introduz a Mega Evolução e celebra a conexão entre beleza e batalha."
    ]
    
    lista_imagens = [
        'https://archives.bulbagarden.net/media/upload/thumb/7/7d/PE_Kanto_Map.png/300px-PE_Kanto_Map.png',
        'https://archives.bulbagarden.net/media/upload/thumb/6/64/JohtoMap.png/300px-JohtoMap.png',
        'https://archives.bulbagarden.net/media/upload/thumb/8/85/Hoenn_ORAS.png/300px-Hoenn_ORAS.png',
        'https://archives.bulbagarden.net/media/upload/thumb/0/08/Sinnoh_BDSP_artwork.png/300px-Sinnoh_BDSP_artwork.png',
        'https://archives.bulbagarden.net/media/upload/thumb/f/fc/Unova_B2W2_alt.png/300px-Unova_B2W2_alt.png',
        'https://archives.bulbagarden.net/media/upload/thumb/8/8a/Kalos_alt.png/300px-Kalos_alt.png'
    ]
    
    lista_id_pokedex = [2, 3, 4, 5, 8, [12, 13, 14]]

    return pd.DataFrame({
        'ID_REGIAO': id_regioes,
        'NOME_REGIAO': lista_nome_regiao,
        'DESCRICAO_REGIAO': lista_descricoes,
        'IMAGEM_REGIAO': lista_imagens,
        'ID_POKEDEX': lista_id_pokedex
    })

def obter_pokemons_por_regiao(tabela_regioes):
    '''
    Obtem os dados dos pokémons de acordo com a pokédex que corresponde a cada região.
    Obs.: A região de kalos possui 3 pokédexes e para isso foi implementado uma condição especial.
    - Argumentos:
        - tabela_regioes: É utilizado os dados da coluna ID_POKEDEX para gerar a rota da API dinâmicamente.
    - Saída:
        - regiao_x_pokemons: É um dicionário contendo a relação de todos os pokémons (incluindo os duplicados) de cada respectiva região.
    '''

    regiao_x_pokemons = {str(i + 1): [] for i in range(6)}  # O dict comprehension gera um dicionário em que, respectivamente, as chaves são números de 1-6 com os valores sem listas vazias.

    kalos_pokedexes = {'Kalos Central': [], 'Kalos Coastal': [], 'Kalos Mountain': []}

    for id_pokedex in tabela_regioes['ID_POKEDEX']:
        
        if not isinstance(id_pokedex, list):
            
            response = requests.get(f'https://pokeapi.co/api/v2/pokedex/{id_pokedex}/') #Acessa a rota de cada pokedex
            
            time.sleep(0.2) # Pausa para não sobrecarregar os requests na API

            if response.status_code == 200:
                data = response.json()
                nome = data['name']
                index = {
                    'kanto': '1',
                    'johto': '2',
                    'hoenn': '3',
                    'sinnoh': '4',
                    'unova': '5'
                }.get(nome, None)
                if index:
                    regiao_x_pokemons[index].extend(
                        [entry['pokemon_species']['name'] for entry in data['pokemon_entries']]
                    )
        else:
            for subid in id_pokedex:   # Loop para iterar sobre a sublista de Kalos
                response = requests.get(f'https://pokeapi.co/api/v2/pokedex/{subid}/')
                
                time.sleep(1.2)
                
                if response.status_code == 200:
                    
                    data = response.json()
                    key = data['name']   # Local onde está o nome da região
                    
                    if 'central' in key:   # Verifica se a parte da região está inserida no nome
                        kalos_pokedexes['Kalos Central'] += [pokemon['pokemon_species']['name'] for pokemon in data['pokemon_entries']]
                    elif 'coastal' in key:
                        kalos_pokedexes['Kalos Coastal'] += [pokemon['pokemon_species']['name'] for pokemon in data['pokemon_entries']]
                    elif 'mountain' in key:
                        kalos_pokedexes['Kalos Mountain'] += [pokemon['pokemon_species']['name'] for pokemon in data['pokemon_entries']]

    uniao_kalos = set().union(*kalos_pokedexes.values())  # Une as partes de Kalos sem repetir os nomes a partir do objeto conjunto, método union.
    
    regiao_x_pokemons['6'].extend(list(uniao_kalos))

    return regiao_x_pokemons

def criar_tabela_pokemons(regiao_x_pokemons):
    '''
    Cria a tabela Pokemon.
    - Argumentos:
        - regiao_x_pokemons: Recebe esse dicionário para gerar o conjunto com todos os pokémons não duplicados.
    - Saída:
        - tabela_pokemons: Um objeto dataframe contendo as colunas ID_POKEMON, NOME_POKEMON, TIPOS, ALTURAS, PESO, IMAGEM e SOM_POKEMON.   
    '''
    nomes = set().union(*regiao_x_pokemons.values())  # Faz a união de todos os pokemons que existem em todas as regiões, transformando-os em conjunto para tirar as duplicatas.

    ids, nomes_final, tipos_do_pokemon, alturas, pesos, imagens, som_pokemon = [], [], [], [], [], [], []  # inicializa as listas

    for nome in nomes:
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{nome}')
        time.sleep(0.2)
        
        if response.status_code == 200:
            data = response.json()
            ids.append(data['id'])
            nomes_final.append(nome)
            
            # Lógica para os tipos: Pokémons podem ter +1 de tipo.
            if len(data['types']) < 2:
                tipos_do_pokemon.append(data['types'][0]['type']['name'])
            else:
                lista_sup_tipos = []
                for tipo in data['types']:
                    lista_sup_tipos.append(tipo['type']['name'])
                tipos_do_pokemon.append(', '.join(lista_sup_tipos))

            alturas.append(data['height'])
            pesos.append(data['weight'])
            imagens.append(data['sprites']['front_default'])
            som_pokemon.append(str(data['cries']['latest']) if data['cries']['latest'] else str(data['cries']['legacy']))   # Verifica se existe o som mais recente, caso contrário pega a url do legado.
        else:
            print(f"Erro ao buscar {nome}")

    return pd.DataFrame({
        'ID_POKEMON': ids,
        'NOME_POKEMON': nomes_final,
        'TIPOS': tipos_do_pokemon,
        'ALTURA': alturas,
        'PESO': pesos,
        'IMAGEM': imagens,
        'SOM_POKEMON': som_pokemon
    }).sort_values(by='ID_POKEMON')   

def criar_tabela_pokedex(tabela_pokemons, regiao_x_pokemons):
    '''
    Essa função gera a tabela Pokedex.
    - Argumentos:
        - tabela_pokemons: Recebe a tabela_pokemon para utilizar os dados dos pokémons que foram registrados sem estar duplicados.
        - regia_x_pokemons: Recebe a regiao_x_pokemons para estabelecer a relação com os pokémons de cada região.
    - Saída:
        - tabela_pokedex: Um objeto dataframe que contém as colunas ID_POKEDEX, ID_REGIAO e ID_POKEMON.

    '''
    id_e_nome = dict(zip(tabela_pokemons['NOME_POKEMON'], tabela_pokemons['ID_POKEMON']))   # Gera uma tupla que contém, respectivamente, o nome do pokémon e seu id.
    
    id_pokedex, id_regiao, id_pokemon = [], [], []

    for regiao, lista in regiao_x_pokemons.items():     # Acessa o index das regiões e seus pokémons.
        for nome in lista: # Itera sobre cada pokemon da lista de pokémons.
            if nome in id_e_nome:  # Verifica se o nome existe nas tuplas que corresponem aos pokémons cadastrados e então preenche os dados na tabela.
                id_pokedex.append(int(regiao))
                id_regiao.append(int(regiao))
                id_pokemon.append(id_e_nome[nome])

    return pd.DataFrame({
        'ID_POKEDEX': id_pokedex,
        'ID_REGIAO': id_regiao,
        'ID_POKEMON': id_pokemon
    })


# ======== Função para Gerar as Tabelas ======== #

def gerar_tabelas():
    '''
    Essa função gera os 3 objetos dataframe para regioes, pokedex e pokemons.
    - Argumento:
        - Nenhum declarado.
    - Saída:
        - tabela_regioes, tabela_pokemons, tabela_pokedex = Objetos dataframes. 
    
    '''
    print('Criando o dataframe Regiões...')
    tabela_regioes = criar_tabela_regioes()
    
    print('Obtendo os pokémons por região...')
    regiao_x_pokemons = obter_pokemons_por_regiao(tabela_regioes)
    
    print('Criando o dataframe Pokémon....')
    tabela_pokemons = criar_tabela_pokemons(regiao_x_pokemons)

    print('Criando o dataframe Pokédex...')
    tabela_pokedex = criar_tabela_pokedex(tabela_pokemons, regiao_x_pokemons)

    # Modifica o dataframe REGIOES, coluna ID_POKEDEX para corresponder com os ID's adicionados no dataframe Pokedex
    novos_ids_pokedex = [1, 2, 3, 4, 5, 6]

    tabela_regioes['ID_POKEDEX'] = novos_ids_pokedex

    print(' As tabelas foram geradas com sucesso.')
    
    return tabela_regioes, tabela_pokemons, tabela_pokedex



