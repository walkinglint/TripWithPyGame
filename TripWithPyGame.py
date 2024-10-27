import pygame
import colorsys
from random import random, randrange, uniform
from math import cos, pi, sin
import gc

# 初期設定
pygame.init()
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
clock = pygame.time.Clock()

circles = []
clss = []
cn = 0
nc = 1
nel = 100
elidx = 0
nl = []

def mp(v, ol, oh, nl, nh):
    return nl + (v - ol) * (nh - nl) / (oh - ol)

class Circle():
    def __init__(self, hue, parent):
        self.color = tuple(int(c * 255) for c in colorsys.hsv_to_rgb(hue, 1, 1))
        self.parent = parent
        circles.append(self)
    def set_location(self, loc):
        self.loc = loc
    def set_r(self, r):
        self.r = r
    def draw(self):
        x, y = self.parent.loc
        lx, ly = self.loc
        pygame.draw.circle(screen, self.color, (int(x + lx), int(y + ly)), int(self.r), 1)

class Circles():
    def __init__(self, depth, loc, n, clsr, r, hue, da, ira, dra, icra, dcra):
        global elidx
        self.loc = loc
        self.n = n
        self.clsr = clsr
        self.r = r
        self.hue = hue
        self.da = da
        self.dra = dra
        self.dcra = dcra
        self.a = 0
        self.ra = ira
        self.cra = icra
        self.cls = []
        self.clss = []
        r1 = randrange(3, 20)
        r2 = randrange(2, 500)
        r3 = randrange(50, 300)
        elidx += 1
        if nel <= elidx:
            elidx = 0
            init_pn()
        r4 = nl[elidx]
        elidx += 1
        r5 = uniform(-1, 1) / 15
        r6 = uniform(0, 2 * pi)
        r7 = uniform(-1, 1) / 30
        r8 = uniform(0, 2 * pi)
        r9 = uniform(-1, 1) / 30
        for i in range(n):
            if 0 < depth:
                a = 2 * pi * i / n
                r = min(screen_width, screen_height) // 2  # 画面サイズに合わせてスケーリング
                p = (r * cos(a), r * sin(a))
                clss.append(Circles(depth - 1, p, r1, r2, r3, r4, r5, r6, r7, r8, r9))
            self.cls.append(Circle(self.hue, self))
    def set_location(self, loc):
        self.loc = loc
    def update(self):
        for i in range(self.n):
            c = self.cls[i]
            a = 2 * pi * i / self.n + self.a
            r = self.clsr * (1 + cos(self.ra)) / 2
            c.set_location((r * cos(a), r * sin(a)))
            cr = self.r * (2 + cos(self.cra)) / 2
            c.set_r(cr)
        self.a += self.da
        self.ra += self.dra
        self.cra += self.dcra

def init_pn():
    global nl
    nl = [random() for _ in range(nel)]

def main():
    global cn
    init_pn()
    clss.append(Circles(1, (0, 0), randrange(3, 20), randrange(2, 500), randrange(50, 300), nl[elidx], uniform(-1, 1) / 15, uniform(0, 2 * pi), uniform(-1, 1) / 30, uniform(0, 2 * pi), uniform(-1, 1) / 30))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                running = False  # 任意のキーまたはマウスクリックで終了
        screen.fill((0, 0, 0))  # 毎フレーム背景を黒に設定
        cn += 1
        if cn % 40 == 0:
            clss.clear()
            del circles[:]  # 不要なオブジェクトを削除
            gc.collect()  # ガベージコレクションを実行
            screen.fill((0, 0, 0))  # 新しいパラメータで描画を始めるときに背景を黒に設定
            init_pn()
            clss.append(Circles(1, (0, 0), randrange(3, 20), randrange(2, 500), randrange(50, 300), nl[elidx], uniform(-1, 1) / 15, uniform(0, 2 * pi), uniform(-1, 1) / 30, uniform(0, 2 * pi), uniform(-1, 1) / 30))
        for cls in clss:
            cls.update()
        for c in circles:
            # 描画の中心を画面の中央に固定し、画面全体に広がるようにスケーリング
            c.set_location((c.loc[0] + screen_width // 2, c.loc[1] + screen_height // 2))
            c.draw()
        pygame.display.flip()
        clock.tick(30)  # フレームレートを調整して表示タイミングを調整

if __name__ == '__main__':
    main()
    pygame.quit()