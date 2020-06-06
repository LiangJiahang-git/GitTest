import pygame
import RL2
import sys
from mxnet import nd
import time
import rockManSprites1 as  rms
#from rockManSprites1 import *

class PlaneGame(object):

    def __init__(self):
        # 1.创建游戏的窗口

        self.diedai=1
        self.screen = pygame.display.set_mode(rms.SCREEN_RECT.size)
        # 2.创建游戏的时钟
        self.battle_num=0
        self.back_group = pygame.sprite.Group()
        for i in range(7):
            bg = rms.BackGround(i * rms.BACK_RECT[0])
            self.back_group.add(bg)
        # 3.调用私有方法，精灵和精灵组的创建

    #从100个随机模型中取前4个，循环25次，得到前100个模型
    def get_top100(self):
        num=0
        newallplayer = RL2.all_weight()
        newallplayer.creat_first()
        while num<25:
            RL2.allplayer.reinit()
            while True:
                self.init()
                while True:
                    # 2. 事件监听
                    pygame.display.update()
                    self.__update_sprites()
                    RL2.update()
                    # if not self.rock1.attacked:
                    if not self.rock1.attacked_time > 3:
                        # self.handplay1()
                        self.autoplay1()
                    if not self.rock2.attacked_time > 3:
                        self.autoplay2()
                    if self.__check_collide():
                        RL2.allplayer.allweight[self.player1].score += rms.getscore1()
                        RL2.allplayer.allweight[self.player2].score += rms.getscore2()
                        RL2.allplayer.allweight[self.player1].unhitnum += rms.player1_unshootnum
                        RL2.allplayer.allweight[self.player2].unhitnum += rms.player2_unshootnum
                        RL2.allplayer.allweight[self.player1].shootnum += rms.player1_shootnum
                        RL2.allplayer.allweight[self.player2].shootnum += rms.player2_shootnum
                        RL2.allplayer.allweight[self.player1].beshootnum += rms.player2_shootnum
                        RL2.allplayer.allweight[self.player2].beshootnum += rms.player1_shootnum
                        RL2.allplayer.allweight[self.player1].dodgenum += rms.player2_unshootnum
                        RL2.allplayer.allweight[self.player2].dodgenum += rms.player1_unshootnum
                        break

                    if time.time() - self.starttime > 3:
                        RL2.allplayer.allweight[self.player1].score += rms.getscore1()
                        RL2.allplayer.allweight[self.player2].score += rms.getscore2()
                        RL2.allplayer.allweight[self.player1].unhitnum += rms.player1_unshootnum
                        RL2.allplayer.allweight[self.player2].unhitnum += rms.player2_unshootnum
                        RL2.allplayer.allweight[self.player1].shootnum += rms.player1_shootnum
                        RL2.allplayer.allweight[self.player2].shootnum += rms.player2_shootnum
                        RL2.allplayer.allweight[self.player1].beshootnum += rms.player2_shootnum
                        RL2.allplayer.allweight[self.player2].beshootnum += rms.player1_shootnum
                        RL2.allplayer.allweight[self.player1].dodgenum += rms.player2_unshootnum
                        RL2.allplayer.allweight[self.player2].dodgenum += rms.player1_unshootnum

                        break

                if self.battle_num == 719:
                    self.battle_num = 0
                    RL2.allplayer.getbegin80()
                    newallplayer.allweight[num*4].copy(RL2.allplayer.allweight[0])
                    newallplayer.allweight[num*4+1].copy(RL2.allplayer.allweight[1])
                    newallplayer.allweight[num * 4 + 2].copy(RL2.allplayer.allweight[2])
                    newallplayer.allweight[num * 4 + 3].copy(RL2.allplayer.allweight[3])
                    break
            num+=1
        RL2.allplayer=newallplayer
        self.record()

    #此函数是获取下次对战的两个决策矩阵的编号
    def getnextplayer(self):
        self.battle_num += 1
        # 此处400代表完成了400次对战
        if self.battle_num == 400:
            RL2.allplayer.add_scores()
            RL2.allplayer.getbegin80()
        if self.battle_num ==720:
            RL2.allplayer.add_scores()
            RL2.allplayer.getbegin80()
        if self.battle_num ==1040:
            self.diedai += 1
            RL2.allplayer.add_scores()
            self.record()
            RL2.allplayer.get_next_params()
            self.battle_num = 0

        self.player1,self.player2 = RL2.battle_table[self.battle_num][0],RL2.battle_table[self.battle_num][1]
        print(self.player2)
        #self.player1,self.player2 = 2,1

    def init(self):

        self.bullets_group = pygame.sprite.Group()
        self.rock_group = pygame.sprite.Group()
        self.blood_group = pygame.sprite.Group()

        for i in range(14):
            blood1 = rms.Blood1(i)
            blood2 = rms.Blood2(i)
            self.blood_group.add(blood1, blood2)

        #每次调用这个init函数都说明要新开始一句对战，要重新获取下一轮对战需要的决策矩阵编号
        self.getnextplayer()

        # 将self.player1 和self.player2序号的决策矩阵加载进来
        RL2.init(self.player1, self.player2)

        # 初始化洛克人的位置
        self.rock1 = rms.RockMan1(336)
        self.rock2 = rms.RockMan2(1008)

        # 此处的初始化为初始化游戏需要的一些参数
        rms.init()
        self.rock_group = pygame.sprite.Group(self.rock1, self.rock2)

        # 获取游戏开始时的时间
        self.starttime = time.time()

    def start_game(self):
        RL2.allplayer.load_last()
        while True:
            self.init()
            cishu = -1
            # 1. 设置刷新帧率
            while True:
                cishu+=1
                b = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        b = True
                if b:
                   break

                ###########
                pygame.display.update()

                self.__update_sprites()

                RL2.update()
                if not self.rock1.attacked_time > 3:
                    # self.handplay1()
                    self.autoplay1()
                if not self.rock2.attacked_time > 3:
                    self.autoplay2()

                if self.__check_collide():
                    RL2.allplayer.allweight[self.player1].score += rms.getscore1()
                    RL2.allplayer.allweight[self.player2].score += rms.getscore2()
                    RL2.allplayer.allweight[self.player1].unhitnum += rms.player1_unshootnum
                    RL2.allplayer.allweight[self.player2].unhitnum += rms.player2_unshootnum
                    RL2.allplayer.allweight[self.player1].shootnum += rms.player1_shootnum
                    RL2.allplayer.allweight[self.player2].shootnum += rms.player2_shootnum
                    RL2.allplayer.allweight[self.player1].beshootnum += rms.player2_shootnum
                    RL2.allplayer.allweight[self.player2].beshootnum += rms.player1_shootnum
                    RL2.allplayer.allweight[self.player1].dodgenum += rms.player2_unshootnum
                    RL2.allplayer.allweight[self.player2].dodgenum += rms.player1_unshootnum
                    break

                if time.time() - self.starttime > 80:
                    RL2.allplayer.allweight[self.player1].score += rms.getscore1()
                    RL2.allplayer.allweight[self.player2].score += rms.getscore2()
                    RL2.allplayer.allweight[self.player1].unhitnum += rms.player1_unshootnum
                    RL2.allplayer.allweight[self.player2].unhitnum += rms.player2_unshootnum
                    RL2.allplayer.allweight[self.player1].shootnum += rms.player1_shootnum
                    RL2.allplayer.allweight[self.player2].shootnum += rms.player2_shootnum
                    RL2.allplayer.allweight[self.player1].beshootnum += rms.player2_shootnum
                    RL2.allplayer.allweight[self.player2].beshootnum += rms.player1_shootnum
                    RL2.allplayer.allweight[self.player1].dodgenum += rms.player2_unshootnum
                    RL2.allplayer.allweight[self.player2].dodgenum += rms.player1_unshootnum
                    break

    def battle(self,isleft):

        self.bullets_group = pygame.sprite.Group()
        self.rock_group = pygame.sprite.Group()
        self.blood_group = pygame.sprite.Group()

        for i in range(14):
            blood1 = rms.Blood1(i)
            blood2 = rms.Blood2(i)
            self.blood_group.add(blood1, blood2)

        self.rock1 = rms.RockMan1(336)
        self.rock2 = rms.RockMan2(1008)
        rms.init()
        self.rock_group = pygame.sprite.Group(self.rock1, self.rock2)
        self.starttime = time.time()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    b = True
            pygame.display.update()
            self.__update_sprites()
            RL2.update()
            # if not self.rock1.attacked:
            if not self.rock1.attacked_time > 3:
                # self.handplay1()
                self.autoplay1()
            if not self.rock2.attacked_time > 3:
                self.autoplay2()

            if self.__check_collide():
                if isleft:
                    return rms.getscore1()
                else:
                    return rms.getscore2()
            self.__update_sprites()
            if time.time() - self.starttime >3:
                if isleft:
                    return rms.getscore1()
                else:
                    return rms.getscore2()


    def record(self):
        f = open('%d.csv'%self.diedai,'w')

        for num in RL2.allplayer.allweight:
            for num1 in num.input:
                for num2 in num1:
                    print(num2, end=',', file=f)
            for num1 in num.hidden:
                for num2 in num1:
                    print(num2, end=',', file=f)
            print(num.father, end=',', file=f)
            print("", file=f)

        for num in RL2.allplayer.allweight:
            print(num.score, end=',', file=f)
        f.close()

    def __check_collide(self):
        if (not self.rock1.attacked) and pygame.sprite.spritecollide(self.rock1, self.bullets_group, True):
            if (rms.addPlayer2Num()):
                return True
            self.rock1.be_attack()
            return False
        if (not self.rock2.attacked) and pygame.sprite.spritecollide(self.rock2, self.bullets_group, True):
            if (rms.addPlayer1Num()):
                return True
            self.rock2.be_attack()
            return False

    # 此处为控制游戏精灵自动更新
    def __update_sprites(self):

        self.back_group.draw(self.screen)
        self.rock_group.update()
        self.rock_group.draw(self.screen)
        self.bullets_group.update()
        self.bullets_group.draw(self.screen)
        self.blood_group.update()
        self.blood_group.draw(self.screen)


    @staticmethod
    def __game_over():
        print("游戏结束")
        pygame.quit()
        exit()

    def autoplay1(self):

        if RL2.player1_output[2] > 0:
            bullet = self.rock1.shoot()
            if bullet:
                self.bullets_group.add(bullet)
        #if RL2.player1_output[3] > 0 and self.rock1.hav_jump and not self.rock1.isfall:
        #    self.rock1.fall()

        if RL2.player1_output[1] > 0 and not self.rock1.hav_jump:
            self.rock1.hav_jump = True
            self.rock1.ver_v = -28
        elif RL2.player1_output[0] >0.2:
            if self.rock1.speed < 0:
                self.rock1.speed = 0
            self.rock1.speed += 5
            if self.rock1.speed > 15:
                self.rock1.speed = 15
        elif RL2.player1_output[0] < -0.2:
            if self.rock1.speed > 0:
                self.rock1.speed = 0
            self.rock1.speed -= 5
            if self.rock1.speed < -15:
                self.rock1.speed = -15
        else:
            self.rock1.speed = 0

        if self.rock1.speed < 0:
            self.rock1.dir_Left = True
            RL2.player1_feature[14]=10
        elif self.rock1.speed > 0:
            self.rock1.dir_Left = False
            RL2.player1_feature[14] = -10

    def handplay1(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_u]:
            bullet = self.rock1.shoot()
            if bullet:
                self.bullets_group.add(bullet)

        #if keys_pressed[pygame.K_s] and self.rock1.hav_jump and not self.rock1.isfall:
        #    self.rock1.fall()

        if keys_pressed[pygame.K_w] and not self.rock1.hav_jump:
            self.rock1.hav_jump = True
            self.rock1.ver_v = -28
        elif keys_pressed[pygame.K_d]:
            if self.rock1.speed < 0:
                self.rock1.speed = 0
            self.rock1.speed += 5
            if self.rock1.speed > 15:
                self.rock1.speed = 15
        elif keys_pressed[pygame.K_a]:
            if self.rock1.speed > 0:
                self.rock1.speed = 0
            self.rock1.speed -= 5
            if self.rock1.speed < -15:
                self.rock1.speed = -15
        else:
            self.rock1.speed = 0


        if self.rock1.speed < 0:
            self.rock1.dir_Left = True
        elif self.rock1.speed > 0:
            self.rock1.dir_Left = False

    def autoplay2(self):

        if RL2.player2_output[2] > 0:
            bullet = self.rock2.shoot()
            if bullet:
                self.bullets_group.add(bullet)


        #if RL2.player2_output[3]>0 and self.rock2.hav_jump and not self.rock2.isfall:
        #    self.rock2.fall()
        if RL2.player2_output[1] > 0 and not self.rock2.hav_jump:
            self.rock2.hav_jump = True
            self.rock2.ver_v = -28
        elif RL2.player2_output[0]  >0.2:
            if self.rock2.speed < 0:
                self.rock2.speed = 0
            self.rock2.speed += 5
            if self.rock2.speed > 15:
                self.rock2.speed = 15
        elif RL2.player2_output[0] < -0.2:
            if self.rock2.speed > 0:
                self.rock2.speed = 0
            self.rock2.speed -= 5
            if self.rock2.speed < -15:
                self.rock2.speed = -15
        else:
            self.rock2.speed = 0



        if self.rock2.speed < 0:
            self.rock2.dir_Left = True
            RL2.player2_feature[14]=10
        elif self.rock2.speed > 0:
            self.rock2.dir_Left = False
            RL2.player2_feature[14]=-10

game = PlaneGame()
if __name__ == '__main__':
    game.start_game()
