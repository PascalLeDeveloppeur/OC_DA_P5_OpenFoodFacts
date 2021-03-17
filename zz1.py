from pprint import pprint


# Order the list by nbr of categories then nutri_score

body = [("Mont Pelée", "C", 3),
        ("Vaval", "A", 3),
        ("Coca", "E", 3),
        ("Danao", "A", 2),
        ("Cacolac", "B", 2),
        ("Milky", "blue", 2),
        ("Sixn", "C", 2),
        ("Heinken", "B", 1),
        ("Chrystaline", "A", 1),
        ("Mercier", "D", 1),
        ("Depaz", "B", 1)]

# Calculation of the importance of the product in order to display it:
# Index 2 (x[2]) is the most important factor, followed by the score (x[1]).
# weight = str(10000 - x[2])
# importance = weight + score = str(10000 - x[2]) + x[1]
body.sort(reverse=False, key=lambda x: str(10000-x[2])+x[1])

pprint(body)
