typ = [] # type name
act = [] # actions
pred = [] # predicates name
vari = [] # variables name
var2 = [] # variables type
var3 = [] # id in each type
feat = [] # features, type = predi
goal = []
mk1 = []
st = []
cnt = []
sta = set() # current state
argc = [] # type of arguments of each predicate
class predi():
    def __init__(self, id, neg):
        self.id = id
        self.neg = neg
        self.arg = []
class action():
    def __init__(self, nam):
        self.nam = nam
        self.par1 = [] # variables name
        self.par2 = [] # variables type
        self.prec = [] # predi
        self.eff = [] # predi

    