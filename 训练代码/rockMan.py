import pygame
import RL2
import sys
from mxnet import nd
import time
import rockManSprites1 as rms

class PlaneGame(object):

    def __init__(self):
        # 1.创建游戏的窗口

        self.diedai=0
        self.diedai25=0
        self.diedai4=0
        ##self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 2.创建游戏的时钟
        self.battle_num=0
        ##self.back_group = pygame.sprite.Group()
        ##for i in range(7):
        ##    bg = BackGround(i * BACK_RECT[0])
        ##    self.back_group.add(bg)
        # 3.调用私有方法，精灵和精灵组的创建

    #从100个随机模型中取前4个，循环25次，得到前100个模型
    def get_top100(self):
        num=0
        newallplayer = RL2.all_weight()
        newallplayer.creat_first()
        while num<50:
            RL2.allplayer.reinit()
            while True:
                self.init2()
                cishu=-1
                while True:
                    # 2. 事件监听
                    ##pygame.display.update()
                    self.__update_sprites()
                    cishu+=1
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

                    if cishu >900:
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



                if self.battle_num == 1039:
                    self.battle_num = 0
                    RL2.allplayer.add_scores()
                    RL2.allplayer.allweight.sort(key=lambda x: -x.score)
                    newallplayer.allweight[num*2].copy(RL2.allplayer.allweight[0])
                    newallplayer.allweight[num*2+1].copy(RL2.allplayer.allweight[1])
                    break
            num+=1
        RL2.allplayer=newallplayer
        self.record()
    def getnextplayer2(self):
        self.battle_num += 1
        if self.battle_num == 400:
            RL2.allplayer.add_scores()
            RL2.allplayer.getbegin80()
        if self.battle_num ==720:
            RL2.allplayer.add_scores()
            RL2.allplayer.getbegin80()
        if self.battle_num ==1040:
            self.diedai += 1
            self.diedai4+= 1
            RL2.allplayer.add_scores()
            RL2.allplayer.allweight.sort(key=lambda x: -x.score)
            if self.diedai4%4==1:
                if self.diedai25==0:
                    self.newallplayer = RL2.all_weight()
                    self.newallplayer.creat_first()
                self.newallplayer.allweight[self.diedai25 * 4].copy(RL2.allplayer.allweight[0])
                self.newallplayer.allweight[self.diedai25 * 4].father=self.diedai25 * 4
                self.newallplayer.allweight[self.diedai25 * 4 + 1].copy(RL2.allplayer.allweight[1])
                self.newallplayer.allweight[self.diedai25 * 4+1].father=self.diedai25 * 4+1
                self.newallplayer.allweight[self.diedai25 * 4 + 2].copy(RL2.allplayer.allweight[2])
                self.newallplayer.allweight[self.diedai25 * 4+2].father=self.diedai25 * 4+2
                self.newallplayer.allweight[self.diedai25 * 4 + 3].copy(RL2.allplayer.allweight[3])
                self.newallplayer.allweight[self.diedai25 * 4+3].father=self.diedai25 * 4+3
                self.diedai25+=1
                if self.diedai25==25:
                    self.diedai25=0
                    RL2.allplayer = self.newallplayer
                    self.diedai += 1
                    self.record()
                    self.battle_num = 0
                    self.player1,self.player2 = RL2.battle_table[self.battle_num][0],RL2.battle_table[self.battle_num][1]
                    return
			
            self.record()
            RL2.allplayer.get_next_params()
            self.battle_num = 0

        self.player1,self.player2 = RL2.battle_table[self.battle_num][0],RL2.battle_table[self.battle_num][1]

    def getnextplayer1(self):
        self.battle_num += 1
        if self.battle_num == 400:
            RL2.allplayer.add_scores()
            RL2.allplayer.getbegin80()
        if self.battle_num ==720:
            RL2.allplayer.add_scores()
            RL2.allplayer.getbegin80()
        if self.battle_num ==1040:
            self.diedai += 1
            RL2.allplayer.add_scores()
            RL2.allplayer.allweight.sort(key=lambda x: -x.score)
            self.record()
            RL2.allplayer.get_next_params()
            self.battle_num = 0

        self.player1,self.player2 = RL2.battle_table[self.battle_num][0],RL2.battle_table[self.battle_num][1]

    def init(self):

        self.bullets_group = pygame.sprite.Group()
        self.rock_group = pygame.sprite.Group()
        ##self.blood_group = pygame.sprite.Group()

        ##for i in range(14):
        ##    blood1 = Blood1(i)
        ##    blood2 = Blood2(i)
        ##    self.blood_group.add(blood1, blood2)

        #self.getnextplayer1()
        self.getnextplayer1()
        RL2.init(self.player1, self.player2)
        self.rock1 = rms.RockMan1(336)
        self.rock2 = rms.RockMan2(1008)
        rms.init()
        self.rock_group = pygame.sprite.Group(self.rock1, self.rock2)

    def init2(self):

        self.bullets_group = pygame.sprite.Group()
        self.rock_group = pygame.sprite.Group()
        ##self.blood_group = pygame.sprite.Group()

        ##for i in range(14):
        ##    blood1 = Blood1(i)
        ##    blood2 = Blood2(i)
        ##    self.blood_group.add(blood1, blood2)

        #self.getnextplayer1()
        self.getnextplayer1()
        RL2.init(self.player1, self.player2)
        self.rock1 = rms.RockMan1(336)
        self.rock2 = rms.RockMan2(1008)
        rms.init()
        self.rock_group = pygame.sprite.Group(self.rock1, self.rock2)


		
    def start_game(self):
        self.get_top100()
        while True:
            self.init()
            cishu = -1
            # 1. 设置刷新帧率
            while True:

                cishu += 1
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

                if cishu > 1200:
                    RL2.allplayer.allweight[self.player1].score += rms.getscore1()-100
                    #print(RL2.allplayer.allweight[self.player1].score)
                    RL2.allplayer.allweight[self.player2].score += rms.getscore2()-100
                    #print(RL2.allplayer.allweight[self.player2].score)
                    RL2.allplayer.allweight[self.player1].unhitnum += rms.player1_unshootnum
                    RL2.allplayer.allweight[self.player2].unhitnum += rms.player2_unshootnum
                    RL2.allplayer.allweight[self.player1].shootnum += rms.player1_shootnum
                    RL2.allplayer.allweight[self.player2].shootnum += rms.player2_shootnum
                    RL2.allplayer.allweight[self.player1].beshootnum += rms.player2_shootnum
                    RL2.allplayer.allweight[self.player2].beshootnum += rms.player1_shootnum
                    RL2.allplayer.allweight[self.player1].dodgenum += rms.player2_unshootnum
                    RL2.allplayer.allweight[self.player2].dodgenum += rms.player1_unshootnum
                    break

                self.__update_sprites()
    def battle(self,isleft):
        self.bullets_group = pygame.sprite.Group()
        self.rock_group = pygame.sprite.Group()
        self.rock1 = rms.RockMan1(336)
        self.rock2 = rms.RockMan2(1008)
        rms.init()
        self.rock_group = pygame.sprite.Group(self.rock1, self.rock2)
        cishu = 0
        while True:
            self.__update_sprites()
            RL2.update()

            RL2.update()
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
            cishu += 1
            if cishu >900:
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
    def __update_sprites(self):

        ##self.back_group.draw(self.screen)
        self.rock1.update()
        self.rock2.update()
        ##self.rock_group.draw(self.screen)
        self.bullets_group.update()
        ##self.bullets_group.draw(self.screen)
        ##self.blood_group.update()
        ##self.blood_group.draw(self.screen)


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
        #if RL2.player1_output[3]>0 and self.rock1.hav_jump and not self.rock1.isfall:
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
        elif self.rock1.speed > 0:
            self.rock1.dir_Left = False

    def handplay1(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_u]:
            bullet = self.rock1.shoot()
            if bullet:
                self.bullets_group.add(bullet)

        if keys_pressed[pygame.K_s] and self.rock1.hav_jump and not self.rock1.isfall:
            self.rock1.fall()

        if keys_pressed[pygame.K_w] and not self.rock1.hav_jump:
            self.rock1.hav_jump = True
            self.rock1.ver_v = -33
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
        elif self.rock2.speed > 0:
            self.rock2.dir_Left = False


game = PlaneGame()
if __name__ == '__main__':
    game.start_game()
