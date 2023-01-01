with open("inputs/25.txt", "r") as f:
    data = [a for a in f.read().split("\n") if a!=""]

def snafu_to_int_ls(s):
    return [{"=":-2, "-":-1, "0":0, "1":1, "2":2}[s[-i]] for i in range(1,len(s)+1)]

def ls_to_int(ls, base=5):
    num = 0
    mult = 1
    for i in range(len(ls)):
        num += ls[i]*mult
        mult *= base
    return num

def int_to_snafu_ls(num, base=5):
    ls = []
    rest = num
    while rest>0:
        current = rest % base
        ls.append([0,1,2,-2,-1][current])
        rest = rest // base
        if current>2:
            rest += 1
    return ls

def ls_to_str(ls):
    return "".join(["=-012"[ls[-i]+2] for i in range(1,len(ls)+1)])

print(f"1) {ls_to_str(int_to_snafu_ls(sum([ls_to_int(snafu_to_int_ls(o)) for o in data])))}")
print(f"2) ( •̀ ω •́ )✧")