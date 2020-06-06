import csv
import random as rd
import copy
import rockMan
import math
battle_table = []

player_feature_num = 19
player_hidden_num = 19
player_out_num = 3

player1_feature = [1]*player_feature_num
player1_feature[14]=10
player1_feature[15:] = [0]*4

player2_feature =[1]*player_feature_num
player2_feature[14]=10
player2_feature[15:] = [0]*4

player1_output = [0]*3
player2_output = [0]*3

def getrandomMat(min,max,r,l):
    tmp=[[0 for t in range(l)]for i in range(r)]
    for i in range(r):
        for j in range(l):
            tmp[i][j]=rd.uniform(min,max)
    return tmp

class weights(object):
    global player_feature_num
    global player_hidden_num
    global player_out_num


    def __init__(self):
        self.unhitnum = 0
        self.shootnum = 0
        self.beshootnum = 0
        self.dodgenum = 0
        pass

    def init(self, father):
        self.input = getrandomMat(-10,10, player_feature_num, player_hidden_num)
        self.hidden = getrandomMat(-10,10, player_hidden_num, player_out_num)
        self.score_father(father, -1)
    def getscore(self):
        if not self.shootnum == 0 :
            self.score+=(((self.shootnum-self.unhitnum)/self.shootnum-0.3)*24)**3
        else:
            self.score -=7*7*7
        if not self.beshootnum == 0:
            self.score+=((self.dodgenum/self.beshootnum-0.3)*24)**3
        self.unhitnum = 0
        self.shootnum = 0
        self.beshootnum = 0
        self.dodgenum = 0

    def zeroinit(self, father):
        self.input = [[0]*player_hidden_num]*player_feature_num
        self.hidden = [[0]* player_out_num]*player_hidden_num
        self.score_father(father, -1)



    def score_father(self, father, mather):
        self.score = 0
        self.father = father
        self.mather = mather
        self.unhitnum = 0
        self.shootnum = 0
        self.beshootnum = 0
        self.dodgenum = 0

    def copy(self, copied):
        self.input = copy.deepcopy(copied.input)
        self.hidden = copy.deepcopy(copied.hidden)
        self.score_father(copied.father, copied.mather)


class all_weight(object):
    def __init__(self):
        self.allweight = []

    def reinit(self):
        self.allweight=[]
        for i in range(100):
            tempw = weights()
            tempw.init(i)
            self.allweight.append(tempw)

    def creat_first(self):
        for i in range(100):
            tempw = weights()
            tempw.init(i)
            self.allweight.append(tempw)

    def load(self, num, item):
        for num1 in range(2):
            if num1 == 0:
                for num2 in range(player_feature_num):
                    for num3 in range(player_hidden_num):
                        self.allweight[num].input[num2][num3] = float(item[num2 * player_hidden_num  + num3])
            if num1 == 1:
                for num2 in range(player_hidden_num ):
                    for num3 in range(player_out_num):
                        self.allweight[num].hidden[num2][num3] = float(item[num2 * player_out_num + num3 + player_feature_num * player_hidden_num ])
        self.allweight[num].father = int(item[-2])
    def load_last(self):
        for i in range(100):
            tempw = weights()
            tempw.init(i)
            self.allweight.append(tempw)

        csvFile = open("1008.csv", "r")
        reader = csv.reader(csvFile)
        num = 0
        for item in reader:
            self.load(num, item)
            num += 1
            if num == 100:
                break


    def variation(self):
        for i in range(40):
            maxscore=-0x7f7f7f7f
            maxlabel=-1
            tmplist=[]
            for tmplabel in range(40):
                temp = weights()
                temp.copy(self.allweight[i])
                tmplist.append(temp)
                for j in range(30):
                    x1 = rd.randint(0, 1)
                    if x1 == 0:
                        x2 = rd.randint(0, player_feature_num - 1)
                        x3 = rd.randint(0, player_hidden_num - 1)
                        tmplist[tmplabel].input[x2][x3] = rd.uniform(-10, 10)
                    if x1 == 1:
                        x2 = rd.randint(0, player_hidden_num - 1)
                        x3 = rd.randint(0, player_out_num-1)
                        tmplist[tmplabel].hidden[x2][x3] = rd.uniform(-10, 10)
                global player1w_input, player1w_hidden, player2w_input, player2w_hidden
                player1w_input = tmplist[tmplabel].input
                player2w_input = allplayer.allweight[0].input
                player1w_hidden = tmplist[tmplabel].hidden
                player2w_hidden = allplayer.allweight[0].hidden
                score = rockMan.game.battle(True)
                player2w_input = tmplist[tmplabel].input
                player1w_input = allplayer.allweight[0].input
                player2w_hidden = tmplist[tmplabel].hidden
                player1w_hidden = allplayer.allweight[0].hidden
                score += rockMan.game.battle(False)
                if score>maxscore:
                    maxlabel=tmplabel
                    maxscore=score
            tmplist[maxlabel].father = self.allweight[i].father
            self.allweight.append(tmplist[maxlabel])


    def match(self):
        for i in range(20):
            fa = rd.randint(0, 39)
            ma = rd.randint(0, 39)
            while fa==ma:
                fa = rd.randint(0, 39)
                ma = rd.randint(0, 39)

            maxscore = -0x7f7f7f7f
            maxlabel = -1
            tmplist = []
            for tmplabel in range(20):
                temp = weights()
                temp.copy(self.allweight[fa])
                tmplist.append(temp)
                for _ in range(100):

                    x1 = rd.randint(0, 1)
                    if x1 == 0:
                        x2 = rd.randint(0, player_feature_num - 1)
                        x3 = rd.randint(0, player_hidden_num - 1)
                        tmp=float(self.allweight[ma].input[x2][x3])
                        tmplist[tmplabel].input[x2][x3] = tmp
                    if x1 == 1:
                        x2 = rd.randint(0, player_hidden_num - 1)
                        x3 = rd.randint(0, player_out_num-1)
                        tmplist[tmplabel].hidden[x2][x3] = self.allweight[ma].hidden[x2][x3]

                global player1w_input, player1w_hidden, player2w_input, player2w_hidden
                player1w_input = tmplist[tmplabel].input
                player2w_input = allplayer.allweight[0].input
                player1w_hidden = tmplist[tmplabel].hidden
                player2w_hidden = allplayer.allweight[0].hidden
                score = rockMan.game.battle(True)
                player2w_input = tmplist[tmplabel].input
                player1w_input = allplayer.allweight[0].input
                player2w_hidden = tmplist[tmplabel].hidden
                player1w_hidden = allplayer.allweight[0].hidden
                score += rockMan.game.battle(False)
                if score > maxscore:
                    maxlabel = tmplabel
                    maxscore = score
            tmplist[maxlabel].father = self.allweight[ma].father
            self.allweight.append(tmplist[maxlabel])

    def add_scores(self):
        for i in range(100):
            self.allweight[i].getscore()

    def initzero(self):
        for i in range(100):
            self.allweight[i].score_father(i,-1)


    def get_next_params(self):
        self.get_begin40()
        self.variation()
        self.match()

        rd.shuffle(self.allweight)

    def get_begin40(self):
        self.allweight.sort(key=lambda x: -x.score)
        label = [1]*100
        tmpweight=[]
        num = 0
        for i in self.allweight:
            if label[i.father]:
                label[i.father]-=1
                i.score = 0
                i.unhitnum = 0
                i.shootnum = 0
                i.beshootnum = 0
                i.dodgenum = 0
                tmpweight.append(i)
                num += 1
                if (num == 40):
                    break
        self.allweight = tmpweight

    def getbegin80(self):
        self.allweight.sort(key=lambda x: -x.score)
        tmp=self.allweight[0:80]
        rd.shuffle(tmp)
        self.allweight[0:80]=tmp

allplayer = all_weight()


def init(player1, player2):
    global player1w_input, player1w_hidden, player2w_input, player2w_hidden
    player1w_input = allplayer.allweight[player1].input
    player2w_input = allplayer.allweight[player2].input
    player1w_hidden = allplayer.allweight[player1].hidden
    player2w_hidden = allplayer.allweight[player2].hidden


def sigmoid(x):
    try:
        y = 1.0 / (1.0 + math.exp(-x/150))-0.5
    except OverflowError:
        y = 0
    return y

def listsigmoid(x):
    y = [0]*len(x)
    num=0
    for i in x:
        y[num]=sigmoid(i)*6
        num+=1
    return y


def sigmoid2(x):
    try:
        y = 1.0 / (1.0 + math.exp(-x/30))-0.5
    except OverflowError:
        y = 0
    return y

def listsigmoid2(x):
    y = [0]*len(x)
    num=0
    for i in x:
        y[num]=sigmoid2(i)*6
        num+=1
    return y


def relu(x):
    if x>0:
        return x
    else:
        return 0

def listrelu(x):
    y = [0]*len(x)
    num=0
    for i in x:
        y[num]=relu(i)
        num+=1
    return y



def featuredotinput(x,y):
    z=[0]*player_hidden_num
    for i in range(player_hidden_num):
        num=0
        for j in range(player_feature_num):
            num+=x[j]*y[j][i]
        z[i]=num
    return z

def inputdothidden(x,y):
    z=[0]*player_out_num
    for i in range(player_out_num):
        num=0
        for j in range(player_hidden_num):
            num+=x[j]*y[j][i]
        z[i]=num
    return z

def update():
    global player1_output, player2_output
    hidden1 = listsigmoid(featuredotinput(player1_feature, player1w_input))

    player1_output = listsigmoid2(inputdothidden(hidden1, player1w_hidden))
    hidden2 = listsigmoid(featuredotinput(player2_feature, player2w_input))
    player2_output = listsigmoid2(inputdothidden(hidden2, player2w_hidden))


def getbattletable():
    global battle_table
    battle = [[0, 1], [0, 2], [0, 3], [0, 4], [1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4],
              [1, 0], [2, 0], [3, 0], [4, 0], [2, 1], [3, 1], [4, 1], [3, 2], [4, 2], [4, 3]]
    for i in range(20):
        for [x, y] in battle:
            battle_table.append([x + i * 5, y + i * 5])
    for i in range(16):
        for [x, y] in battle:
            battle_table.append([x + i * 5, y + i * 5])
    for i in range(16):
        for [x, y] in battle:
            battle_table.append([x + i * 5, y + i * 5])

getbattletable()