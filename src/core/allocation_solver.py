import pandas as pd
from pulp import LpMaximize, LpProblem, LpVariable, lpSum

def preprocess_data(alunos_data, projetos_data):
    """
    Pré-processa os dados de alunos e projetos para uso na otimização.
    """
    # Substituir valores vazios por 0
    alunos_data = alunos_data.fillna(0)
    projetos_data = projetos_data.fillna(0)

    # Converter coluna "pode_comparecer" em valores numéricos
    alunos_data["pode_comparecer"] = alunos_data["pode_comparecer"].replace({"Sim": 1, "Não": 0}).fillna(0)

    # Pré-alocações (substituir strings vazias por None para facilitar o cálculo)
    alunos_data["Projeto 1"] = alunos_data["Projeto 1"].replace("", None)
    alunos_data["Projeto 2"] = alunos_data["Projeto 2"].replace("", None)

    # Remover colunas irrelevantes
    alunos_habilidades = alunos_data.iloc[:, 4:-2]  # Da 5ª coluna até antes de 'Projeto 1' e 'Projeto 2'
    projetos_demandas = projetos_data.iloc[:, 2:]  # Da 3ª coluna em diante

    return alunos_habilidades, projetos_demandas, alunos_data

def solve_allocation(alunos_data, projetos_data):
    """
    Resolve o problema de alocação de alunos para projetos.
    """
    # Pré-processar dados
    alunos_habilidades, projetos_demandas, alunos_data = preprocess_data(alunos_data, projetos_data)

    num_alunos = alunos_habilidades.shape[0]
    num_projetos = projetos_demandas.shape[0]

    # Criar o modelo de otimização
    model = LpProblem("Alocacao_Alunos_Projetos", LpMaximize)

    # Variáveis de decisão
    x = {(i, j): LpVariable(f"x_{i}_{j}", cat="Binary") for i in range(num_alunos) for j in range(num_projetos)}

    # Função objetivo: maximizar compatibilidade e desempate (pode_comparecer)
    model += lpSum(
        x[i, j] * (
            alunos_habilidades.iloc[i].dot(projetos_demandas.iloc[j]) +  # Compatibilidade
            alunos_data.loc[i, "pode_comparecer"]  # Desempate
        )
        for i in range(num_alunos) for j in range(num_projetos)
    )

    # Restrição: Respeitar pré-alocações
    for i in range(num_alunos):
        # Projetos já alocados
        pre_allocations = [
            projetos_data.index[projetos_data.iloc[:, 0] == alunos_data.loc[i, "Projeto 1"]].tolist(),
            projetos_data.index[projetos_data.iloc[:, 0] == alunos_data.loc[i, "Projeto 2"]].tolist()
        ]

        # Converter listas de listas em um único conjunto de índices
        pre_allocated_indices = {j for alloc in pre_allocations for j in alloc if alloc}

        # Se o aluno já está alocado no número total de projetos, nenhuma alocação adicional
        if len(pre_allocated_indices) >= alunos_data.loc[i, "Projetos Tentados"]:
            for j in range(num_projetos):
                model += x[i, j] == 0
        else:
            # Se há vagas restantes, limitar a alocação a projetos adicionais
            remaining_projects = alunos_data.loc[i, "Projetos Tentados"] - len(pre_allocated_indices)
            model += lpSum(x[i, j] for j in range(num_projetos)) == remaining_projects

        # Garantir que não seja alocado em projetos já pré-alocados
        for j in pre_allocated_indices:
            model += x[i, j] == 0

    # Restringir alocação a projetos compatíveis
    for i in range(num_alunos):
        for j in range(num_projetos):
            if alunos_habilidades.iloc[i].dot(projetos_demandas.iloc[j]) == 0:
                model += x[i, j] == 0

    # Resolver o problema
    model.solve()

    # Extrair a solução
    allocation = []
    for i in range(num_alunos):
        allocated_projects = []
        # Adicionar pré-alocações diretamente
        if alunos_data.loc[i, "Projeto 1"]:
            allocated_projects.append(alunos_data.loc[i, "Projeto 1"])
        if alunos_data.loc[i, "Projeto 2"]:
            allocated_projects.append(alunos_data.loc[i, "Projeto 2"])

        # Adicionar projetos alocados pelo solver
        for j in range(num_projetos):
            if x[i, j].value() == 1:
                allocated_projects.append(projetos_data.iloc[j, 0])  # Nome do projeto
        allocation.append((alunos_data.iloc[i, 0], allocated_projects))  # Nome do aluno e projetos alocados

    return allocation
