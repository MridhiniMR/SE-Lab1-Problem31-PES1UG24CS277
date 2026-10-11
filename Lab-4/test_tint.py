
from game import enemy_tint

assert enemy_tint("red") is None
assert enemy_tint("red", 1) is None
assert enemy_tint("red", 2) == (255, 140, 60)
assert enemy_tint("blue", 3) == (100, 100, 255)
assert enemy_tint("boss", 5) is None
assert enemy_tint("ghost", 2) is None

print("All enemy tint tests passed!")
