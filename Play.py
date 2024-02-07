from Board import Game
import sys
import pygame
import time

class Node:
    def __init__(self, currentState):
        self.Current = currentState
        self.CurrentScore = 0
        self.children = {}

    def Make(self, i, j, player):
        self.children[(i, j)] = Node(self.Current.Get_currentState())
        mul = 1
        if player:
            mul *= -1
        self.children[(i, j)].CurrentScore = (self.children[(i, j)].Current.action(i, j) * mul) + self.CurrentScore


class Play: 
    def __init__(self, Board_Xdim, Board_Ydim, Ply_num):
        currentState = Game([], Board_Xdim, Board_Ydim)
        currentState.Initiate()
        self.State = Node(currentState)
        self.Ply_num = Ply_num
        self.Score = 0
        
    def miniMax(self, State, Ply_num): 

        for i in range(State.Current.dimY):
            for j in range(State.Current.dimX):
                if State.Current.Mat[i][j] == ' ' and (j, i) not in State.children:
                    State.Make(j, i, True)
                    if Ply_num < 2:
                        return (i, j)

        Minimum_Score = 1000
        i = 0
        j = 0
        for k, z in State.children.items():
            Result = self.Maximum(z, Ply_num - 1, Minimum_Score)
            if Minimum_Score > Result:
                Minimum_Score = Result
                i = k[0]
                j = k[1]

        return (i, j)


    def Maximum(self, State, Ply_num, Alpha):
        if Ply_num == 0:
            return State.CurrentScore

        for i in range(State.Current.dimY):
            for j in range(State.Current.dimX):
                if State.Current.Mat[i][j] == ' ' and (j, i) not in State.children:
                    State.Make(j, i, False)

        Maximum_Score = -1000
        i = 0
        j = 0
        for k, z in State.children.items():
            Result = self.Minimum(z, Ply_num - 1, Maximum_Score)
            if Maximum_Score < Result:
                Maximum_Score = Result
            if Result > Alpha:
                return Result

        return Maximum_Score


    def Minimum(self, State, Ply_num, Beta): 
        if Ply_num == 0:
            return State.CurrentScore

        for i in range(State.Current.dimY):
            for j in range(State.Current.dimX):
                if State.Current.Mat[i][j] == ' ' and (j, i) not in State.children:
                    State.Make(j, i, True)

        Minimum_Score = 1000
        i = 0
        j = 0
        for k, z in State.children.items():
            Result = self.Maximum(z, Ply_num - 1, Minimum_Score)
            if Minimum_Score > Result:
                Minimum_Score = Result
            if Result < Beta:
                return Result

        return Minimum_Score

    def Human(self, a, b): 
        HumanY, HumanX = self.State.Current.Show_board(self.State.CurrentScore, a, b)
        

        if (HumanX, HumanY) not in self.State.children:
            self.State.Make(HumanX, HumanY, False)
            self.State = self.State.children[(HumanX, HumanY)]
        else:
            self.State = self.State.children[(HumanX, HumanY)]

        print("Current Score =====>> Your Score - AI Score = " + str(self.State.CurrentScore),end ="\n\n\n")

        self.Computer()


    def Computer(self): 
        
        move = self.miniMax(self.State, self.Ply_num)
        
        self.State = self.State.children[(move[0], move[1])]

        print("AI selected the following coordinates to play:\n" + "(" ,str(move[0]), ", " + str(move[1]), ")", end = "\n\n")

        print("Current Score =====>> Your Score - AI Score = " + str(self.State.CurrentScore), end = "\n\n\n")

        if len(self.State.children) == 0:
            # pygame.init()

            cell_size = 50
            rows = self.State.Current.dimX  
            cols = self.State.Current.dimY  
            width = rows * 80
            height = cols * 80
            window = pygame.display.set_mode((width, height))
            pygame.display.set_caption("Cap the cells!!!")
            
            grid_width = cols * cell_size
            grid_height = rows * cell_size
            x_offset = (width - grid_width) // 2
            y_offset = (height - grid_height) // 2
            
            WHITE = (255, 255, 255)
            BLACK = (0, 0, 0)
            GREY = (110, 110, 110)
            CLICKED_GREY = (80, 80, 80)
            
            matrix = self.State.Current.Mat
            
            cell_color = [[GREY if matrix[i][j] != '*' else BLACK for j in range(cols)] for i in range(rows)]
            cell_color[move[0]][move[1]] = CLICKED_GREY
            
            running = True
            start_time = time.time()
            
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
            
                if time.time() - start_time >= 1:
                    running = False
            
                window.fill(WHITE)
                for row in range(rows):
                    for col in range(cols):
                        cell_rect = pygame.Rect(col * cell_size + x_offset, row * cell_size + y_offset, cell_size, cell_size)
                        pygame.draw.rect(window, cell_color[row][col], cell_rect)
                        cell_text = pygame.font.SysFont(None, 24).render(str(matrix[row][col]), True, WHITE)
                        text_rect = cell_text.get_rect(center=(col * cell_size + x_offset + cell_size // 2, row * cell_size + y_offset + cell_size // 2))
                        window.blit(cell_text, text_rect)
                        score_text = pygame.font.SysFont(None, 30).render(("Your Score - AI Score = " + str(self.State.CurrentScore)), True, BLACK)
                        score_rect = score_text.get_rect()
                        score_rect.topright = (width - 10, 10)
                        window.blit(score_text, score_rect)
            
                pygame.display.flip()
            
            pygame.quit()
            self.Evaluation()
            return
        self.Human(move[0], move[1])

    def Evaluation(self):
        pygame.init()
        rows = self.State.Current.dimX  
        cols = self.State.Current.dimY
        depth = self.Ply_num
        width = rows * 80
        height = cols * 80
        font = pygame.font.Font(None, 36)
        display = pygame.display.set_mode((width, height))
        alpha = 0  # Initial alpha value for fade-in effect
        fade_speed = 3  # Speed of the fade-in effect
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                    if event.key == pygame.K_r:
                        Match = Play(cols, rows, depth)
                        Match.start()

            if self.State.CurrentScore < 0:
                text = font.render("AI Won!", True, (255, 255, 255, alpha))
                text2 = font.render("Press 'r' to Reset!", True, (255, 255, 255, alpha))
            elif self.State.CurrentScore > 0:
                text = font.render("You Won!", True, (207, 188, 188, alpha))
                text2 = font.render("Press 'r' to Reset!", True, (207, 188, 188, alpha))
            else:
                text = font.render("Draw", True, (207, 188, 188, alpha))
                text2 = font.render("Press 'r' to Reset!", True, (207, 188, 188, alpha))

            # Fade-in effect for the text
            if alpha < 255:
                alpha += fade_speed

            display.fill((0, 0, 0))
            display.blit(text, (width / 3, height / 3))
            display.blit(text2, (width / 3, height / 2))

            pygame.display.update()
        

    def start(self):
        self.Human(None, None)
