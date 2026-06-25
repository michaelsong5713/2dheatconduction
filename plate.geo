// Rectangular plate geometry for heat_ex.py.
// Physical group IDs must match the tag constants defined there.

lc = 0.025;
L  = 1.0;
H  = 0.5;

Point(1) = {0, 0, 0, lc};
Point(2) = {L, 0, 0, lc};
Point(3) = {L, H, 0, lc};
Point(4) = {0, H, 0, lc};

Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};

Curve Loop(1) = {1, 2, 3, 4};
Plane Surface(1) = {1};

Physical Surface("domain", 1) = {1};
Physical Curve("left",   2)   = {4};
Physical Curve("right",  3)   = {2};
Physical Curve("top",    4)   = {3};
Physical Curve("bottom", 5)   = {1};
