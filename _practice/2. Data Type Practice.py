# 1. Lists -  ordered and mutable
my_list = ['epicurious','the new yorker','vogue','ars technica','pitchfork']
my_list2 = ['wired', 'vanity fair', 'cookie']
my_list += my_list2
my_list.remove('cookie')
my_list.append('GQ')
my_list = [x.lower() if 'GQ' in x else x for x in my_list]
my_list[2] = 'teen ' + my_list[2]

# 2. Tuples -  ordered and immutable
my_tuple = ('epicurious','the new yorker','vogue','ars technica','pitchfork')
my_tuple = [my_tuple.index(x) for x in my_tuple]

# 3. Sets -  unordered and mutable, no duplicates
my_set = {'epicurious','the new yorker','vogue','ars technica','pitchfork'}
my_set2 = {'x','y','z',}
my_set.update(my_set2)
my_set.symmetric_difference_update(my_set2)

# 4. Dicts -  ordered (as of 3.7) and mutable
my_dict = {1:'epicurious',2:'the new yorker',3:'vogue',4:'ars technica',5:'pitchfork'}
my_dict[6] = 'wired'
my_dict = {k:v.upper() if 'or' in v else v for k,v in sorted(my_dict.items(), key=lambda key:key[1],reverse=True)}

# Results
print(my_list)
print(my_tuple)
print(my_set)
print(my_dict)

# 1. sort list, append item to list, extend list, if else comprehension, change element
# 2. return 'x' index, return number of elements
# 3. combine with new set, comparitive filtering with new set
# 4. add new dict element, sort by value, capitalize specific entries
