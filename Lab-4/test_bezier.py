
from game import bezier

p0 = (0, 0)
p1 = (0, 100)
p2 = (100, 100)
p3 = (100, 0)

print("t=0:", bezier(p0, p1, p2, p3, 0))
print("t=1:", bezier(p0, p1, p2, p3, 1))
print("t=0.5:", bezier(p0, p1, p2, p3, 0.5))

assert bezier(p0, p1, p2, p3, 0) == (0, 0)
assert bezier(p0, p1, p2, p3, 1) == (100, 0)

x, y = bezier(p0, p1, p2, p3, 0.5)
assert abs(x - 50) < 1e-9
assert abs(y - 75) < 1e-9

print("All Bézier tests passed!")
