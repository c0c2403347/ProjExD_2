import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect or ばくだんRect
    戻り値：判定結果タプル（横方向，縦方向）
    画面内ならTrue／画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向にはみ出ていたら
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: # 縦方向にはみ出ていたら
        tate = False
    return yoko, tate

def game_over(screen: pg.Surface) -> None:
   
    # 黒いSurfaceを半透明で作成
    over_sfc = pg.Surface((WIDTH, HEIGHT))
    over_sfc.fill((0, 0, 0))
    over_sfc.set_alpha(200)

    # 「Game Over」テキスト
    font = pg.font.Font(None, 100)
    text_sfc = font.render("Game Over", True, (255, 255, 255))
    text_rct = text_sfc.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))

    # 泣いているこうかとん画像（5.pngなど）
    cry_img = pg.transform.rotozoom(pg.image.load("fig/5.png"), 0, 0.9)
    cry_img2 = pg.transform.rotozoom(pg.image.load("fig/5.png"), 0, 0.9)

    padding = 20  
    cry_rct = cry_img.get_rect()
    cry_rct2 = cry_img2.get_rect()

    # テキストの左端・右端を取得
    text_left = text_rct.left
    text_right = text_rct.right
    text_center_y = text_rct.centery

    # 左こうかとんをテキストの左側に配置
    cry_rct.right = text_left - padding
    cry_rct.centery = text_center_y
    # 右こうかとんをテキストの右側に配置
    cry_rct2.left = text_right + padding
    cry_rct2.centery = text_center_y



    # 描画
    screen.blit(over_sfc, (0, 0))
    screen.blit(text_sfc, text_rct)
    screen.blit(cry_img, cry_rct)
    screen.blit(cry_img, cry_rct2)
    
    pg.display.update()
    time.sleep(5)

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:

    bb_imgs = []
    bb_accs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r))
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
        bb_accs.append(r)
    return bb_imgs, bb_accs


def main():

    bb_imgs, bb_accs = init_bb_imgs()
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  # 爆弾用の空Surface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 赤い爆弾円
    bb_img.set_colorkey((0, 0, 0))  # 四隅の黒い部分を透過
    bb_rct = bb_img.get_rect()  # 爆弾Rect
    bb_rct.centerx = random.randint(0, WIDTH)  # 爆弾横座標
    bb_rct.centery = random.randint(0, HEIGHT)  # 爆弾縦座標
    vx, vy = +5, +5  # 爆弾の速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
    
        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bb_rct):  # こうかとんと爆弾の衝突判定

            game_over(screen)

            return  # ゲームオーバー
        
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  # 横方向の移動量を加算
                sum_mv[1] += mv[1]  # 縦方向の移動量を加算
        # if key_lst[pg.K_w]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        idx = min(tmr // 500, 9)  # 段階的に選択
        bb_img =   bb_imgs[idx]
        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]
        bb_rct.move_ip(avx, avy)

        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出ていたら
            vx *= -1
        if not tate:  # 縦方向にはみ出ていたら
            vy *= -1
        screen.blit(bb_img, bb_rct)  # 爆弾描画
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()