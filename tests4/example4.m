k = [1, 2, 3, 4];
dudu = [[1, 2],
        [3, 4]];
aaaaaa = [["string", 1]];   # error string and int in array         ## line 4
g = 11;
j = "XDDD";
a = g[1];                   # error subscripted not an array        ## line 7
a = j[1 ,2];                # error wrong string subscript          ## line 8
a = dudu;
a = "taktak"[3:4];
a = dudu[1:1, 2:3];         # error indices out of range and one dim is 0 ## line 11
a = k[1];
a = k[1, 1];                # error index out of range              ## line 13
a = k[1:2];
