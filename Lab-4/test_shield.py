
from game import shield_charges

for wave in range(1, 10):
    expected = 1 if wave % 3 == 0 else None
    actual = shield_charges(wave)

    print(f"Wave {wave}: {actual}")
    assert actual == expected

print("All shield tests passed!")
