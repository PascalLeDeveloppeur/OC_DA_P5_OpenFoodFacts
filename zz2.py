l1 = ["a", "b", "c", "d", "e", "f"]
l2 = ["b", "c", "e"]

l1 = [elt for elt in l1 if elt not in l2]
# l1 = ['a', 'd', 'f']
print(l1)
