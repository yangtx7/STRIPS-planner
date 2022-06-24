import copy
import re
import time

###----------------------------------------------------------------------###
###-------------------------------initial--------------------------------###
""" items """
requirements=[]
types=[]
actions={}
""" items """
objects={}
init=[]
goal=[]

def initial():
    global requirements
    global types
    global actions
    global objects
    global init
    global goal

    file_cont=[]
    print("input the testcase number:")
    test_num=input()
    domain_filename=".\\pddl\\test"+str(test_num)+"\\test"+str(test_num)+"_domain.txt"
    problem_filename=".\\pddl\\test"+str(test_num)+"\\test"+str(test_num)+"_problem.txt"

    #----------------------------------input domain file
    with open(domain_filename) as fp:
        file_cont=fp.read()
    index1=file_cont.find("domain")
    index2=0
    for i in range(index1,len(file_cont)):
        if file_cont[i]==')':
            index2=i
            break
    domain_name=file_cont[index1+7:index2]

    for latter in range(index2,len(file_cont)):
        if file_cont[latter] == ":":
            if file_cont[latter:].find("requirements") >= 0:
                for i in range(latter+len("requirements "),len(file_cont)):
                    if file_cont[i] == ":":
                        out=0
                        if file_cont[i:].find(" ") < file_cont[i:].find(")"):
                            end=file_cont[i:].find(" ")
                        else:
                            end=file_cont[i:].find(")")
                            out=1
                        require=file_cont[i+1:i+end]
                        requirements.append(require)
                        if out:
                            break

            elif file_cont[latter:].find("types") >= 0:
                end=file_cont[latter:].find(")")
                types=file_cont[latter+7:latter+end].split(" ")

    action_list=file_cont.split(":action")
    action_list.pop(0)

    for string in action_list:
        name=string[1:].split()[0]
        dic={}
        ###parameters
        start=string.find(":parameters")
        end=string[start:].find(")")+start
        start+=string[start:].find("(")
        result=string[start+1:end].split("?")
        result.pop(0)
        para_list=[]
        for sub_str in result:
            sub_str="".join(sub_str.split())
            para_list.append(sub_str.split("-"))
        dic["parameters"]=para_list
        
        ###precondition
        start=string.find(":precondition")
        end=0
        tag=0
        for i in range(start+string[start:].find("("),len(string)):
            if string[i]=="(":
                tag+=1
            elif string[i]==")":
                tag-=1
            if tag==0:
                end=i
                break
        start+=string[start:].find("and")
        
        pre_list=[]
        stack=[]
        for k in range(start,end):
            if string[k]=="(":
                stack.append(k+1)
            if string[k]==")":
                if not len(stack):
                    break
                Begin=stack.pop()
                item=string[Begin:k].replace("?", "").split()
                if item[0]=="not":
                    pre_list[-1][1]=0
                else:
                    pre_list.append([item,1])
        dic["precondition"]=pre_list
        
        ###effect                          
        start=string.find(":effect")
        end=0
        tag=0
        for i in range(start+string[start:].find("("),len(string)):
            if string[i]=="(":
                tag+=1
            elif string[i]==")":
                tag-=1
            if tag==0:
                end=i
                break
        start+=string[start:].find("and")
        
        effect_list=[]
        stack=[]
        for k in range(start,end):
            if string[k]=="(":
                stack.append(k+1)
            if string[k]==")":
                if not len(stack):
                    break
                Begin=stack.pop()
                item=string[Begin:k].replace("?", "").split()
                if item[0]=="not":
                    effect_list[-1][1]=0
                else:
                    effect_list.append([item,1])
        dic["effect"]=effect_list
                            
        actions[name]=dic

    #----------------------------------input problem file
    with open(problem_filename) as fp:
        file_cont=fp.read()
    #print(file_cont)
    index1=file_cont.find("problem")
    index2=file_cont[index1:].find(")")+index1
    problem_name=file_cont[index1+8:index2]

    index1=file_cont.find("domain")
    index2=file_cont[index1:].find(")")+index1

    ###objects
    start=file_cont.find(":objects")
    end=start+file_cont[start:].find(")")
    new_content=file_cont[start+8:end]
    new_content=new_content.replace(" - ", "-")
    begin=0
    for i in range(0,len(new_content)):
        if new_content[i]=="-":
            obj_list=new_content[begin:i].split()
            record=0
            for k in range(i+1,len(new_content)):
                if not new_content[k].isdigit() and not new_content[k].isalpha():
                    record=k
                    break
            obj_name=new_content[i+1:record]
            begin=record
            objects[obj_name]=obj_list
    for item in objects:
        if item not in types:
            print("error: no matching type found")
            break

    ###init
    start=file_cont.find(":init")
    end=0
    tag=0
    for i in range(start, len(file_cont)):
        if file_cont[i]=='(':
            tag+=1
        elif file_cont[i]==')':
            tag-=1
        if tag==-1:
            end=i
            break
    start+=5
    new_content=file_cont[start:end]
    pattern = re.compile(r'[(](.*?)[)]', re.S)  
    result=pattern.findall(new_content)
    for val in result:
        init.append([val.split(),1])


    ###goal
    start=file_cont.find(":goal")
    end=0
    tag=0
    for i in range(start+file_cont[start:].find("("),len(file_cont)):
        if file_cont[i]=="(":
            tag+=1
        elif file_cont[i]==")":
            tag-=1
        if tag==0:
            end=i
            break
    start+=file_cont[start:].find("and")

    goal=[]
    stack=[]
    for k in range(start,end):
        if file_cont[k]=="(":
            stack.append(k+1)
        if file_cont[k]==")":
            if not len(stack):
                break
            Begin=stack.pop()
            item=file_cont[Begin:k].split()
            if item[0]=="not":
                goal[-1][1]=0
            else:
                goal.append([item,1])

    print("domain:",domain_name) # 打印domain信息
    print("requirements:")
    print(requirements)
    print("types:")
    print(types)
    print("actions:")
    for i in actions:
        print(i)
        for k in actions[i]:
            print("  ",k)
            print("  ",actions[i][k])
    if not len(requirements):
        print("error:domain file")
    elif "typing" not in requirements and not len(types):
        print("error:domain file")

    print("\n")
    
    if domain_name != file_cont[index1+7:index2]:
        print("error:No matching input file found")
    print("problem:",problem_name) # 打印problem信息
    print("objects:")
    for i in objects:
        print("  ",i,":")
        print("  ",objects[i])
    print("init:")
    for i in init:
        print(i)
    print("goal:")
    for i in goal:
        print(i)
        

###----------------------------------------------------------------------###
###---------------------------heuristic function-------------------------###


###----------------------------------------------------------------------###
###------------------------------aid functions---------------------------###
def assign(param=[],objects=[]):
    """获取所有可能的赋值方式"""
    """
    输入
        对象集合
        npc - player
        town field castle - location
        参数集合
        ?p - player ?l1 - location ?l2 - location
    输出
        赋值方式有 1*3*3=9 种，因为p, l1, l2分别有1, 3, 3种取法（PS: 如果认为l1和l2不能相同的话则是1*3*2种）
        [p:npc, l1:town, l2:town, ..., p:npc, l1:field, l2:field]
    """
    pass
    
def get_pre_ofAct(precon=[],assign=[]):
    """输入赋值返回precondition，就是把precondition里面的参数实例化"""
    """
    输入
        assign = ["p":"npc", "l1": "town", "l2", "field"]
        precondition = (and (at ?p ?l1) (border ?l1 ?l2) (not (guarded ?l2)))
        可以实例化为
        at npc town
        border town field
        not guarded field
    输出
        current_condition = [at npc town, border town field, not guarded field]
    """
    pass

def is_action_valid(current_condition=[],state=[]):
    """输入当前状态，返回current_condition是否满足"""
    """
    输入
        current_condition = [at npc town, border town field, not guarded field]
        state = [border town field, border field castle, at npc town]
    输出
        判断
        at npc town 在state当中
        border town field 在state当中
        guarded field 不在state当中
        则move可以被触发，返回True，否则返回False
        此处返回True
    """
    pass

def get_eff_ofAct(effect=[],assign=[]):
    """输入赋值返回effect，就是把effect里面的参数实例化"""
    """
    输入
        assign = ["p":"npc", "l1": "town", "l2", "field"]
        effect = (and (at ?p ?l2) (not (at ?p ?l1)))
        可以实例化为
        at npc field
        not at npc town
    输出
        effect = [at npc field, not at npc town]
    """
    pass

def get_next_state(current_effect=[],state=[]):
    """输入动作结束后产生的效果，返回该效果作用后的下一状态"""
    """
    输入
        effect = [at npc field, not at npc town]
        state = [border town field, border field castle, at npc town]
    输出
        判断
        正原子at npc field是否在state当中
            如果不在，则添加这条到state
            如果以“not at npc field”的形式存在于state中，则删去state中的“not at npc field”
        负原子not at npc town是否在state当中
            如果不再，则添加到state中
            如果以“at npc town”的形式存在于state中，则删去state中的“at npc town”
        next_state = [border town field, border field castle, at npc field]
    """
    return next_state
    
def is_reach_goal(state=[], goal=[]):
    """state需要满足goal中的所有条件，就是说goal是state的子集，则返回True"""
    """
    输入
        state = [border town field, border field castle, at npc town]
        goal = [at npc castle]
    返回
        判断goal是否是state的子集
        这里[at npc castle]不是state的子集，返回False
    """
    pass

###----------------------------------------------------------------------###
###----------------------------search function---------------------------###
def Astar():
    global actions
    global objects
    global init
    global goal
    
    from queue import PriorityQueue
    openlist = PriorityQueue()
    closelist = []
    # 这里写你的规划算法
    
initial()
time_start=time.time()
Astar()
time_end=time.time()
print('time used:', time_end-time_start, 'seconds')


# 可以访问https://stripsfiddle.herokuapp.com/，粘贴pddl的problem和domain文件，得到答案，与你自己的答案进行对比
# 如果对这个作业来源感兴趣，可以参考http://www.primaryobjects.com/2015/11/06/artificial-intelligence-planning-with-strips-a-gentle-introduction/


# 不做任何修改直接运行文件，可以得到如下解析结果：
###----------------------------------------------------------------------###
###--------------------------------case 0--------------------------------###
# domain: magic-world
# requirements:
# ['strips', 'typing']
# types:
# ['player', 'location', 'monster', 'element', 'chest']
# actions:
# move
#    parameters
#    [['p', 'player'], ['l1', 'location'], ['l2', 'location']]
#    precondition
#    [[['at', 'p', 'l1'], 1], [['border', 'l1', 'l2'], 1], [['guarded', 'l2'], 0]]
#    effect
#    [[['at', 'p', 'l2'], 1], [['at', 'p', 'l1'], 0]]


# problem: move-to-castle
# objects:
#    player :
#    ['npc']
#    location :
#    ['town', 'field', 'castle']
# init:
# [['border', 'town', 'field'], 1]
# [['border', 'field', 'castle'], 1]
# [['at', 'npc', 'town'], 1]
# goal:
# [['at', 'npc', 'castle'], 1]




###----------------------------------------------------------------------###
###--------------------------------case 1--------------------------------###
# domain: magic-world
# requirements:
# ['strips', 'typing']
# types:
# ['player', 'location', 'monster', 'element', 'chest']
# actions:
# move
#    parameters
#    [['p', 'player'], ['l1', 'location'], ['l2', 'location']]
#    precondition
#    [[['at', 'p', 'l1'], 1], [['border', 'l1', 'l2'], 1], [['guarded', 'l2'], 0]]
#    effect
#    [[['at', 'p', 'l2'], 1], [['at', 'p', 'l1'], 0]]


# problem: sneak-past-dragon-to-castle
# objects:
#    player :
#    ['npc']
#    monster :
#    ['dragon']
#    location :
#    ['town', 'field', 'castle', 'tunnel', 'river']
# init:
# [['border', 'town', 'field'], 1]
# [['border', 'town', 'tunnel'], 1]
# [['border', 'field', 'castle'], 1]
# [['border', 'tunnel', 'river'], 1]
# [['border', 'river', 'castle'], 1]
# [['at', 'npc', 'town'], 1]
# [['at', 'dragon', 'field'], 1]
# [['guarded', 'field'], 1]
# goal:
# [['at', 'npc', 'castle'], 1]


###----------------------------------------------------------------------###
###--------------------------------case 2--------------------------------###
# domain: magic-world
# requirements:
# ['strips', 'typing']
# types:
# ['player', 'location', 'monster', 'element', 'chest']
# actions:
# move
#    parameters
#    [['p', 'player'], ['l1', 'location'], ['l2', 'location']]
#    precondition
#    [[['at', 'p', 'l1'], 1], [['border', 'l1', 'l2'], 1], [['guarded', 'l2'], 0]]
#    effect
#    [[['at', 'p', 'l2'], 1], [['at', 'p', 'l1'], 0]]
# attack
#    parameters
#    [['p', 'player'], ['m', 'monster'], ['l1', 'location'], ['l2', 'location']]
#    precondition
#    [[['at', 'p', 'l1'], 1], [['at', 'm', 'l2'], 1], [['border', 'l1', 'l2'], 1], [['guarded', 'l2'], 1]]
#    effect
#    [[['at', 'm', 'l2'], 0], [['guarded', 'l2'], 0]]
# open
#    parameters
#    [['p', 'player'], ['c', 'chest'], ['l1', 'location']]
#    precondition
#    [[['at', 'p', 'l1'], 1], [['at', 'c', 'l1'], 1], [['open', 'c'], 0]]
#    effect
#    [[['open', 'c'], 1]]
# collect-fire
#    parameters
#    [['p', 'player'], ['c', 'chest'], ['l1', 'location'], ['e', 'element']]
#    precondition
#    [[['at', 'p', 'l1'], 1], [['at', 'c', 'l1'], 1], [['open', 'c'], 1], [['fire', 'e'], 1], [['in', 'e', 'c'], 1], [['empty', 'c'], 0]]
#    effect
#    [[['empty', 'c'], 1], [['has-fire', 'p'], 1]]
# collect-earth
#    parameters
#    [['p', 'player'], ['c', 'chest'], ['l1', 'location'], ['e', 'element']]
#    precondition
#    [[['at', 'p', 'l1'], 1], [['at', 'c', 'l1'], 1], [['open', 'c'], 1], [['earth', 'e'], 1], [['in', 'e', 'c'], 1], [['empty', 'c'], 0]]
#    effect
#    [[['empty', 'c'], 1], [['has-earth', 'p'], 1]]
# build-fireball
#    parameters
#    [['p', 'player']]
#    precondition
#    [[['has-fire', 'p'], 1], [['has-earth', 'p'], 1]]
#    effect
#    [[['has-fireball', 'p'], 1], [['has-fire', 'p'], 0], [['has-earth', 'p'], 0]]


# problem: fireball
# objects:
#    player :
#    ['npc']
#    monster :
#    ['ogre', 'dragon']
#    location :
#    ['town', 'field', 'river', 'cave']
#    chest :
#    ['box1', 'box2']
#    element :
#    ['reddust', 'browndust']
# init:
# [['border', 'town', 'field'], 1]
# [['border', 'field', 'town'], 1]
# [['border', 'field', 'river'], 1]
# [['border', 'river', 'field'], 1]
# [['border', 'river', 'cave'], 1]
# [['border', 'cave', 'river'], 1]
# [['at', 'npc', 'town'], 1]
# [['at', 'ogre', 'river'], 1]
# [['at', 'dragon', 'cave'], 1]
# [['guarded', 'river'], 1]
# [['guarded', 'cave'], 1]
# [['at', 'box1', 'river'], 1]
# [['at', 'box2', 'cave'], 1]
# [['fire', 'reddust'], 1]
# [['in', 'reddust', 'box1'], 1]
# [['earth', 'browndust'], 1]
# [['in', 'browndust', 'box2'], 1]
# goal:
# [['has-fireball', 'npc'], 1]


###----------------------------------------------------------------------###
###--------------------------------case 3--------------------------------###
# domain: blocksworld
# requirements:
# ['strips', 'typing']
# types:
# ['block', 'table']
# actions:
# move
#    parameters
#    [['b', 'block'], ['t1', 'table'], ['t2', 'table']]
#    precondition
#    [[['block', 'b'], 1], [['table', 't1'], 1], [['table', 't2'], 1], [['on', 'b', 't1'], 1], [['on', 'b', 't2'], 0], [['clear', 'b'], 1]]
#    effect
#    [[['on', 'b', 't2'], 1], [['on', 'b', 't1'], 0]]
# stack
#    parameters
#    [['a', 'block'], ['b', 'block'], ['t1', 'table']]
#    precondition
#    [[['block', 'a'], 1], [['block', 'b'], 1], [['table', 't1'], 1], [['clear', 'a'], 1], [['clear', 'b'], 1], [['on', 'a', 't1'], 1], [['on', 'b', 't1'], 1]]
#    effect
#    [[['on', 'a', 'b'], 1], [['on', 'a', 't1'], 0], [['clear', 'b'], 0]]
# unstack
#    parameters
#    [['a', 'block'], ['b', 'block'], ['t1', 'table']]
#    precondition
#    [[['block', 'a'], 1], [['block', 'b'], 1], [['table', 't1'], 1], [['on', 'b', 't1'], 1], [['clear', 'a'], 1], [['on', 'a', 'b'], 1]]
#    effect
#    [[['on', 'a', 't1'], 1], [['on', 'a', 'b'], 0], [['clear', 'b'], 1]]


# problem: stack-blocks-stacked-ba-from-tablex-to-stacked-ab-tabley
# objects:
#    block :
#    ['a', 'b']
#    table :
#    ['x', 'y']
# init:
# [['block', 'a'], 1]
# [['block', 'b'], 1]
# [['table', 'x'], 1]
# [['table', 'y'], 1]
# [['on', 'a', 'x'], 1]
# [['on', 'b', 'a'], 1]
# [['clear', 'b'], 1]
# goal:
# [['on', 'b', 'y'], 1]
# [['on', 'a', 'b'], 1]
# [['clear', 'a'], 1]
# [['clear', 'b'], 0]

###----------------------------------------------------------------------###
###--------------------------------case 4--------------------------------###
# domain: blocksworld
# requirements:
# ['strips']
# types:
# ['block', 'table']
# actions:
# move
#    parameters
#    [['b', 'block'], ['x', 'table'], ['y', 'table']]
#    precondition
#    [[['block', 'b'], 1], [['table', 'x'], 1], [['table', 'y'], 1], [['on', 'b', 'x'], 1], [['clear', 'b'], 1], [['clear', 'y'], 1]]
#    effect
#    [[['on', 'b', 'x'], 0], [['on', 'b', 'y'], 1], [['clear', 'x'], 1], [['clear', 'y'], 0]]
# stack
#    parameters
#    [['a', 'block'], ['x', 'table'], ['b', 'block'], ['y', 'table']]
#    precondition
#    [[['block', 'a'], 1], [['block', 'b'], 1], [['table', 'x'], 1], [['table', 'y'], 1], [['clear', 'a'], 1], [['clear', 'b'], 1], [['on', 'a', 'x'], 1], [['on', 'b', 'y'], 1]]
#    effect
#    [[['on', 'a', 'b'], 1], [['on', 'a', 'x'], 0], [['clear', 'b'], 0], [['clear', 'x'], 1]]
# unstack
#    parameters
#    [['a', 'block'], ['b', 'block'], ['x', 'table'], ['y', 'table']]
#    precondition
#    [[['block', 'a'], 1], [['block', 'b'], 1], [['table', 'x'], 1], [['table', 'y'], 1], [['on', 'b', 'x'], 1], [['on', 'a', 'b'], 1], [['clear', 'a'], 1], [['clear', 'y'], 1]]
#    effect
#    [[['on', 'a', 'y'], 1], [['on', 'a', 'b'], 0], [['clear', 'b'], 1], [['clear', 'a'], 1], [['clear', 'y'], 0]]


# problem: stack-blocks-stacked-ba-from-table1-to-stacked-ab-table3-onepilepertable
# objects:
#    block :
#    ['a', 'b']
#    table :
#    ['t1', 't2', 't3']
# init:
# [['block', 'a'], 1]
# [['block', 'b'], 1]
# [['table', 't1'], 1]
# [['table', 't2'], 1]
# [['table', 't3'], 1]
# [['on', 'a', 't1'], 1]
# [['on', 'b', 'a'], 1]
# [['clear', 'b'], 1]
# [['clear', 't2'], 1]
# [['clear', 't3'], 1]
# goal:
# [['on', 'a', 'b'], 1]
# [['on', 'b', 't3'], 1]