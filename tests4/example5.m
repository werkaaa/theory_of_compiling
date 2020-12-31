t = "To jest długie zdanie.";
a = [1, 2, 3];

a[0] = 1;
a[1:2] = 1;             
a[1:2] = [1, 2];        # error a[1:2] is just element a[1]             ## line 6
a[0] = [1, 2];          # error cannot do this here - that's too bad    ## line 7
