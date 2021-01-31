import pygame
pygame.init()

class Window:
    def __init__(self,size=(500,500),resizable=True,name="Pygame Window",fps=60):
        self.resizable = resizable
        self.size = size
        self.width = size[0]
        self.height = size[1]
        if self.resizable:
            self.__window = pygame.display.set_mode(self.size,pygame.RESIZABLE)
        else:
            self.__window = pygame.display.set_mode(self.size)
        pygame.display.set_caption(name)
        self.__clock = pygame.time.Clock()
        self.fps = fps
    def update(self):
        if self.isOpen():
            pygame.display.flip()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                elif event.type == pygame.VIDEORESIZE:
                    self.resize(event.size)
            self.__clock.tick(self.fps)
            return events
    def getMousePos(self):
        if self.isOpen():
            return pygame.mouse.get_pos()
    def getMouseRect(self):
        if self.isOpen():
            x,y = self.getMousePos()
            return pygame.Rect(x,y,1,1)
    def fill(self,color):
        if self.isOpen():
            self.__window.fill(color)
    def blit(self,surface,pos=(0,0)):
        if self.isOpen():
            self.__window.blit(surface,pos)
    def smooth_scaled_blit(self,surface):
        pygame.transform.smoothscale(surface, (self.width, self.height), self.__window)
    def scaled_blit(self,surface):
        pygame.transform.scale(surface, (self.width, self.height), self.__window)
    def isOpen(self):
        return pygame.display.get_init()
    def resize(self,newSize):
        if self.isOpen():
            image = self.__window.copy()
            self.size = newSize
            self.width = self.size[0]
            self.height = self.size[1]
            if self.resizable:
                self.__window = pygame.display.set_mode(self.size,pygame.RESIZABLE)
            else:
                self.__window = pygame.display.set_mode(self.size)
            self.blit(pygame.transform.scale(image, self.size))
    def close(self):
        if self.isOpen():
            pygame.display.quit()