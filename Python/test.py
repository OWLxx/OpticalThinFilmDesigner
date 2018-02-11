import collections
G = ['101010', '100100', '000001']
G = [int(i, 2) for i in G]
C = [0, G[0], G[1], G[2], G[0]^G[1], G[0]^G[2], G[1]^G[2], G[0]^G[1]^G[2]]
ans = []
for i in range(64):
    dif = 8
    for num in C:
        temp = i^num
        count = 0
        while temp:
            count += temp&1
            temp >>= 1
        dif = min(dif, count)
    ans.append(dif)
print(ans)
print(collections.Counter(ans))