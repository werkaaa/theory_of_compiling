d = [[1, 2], [2, 1]];
f = zeros(1, 2);
e = ones(2, 2);
g = eye(2);
h = d*g;
print d, e;
print f;
print e;
print h;

for i = 1:10 {
    print i;
    print i;
    break;
}