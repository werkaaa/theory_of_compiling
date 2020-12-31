a = 1;
a += 1;
a += "jabba";                   # error int += str      ## line 3
a += [1, 2, 3];                 # error int += arr      ## line 4
a += [[1, 2], [3, 4]];          # error int += arr      ## line 5
a = [1, 2, 3];
a += 1;                         # error arr += int      ## line 7
a += [1, 2, 3];                 # error arr += arr      ## line 8
a += [[1, 2, 3],                # error arr += arr      ## line 9
      [1, 2, 3]];
a += "jabba";                   # error arr += str      ## line 11
a = "jabba";
a += 1;                         # error str += int      ## line 13
a = "jabba";
a += [1, 2, 3];                 # error str += arr      ## line 15
a = "jabba";
a += [[1, 2, 3],                # error str += arr      ## line 17
      [1, 2, 3]];
a = "jabba";
a += "jabba";
