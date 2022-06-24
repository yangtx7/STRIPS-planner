import re
import time
import stru
from main import debug_
st = 0
cur = 0
def pristat():
    print("--------------Stat Output--------------")
    print("---------------------------------------")
def pristat2(y):
    global debug_
    global cur
    global st
    if debug_ == 1:
        print(">>> State changed:", st, "->", y, " cur=", cur, sep='')
    st = y
def load_domain(path):
    global debug_
    f = open(path, 'r')
    ff = f.readlines()
    f.close()
    tex = " "
    for i in range(len(ff)):
        if ff[i][len(ff[i]) - 1] == '\n':
            tex = tex + ff[i][:-1]
        else:
            tex = tex + ff[i]
    mrk = [0 for i in range(11)]
    print("-----------------------Domain file analysis start-----------------------")
    while 1:
        global st
        global cur
        if st == 0:
            if mrk[0] == 0:
                tmp = re.search(r'[(]', tex[cur:]).span()
                cur += tmp[1]
                mrk[0] = 1
                pristat2(1)
            else:
                tmp = re.search(r'[)]', tex[cur:]).span()
                cur += tmp[1]
                if cur == len(tex):
                    print("Domain-file analyzed successfully.")
                else:
                    print("Error!")
                    pristat()
                print("------------------------Domain file analysis end------------------------")
                break
            continue
        if st == 1:
            if mrk[1] == 0:
                mrk[1] = 1
                pristat2(2)
            else:
                tmp = re.search(r'[(]', tex[cur:])
                if tmp:
                    cur += tmp.span()[1]
                    tmp = re.search(r':', tex[cur:]).span()
                    cur += tmp[1]
                    tmp = re.search(r'[a-z]+', tex[cur:]).span()
                    if tex[cur+tmp[0]:cur+tmp[1]] == "requirements":
                        cur += tmp[1]
                        pristat2(3)
                        continue
                    if tex[cur+tmp[0]:cur+tmp[1]] == "types":
                        cur += tmp[1]
                        pristat2(4)
                        continue
                    if tex[cur+tmp[0]:cur+tmp[1]] == "action":
                        cur += tmp[1]
                        mrk[5] = 0
                        pristat2(5)
                        continue
                else:
                    pristat2(0)
            continue
        if st == 2:
            tmp = re.search(r'domain', tex[cur:]).span()
            cur += tmp[1]
            tmp = re.search(r'[^\s)]+', tex[cur:]).span()
            if debug_ >= 1:
                print(">>>      domain name :", tex[cur+tmp[0]:cur+tmp[1]])
            cur += tmp[1]
            tmp = re.search(r'[)]', tex[cur:]).span()
            cur += tmp[1]
            pristat2(1)
            continue
        if st == 3:
            tmp = re.search(r'[)]', tex[cur:]).span()
            if debug_ >= 1:
                print(">>>      requirement :", tex[cur:cur+tmp[0]])
            cur += tmp[1]
            pristat2(1)
            continue 
        if st == 4:
            tmp = re.search(r'[a-z0-9]+', tex[cur:]).span()
            tmp2 = re.search(r'[)]', tex[cur:]).span()
            while tmp[0] < tmp2[0]:
                stru.typ.append(tex[cur+tmp[0]:cur+tmp[1]])
                cur += tmp[1]
                tmp = re.search(r'[a-z0-9]+', tex[cur:]).span()
                tmp2 = re.search(r'[)]', tex[cur:]).span()
            cur += tmp2[1]
            if debug_ >= 1:
                print(">>>      types :", stru.typ)
            pristat2(1)
            continue
        if st == 5:
            if mrk[5] == 0:
                tmp = re.search(r'[\-a-z]+', tex[cur:]).span()
                stru.act.append(stru.action(tex[cur+tmp[0]:cur+tmp[1]]))
                if debug_ >= 1:
                    print(">>>      action", len(stru.act), "name =", tex[cur+tmp[0]:cur+tmp[1]])
                cur += tmp[1]
                mrk[5] = 1
            else:
                tmp2 = re.search(r'[:]', tex[cur:])
                tmp3 = re.search(r'[)]', tex[cur:])
                if tmp2 and tmp2.span()[0] < tmp3.span()[0]:
                    cur += tmp2.span()[1]
                    tmp = re.search(r'[a-z]+', tex[cur:]).span()
                    if tex[cur+tmp[0]:cur+tmp[1]] == "parameters":
                        cur += tmp[1]
                        pristat2(6)
                        continue
                    if tex[cur+tmp[0]:cur+tmp[1]] == "precondition":
                        cur += tmp[1]
                        pristat2(7)
                        continue
                    if tex[cur+tmp[0]:cur+tmp[1]] == "effect":
                        cur += tmp[1]
                        pristat2(8)
                        continue
                else:
                    cur += tmp3.span()[1]
                    pristat2(1)
                    continue
        if st == 6:
            tmp2 = re.search(r'[0-9a-z]+', tex[cur:])
            tmp3 = re.search(r'[)]', tex[cur:])
            while tmp2 and tmp2.span()[0] < tmp3.span()[0]:
                stru.act[-1].par1.append(tex[cur+tmp2.span()[0]:cur+tmp2.span()[1]])
                cur += tmp2.span()[1]
                tmp = re.search(r'[a-z]+', tex[cur:]).span()
                for i in range(len(stru.typ)):
                    if tex[cur+tmp[0]:cur+tmp[1]] == stru.typ[i]:
                        stru.act[-1].par2.append(i)
                        break
                cur += tmp[1]
                tmp2 = re.search(r'[0-9a-z]+', tex[cur:])
                tmp3 = re.search(r'[)]', tex[cur:])
            cur += tmp3.span()[1]
            if debug_ >= 1:
                print(">>>      para", stru.act[-1].par1)
                print(">>>      para", stru.act[-1].par2)
            pristat2(5)
            continue   
        if st == 7 or st == 8:
            # print("test:", tex[cur:cur+20])
            if mrk[st] == 0:
                tmp = re.search(r'\(and', tex[cur:]).span()
                cur += tmp[1]
                mrk[st] = 1
            tmp2 = re.search(r'[(]', tex[cur:])
            tmp3 = re.search(r'[)]', tex[cur:])
            if tmp2 and tmp2.span()[0] < tmp3.span()[0]:
                cur += tmp2.span()[1]
                mrk[9] = st
                pristat2(9)
                continue
            else:
                if debug_ >= 1:
                    print(">>>      predicates :", stru.pred)
                    if st == 7:
                        for i in range(len(stru.act[-1].prec)):
                            print(">>>      prec : no =", i, "id =", stru.act[-1].prec[i].id, "neg =", stru.act[-1].prec[i].neg, "arg =", stru.act[-1].prec[i].arg)
                    else:
                        for i in range(len(stru.act[-1].eff)):
                            print(">>>      prec : no =", i, "id =", stru.act[-1].eff[i].id, "neg =", stru.act[-1].eff[i].neg, "arg =", stru.act[-1].eff[i].arg)
                cur += tmp3.span()[1]
                mrk[st] = 0
                pristat2(5)
                continue
        if st == 9:
            neg = 0
            tmp2 = re.search(r'[\-a-z]+', tex[cur:])
            tmp3 = re.search(r'not', tex[cur:])
            if tmp3 and tmp3.span()[0] <= tmp2.span()[0]:
                cur += tmp3.span()[1]
                tmp2 = re.search(r'[\-a-z]+', tex[cur:])
                neg = 1
            fnd = 0
            for i in range(len(stru.pred)):
                if tex[cur+tmp2.span()[0]:cur+tmp2.span()[1]] == stru.pred[i]:
                    fnd = 1
                    id = i
                    break
            if fnd == 0:
                stru.pred.append(tex[cur+tmp2.span()[0]:cur+tmp2.span()[1]])
                id = len(stru.pred) - 1
            if mrk[9] == 7:
                stru.act[-1].prec.append(stru.predi(id, neg))
            else:
                stru.act[-1].eff.append(stru.predi(id, neg))
            
            cur += tmp2.span()[1]
            tmp2 = re.search(r'[0-9a-z]+', tex[cur:])
            tmp3 = re.search(r'\)', tex[cur:])
            while tmp2 and tmp2.span()[0] < tmp3.span()[0]:
                for i in range(len(stru.act[-1].par1)):
                    if tex[cur+tmp2.span()[0]:cur+tmp2.span()[1]] == stru.act[-1].par1[i]:
                        id2 = i
                        break
                if mrk[9] == 7:
                    stru.act[-1].prec[-1].arg.append(id2)
                else:
                    stru.act[-1].eff[-1].arg.append(id2)
                cur += tmp2.span()[1]
                tmp2 = re.search(r'[0-9a-z]+', tex[cur:])
                tmp3 = re.search(r'\)', tex[cur:])
            cur += tmp3.span()[1]
            if neg == 1:
                tmp3 = re.search(r'\)', tex[cur:])
                cur += tmp3.span()[1]
            pristat2(mrk[9])
            continue


def load_prob(path):
    global st
    global cur
    stru.cnt = [0 for i in range(len(stru.typ))]
    f = open(path, 'r')
    ff = f.readlines()
    f.close()
    tex = ""
    for i in range(len(ff)):
        if ff[i][len(ff[i]) - 1] == '\n':
            tex = tex + ff[i][:-1]
        else:
            tex = tex + ff[i]
    mrk = [0 for i in range(10)]
    cur = 0
    print("----------------------Problem file analysis start-----------------------")
    while 1:
        if st == 0:
            if mrk[0] == 0:
                tmp = re.search(r'\(', tex[cur:]).span()
                cur += tmp[1]
                mrk[0] = 1
                pristat2(1)
            else:
                tmp = re.search(r'\)', tex[cur:]).span()
                cur += tmp[1]
                if cur == len(tex):
                    print("Problem-file analyze completed.")
                else:
                    print("Error!")
                    pristat()
                print("-----------------------Problem file analysis end------------------------")
                break
            continue
        if st == 1:
            if mrk[1] == 0:
                mrk[1] = 1
                pristat2(2)
            else:
                tmp = re.search(r'[(]', tex[cur:])
                if tmp:
                    cur += tmp.span()[1]
                    tmp = re.search(r':', tex[cur:]).span()
                    cur += tmp[1]
                    tmp = re.search(r'[a-z]+', tex[cur:]).span()
                    if tex[cur+tmp[0]:cur+tmp[1]] == "domain":
                        cur += tmp[1]
                        pristat2(3)
                        continue
                    if tex[cur+tmp[0]:cur+tmp[1]] == "objects":
                        cur += tmp[1]
                        pristat2(4)
                        continue
                    if tex[cur+tmp[0]:cur+tmp[1]] == "init":
                        cur += tmp[1]
                        pristat2(6)
                        continue
                    if tex[cur+tmp[0]:cur+tmp[1]] == "goal":
                        cur += tmp[1]
                        pristat2(8)
                        continue
                else:
                    pristat2(0)
            continue
        if st == 2:
            tmp = re.search(r'problem', tex[cur:]).span()
            cur += tmp[1]
            tmp = re.search(r'[^\s)]+', tex[cur:]).span()
            if debug_ >= 1:
                print(">>>      problem name :", tex[cur+tmp[0]:cur+tmp[1]])
            cur += tmp[1]
            tmp = re.search(r'[)]', tex[cur:]).span()
            cur += tmp[1]
            pristat2(1)
            continue
        if st == 3:
            tmp = re.search(r'[\-a-z]+', tex[cur:]).span()
            if debug_ >= 1:
                print(">>>      domain name :", tex[cur+tmp[0]:cur+tmp[1]])
            cur += tmp[1]
            tmp = re.search(r'[)]', tex[cur:]).span()
            cur += tmp[1]
            pristat2(1)
            continue
        if st == 4:
            tmp2 = re.search(r'[0-9a-z]+', tex[cur:])
            tmp3 = re.search(r'\)', tex[cur:])
            if tmp2 and tmp2.span()[0] < tmp3.span()[0]:
                pristat2(5)
                continue
            else:
                cur += tmp3.span()[1]
                if debug_ >= 1:
                    print(">>>      variables :", stru.vari)
                    print(">>>      variables :", stru.var2)
                    print(">>>      variables :", stru.var3)
                pristat2(1)
                continue
        if st == 5:
            tmp2 = re.search(r'[0-9a-z]+', tex[cur:]).span()
            tmp3 = re.search(r'\-', tex[cur:]).span()
            lst = len(stru.vari)
            while tmp2[0] < tmp3[0]:
                stru.vari.append(tex[cur+tmp2[0]:cur+tmp2[1]])
                cur += tmp2[1]
                tmp2 = re.search(r'[0-9a-z]+', tex[cur:]).span()
                tmp3 = re.search(r'\-', tex[cur:]).span()
            tmp = re.search(r'[0-9a-z]+', tex[cur:]).span()
            wrd = tex[cur+tmp[0]:cur+tmp[1]]
            for i in range(len(stru.typ)):
                if stru.typ[i] == wrd:
                    id = i
                    break
            for i in range(lst, len(stru.vari)):
                stru.var3.append(stru.cnt[id])
                stru.cnt[id] += 1
                stru.var2.append(id)
            cur += tmp[1]
            pristat2(4)
            continue
        if st == 6:
            tmp2 = re.search(r'\(', tex[cur:])
            tmp3 = re.search(r'\)', tex[cur:])
            if tmp2 and tmp2.span()[0] < tmp3.span()[0]:
                mrk[7] = 6
                pristat2(7)
                continue
            else:
                if debug_ >= 1:
                    print(">>>      init :", stru.pred)
                    print(">>>      init :", stru.vari)
                    for i in range(len(stru.feat)):
                        print(">>>      init :", stru.feat[i].id, stru.feat[i].arg) 
                cur += tmp3.span()[1]
                pristat2(1)
                continue
        if st == 7:
            tmp = re.search(r'[\-a-z]+', tex[cur:]).span()
            wrd = tex[cur+tmp[0]:cur+tmp[1]]
            for i in range(len(stru.pred)):
                if stru.pred[i] == wrd:
                    id = i
                    break
            if mrk[7] == 6:
                stru.feat.append(stru.predi(id, 0))
            else:
                stru.goal.append(stru.predi(id, 0))
            cur += tmp[1]
            tmp2 = re.search(r'[0-9a-z]+', tex[cur:])
            tmp3 = re.search(r'\)', tex[cur:])
            while tmp2 and tmp2.span()[0] < tmp3.span()[0]:
                wrd = tex[cur+tmp2.span()[0]:cur+tmp2.span()[1]]
                for i in range(len(stru.vari)):
                    if stru.vari[i] == wrd:
                        id = i
                        break
                if mrk[7] == 6:
                    stru.feat[-1].arg.append(id)
                else:
                    stru.goal[-1].arg.append(id)
                cur += tmp2.span()[1]
                tmp2 = re.search(r'[0-9a-z]+', tex[cur:])
                tmp3 = re.search(r'\)', tex[cur:])
            cur += tmp3.span()[1]
            pristat2(mrk[7])
            continue
        if st == 8:
            if mrk[8] == 0:
                tmp = re.search(r'\(and', tex[cur:]).span()
                cur += tmp[1]
                mrk[8] = 1
            tmp2 = re.search(r'[\-0-9a-z]+', tex[cur:])
            tmp3 = re.search(r'\)', tex[cur:])
            if tmp2 and tmp2.span()[0] < tmp3.span()[0]:
                mrk[7] = 8
                pristat2(7)
                continue
            else:
                tmp = re.search(r'\)', tex[cur:]).span()
                cur += tmp[1]
                tmp = re.search(r'\)', tex[cur:]).span()
                cur += tmp[1]
                if debug_ >= 1:
                    print(">>>      goal :", stru.pred)
                    print(">>>      goal :", stru.vari)
                    for i in range(len(stru.goal)):
                        print(">>>      init :", stru.goal[i].id, stru.goal[i].arg)
                pristat2(1)
                continue