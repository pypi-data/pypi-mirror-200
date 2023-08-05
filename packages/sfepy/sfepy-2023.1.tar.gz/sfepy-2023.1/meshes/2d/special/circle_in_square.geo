a = 1;
r = 0.6;
out = 0.2;
in = 0.08;
Point(1) = {-a,-a,0, out};
Point(2) = {-a,a,0, out};
Point(3) = {a, a,0, out};
Point(4) = {a,-a,0, out};
Point(5) = {0, 0, 0, in};
Point(6) = {r, 0, 0, in};
Point(7) = {0, r, 0, in};
Point(8) = {-r, 0, 0, in};
Point(9) = {0, -r, 0, in};
Line(1) = {1,4};
Line(2) = {4,3};
Line(3) = {3,2};
Line(4) = {2,1};
Circle(5) = {6,5,7};
Circle(6) = {7,5,8};
Circle(7) = {8,5,9};
Circle(8) = {9,5,6};
Line Loop(5) = {2,3,4,1};
Line Loop(50) = {5,6,7,8};
Plane Surface(1) = {5,50};
Plane Surface(2) = {50};
Physical Surface(1) = {1};
Physical Surface(2) = {2};
