t = [[1, 2, 3],
     [1, 2, 3]];

#x = ones(3 * 1, 3);

#t = t * x;

print t[0];
print "";
print t[0, 0];
print "";
print t[0:2, 1];
print "";

t[1, 2] = 2137;
print t;
print "";
t[0:2, 0:2] = [[-1, -1], [-1, -1]];
print t;
print "";
t[1] = [1, 1, 1];
print t;
print "";
t[1, 0:2] = [-1, 2];
print t;
print "";

x = [1, 2, 3];
x[0] = 1;

alpha = "string my boi";
print alpha[0:5];
print alpha[0, 0];
print alpha[0];
print alpha[0, 0:5];

x = "string";
x[1:4] = "abc";
print x;