import copy

orijinal_list = [[1, 2, 3], [4, 5]]
shallow_copy = copy.copy(orijinal_list)
deep_copy = copy.deepcopy(orijinal_list)

shallow_copy[0][0] = 'X'

deep_copy[0][1] = 'X'

print("Orijinal Liste:", orijinal_list)
print("Shallow Copy:", shallow_copy)
print("Deep Copy:", deep_copy)