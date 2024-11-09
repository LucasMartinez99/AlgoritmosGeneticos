import random

def initialize_individual(icls, crime_data, comisarias_data):
    num_comisarias = len(comisarias_data)
    total_patrullas = 39

    initial_allocation = [1] * num_comisarias
    remaining_patrullas = total_patrullas - num_comisarias

    while remaining_patrullas > 0:
        idx = random.choice(range(num_comisarias))
        initial_allocation[idx] += 1
        remaining_patrullas -= 1

    return icls(initial_allocation)

def mutate(individual):
    num_comisarias = len(individual)
    # Cambiar varios valores en cada mutación
    for _ in range(random.randint(1, 3)):
        idx = random.choice(range(num_comisarias))
        change = random.choice([-1, 1])
        if 1 <= individual[idx] + change <= 39:
            individual[idx] += change
    return individual,


def cxUniformKeepSum(ind1, ind2, prob=0.5):
    size = len(ind1)
    for i in range(size):
        if random.random() < prob:
            ind1[i], ind2[i] = ind2[i], ind1[i]

    for ind in [ind1, ind2]:
        total_patrullas = sum(ind)
        while total_patrullas != 39:
            if total_patrullas > 39:
                idx = random.choice(range(size))
                if ind[idx] > 1:
                    ind[idx] -= 1
                    total_patrullas -= 1
            elif total_patrullas < 39:
                idx = random.choice(range(size))
                ind[idx] += 1
                total_patrullas += 1

    return ind1, ind2
