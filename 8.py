import pygame  
from pygame.locals import *
from abc import ABC, abstractmethod
class TeamAlreadyExistsError(Exception):
    """Исключение, возникающее при попытке добавить команду, которая уже существует."""
    pass

class TeamNotFoundError(Exception):
    """Исключение, возникающее при попытке найти команду, которой не существует."""
    pass

#Абстрактный класс
class Team(ABC):
    @abstractmethod
    def get_positions(self):#Абстрактный метод
        pass

    @abstractmethod
    def set_position(self, position):#Абстрактный метод
        pass

class First_Team(Team):
    def __init__(self):
        super().__init__()
        self.positions = []
    #возвращает список позиций команды.
    def get_positions(self):
        return self.positions 
    #добавляет новую позицию в команду
    def set_position(self, position):
        if position in self.positions:
            raise TeamAlreadyExistsError("Эта позиция уже занята.")
        self.positions.append(position)
    #удаляет позицию из команды
    def del_position(self, position):
        if position not in self.positions:
            raise TeamNotFoundError("Такой позиции нет в команде.")
        self.positions.remove(position)
    # возвращает количество позиций в команде
    def get_len(self):
        return len(self.positions)

class Second_Team(Team):
    def __init__(self):
        super().__init__()
        self.positions = []
    #возвращает список позиций команды.
    def get_positions(self):
        return self.positions 
    #добавляет новую позицию в команду
    def set_position(self, position):
        if position in self.positions:
            raise TeamAlreadyExistsError("Эта позиция уже занята.")
        self.positions.append(position)
    #даляет позицию из команды
    def del_position(self, position):
        if position not in self.positions:
            raise TeamNotFoundError("Такой позиции нет в команде.")
        self.positions.remove(position)
    ## возвращает количество позиций в команде
    def get_len(self):
        return len(self.positions)
#количества установленных позиций игровыми командами
count=0
key_first=1
# рисуем доску для игры
class MyGameClass():
    def __init__(self):
        pygame.init()
        self.screen_width, self.screen_height = 1425, 630
        self.screen_sizes = (self.screen_width, self.screen_height)
        self.screen = pygame.display.set_mode(self.screen_sizes)  # pygame.RESIZABLE
        pygame.display.set_caption('Морской бой')
        self.screen.fill((79, 122, 176))
        self.first_team_Team = First_Team()
        self.second_team_Team = Second_Team()

        self.WHITE=(255,255,255)
        
        self.rect_sizes_delimiter = (26, self.screen_sizes[1])
        self.rect_delimiter = pygame.Surface(self.rect_sizes_delimiter)  
        self.rect_delimiter.fill(self.WHITE)
        self.position_delimiter=(700, 0)

        self.spaces_rect_sizes=(self.position_delimiter[0],630)
        self.spaces_rect = pygame.Surface(self.spaces_rect_sizes, pygame.SRCALPHA) #тут первые два параметра это на сколько можно растянуть этот прямоугольник
        self.spaces_rect2 = pygame.Surface(self.spaces_rect_sizes, pygame.SRCALPHA)
    #рисуем сетку квадратов
    def draw_squares(self,surface, was_x,was_y):
        for y in range(0,was_y,70):
            for x in range(0,was_x,70):
                pygame.draw.rect(surface, self.WHITE, (x, y, 70, 70),2)
    #изменяет цвет квадрата на игровом поле
    def change_square_color(self, x, y, color):
        if 0 <= x < self.spaces_rect_sizes[0] and 0 <= y < self.spaces_rect_sizes[1]:
            self.spaces_rect.blit(pygame.Surface((70, 70), pygame.SRCALPHA), (x, y), special_flags=pygame.BLEND_RGBA_MULT)
            pygame.draw.rect(self.spaces_rect, color, (x, y, 70, 70))
        elif self.spaces_rect_sizes[0] + 25 <= x < self.spaces_rect_sizes[0] + 25 + self.spaces_rect_sizes[0] and 0 <= y < self.spaces_rect_sizes[1]:
            self.spaces_rect2.blit(pygame.Surface((70, 70), pygame.SRCALPHA), (x - self.spaces_rect_sizes[0] - 25, y), special_flags=pygame.BLEND_RGBA_MULT)
            pygame.draw.rect(self.spaces_rect2, color, (x - self.spaces_rect_sizes[0] - 25, y, 70, 70))
    #очищает все квадраты возвращая их к исходному цвету 
    def clear_all_cells(self,key=0):
        delta=0
        if key==1:
            delta=25
        for y1 in range(630):
            for x1 in range(1450):
                self.change_square_color(x1//70 * 70+delta, y1 * 70, (79, 122, 176))
    #размещением позиций 
    def set_position_Teams(self,x_index,y_index):
        global count
        if count<10:
            if 0 <= x_index < self.spaces_rect_sizes[0] // 70 and 0 <= y_index < self.spaces_rect_sizes[1] // 70:
                self.change_square_color(x_index * 70, y_index * 70, (132,132,132))
                self.first_team_Team.set_position((x_index * 70, y_index * 70))
                count=count+1
        elif count==10:
            self.clear_all_cells()
            count=count+1
        if count>10 and count<=20:
            if 10<=x_index<=19 and 0<=y_index<=8:
                self.change_square_color(x_index * 70 + 25, y_index * 70, (132,132,132))
                self.second_team_Team.set_position((x_index * 70 + 25, y_index * 70))
                count=count+1
        elif count==21:
            self.clear_all_cells(key=1)
            count=count+1

    def BadaBOOM(self, x_index, y_index):
        global key_first
        if key_first==1:# Проверка хода первой команды
            if 0 <= x_index < self.spaces_rect_sizes[0] // 70 and 0 <= y_index < self.spaces_rect_sizes[1] // 70:
                if (x_index * 70, y_index * 70) in self.first_team_Team.get_positions():
                    self.change_square_color(x_index * 70, y_index * 70, (247, 103, 103))
                    self.first_team_Team.del_position((x_index * 70, y_index * 70))  
                else:
                    key_first=0 #Проверка хода второй команды 
                    self.change_square_color(x_index * 70, y_index * 70, (32, 32, 32))
        if key_first==0:
            if 10 <= x_index <= 19 and 0 <= y_index <= 8:
                if (x_index * 70 + 25, y_index * 70) in self.second_team_Team.get_positions():
                    self.change_square_color(x_index * 70 + 25, y_index * 70, (247, 103, 103))
                    self.second_team_Team.del_position((x_index * 70 + 25, y_index * 70))  
                else:
                    key_first=1
                    self.change_square_color(x_index * 70 + 25, y_index * 70, (32, 32, 32))
    #Запускаем весь цикл
    def run(self):
        running = True

        while running:
            self.draw_squares(self.spaces_rect, self.spaces_rect_sizes[0], self.spaces_rect_sizes[1])
            self.screen.blit(self.spaces_rect, (0, 0))
            self.draw_squares(self.spaces_rect2, self.spaces_rect_sizes[0], self.spaces_rect_sizes[1])
            self.screen.blit(self.spaces_rect2, (self.spaces_rect_sizes[0] + 25, 0))
            self.screen.blit(self.rect_delimiter, self.position_delimiter)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    global count
                    global key_first
                    x, y = event.pos
                    if x>=730:
                        x=x-25 #эта херня из-за разделения белой линии
                    # Преобразование координат мыши в индексы ячеек
                    x_index = x // 70
                    y_index = y // 70
                    if count<22:
                        self.set_position_Teams(x_index,y_index)
                    else:
                        self.BadaBOOM(x_index,y_index)
                        if self.second_team_Team.get_len() == 0:
                            running=False
                            print("Первая команда выиграла")
                            pygame.time.delay(3000)
                        elif self.first_team_Team.get_len() == 0:
                            running=False
                            print("Вторая команда выиграла")
                            pygame.time.delay(3000)
            pygame.display.update()

if __name__ == '__main__':
    MyGameClass().run()
