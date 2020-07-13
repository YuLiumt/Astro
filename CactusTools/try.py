import re

# class parfile:
#     def __init__(self):
#         self._dict = {}

#     def __setitem__(self, key, value):
#         self._dict[key] = value
#         # print(key, value)

# p = parfile()
# p['a'] = 'b'
# print(p._dict)
it=768
rl=6
pattern = "(\S*)::(\S*) it={} tl=(\d*) rl={} c=(\d*)\S*".format(it, rl)
x = re.search(pattern, 'ADMBASE::alp it=768 tl=0 rl=6 c=9')
print(x)
