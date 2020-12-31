a = 2;
b = a;
c = a+"4";              # error INT + STRING        ## line 3
print "ala", 2+2, d;    # error d undeclared        ## line 4
c = a + "ala" + 3 + 2;  # error INT + STRING        ## line 5
w = (2+2)';             # error transpose of INT    ## line 6
t = [[2, 2],
    [3, 1]];

n = eye(3) .+ t;        # error wrong dimensions    ## line 10
v = n;
m = n + 2;              # error adding num and array ## line 12
d = 2;
for b = 1:4{            # error iterating var already declared ## line 14
 if (0 < 2){
 break;
 }
 i = 1;
 d = 3;
}
print i;                 # error var not declared in scope ## line 21
print d;
