import pygame
import RL2
import time

SCREEN_RECT = pygame.Rect(0, 0, 1344, 672)

BACK_RECT = (192, 672)

ROCK_RECT = (98, 112)

ROCK_BOTTOM = 578

ROCK_BLINK_TIME = 20

tick = pygame.time.Clock()

player1_can_shoot_num = 2
player2_can_shoot_num = 2

player1_blood = 14
player2_blood = 14

player1_unshootnum=0
player1_shootnum=0

player2_unshootnum=0
player2_shootnum=0


def getscore1():
    global player1_blood,player2_blood
    score=(player1_blood-player2_blood)*100
    return score

def getscore2():
    global player1_blood, player2_blood
    score =(player2_blood - player1_blood) * 100
    return score

def init():
    global player1_can_shoot_num,player2_can_shoot_num
    player1_can_shoot_num =2
    player2_can_shoot_num = 2
    global player1_blood,player2_blood,player1_unshootnum,player2_unshootnum
    player1_blood = 14
    player2_blood = 14
    player1_unshootnum = 0
    player2_unshootnum = 0
    global player1_shootnum,player2_shootnum
    player1_shootnum = 0
    player2_shootnum = 0

def addPlayer1Num():
    global player1_can_shoot_num
    player1_can_shoot_num += 1
    global player2_blood
    player2_blood -= 1
    if player2_blood == 0:
        return True
    return False


def addPlayer2Num():
    global player2_can_shoot_num
    player2_can_shoot_num += 1
    global player1_blood
    player1_blood -= 1
    if player1_blood == 0:
        return True
    return False


class AllImage:

    def __init__(self):
        self.Back00 = pygame.image.load("./data/Back00.png")
        self.Back00 = pygame.transform.scale(self.Back00, BACK_RECT)
        self.M00 = pygame.image.load("./data/M00.png")
        self.M00 = pygame.transform.scale(self.M00, ROCK_RECT)
        self.M01 = pygame.image.load("./data/M01.png")
        self.M01 = pygame.transform.scale(self.M01, ROCK_RECT)
        self.M02 = pygame.image.load("./data/M02.png")
        self.M02 = pygame.transform.scale(self.M02, (93, 112))
        self.M03 = pygame.image.load("./data/M03.png")
        self.M03 = pygame.transform.scale(self.M03, (121, 140))
        self.M04 = pygame.image.load("./data/M04.png")
        self.M04 = pygame.transform.scale(self.M04, (112, 102))
        self.M05 = pygame.image.load("./data/M05.png")
        self.M05 = pygame.transform.scale(self.M05, (75, 112))
        self.M06 = pygame.image.load("./data/M06.png")
        self.M06 = pygame.transform.scale(self.M06, (98, 102))
        self.M07 = pygame.image.load("./data/M07.png")
        self.M07 = pygame.transform.scale(self.M07, (145, 112))
        self.M08 = pygame.image.load("./data/M08.png")
        self.M08 = pygame.transform.scale(self.M08, (145, 112))
        self.M09 = pygame.image.load("./data/M09.png")
        self.M09 = pygame.transform.scale(self.M09, (135, 140))
        self.M10 = pygame.image.load("./data/M10.png")
        self.M10 = pygame.transform.scale(self.M10, (135, 103))
        self.M11 = pygame.image.load("./data/M11.png")
        self.M11 = pygame.transform.scale(self.M11, (121, 112))
        self.M12 = pygame.image.load("./data/M12.png")
        self.M12 = pygame.transform.scale(self.M12, (140, 103))
        self.M13 = pygame.image.load("./data/M13.png")
        self.M13 = pygame.transform.scale(self.M13, ROCK_RECT)
        self.M14 = pygame.image.load("./data/M14.png")
        self.M14 = pygame.transform.scale(self.M14, ROCK_RECT)
        self.M15 = pygame.image.load("./data/M15.png")
        self.M15 = pygame.transform.scale(self.M15, (93, 112))
        self.M16 = pygame.image.load("./data/M16.png")
        self.M16 = pygame.transform.scale(self.M16, (121, 140))
        self.M17 = pygame.image.load("./data/M17.png")
        self.M17 = pygame.transform.scale(self.M17, (112, 102))
        self.M18 = pygame.image.load("./data/M18.png")
        self.M18 = pygame.transform.scale(self.M18, (75, 112))
        self.M19 = pygame.image.load("./data/M19.png")
        self.M19 = pygame.transform.scale(self.M19, (98, 102))
        self.M20 = pygame.image.load("./data/M20.png")
        self.M20 = pygame.transform.scale(self.M20, (145, 112))
        self.M21 = pygame.image.load("./data/M21.png")
        self.M21 = pygame.transform.scale(self.M21, (145, 112))
        self.M22 = pygame.image.load("./data/M22.png")
        self.M22 = pygame.transform.scale(self.M22, (135, 140))
        self.M23 = pygame.image.load("./data/M23.png")
        self.M23 = pygame.transform.scale(self.M23, (135, 103))
        self.M24 = pygame.image.load("./data/M24.png")
        self.M24 = pygame.transform.scale(self.M24, (121, 112))
        self.M25 = pygame.image.load("./data/M25.png")
        self.M25 = pygame.transform.scale(self.M25, (140, 103))
        self.Z00 = pygame.image.load("./data/Z00.png")
        self.Z00 = pygame.transform.scale(self.Z00, (32, 24))
        self.Z01 = pygame.image.load("./data/Z01.png")
        self.Z01 = pygame.transform.scale(self.Z01, (32, 24))
        self.Z02 = pygame.image.load("./data/Z02.png")
        self.Z02 = pygame.transform.scale(self.Z02, (37, 19))
        self.Z03 = pygame.image.load("./data/Z03.png")
        self.Z03 = pygame.transform.scale(self.Z03, (1, 1))


images = AllImage()


class RockManSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def update(self):
        pass


class BackGround(RockManSprite):
    def __init__(self, zuobiaox):
        super().__init__()
        self.image = images.Back00
        self.rect = self.image.get_rect()
        self.rect.x = zuobiaox

    def update(self):
        pass


class RockMan1(RockManSprite):
    def __init__(self, zuobiaox):
        super().__init__()
        #self.image = images.M00
        self.rect = images.M00.get_rect()
        self.rect.centerx = zuobiaox
        self.rect.bottom = ROCK_BOTTOM
        self.stay_time = 0
        self.stay_image1 = True
        self.speed = 0
        self.runtime = 0
        self.dir_Left = False
        # 洛克人的跳时的垂直速度
        self.ver_v = 0
        self.hav_jump = False
        self.shootNum = 3
        self.shootTime = 50
        self.jump_shoot = False
        self.shooting = False
        self.attacked = False
        self.isfall=False
        self.attacked_time = 0

    def __stay(self):
        """if self.speed == 0:
            if self.shooting:
                self.image = images.M07
                self.image = pygame.transform.flip(self.image, self.dir_Left, False)
            else:
                if self.stay_time == 0:
                    if self.stay_image1:
                        self.image = images.M01
                        self.stay_time = ROCK_BLINK_TIME
                        self.stay_image1 = False
                    else:
                        self.image = images.M00
                        self.stay_time = ROCK_BLINK_TIME
                        self.stay_image1 = True
                    self.image = pygame.transform.flip(self.image, self.dir_Left, False)
                    # 每次更新图片之后要判断图片的方向是否需要旋转
                self.stay_time -= 1
        """

        if self.attacked:
            self.be_attacked()

    def __jump(self):
        # tick.tick(20)
        """if self.shooting:
            self.image = images.M09
            self.image = pygame.transform.flip(self.image, self.dir_Left, False)
        else:
            self.image = images.M03
            self.image = pygame.transform.flip(self.image, self.dir_Left, False)
        """
        if self.attacked:
            self.be_attacked()
        self.rect.y += self.ver_v
        self.rect.x += self.speed
        if self.ver_v>0:
            self.isfall = True
        self.ver_v += 2
        if self.rect.bottom >= ROCK_BOTTOM:
            self.ver_v = 0
            self.rect.bottom = ROCK_BOTTOM
            self.hav_jump = False
            self.jump_shoot = False
            self.isfall=False
        self.stay_time = 0

    def __image_run(self):
        self.runtime += 1
        # tick.tick(10)
        """
        if self.shooting:
        
            if self.runtime % 4 == 0:
                self.image = images.M10
            elif self.runtime % 4 == 1:
                self.image = images.M11
            elif self.runtime % 4 == 2:
                self.image = images.M12
            elif self.runtime % 4 == 3:
                self.image = images.M11
        else:
            if self.runtime % 4 == 0:
                self.image = images.M04
            elif self.runtime % 4 == 1:
                self.image = images.M05
            elif self.runtime % 4 == 2:
                self.image = images.M06
            elif self.runtime % 4 == 3:
                self.image = images.M05
        self.image = pygame.transform.flip(self.image, self.dir_Left, False)
        """
        self.rect.x += self.speed
        if self.attacked:
            self.be_attacked()

    def __move_left(self):
        """if self.shooting:
            self.image = images.M07
        else:
            self.image = images.M02

        self.image = pygame.transform.flip(self.image, self.dir_Left, False)
        """
        self.rect.x += self.speed
        # tick.tick(10)
        if self.attacked:
            self.be_attacked()

    def __run(self):
        if self.speed == 15 or self.speed == -15:
            self.__image_run()
            self.stay_time = 0
        elif self.speed != 0:
            self.__move_left()
            self.stay_time = 0

    def shoot(self):
        global player1_can_shoot_num
        if player1_can_shoot_num > 0 and self.shootTime > 10:
            player1_can_shoot_num -= 1
            self.shootTime = 0
            self.shooting = True
            if self.dir_Left:
                bullet = Bullet1(True, self.rect.left - 40, self.rect.centery - 16)
                """self.image = pygame.transform.flip(self.image, True, False)"""
            else:
                bullet = Bullet1(False, self.rect.right + 20, self.rect.centery - 16)
            return bullet

    def be_attacked(self):
        """
        if self.attacked_time > 0:
            if self.attacked_time % 2 == 0:
                self.image = images.M08
                self.image = pygame.transform.flip(self.image, self.dir_Left, False)
            else:
                self.image = images.Z03
        else:
            self.attacked = False
            self.stay_time = 0
        """
        if self.attacked_time < 0:
            self.attacked = False
        self.attacked_time -= 1

    def be_attack(self):
        self.attacked = True
        self.attacked_time = 20
        self.speed = 0
        self.ver_v = 0

    def fall(self):
        self.ver_v=10



    def update(self):

        self.shootTime += 1
        tmplist=[(self.rect.centerx-672) / 387, self.rect.centery / 100,
                    player1_can_shoot_num, self.dir_Left*10, self.ver_v / 15, self.speed / 7.5,
                    self.attacked_time / 10]
        RL2.player1_feature[0:7] = tmplist
        RL2.player2_feature[7:14] =tmplist

        time1 = time.time()
        if self.hav_jump:
            self.__jump()
        else:
            self.__stay()
            self.__run()
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 1344:
            self.rect.right = 1344
        if self.shootTime > 10:
            self.shooting = False




class RockMan2(RockManSprite):
    def __init__(self, zuobiaox):
        super().__init__()
        #self.image = images.M13
        self.rect =  images.M13.get_rect()
        self.rect.centerx = zuobiaox
        self.rect.bottom = ROCK_BOTTOM
        self.stay_time = 0
        self.stay_image1 = True
        self.speed = 0
        self.runtime = 0
        self.dir_Left = True
        # 洛克人的跳时的垂直速度
        self.ver_v = 0
        self.hav_jump = False
        self.shootNum = 3
        self.shootTime = 50
        self.jump_shoot = False
        self.shooting = False
        self.attacked = False
        self.isfall=False
        self.attacked_time = 0

    def be_attack(self):
        self.attacked = True
        self.attacked_time = 20
        self.speed = 0
        self.ver_v = 0

    def __stay(self):
        """if self.speed == 0:
            if self.shooting:
                self.image = images.M20
                self.image = pygame.transform.flip(self.image, self.dir_Left, False)
            else:
                if self.stay_time == 0:
                    if self.stay_image1:
                        self.image = images.M14
                        self.stay_time = ROCK_BLINK_TIME
                        self.stay_image1 = False
                    else:
                        self.image = images.M13
                        self.stay_time = ROCK_BLINK_TIME
                        self.stay_image1 = True
                    self.image = pygame.transform.flip(self.image, self.dir_Left, False)
                self.stay_time -= 1
                """
                # 每次更新图片之后要判断图片的方向是否需要旋转
        if self.attacked:
            self.be_attacked()

    def __jump(self):
        # tick.tick(20)
        """if self.shooting:
            self.image = images.M22
            self.image = pygame.transform.flip(self.image, self.dir_Left, False)
        else:
            self.image = images.M16
            self.image = pygame.transform.flip(self.image, self.dir_Left, False)
            """
        if self.attacked:
            self.be_attacked()

        self.rect.y += self.ver_v
        self.rect.x += self.speed
        if self.ver_v>0:
            self.isfall = True
        self.ver_v += 2
        if self.rect.bottom >= ROCK_BOTTOM:
            self.ver_v = 0
            self.rect.bottom = ROCK_BOTTOM
            self.hav_jump = False
            self.jump_shoot = False
            self.isfall=False
        self.stay_time = 0

    def fall(self):
        self.ver_v=10

    def __image_run(self):

        # tick.tick(10)
        """if self.shooting:
            if self.runtime % 4 == 0:
                self.image = images.M23
            elif self.runtime % 4 == 1:
                self.image = images.M24
            elif self.runtime % 4 == 2:
                self.image = images.M25
            elif self.runtime % 4 == 3:
                self.image = images.M24
        else:
            if self.runtime % 4 == 0:
                self.image = images.M17
            elif self.runtime % 4 == 1:
                self.image = images.M18
            elif self.runtime % 4 == 2:
                self.image = images.M19
            elif self.runtime % 4 == 3:
                self.image = images.M18
        self.image = pygame.transform.flip(self.image, self.dir_Left, False)
        """
        self.runtime += 1
        self.rect.x += self.speed
        if self.attacked:
            self.be_attacked()

    def __move_left(self):
        """if self.shooting:
            self.image = images.M20
        else:
            self.image = images.M15
        self.image = pygame.transform.flip(self.image, self.dir_Left, False)
        """
        self.rect.x += self.speed
        # tick.tick(10)

    def __run(self):
        if self.speed == 15 or self.speed == -15:
            self.__image_run()

        elif self.speed != 0:
            self.__move_left()


    def shoot(self):
        global player2_can_shoot_num
        if player2_can_shoot_num > 0 and self.shootTime > 10:
            player2_can_shoot_num -= 1
            self.shootTime = 0
            self.shooting = True
            if self.dir_Left:
                bullet = Bullet2(True, self.rect.left - 40, self.rect.centery - 16)
                """self.image = pygame.transform.flip(self.image, True, False)"""
            else:
                bullet = Bullet2(False, self.rect.right + 20, self.rect.centery - 16)
            return bullet

    def be_attacked(self):
        """if self.attacked_time > 0:
            if self.attacked_time % 2 == 0:
                self.image = images.M21
                self.image = pygame.transform.flip(self.image, self.dir_Left, False)
            else:
                self.image = images.Z03
        else:
            self.attacked = False
            self.stay_time = 0
        """
        if self.attacked_time < 0:
            self.attacked = False
        self.attacked_time -= 1

    def update(self):
        self.shootTime += 1
        tmplist=[(self.rect.centerx-672) / 387, self.rect.centery / 100,
                                    player2_can_shoot_num, self.dir_Left*10, self.ver_v / 15, self.speed / 7.5,
                                    self.attacked_time / 10]
        RL2.player2_feature[0:7] =tmplist
        RL2.player1_feature[7:14] =tmplist

        if self.hav_jump:
            self.__jump()
        else:
            self.__stay()
            self.__run()
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 1344:
            self.rect.right = 1344
        if self.shootTime > 10:
            self.shooting = False


class Bullet1(RockManSprite):
    def __init__(self, dir_left, loca_x, loca_y):
        if dir_left:
            super().__init__()
            self.image = images.Z00
            self.speed = -25
        else:
            super().__init__()
            self.image = images.Z01
            self.speed = 25

        self.rect = self.image.get_rect()
        self.rect.x = loca_x
        self.rect.y = loca_y
        self.num = player1_can_shoot_num
        global player1_shootnum
        player1_shootnum += 1

    def update(self):
        self.rect.x += self.speed
        RL2.player2_feature[17 - self.num * 2:17 - self.num * 2 + 2] = [(self.rect.centerx-672)/387, self.rect.centery/100]
        global player1_can_shoot_num,player1_unshootnum
        if self.rect.left < 0:
            player1_can_shoot_num += 1
            player1_unshootnum += 1
            RL2.player2_feature[17 - self.num * 2:17 - self.num * 2 + 2] = [0, 0]
            self.kill()
        elif self.rect.right > 1344:
            player1_can_shoot_num += 1
            player1_unshootnum += 1
            RL2.player2_feature[17 - self.num * 2:17- self.num * 2 + 2] = [0, 0]
            self.kill()


class Bullet2(RockManSprite):
    def __init__(self, dir_left, loca_x, loca_y):
        if dir_left:
            super().__init__()
            self.image = images.Z00
            self.speed = -25
        else:
            super().__init__()
            self.image = images.Z01
            self.speed = 25

        self.rect = self.image.get_rect()
        self.rect.x = loca_x
        self.rect.y = loca_y
        self.num = player2_can_shoot_num
        global player2_shootnum
        player2_shootnum += 1

    def update(self):
        self.rect.x += self.speed
        RL2.player1_feature[17 - self.num * 2:17 - self.num * 2 + 2] = [(self.rect.centerx-672)/387, self.rect.centery/100]
        global player2_can_shoot_num,player2_unshootnum
        if self.rect.left < 0:
            player2_can_shoot_num += 1
            player2_unshootnum += 1
            RL2.player1_feature[17 - self.num * 2:17 - self.num * 2 + 2] = [0, 0]
            self.kill()
        elif self.rect.right > 1344:
            player2_can_shoot_num += 1
            RL2.player1_feature[17 - self.num * 2:17 - self.num * 2 + 2] = [0, 0]
            player2_unshootnum+=1
            self.kill()


class Blood1(RockManSprite):
    def __init__(self, id):
        super().__init__()
        self.image = images.Z02
        self.rect = self.image.get_rect()
        self.rect.x = 120
        self.id = id
        self.rect.y = 350 - id * 19

    def update(self):
        if self.id > player1_blood:
            self.kill()


class Blood2(RockManSprite):
    def __init__(self, id):
        super().__init__()
        self.image = images.Z02
        self.rect = self.image.get_rect()
        self.rect.x = 1187
        self.id = id
        self.rect.y = 350 - id * 19

    def update(self):
        if self.id > player2_blood:
            self.kill()
