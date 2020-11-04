class Player(pygame.sprite.Sprite):
    def _init_(self, pos_x,pos_y):
        super()._init_()
        self.is_animating = False
        self.sprites = []
        self.sprites.append(pygame.image.load('character_malePerson_side.png'))
        self.sprites.append(pygame.image.load('character_malePerson_walk1.png'))
        self.sprites.append(pygame.image.load('character_malePerson_walk2.png'))
        self.sprites.append(pygame.image.load('character_malePerson_walk3.png'))
        self.sprites.append(pygame.image.load('character_malePerson_walk4.png'))
        self.sprites.append(pygame.image.load('character_malePerson_walk5.png'))
        self.sprites.append(pygame.image.load('character_malePerson_walk6.png'))
        self.sprites.append(pygame.image.load('character_malePerson_walk7.png'))
        self.sprites.append(pygame.image.load('character_malePerson_walk0.png'))
        self.sprite_atual = 0
        self.image = self.sprites[self.sprite_atual]

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x,pos_y]


    def animate(self):        
        self.is_animating = True
        
    def update(self):
        if self.is_animating == True:
            self.sprite_atual += 0.2

            if self.sprite_atual >= len(self.sprites):
                self.sprite_atual = 0
                #self.is_animating = False
                
            self.image = self.sprites[int(self.sprite_atual)]
