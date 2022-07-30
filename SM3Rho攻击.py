import random
import time

IV = [0x7380166F, 0x4914B2B9, 0x172442D7, 0xDA8A0600, 0xA96F30BC, 0x163138AA, 0xE38DEE4D, 0xB0FB0E4E]
T = [0x79cc4519, 0x7a879d8a]


def Iterate(M):
    n = len(M)
    V = [IV]
    for i in range(n):
        V.append(compress(V, M, i))
    return V[n]


def FF(x, y, z, j):  # 布尔函数1，式中X,Y,Z 为字。
    if j <= 15:
        return x ^ y ^ z
    else:
        return (x & y) | (y & z) | (x & z)


def GG(x, y, z, j):  # 布尔函数2，式中X,Y,Z 为字。
    if j <= 15:
        return x ^ y ^ z
    else:
        return (x & y) | (~x & z)


def zy(n, k):  # 循环左移k位,共32比特
    k = k % 32
    b = str(bin(n))
    b = b.split('0b')[1]
    b = (32 - len(b)) * '0' + b
    return int(b[k:] + b[:k], 2)


def P0(X):
    return X ^ zy(X, 9) ^ zy(X, 17)


def P1(X):
    return X ^ zy(X, 15) ^ zy(X, 23)


def T_(j):
    if j <= 15:
        return T[0]
    else:
        return T[1]


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


def Group(m):
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
    W, W_ = extend(M, i)
    for j in range(64):
        SS1 = zy((zy(A, 12) + E + zy(T_(j), j % 32)) % (2 ** 32), 7)
        SS2 = SS1 ^ zy(A, 12)
        TT1 = (FF(A, B, C, j) + D + SS2 + W_[j]) % (2 ** 32)
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
    V_ = [a ^ A, b ^ B, c ^ C, d ^ D, e ^ E, f ^ F, g ^ G, h ^ H]
    return V_


def enc(mes):
    m = padding(mes)
    M = Group(m)
    Vn = Iterate(M)
    result = ''
    for x in Vn:
        result += (hex(x)[2:] + ' ')
    return result


def rho_attack(text):
    start = time.time()
    message = str(random.randint(0, 2 ** 2048))
    message1 = message
    a = []
    for i in range(0, 2 ** 128):
        a.append((enc(message))[:int(text)])
        message = str(2 * int(message) + 1)
        if enc(message)[:int(text)] in a:
            print("success")
            b = a.index((enc(message))[:int(text)])
            # print("当前消息为:", message)
            print("当前消息hash值为:", enc(message))
            end = time.time()
            for j in range(0, b):
                message1 = str(2 * int(message1) + 1)
            # print("碰撞消息为:", message1)
            print("碰撞消息散列值为:", enc(message1))
            print("碰撞比特位数:", 4 * text, "所用时间为：", end - start, "s")
            break


n = int(input("请输入长度："))
rho_attack(n)
