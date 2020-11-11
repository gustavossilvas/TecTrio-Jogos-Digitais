class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x,pos_y):
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
            
#Configuração geral
 
pygame.init()
clock = pygame.time.Clock()

#Tela do jogo

screen_width = 400
screen_height = 400
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Crisis Scape')

#Criando os sprites e os grupos
pos_x = 10
pos_y = 10
moving_sprites = pygame.sprite.Group()
player = Player(pos_x,pos_y)
moving_sprites.add(player)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            player.animate()
            


    #Desenhando
        screen.fill((0,0,0))
        moving_sprites.draw(screen)
        moving_sprites.update()
        pygame.display.flip()
        clock.tick(60)
