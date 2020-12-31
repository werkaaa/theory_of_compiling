a = "jabba";
b = "abbaj";
a -= b;             # error op not sup  ## line 3
a *= b;             # error op not sup  ## line 4
a /= b;             # error op not sup  ## line 5
a -= "a";           # error op not sup  ## line 6
a *= "jaj";         # error op not sup  ## line 7
a += b;
