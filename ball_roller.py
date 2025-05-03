from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random,math

# This is Game Constant
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 800
INTERVAL = 10
POSITIONS_LIST = [0, 2, -2]
BASE_SPEED = 0.3
MIN_SPEED = 0.1
MAX_SPEED = 2.0
BASE_BALL_COUNT = 1
LEVEL_SPEED_INCREASE = 0.2
LEVEL_BALL_INCREASE = 1
MAX_JUMP_HEIGHT = 2.5
MAX_LIVES = 5

#This is  Power-up Constants
POWERUP_TYPES = ["MAGNET", "HEART"]
POWERUP_SPAWN_RATE = 0.005
MAGNET_DURATION = 450

#This is  Level Constants
BASE_LEVEL_LENGTH = -600
LEVEL_LENGTH_INCREMENT = -200

#This is  Game State
LAST_PLAY = False
START_GAME = False
AT_START = True
PLAY = False
BEGIN = True
POINTS = 0
LEVEL = 1
DEAD = False
PAUSE = False
LEVEL_UP = False
GO_NEXT_LEVEL = False
INC_LEVEL = False
ENTERED_NEXT_LEVEL = False
CHEAT_MODE = False
LIVES = 3
INVINCIBLE = False
INVINCIBLE_TIMER = 0
active_powerups = []
powerups = []
level_finish_z = BASE_LEVEL_LENGTH
color_changed_in_level = False
DAY_MODE = True  # starting with day view

DAY_BG_COLOR = [0.53, 0.81, 0.98, 1.0]  # Sky blue
NIGHT_BG_COLOR = [0.05, 0.05, 0.15, 1.0]  # Dark blue
DAY_ROAD_COLOR = [0.2, 0.2, 0.2]  # Dark gray
NIGHT_ROAD_COLOR = [0.1, 0.1, 0.1]  # Very dark gray
DAY_STAR_COLOR = [1.0, 1.0, 1.0]  # White
NIGHT_STAR_COLOR = [1.0, 1.0, 0.8]  # Bright yellow

# Ball  color
MAIN_BALL_COLOR = [232 / 255, 99 / 255, 10 / 255]
MAIN_BALL_Y = 0
MAIN_BALL_CURR_X = 0
MAIN_BALL_NEXT_X = 0
DIREC = "STOP"
JUMPING = False
NEXT_JUMP = False
FALLING = False
BALL_ROT_ANGLE = 0

# Camera position
CAMERA_THIRD_PERSON = 0
CAMERA_FIRST_PERSON = 1
current_camera = CAMERA_THIRD_PERSON
FP_CAMERA_OFFSET = (0, 0.5, 0.8)

# Environment setup
WALL_Z = -140
SHOW_WALL = False
WALL_COLOR = [84 / 255, 99 / 255, 255 / 255]
FINISH_Z = -400
ROAD_DELTA_Z = 0
STARS_DELTA_Y = 0
ROT_ANGLE = 0
ROT_DIREC = 1

# Stars in night view
STARS_POSITIONS = [(random.uniform(-2, 2), random.uniform(-3, 3)) for _ in range(100)]
COLORS_LIST = [
    [232 / 255, 99 / 255, 10 / 255],
    [248 / 255, 6 / 255, 204 / 255],
    [84 / 255, 99 / 255, 255 / 255]
]


class Ball:
    def __init__(self, x, y, z, radius, color):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius
        self.color = color
        self.scale = [0.5, 0.5, 0.5]

    def draw(self):
        glColor3f(*self.color)
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glScale(*self.scale)
        glutSolidSphere(1, 20, 10)
        glPopMatrix()


class Powerup:
    def __init__(self, z_pos):
        self.type = random.choice(POWERUP_TYPES)
        self.x = random.choice(POSITIONS_LIST)
        self.z = z_pos
        self.collected = False
        self.rotation = 0
        self.scale = 0.6 if self.type == "HEART" else 0.4

    def draw(self):
        if not self.collected:
            glPushMatrix()
            glTranslatef(self.x, 0.5, self.z)
            glRotatef(self.rotation, 0, 1, 0)
            glScalef(self.scale, self.scale, self.scale)

            if self.type == "MAGNET":
                glColor3f(0, 0.8, 1)  # Cyan
                glutSolidTorus(0.2, 0.5, 10, 20)
            elif self.type == "HEART":
                glColor3f(1, 0, 0)  # Red
                # Draw heart shape
                glBegin(GL_TRIANGLE_FAN)
                glVertex2f(0, 0.3)
                glVertex2f(-0.3, 0.1)
                glVertex2f(-0.2, -0.2)
                glVertex2f(0, -0.1)
                glVertex2f(0.2, -0.2)
                glVertex2f(0.3, 0.1)
                glEnd()

            glPopMatrix()
            self.rotation = (self.rotation + 2) % 360


BALLS_LIST = [Ball(0, 0, -100, 0.5, COLORS_LIST[0])]


def setupCamera():
    global current_camera, MAIN_BALL_CURR_X, MAIN_BALL_Y

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.25, 0.1, 1000)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if current_camera == CAMERA_THIRD_PERSON:
        gluLookAt(0, 3.5, 10, 0, 0, 0, 0, 1, 0)
    else:
        eye_x = MAIN_BALL_CURR_X + FP_CAMERA_OFFSET[0]
        eye_y = MAIN_BALL_Y + FP_CAMERA_OFFSET[1]
        eye_z = 4 + FP_CAMERA_OFFSET[2]
        gluLookAt(eye_x, eye_y, eye_z, eye_x, eye_y, eye_z - 1, 0, 1, 0)


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def reset():
    global ROAD_DELTA_Z, POINTS, MAIN_BALL_Y, LEVEL, MAIN_BALL_CURR_X, MAIN_BALL_NEXT_X
    global DIREC, JUMPING, WALL_Z, SHOW_WALL, WALL_COLOR, DEAD, STARS_DELTA_Y
    global MAIN_BALL_COLOR, START_GAME, NEXT_JUMP, FALLING, PAUSE, ROT_ANGLE
    global FINISH_Z, LEVEL_UP, ROT_DIREC, GO_NEXT_LEVEL, INC_LEVEL, ENTERED_NEXT_LEVEL, BALL_ROT_ANGLE
    global BASE_SPEED, BASE_BALL_COUNT, CHEAT_MODE, LIVES, INVINCIBLE, INVINCIBLE_TIMER
    global active_powerups, powerups, level_finish_z, color_changed_in_level, DAY_MODE

    ROAD_DELTA_Z = 0
    POINTS = 0
    MAIN_BALL_Y = 0
    LEVEL = 1
    MAIN_BALL_CURR_X = 0
    MAIN_BALL_NEXT_X = 0
    DIREC = "STOP"
    JUMPING = False
    NEXT_JUMP = False
    FALLING = False
    WALL_Z = -140
    SHOW_WALL = False
    WALL_COLOR = [84 / 255, 99 / 255, 255 / 255]
    DEAD = False
    STARS_DELTA_Y = 0
    START_GAME = True
    BALLS_LIST.clear()
    BALLS_LIST.append(Ball(0, 0, -100, 0.5, COLORS_LIST[0]))
    MAIN_BALL_COLOR = COLORS_LIST[0]
    PAUSE = False
    ROT_ANGLE = 0
    level_finish_z = BASE_LEVEL_LENGTH
    LEVEL_UP = False
    INC_LEVEL = False
    GO_NEXT_LEVEL = False
    ENTERED_NEXT_LEVEL = False
    ROT_DIREC = 1
    BALL_ROT_ANGLE = 0
    BASE_SPEED = 0.3
    BASE_BALL_COUNT = 1
    CHEAT_MODE = False
    LIVES = 3
    INVINCIBLE = False
    INVINCIBLE_TIMER = 0
    active_powerups = []
    powerups = []
    color_changed_in_level = False
    DAY_MODE = True  # Reset to day mode


def draw_road():
    if DAY_MODE:
        glColor3f(*DAY_ROAD_COLOR)
    else:
        glColor3f(*NIGHT_ROAD_COLOR)
    glBegin(GL_QUADS)
    glVertex3f(-3, -0.5, -20000 + ROAD_DELTA_Z)
    glVertex3f(-3, -0.5, 100 + ROAD_DELTA_Z)
    glVertex3f(3, -0.5, 100 + ROAD_DELTA_Z)
    glVertex3f(3, -0.5, -20000 + ROAD_DELTA_Z)
    glEnd()


def draw_stars():
    if DAY_MODE:
        glColor3f(*DAY_STAR_COLOR)
    else:
        glColor3f(*NIGHT_STAR_COLOR)
    glPointSize(2)
    glBegin(GL_POINTS)
    for x, y in STARS_POSITIONS:
        glVertex2f(x, y - STARS_DELTA_Y)
    glEnd()


def draw_main_ball():
    if current_camera == CAMERA_THIRD_PERSON:
        glColor3f(*MAIN_BALL_COLOR)
        glPushMatrix()
        glTranslatef(MAIN_BALL_CURR_X, MAIN_BALL_Y, 4)
        glRotatef(BALL_ROT_ANGLE, 1, 0, 0)
        glutWireSphere(0.5, 30, 10)
        glPopMatrix()


def draw_wall(z):
    glColor3f(*WALL_COLOR)
    glPushMatrix()
    glTranslate(0, 0, z)
    glScale(6, 1, 1)
    glutSolidCube(1)
    glPopMatrix()


def change_wall_color():
    global WALL_COLOR
    colors_except_curr = [c for c in COLORS_LIST if c != MAIN_BALL_COLOR]
    WALL_COLOR = random.choice(colors_except_curr)


def get_wall():
    global POINTS, WALL_Z, SHOW_WALL, MAIN_BALL_COLOR, DEAD, color_changed_in_level

    draw_wall(WALL_Z)

    if START_GAME and not color_changed_in_level:
        if POINTS % 25 == 0 and POINTS != 0:
            SHOW_WALL = True

        if SHOW_WALL:
            WALL_Z = min(WALL_Z + 1, 10)

        if WALL_Z == 4:
            MAIN_BALL_COLOR = WALL_COLOR.copy()
            WALL_Z = -140
            SHOW_WALL = False
            change_wall_color()
            color_changed_in_level = True


def move_main_ball():
    global MAIN_BALL_CURR_X, MAIN_BALL_NEXT_X, MAIN_BALL_Y, JUMPING, NEXT_JUMP, FALLING

    # Horizontal movement
    if DIREC == "LEFT":
        MAIN_BALL_CURR_X = max(MAIN_BALL_CURR_X - 0.2, MAIN_BALL_NEXT_X)
    elif DIREC == "RIGHT":
        MAIN_BALL_CURR_X = min(MAIN_BALL_CURR_X + 0.2, MAIN_BALL_NEXT_X)

    # Jump
    if NEXT_JUMP and not JUMPING and not FALLING:
        JUMPING = True
        NEXT_JUMP = False
        MAIN_BALL_Y = 0.1

    # Enhanced jump higher maximum height
    if JUMPING:
        if not FALLING:
            MAIN_BALL_Y += 0.15
            if MAIN_BALL_Y >= MAX_JUMP_HEIGHT:
                FALLING = True
        else:
            MAIN_BALL_Y -= 0.15
            if MAIN_BALL_Y <= 0:
                MAIN_BALL_Y = 0
                JUMPING = False
                FALLING = False


def handle_powerups():
    global powerups, active_powerups, LIVES

    #new powerups
    if random.random() < POWERUP_SPAWN_RATE and not LEVEL_UP and not DEAD:
        powerups.append(Powerup(-50))

    # Update and draw powerups
    for p in powerups[:]:
        if not p.collected:
            p.z += BASE_SPEED * (1 + LEVEL / 10)
            p.draw()

            # Collision detection condition
            if (abs(p.z - 4) < 0.8 and abs(MAIN_BALL_CURR_X - p.x) < 0.8):
                p.collected = True

                if p.type == "MAGNET":
                    active_powerups.append({"type": p.type, "timer": MAGNET_DURATION})
                elif p.type == "HEART":
                    LIVES = min(LIVES + 1, MAX_LIVES)

                powerups.remove(p)
        elif p.z > 10:
            powerups.remove(p)

    # Update active powerups
    for p in active_powerups[:]:
        p["timer"] -= 1
        if p["timer"] <= 0:
            active_powerups.remove(p)


def ball_generation():
    global POINTS, DEAD, CHEAT_MODE, LIVES, INVINCIBLE, INVINCIBLE_TIMER

    magnet_active = any(p["type"] == "MAGNET" for p in active_powerups)

    for ball in BALLS_LIST:
        ball.draw()

        if START_GAME and not DEAD and not LEVEL_UP:
            ball.z += BASE_SPEED * (1 + LEVEL / 10)

            # Magnet effect - auto-attract same color balls
            if magnet_active and ball.color == MAIN_BALL_COLOR:
                ball.x = MAIN_BALL_CURR_X * 0.95 + ball.x * 0.05  # Smooth attraction

            if (abs(ball.z - 4) < 0.5 and
                    abs(MAIN_BALL_Y - ball.y) < 0.5 and
                    abs(MAIN_BALL_CURR_X - ball.x) < 0.5):

                if CHEAT_MODE:
                    POINTS += 2
                    ball.x = random.choice(POSITIONS_LIST)
                    ball.z = -100 * (BALLS_LIST.index(ball) + 1)
                else:
                    if ball.color == MAIN_BALL_COLOR:
                        POINTS += 1
                        ball.x = random.choice(POSITIONS_LIST)
                        ball.z = -100 * (BALLS_LIST.index(ball) + 1)
                    else:
                        if not INVINCIBLE:
                            LIVES -= 1
                            if LIVES <= 0:
                                DEAD = True
                            else:
                                INVINCIBLE = True
                                INVINCIBLE_TIMER = 60
                        ball.x = random.choice(POSITIONS_LIST)
                        ball.z = -100 * (BALLS_LIST.index(ball) + 1)
            elif ball.z > 7:
                ball.x = random.choice(POSITIONS_LIST)
                ball.z = -100 * (BALLS_LIST.index(ball) + 1)
                ball.color = random.choice(COLORS_LIST)


def draw_checkerboard():
    glBegin(GL_QUADS)
    for i in range(-3, 3):
        for j in range(-5, 5):
            if (i + j) % 2 == 0:
                glColor3f(1, 1, 1)
            else:
                glColor3f(0, 0, 0)
            glVertex3f(i, -0.49, j + FINISH_Z)
            glVertex3f(i + 1, -0.49, j + FINISH_Z)
            glVertex3f(i + 1, -0.49, j + 1 + FINISH_Z)
            glVertex3f(i, -0.49, j + 1 + FINISH_Z)
    glEnd()


def draw_interface():
    # cheat mode indicator
    if CHEAT_MODE:
        draw_text(WINDOW_WIDTH - 200, WINDOW_HEIGHT - 30, "CHEAT MODE ACTIVE", GLUT_BITMAP_HELVETICA_18)

    # invincibility indicator
    if INVINCIBLE:
        draw_text(WINDOW_WIDTH - 200, WINDOW_HEIGHT - 60, "INVINCIBLE!", GLUT_BITMAP_HELVETICA_18)

    #active powerups
    if active_powerups:
        draw_text(WINDOW_WIDTH - 200, WINDOW_HEIGHT - 90,
                  f"Active: {', '.join(p['type'] for p in active_powerups)}",
                  GLUT_BITMAP_HELVETICA_12)

    #day/night mode indicator
    mode_text = "DAY MODE" if DAY_MODE else "NIGHT MODE"
    draw_text(WINDOW_WIDTH - 200, WINDOW_HEIGHT - 120, mode_text, GLUT_BITMAP_HELVETICA_12)

    #lives
    for i in range(LIVES):
        glPushMatrix()
        glTranslatef(WINDOW_WIDTH - 50 - (i * 30), WINDOW_HEIGHT - 30, 0)
        glColor3f(1, 0, 0)  # Red
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(0, 0.3)
        glVertex2f(-0.3, 0.1)
        glVertex2f(-0.2, -0.2)
        glVertex2f(0, -0.1)
        glVertex2f(0.2, -0.2)
        glVertex2f(0.3, 0.1)
        glEnd()
        glPopMatrix()

    # Game state messages
    if DEAD:
        draw_text(WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2, "GAME OVER! Press F1 to restart",
                  GLUT_BITMAP_TIMES_ROMAN_24)
    elif PAUSE:
        draw_text(WINDOW_WIDTH / 2 - 80, WINDOW_HEIGHT / 2, "PAUSED - F1 to continue", GLUT_BITMAP_TIMES_ROMAN_24)
    elif LEVEL_UP:
        draw_text(WINDOW_WIDTH / 2 - 120, WINDOW_HEIGHT / 2, f"LEVEL {LEVEL} COMPLETE! F1 to continue",
                  GLUT_BITMAP_TIMES_ROMAN_24)
    elif GO_NEXT_LEVEL:
        draw_text(WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2,
                  f"STARTING LEVEL {LEVEL}...",
                  GLUT_BITMAP_TIMES_ROMAN_24)


def keyboardListener(key, x, y):
    global current_camera, NEXT_JUMP, PAUSE, START_GAME, PLAY, DEAD, LEVEL_UP, GO_NEXT_LEVEL, CHEAT_MODE, BASE_SPEED, DAY_MODE

    key = key.decode('utf-8').lower()

    if key == 'v':
        current_camera = CAMERA_FIRST_PERSON if current_camera == CAMERA_THIRD_PERSON else CAMERA_THIRD_PERSON
    elif key == ' ':
        NEXT_JUMP = True
    elif key == '\x1b':
        glutLeaveMainLoop()
    elif key == 'c':
        CHEAT_MODE = not CHEAT_MODE
        print(f"Cheat mode {'ON' if CHEAT_MODE else 'OFF'}")
    elif key == '8':  # Increase speed
        BASE_SPEED = min(BASE_SPEED + 0.1, MAX_SPEED)
        print(f"Speed increased to: {BASE_SPEED:.1f}")
    elif key == '2':  # Decrease speed
        BASE_SPEED = max(BASE_SPEED - 0.1, MIN_SPEED)
        print(f"Speed decreased to: {BASE_SPEED:.1f}")
    elif key == '5':  # Toggle day/night mode
        DAY_MODE = not DAY_MODE
        print(f"Switched to {'DAY' if DAY_MODE else 'NIGHT'} mode")
        # Clear the screen to apply new background color
        if DAY_MODE:
            glClearColor(*DAY_BG_COLOR)
        else:
            glClearColor(*NIGHT_BG_COLOR)
        glutPostRedisplay()


def specialKeyListener(key, x, y):
    global MAIN_BALL_NEXT_X, DIREC, PAUSE, START_GAME, PLAY, DEAD, LEVEL_UP, GO_NEXT_LEVEL

    if key == GLUT_KEY_F1:
        if DEAD:
            reset()
        elif LEVEL_UP:
            GO_NEXT_LEVEL = True
            LEVEL_UP = False
        PAUSE = False
        PLAY = True
        START_GAME = True
    elif key == GLUT_KEY_F2:
        PAUSE = not PAUSE
        START_GAME = not PAUSE
    elif key == GLUT_KEY_LEFT:
        MAIN_BALL_NEXT_X = max(MAIN_BALL_NEXT_X - 2, -2)
        DIREC = "LEFT"
    elif key == GLUT_KEY_RIGHT:
        MAIN_BALL_NEXT_X = min(MAIN_BALL_NEXT_X + 2, 2)
        DIREC = "RIGHT"
    elif key == GLUT_KEY_UP:
        NEXT_JUMP = True


def update_game():
    global FINISH_Z, ROAD_DELTA_Z, STARS_DELTA_Y, BALL_ROT_ANGLE
    global LEVEL_UP, INC_LEVEL, ENTERED_NEXT_LEVEL, LEVEL, GO_NEXT_LEVEL
    global BASE_SPEED, BASE_BALL_COUNT, INVINCIBLE, INVINCIBLE_TIMER
    global level_finish_z, color_changed_in_level

    if START_GAME and not PAUSE:
        if INVINCIBLE:
            INVINCIBLE_TIMER -= 1
            if INVINCIBLE_TIMER <= 0:
                INVINCIBLE = False

        if not LEVEL_UP:
            if FINISH_Z < 2.5:
                FINISH_Z = min(FINISH_Z + (0.3 * (1 + LEVEL / 10)), 2.5)
                ROAD_DELTA_Z += (0.3 * (1 + LEVEL / 10))
                STARS_DELTA_Y += (0.0005 * (1 + LEVEL / 10))
                BALL_ROT_ANGLE += (5 * (1 + LEVEL / 10))

            if FINISH_Z >= 2.5 and not ENTERED_NEXT_LEVEL:
                LEVEL_UP = True
                INC_LEVEL = True
                ENTERED_NEXT_LEVEL = True

        if GO_NEXT_LEVEL:
            if INC_LEVEL:
                LEVEL += 1
                INC_LEVEL = False

            BASE_SPEED += LEVEL_SPEED_INCREASE
            BASE_BALL_COUNT = min(BASE_BALL_COUNT + LEVEL_BALL_INCREASE, 5)
            level_finish_z = BASE_LEVEL_LENGTH + (LEVEL - 1) * LEVEL_LENGTH_INCREMENT

            FINISH_Z = level_finish_z
            ROAD_DELTA_Z = 0
            BALL_ROT_ANGLE = 0
            WALL_Z = -140
            SHOW_WALL = False
            color_changed_in_level = False

            change_wall_color()

            BALLS_LIST.clear()
            for i in range(BASE_BALL_COUNT):
                BALLS_LIST.append(Ball(
                    random.choice(POSITIONS_LIST),
                    0,
                    -100 * (i + 1),
                    0.5,
                    random.choice(COLORS_LIST)
                ))

            GO_NEXT_LEVEL = False
            ENTERED_NEXT_LEVEL = False


def showScreen():
    # Set background color based on day/night mode
    if DAY_MODE:
        glClearColor(*DAY_BG_COLOR)
    else:
        glClearColor(*NIGHT_BG_COLOR)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    setupCamera()

    draw_stars()
    draw_road()
    draw_checkerboard()

    draw_main_ball()
    ball_generation()
    get_wall()
    handle_powerups()

    # Display
    draw_text(20, WINDOW_HEIGHT - 30, f"Score: {POINTS}")
    draw_text(20, WINDOW_HEIGHT - 60, f"Level: {LEVEL}")
    draw_text(20, WINDOW_HEIGHT - 90, "Controls: Arrows=Move, Space=Jump, V=Toggle View")
    draw_text(20, WINDOW_HEIGHT - 120, "F1=Start/Pause/Continue, F2=Pause")
    draw_text(20, WINDOW_HEIGHT - 150, "C=Cheat Mode, 8=Speed+, 2=Speed-, 5=Day/Night")
    draw_text(20, WINDOW_HEIGHT - 180, f"Current Speed: {BASE_SPEED:.1f} (Min {MIN_SPEED}, Max {MAX_SPEED})")
    draw_text(20, WINDOW_HEIGHT - 210, f"Lives: {LIVES} (Max {MAX_LIVES})")
    draw_text(20, WINDOW_HEIGHT - 240,
              f"Level Progress: {int((FINISH_Z - level_finish_z) / (2.5 - level_finish_z) * 100)}%")

    draw_interface()

    if START_GAME and not PAUSE and not LEVEL_UP:
        move_main_ball()
        update_game()

    glutSwapBuffers()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"3D Ball Roller Game")

    glEnable(GL_DEPTH_TEST)
    glClearColor(*DAY_BG_COLOR)

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutIdleFunc(lambda: glutPostRedisplay())

    reset()
    glutMainLoop()


if __name__ == "__main__":
    main()
