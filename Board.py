from random import randint
import pygame

class Game: 
    def __init__(self, Mat, dimX, dimY):
        self.Mat = Mat
        self.dimX = dimX
        self.dimY = dimY

    def Initiate(self): 
        for i in range(0, self.dimY):
            R = []
            for j in range (0, self.dimX):
                if i % 2 == 1 and j % 2 == 1:
                    R.append(randint(1, 9))  
                elif i % 2 == 0 and j % 2 == 0:
                    R.append('*') 
                else:
                    R.append(' ') 
            self.Mat.append(R)

    def Get_matrix(self):
        ans = []
        for i in range(0, self.dimY):
            R = []
            for j in range(0, self.dimX):
                R.append(self.Mat[i][j])
            ans.append(R)
        return ans

    def Show_board(self, score,a, b):
        
        # pygame.init()
        cell_size = 50
        rows = self.dimX  
        cols = self.dimY
        width = rows * 80
        height = cols * 80
        window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Cap the Cells!!!")

        grid_width = cols * cell_size
        grid_height = rows * cell_size
        x_offset = (width - grid_width) // 2
        y_offset = (height - grid_height) // 2

        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        GREY = (110,110,110)
        CLICKED_GREY = (80,80,80)

        matrix = self.Mat

        cell_color = [[GREY if matrix[i][j] != '*' else BLACK for j in range(cols)] for i in range(rows)]
        if a!=None and b!=None:
            cell_color[b][a] = CLICKED_GREY

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    col = (mouse_pos[0] - x_offset) // cell_size
                    row = (mouse_pos[1] - y_offset) // cell_size
                    if 0 <= row < rows and 0 <= col < cols and matrix[row][col] == ' ':
                        print("Clicked Cell: [{}][{}] - Value: {}".format(row, col, matrix[row][col]))
                        return row,col

            window.fill(WHITE)
            for row in range(rows):
                for col in range(cols):
                    cell_rect = pygame.Rect(col * cell_size + x_offset, row * cell_size + y_offset, cell_size, cell_size)
                    pygame.draw.rect(window, cell_color[row][col], cell_rect)
                    cell_text = pygame.font.SysFont(None, 24).render(str(matrix[row][col]), True, WHITE)
                    text_rect = cell_text.get_rect(center=(col * cell_size + x_offset + cell_size // 2, row * cell_size + y_offset + cell_size // 2))
                    window.blit(cell_text, text_rect)
                    score_text = pygame.font.SysFont(None, 30).render(("Your Score - AI Score = " + str(score)), True, BLACK)
                    score_rect = score_text.get_rect()
                    score_rect.topright = (width - 10, 10)
                    window.blit(score_text, score_rect)

            pygame.display.flip()

        pygame.quit()

    def Get_currentState(self):
        return Game(self.Get_matrix(), self.dimX, self.dimY)

    def action(self, i, j):
        Sum = 0

        if j % 2 == 0 and i % 2 == 1:
            self.Mat[j][i] = '-'
            if j < self.dimY - 1:
                if self.Mat[j+2][i] == '-' and self.Mat[j+1][i+1] == '|' and self.Mat[j+1][i-1] == '|':
                    Sum += self.Mat[j+1][i]
            if j > 0:
                if self.Mat[j-2][i] == '-' and self.Mat[j-1][i+1] == '|' and self.Mat[j-1][i-1] == '|':
                    Sum += self.Mat[j-1][i]

        else:
            self.Mat[j][i] = '|'
            if i < self.dimX - 1:
                if self.Mat[j][i+2] == '|' and self.Mat[j+1][i+1] == '-' and self.Mat[j-1][i+1] == '-':
                    Sum += self.Mat[j][i+1]
            if i > 0:
                if self.Mat[j][i-2] == '|' and self.Mat[j+1][i-1] == '-' and self.Mat[j-1][i-1] == '-':
                    Sum += self.Mat[j][i-1]
        return Sum
