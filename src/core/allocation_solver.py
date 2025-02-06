from pulp import LpProblem, LpVariable, lpSum, LpMinimize, LpStatus, LpMaximize
import pandas as pd

def preprocess_data(alunos_df, projetos_df):
    """
    Pré-processa os dados a partir de DataFrames já existentes, separando em informações e dados numéricos.

    Args:
        alunos_df (pd.DataFrame): DataFrame com os dados dos alunos.
        projetos_df (pd.DataFrame): DataFrame com os dados dos projetos.

    Returns:
        tuple: Contém alunos_data, projetos_data, alunos_info, projetos_info.
    """
    # Separar alunos_info
    alunos_info = alunos_df.iloc[:, [0, 1, 2, 3, 4, -2, -1]].copy()  # Criar cópia explícita
    alunos_data = alunos_df.drop(columns=alunos_info.columns).copy()  # Criar cópia explícita

    # Separar projetos_info
    projetos_info = projetos_df.iloc[:, [0, 1, 2]].copy()  # Criar cópia explícita
    projetos_data = projetos_df.drop(columns=projetos_info.columns).copy()  # Criar cópia explícita

    return alunos_data, projetos_data, alunos_info, projetos_info

def solve_allocation(alunos_df, projetos_df):
    """
    Resolve a alocação dos alunos aos projetos considerando compatibilidade de skills.
    """
    # Pré-processar os dados
    alunos_data, projetos_data, alunos_info, projetos_info = preprocess_data(alunos_df, projetos_df)

    # Obter a lista de projetos e alunos
    projetos = projetos_info.iloc[:, 1].values  # Coluna "Código do Projeto"
    alunos = alunos_info.index  # Índices dos alunos

    # Calcular compatibilidade entre alunos e projetos
    compatibilidade = alunos_data.values @ projetos_data.values.T

    # Criar problema de otimização
    model = LpProblem("AlocacaoDeProjetos", LpMaximize)

    # Variáveis de decisão: X[i][j] indica se aluno i participa do projeto j
    x = LpVariable.dicts("x", ((i, j) for i in alunos for j in range(len(projetos))), cat="Binary")

    # Função objetivo: Maximizar a compatibilidade total
    model += lpSum(x[(i, j)] * compatibilidade[i, j] for i in alunos for j in range(len(projetos)))

    # Restrições:
    media_esperada = len(alunos) / len(projetos)
    margem = 0.5 * media_esperada  # Define uma margem aceitável de variação

    for i in alunos:
        # Cada aluno deve participar do número de projetos indicado na coluna "Projetos Tentados"
        projetos_tentados = alunos_info.loc[i, "Projetos Tentados"]
        model += lpSum(x[(i, j)] for j in range(len(projetos))) == projetos_tentados

    for j in range(len(projetos)):
        # Garantir que o número de alunos em cada projeto esteja próximo da média esperada
        alunos_por_projeto = lpSum(x[(i, j)] for i in alunos)
        model += alunos_por_projeto >= max(1, media_esperada)  # Mínimo
        model += alunos_por_projeto <= media_esperada + margem          # Máximo

    # Resolver o problema
    status = model.solve()

    if LpStatus[status] != "Optimal":
        raise ValueError("Não foi possível encontrar uma solução ótima para a alocação.")

    # Atualizar alunos_info com os projetos alocados
    for i in alunos:
        alocados = [projetos[j] for j in range(len(projetos)) if x[(i, j)].varValue == 1]
        for k, col in enumerate(["Projeto 1", "Projeto 2"]):
            if k < len(alocados):  # Evita índice fora do limite
                alunos_info.at[i, col] = alocados[k]

    # Debugging: Imprimir a quantidade de alunos alocados por projeto
    print("\nDEBUG: Quantidade de alunos alocados por projeto:")
    for j in range(len(projetos)):
        alunos_no_projeto = sum(x[(i, j)].varValue for i in alunos)
        print(f"Projeto {projetos[j]}: {alunos_no_projeto} alunos alocados")

    return alunos_info
