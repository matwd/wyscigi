import pygame

class Button():
    def __init__(self,pos,text_var,font,text_color,hover_color,real_screen):
        self.x = pos[0]
        self.y = pos[1]
        self.font = font
        self.text_color = text_color
        self.hover_color = hover_color
        self.text_var = text_var
        self.real_screen = real_screen
        self.text = self.font.render(self.text_var, True, self.text_color)

        
        # self.rect = self.button.get_rect(center=(self.x,self.y))
        self.rect = self.text.get_rect(center=(self.x,self.y))

    def update(self,screen):
        screen.blit(self.text,self.rect)
        
    def checkForInput(self,position):
        position = [round(position[0]/self.real_screen.get_size()[0] * 1920), round(position[1] / self.real_screen.get_size()[1] * 1080)]
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def changeColor(self,position):
        position = [round(position[0]/self.real_screen.get_size()[0] * 1920), round(position[1] / self.real_screen.get_size()[1] * 1080)]
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            print("Wsrodku")
            self.text = self.font.render(self.text_var,True,self.hover_color)
        else:
            self.text = self.font.render(self.text_var, True, self.text_color)