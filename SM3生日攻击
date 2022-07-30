import random
import time
from collections import Counter

IV = [0x7380166F, 0x4914B2B9, 0x172442D7, 0xDA8A0600,
      0xA96F30BC, 0x163138AA, 0xE38DEE4D, 0xB0FB0E4E]


def SM3(M):
    n = len(M)
    V = [IV]
    for i in range(n):
        V.append(compress(V, M, i))
    return V[n]


def FF(x, y, z, i):
    if i <= 15:
        return x ^ y ^ z
    else:
        return (x & y) | (x & z) | (y & z)


def GG(x, y, z, i):
    if 0 <= i <= 15:
        return x ^ y ^ z
    else:
        return (x & y) | (~x & z)


def zy(n, k):  # 循环左移k位,共32比特
    k = k % 32
    b = str(bin(n))
    b = b.split('0b')[1]
    b = (32 - len(b)) * '0' + b
    return int(b[k:] + b[:k], 2)


def P0(x):  # 置换函数1，式中x为字
    return x ^ (zy(x, 9)) ^ (zy(x, 17))


def P1(x):  # 置换函数2，式中x为字
    return x ^ (zy(x, 15)) ^ (zy(x, 23))


def T(i):
    if i < 16:
        T = int('0x79cc4519', 16)
    else:
        T = int('0x7a879d8a', 16)
    return T


def padding(message):
    m = bin(int(message, 16))[2:]
    if len(m) != len(message) * 4:
        m = '0' * (len(message) * 4 - len(m)) + m
    l = len(m)
    l_bin = '0' * (64 - len(bin(l)[2:])) + bin(l)[2:]
    m = m + '1'
    m = m + '0' * (448 - len(m) % 512) + l_bin
    m = hex(int(m, 2))[2:]
    return m


def group(m):
    n = len(m) / 128
    M = []
    for i in range(int(n)):
        M.append(m[0 + 128 * i:128 + 128 * i])
    return M


def extend(M, n):
    W = []
    W1 = []
    for j in range(16):
        W.append(int(M[n][0 + 8 * j:8 + 8 * j], 16))
    for j in range(16, 68):
        W.append(P1(W[j - 16] ^ W[j - 9] ^ zy(W[j - 3], 15)) ^ zy(W[j - 13], 7) ^ W[j - 6])
    for j in range(64):
        W1.append(W[j] ^ W[j + 4])
    s1 = ''
    s2 = ''
    for x in W:
        s1 += (hex(x)[2:] + ' ')
    for x in W1:
        s2 += (hex(x)[2:] + ' ')
    return W, W1


def compress(V, M, i):
    A, B, C, D, E, F, G, H = V[i]
    W, W1 = extend(M, i)
    for j in range(64):
        SS1 = zy((zy(A, 12) + E + zy(T(j), j % 32)) % (2 ** 32), 7)
        SS2 = SS1 ^ zy(A, 12)
        TT1 = (FF(A, B, C, j) + D + SS2 + W1[j]) % (2 ** 32)
        TT2 = (GG(E, F, G, j) + H + SS1 + W[j]) % (2 ** 32)
        D = C
        C = zy(B, 9)
        B = A
        A = TT1
        H = G
        G = zy(F, 19)
        F = E
        E = P0(TT2)

    a, b, c, d, e, f, g, h = V[i]
    V1 = [a ^ A, b ^ B, c ^ C, d ^ D, e ^ E, f ^ F, g ^ G, h ^ H]
    return V1


def random_number(n):
    z = []
    while len(z) < n:
        i = random.randint(0, 2 ** 64)
        if i not in z:
            z.append(i)
    return z


print("碰撞结果:")
start = time.time()
random_value = []
r = random_number(2 ** 16)
for i in range(2 ** 16):
    m = padding(str(r[i]))
    M = group(m)
    M_enc = SM3(M)
    tmp = ""
    for k in M_enc:
        tmp += hex(k)[2:]
    random_value.append(tmp[:7])
collision = dict(Counter(random_value))
for key, value in collision.items():
    if value > 1:
        print(key)
end = time.time()
print("所用时间为：", end - start, "s")
