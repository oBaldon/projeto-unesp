from pulp import LpProblem, LpVariable, lpSum, LpStatus, LpMaximize
import pandas as pd

def preprocess_data(alunos_df, projetos_df):
    """
    Pré-processa os dados a partir de DataFrames já existentes, separando em informações e dados numéricos.
    """
    # Separar alunos_info
    alunos_info = alunos_df.iloc[:, [0, 1, 2, 3, 4, -2, -1]].copy()
    alunos_data = alunos_df.drop(columns=alunos_info.columns).copy()

    # Separar projetos_info
    projetos_info = projetos_df.iloc[:, [0, 1, 2]].copy()
    projetos_data = projetos_df.drop(columns=projetos_info.columns).copy()

    return alunos_data, projetos_data, alunos_info, projetos_info

def solve_allocation(alunos_df, projetos_df):
    """
    Resolve a alocação dos alunos aos projetos considerando compatibilidade e pré-alocação.
    """
    alunos_data, projetos_data, alunos_info, projetos_info = preprocess_data(alunos_df, projetos_df)

    projetos = projetos_info.iloc[:, 1].values  # Códigos dos projetos
    alunos = alunos_info.index

    # Matriz de compatibilidade: produto escalar entre habilidades do aluno e requisitos do projeto
    compatibilidade = alunos_data.values @ projetos_data.values.T

    model = LpProblem("AlocacaoDeProjetos", LpMaximize)

    x = LpVariable.dicts("x", ((i, j) for i in alunos for j in range(len(projetos))), cat="Binary")

    # Função objetivo: maximizar a compatibilidade total
    model += lpSum(x[(i, j)] * compatibilidade[i, j] for i in alunos for j in range(len(projetos)))

    # Cálculo da média com base no total de alocações
    total_de_alocacoes = alunos_info["Projetos Tentados"].sum()
    media_esperada = total_de_alocacoes / len(projetos)
    margem = 0.2 * media_esperada  # tolerância de 20%

    for i in alunos:
        projetos_alocados = []
        for col in ["Projeto 1", "Projeto 2"]:
            projeto_nome = alunos_info.at[i, col]
            if pd.notna(projeto_nome) and projeto_nome.strip() != "":
                if projeto_nome in projetos:
                    j = list(projetos).index(projeto_nome)
                    model += x[(i, j)] == 1
                    projetos_alocados.append(j)
                else:
                    raise ValueError(f"O projeto '{projeto_nome}' do aluno {i} não existe na lista de projetos.")

        projetos_tentados = alunos_info.loc[i, "Projetos Tentados"]
        restantes = projetos_tentados - len(projetos_alocados)

        if restantes < 0:
            raise ValueError(f"Aluno {i} tem mais projetos pré-alocados do que tentados.")

        model += lpSum(
            x[(i, j)] for j in range(len(projetos)) if j not in projetos_alocados
        ) == restantes

    for j in range(len(projetos)):
        alunos_por_projeto = lpSum(x[(i, j)] for i in alunos)
        model += alunos_por_projeto >= media_esperada - margem
        model += alunos_por_projeto <= media_esperada + margem

    # Resolver o problema
    status = model.solve()

    if LpStatus[status] != "Optimal":
        raise ValueError("Não foi possível encontrar uma solução ótima para a alocação.")

    # Atualizar alunos_info com os projetos alocados
    for i in alunos:
        alocados = [projetos[j] for j in range(len(projetos)) if x[(i, j)].varValue == 1]
        for k, col in enumerate(["Projeto 1", "Projeto 2"]):
            if k < len(alocados):
                alunos_info.at[i, col] = alocados[k]

    # DEBUG: Quantidade de alunos alocados por projeto
    print("\nDEBUG: Quantidade de alunos alocados por projeto:")
    for j in range(len(projetos)):
        alunos_no_projeto = sum(x[(i, j)].varValue for i in alunos)
        print(f"Projeto {projetos[j]}: {alunos_no_projeto:.0f} alunos alocados")

    # DEBUG: Compatibilidade dos primeiros alunos
    print("\nDEBUG: Compatibilidade dos primeiros alunos (Top 3 projetos):")
    for i in alunos:  
        scores = [(projetos[j], compatibilidade[i, j]) for j in range(len(projetos))]
        scores.sort(key=lambda x: x[1], reverse=True)
        top3 = scores[:3]
        alocados = [alunos_info.at[i, col] for col in ["Projeto 1", "Projeto 2"] if pd.notna(alunos_info.at[i, col])]
        print(f"Aluno {i}:")
        print(f"  Top 3 compatíveis: {[f'{proj} ({score:.1f})' for proj, score in top3]}")
        print(f"  Projetos alocados: {alocados}")

    return alunos_info
