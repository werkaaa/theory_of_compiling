
x = 0;
y = zeros(5);
z = x + y;                  # error adding int and array        ## line 4

x = eye(5);
y = eye(8);
z = x .+ y;                 # error wrong dimensions            ## line 8

x = [ 1,2,3,4,5 ];
y = [ [1,2,3,4,5],
      [1,2,3,4,5] ];
z = x .+ y;                 # error wrong dimensions            ## line 13

x = zeros(5);
y = zeros(5,7);
z = x .+ y;                 # error wrong dimensions            ## line 17

x = ones(3,5);
z = x[7,10];                # error index out of range          ## line 20
v = x[2,3,4];               # error indices inconsistent with dims ## line 21
