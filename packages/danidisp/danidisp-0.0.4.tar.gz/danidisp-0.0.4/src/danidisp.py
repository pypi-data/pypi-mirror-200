def xor(a, b):
    return bytes([x^y for x,y in zip(a,b)])

def dlog(n: int, b: int, mod: int) -> int:
    i = 0
    while True:
        if b**i % mod == n % mod:
            return i
        i += 1
