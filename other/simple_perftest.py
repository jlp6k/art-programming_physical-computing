# Ce programme montre une façon d'évaluer la vitesse d'exécution de la fonction prédéfinie sorted().
#

import time
import random

def shuffle(x):
    """Shuffle list x in place, and return it.

    The standard shuffle() function isn't provided in the micropython random module.
    The following code come from the Python default implementation.
    """
    for i in reversed(range(1, len(x))):
        # pick an element in x[:i+1] with which to exchange x[i]
        j = int(random.random() * (i+1))
        x[i], x[j] = x[j], x[i]

    return x

# L'évaluation est effectuée en répétant 1000 fois le même code afin d'obtenir une moyenne
test_count = 1000

computation_time = 0
for _ in range(test_count):
    # Une liste d'entiers est préparée pour être triée par la fonction sorted().
    # La liste contient les entiers de 0 à 99 mélangés
    list_to_sort = list(range(100))
    shuffle(list_to_sort)

    # Exécution de la fonction sorted et mesure du temps écoulé.
    start_time = time.ticks_ms()
    s = sorted(list_to_sort)
    computation_time += time.ticks_diff(time.ticks_ms(), start_time)

print("Test avec une liste de valeurs mélangées")
print(f"Temps moyen d'exécution : {computation_time / test_count} ms")

computation_time = 0
for _ in range(test_count):
    # Une liste d'entiers est préparée pour être triée par la fonction sorted().
    # La liste contient les entiers de 0 à 99 dans l'ordre croissant
    list_to_sort = list(range(100))

    # Exécution de la fonction sorted et mesure du temps écoulé.
    start_time = time.ticks_ms()
    s = sorted(list_to_sort)
    computation_time += time.ticks_diff(time.ticks_ms(), start_time)

print("Test avec une liste de valeurs pré-triées")
print(f"Temps moyen d'exécution : {computation_time / test_count} ms")
