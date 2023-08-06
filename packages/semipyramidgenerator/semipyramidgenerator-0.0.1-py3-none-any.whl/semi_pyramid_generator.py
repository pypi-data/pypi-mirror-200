def make_normal_semi_pyramid(a):
    a += 1
    for i in range(1, a):
        print("*" * i)
def make_reversed_semi_pyramid(a):
    for i in range(a, 0, -1):
        print("*" * i)
make_reversed_semi_pyramid(3)