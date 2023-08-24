import pgzrun

WIDTH = 800
HEIGHT = 600

all_bricks = []
broken_bricks = []
unbreakable_bricks = []
balls = []
lives = []
life_points = 3
score = 0
timer = 0

for x in range(0, 800, 200): #brique bleu
    for y in range(0, 210, 60):
        brick = Actor("brick_blue", anchor = ["left", "top"])
        brick.pos = [x, y]
        brick.color = "bleu"
        all_bricks.append(brick)

for x in range(100, 800, 200): #brique bleu 2
    for y in range(30, 210, 60):
        brick = Actor("brick_blue", anchor = ["left", "top"])
        brick.pos = [x, y]
        brick.color = "bleu"
        all_bricks.append(brick)

for x in range(100, 800, 200): #brique bleu clair cassé
    for y in range(0, 210, 60):
        brick = Actor("brick_light_blue_broken", anchor = ["left", "top"])
        brick.pos = [x, y]
        brick.color = None
        all_bricks.append(brick)

for x in range(0, 800, 200): #brique bleu clair cassé
    for y in range(30, 210, 60):
        brick = Actor("brick_light_blue_broken", anchor = ["left", "top"])
        brick.pos = [x, y]
        brick.color = None
        all_bricks.append(brick)

for x in range(50, 750, 300): #brique incassable
    for y in range(350, 380, 30):
        unbreakable = Actor("brick_unbreakable", anchor = ["left", "top"])
        unbreakable.pos = [x, y]
        brick.color = None
        unbreakable_bricks.append(unbreakable)

for x in range(660, 795, 45): #coeurs
    for y in range(555, 600, 50):
        life = Actor("life", anchor = ["left", "top"])
        life.pos = [x, y]
        lives.append(life)

# définir joueur + musique + balle
player = Actor("player")
player.pos = [400, 530]

music.play("musique_de_fond")

ball = Actor("ball")
ball.x = player.x
ball.y = player.y - 25
speed = 3
ball_speed = [speed, -speed]
balls.append(ball)

timer_is_running = False
click = False
lose_game = False
win_game = False

# mouvement souris
def on_mouse_move(pos):
    player.pos = [pos[0], player.pos[1]]

# inverser sens à l'impact
def invert_horizontal_speed():
    ball_speed[0] = ball_speed[0] * -1

def invert_vertical_speed():
    ball_speed[1] = ball_speed[1] * -1

def accelerate_ball():
    global speed
    if ball_speed == [speed, -speed]:
        ball_speed[0] = ball_speed[0] + 1
        ball_speed[1] = ball_speed[1] - 1
        speed = speed + 1
    if ball_speed == [-speed, -speed]:
        ball_speed[0] = ball_speed[0] - 1
        ball_speed[1] = ball_speed[1] - 1
        speed = speed + 1
    if ball_speed == [-speed, speed]:
        ball_speed[0] = ball_speed[0] - 1
        ball_speed[1] = ball_speed[1] + 1
        speed = speed + 1
    if ball_speed == [speed, speed]:
        ball_speed[0] = ball_speed[0] + 1
        ball_speed[1] = ball_speed[1] + 1
        speed = speed + 1

def on_mouse_down(pos):
    if player.collidepoint(pos):
        global click
        click = True

# rafraichissement 60 fps
def update():
    global score, timer, timer_is_running, lose_game, win_game, click, ball

    if click == True:
        new_x = ball.pos[0] + ball_speed[0]
        new_y = ball.pos[1] + ball_speed[1]

        ball.pos = [new_x, new_y]

        timer_is_running = True

    if click == False:
        ball.x = player.pos[0]
        ball.y = player.pos[1] - 25
            
    if timer_is_running == True:
        timer = timer + 1/60

        for i in range(int(timer) + 1):
            if round(timer, 3) == (i*10.000):
                score = score - 50
            if round(timer, 3) == (i*20.000):
                accelerate_ball()
                print(ball_speed)

    if ball.right >= WIDTH or ball.left < 0:
        invert_horizontal_speed()

    if ball.top < 0:
        invert_vertical_speed()

    if ball.colliderect(player):
        sounds.touch_paddle.play()
        invert_vertical_speed()

    for unbreakable in unbreakable_bricks: # briques incassables
        if ball.colliderect(unbreakable):
            sounds.grey_brick.play()
            invert_vertical_speed()

    for brick in broken_bricks: # retirer 1 vie brique cassée
        if ball.colliderect(brick):
            sounds.touch_brick.play()
            score = score + 100
            broken_bricks.remove(brick)
            invert_vertical_speed()

    for brick in all_bricks: # retirer 1 vie brique
        if ball.colliderect(brick):
            sounds.touch_brick.play()
            score = score + 100
            
            if brick.color == "bleu":
                brick_blue = Actor("brick_blue_broken", anchor = ["left", "top"])
                brick_blue.pos = brick.pos
                broken_bricks.append(brick_blue)

            all_bricks.remove(brick)
            invert_vertical_speed()

    if ball.bottom > HEIGHT and life_points == 0:
        lose_game = True
        click = False
        timer_is_running = False
        sounds.lose.play()
        
        
    if len(all_bricks) == 0 and len(broken_bricks) == 0:
        win_game = True
        click = False
        timer_is_running = False
        sounds.win.play()

# affichage
def draw():
    global score, life_points, ball, timer_is_running, lose_game

    screen.blit("background1", (-150, -250))
    screen.draw.text('Score: ' + str(score), fontname="score_font", midleft=[20, 570], color=("Red"), fontsize=20)
    screen.draw.text('Time: ' + str(round(timer, 1)), fontname="score_font", center=[400, 570], color=("Red"), fontsize=20)
    
    for brick in all_bricks:
        brick.draw()

    for unbreakable in unbreakable_bricks:
        unbreakable.draw()

    for brick in broken_bricks:
        brick.draw()

    player.draw()
    
    for ball in balls:
        ball.draw()
    
    for life in lives:
        life.draw()

    if lose_game == True:
        screen.clear()
        music.stop()
        screen.draw.text("Game Over\n", fontname="space_font", fontsize=90, center=[WIDTH / 2, HEIGHT / 2], color=("Red"))
        screen.draw.text("Score : " + str(score) + "\n", fontname="space_font", fontsize=40, center=[WIDTH / 2, 370], color=("Red"))
        screen.draw.text("Time : " + str(round(timer, 1)), fontname="space_font", fontsize=40, center=[WIDTH / 2, 400], color=("Red"))

    if win_game == True:
        screen.clear()
        music.stop()
        screen.draw.text("You win\n", fontname="space_font", fontsize=90, center=[WIDTH / 2, HEIGHT / 2], color=("Green"))
        screen.draw.text("Score : " + str(score) + "\n", fontname="space_font", fontsize=40, center=[WIDTH / 2, 370], color=("Green"))
        screen.draw.text("Time : " + str(round(timer, 1)), fontname="space_font", fontsize=40, center=[WIDTH / 2, 400], color=("Green"))
        
    if ball.bottom > HEIGHT and life_points > 0:
        sounds.lose_life.play()
        life_points = life_points - 1
        invert_vertical_speed()  
        lives.remove(life)

    if click == False and lose_game == False and win_game == False:
        screen.draw.text("Click on player to start", fontname="space_font", fontsize=30, center=[WIDTH / 2, HEIGHT / 2], color=("Red"))

# --- LAST LINE --- #
pgzrun.go()