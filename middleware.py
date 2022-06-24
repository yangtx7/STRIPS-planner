import stru
import main
lst = 0
def assign():
    lst = 0
    stru.mk1 = [0 for i in range(len(stru.pred))]                       
    for nw in stru.act:
        for cu in nw.prec: # type of cu is predi
            if stru.mk1[cu.id] == 1:
                continue
            stru.mk1[cu.id] = 1
            stru.argc.append([])
            tmp = 1
            for i in range(len(cu.arg)):
                stru.argc[-1].append(nw.par2[cu.arg[i]])
                tmp *= stru.cnt[nw.par2[cu.arg[i]]]
            stru.st.append(lst)
            lst += tmp
    print("pred name :", stru.pred)
    print(stru.argc)
    print(stru.st)
    for nw in stru.feat:
        stru.sta.add(convert2(nw.id, nw.arg))
        print(convert2(nw.id, nw.arg))
    print(stru.sta)
def convert(a, b):
    ret = a[0]
    for i in range(1, len(b)):
        ret = ret * b[i-1] + a[i]
    return ret
def convert2(id, a):
    tmp = []
    tmp2 = []
    for i in a:
        tmp.append(stru.var3[i])
        tmp2.append(stru.cnt[stru.var2[i]])
    return stru.st[id]+convert(tmp, tmp2)
def check(id, a):
    if main.debug_2 == 1:
        print("Checking ", stru.act[id].nam, end='')
        for it in a:
            print(stru.vari[a],' ', sep='', end='')
            print(' ')
    for it in stru.act[id].prec:
        tmp = []
        for i in it.arg:
            tmp.append(a[i])
            
