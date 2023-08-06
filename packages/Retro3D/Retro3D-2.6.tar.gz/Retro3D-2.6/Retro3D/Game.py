from Retro3D import *



###############################################################################
#
# base class for all games
#
################################################################################
class Game:

    STATE_INIT              = 0
    STATE_MENU              = 1
    STATE_PLAY              = 2
    STATE_GAME_OVER         = 3    
    STATE_PLAY_AGAIN        = 4 
    STATE_QUIT              = 5

    # dsd make text scale properly with different resolutions!
    MENU_MODE_MAIN           = 0
    MENU_MODE_INSTRUCTIONS   = 1
    MENU_MODE_CREDITS        = 2


    ###############################################################################
    #
    # override me! and call me with super
    #
    ###############################################################################
    def __init__(self, config: ConfigGame, fpath_base_rez:str):
    
        self.game_state = Game.STATE_INIT

        self.key_pressed_dict = dict()
        self.was_space_hit = False

        self.engine = Engine(config)

        self.time_last = time.time()

        self.fpath_base_rez = fpath_base_rez
        self.rez = Rez(self.fpath_base_rez, self.engine)

        self.menu_mode = Game.MENU_MODE_MAIN

        self.flasher_interval = 0.0

    ###############################################################################
    #
    ###############################################################################
    def run(self):


        while True:

            if self.game_state == Game.STATE_QUIT:
                break

        
            if self.game_state == Game.STATE_PLAY:
                self.engine.clear_screen()
                self.get_player_input()
                self.update()
                self.draw_background()
                self.engine.update()
                self.draw_hud()
        
            elif self.game_state == Game.STATE_MENU:
                self.engine.clear_screen()
                self.__draw_menu()
                
                self.key_pressed_dict = pg.key.get_pressed()

                if self.menu_mode == Game.MENU_MODE_MAIN:
                    if self.is_key_down(pg.K_p):
                        self.game_state = Game.STATE_PLAY
                    elif self.is_key_down(pg.K_i):
                        self.menu_mode = Game.MENU_MODE_INSTRUCTIONS
                    elif self.is_key_down(pg.K_c):
                        self.menu_mode = Game.MENU_MODE_CREDITS
                else:
                    if self.is_key_down(pg.K_b):
                        self.menu_mode = Game.MENU_MODE_MAIN
        
            elif self.game_state == Game.STATE_GAME_OVER:
                self.engine.clear_screen()
                self.update()
                self.draw_background()
                self.engine.update()
                self.draw_hud()
                self.draw_game_over()                 

                self.key_pressed_dict = pg.key.get_pressed()
                if self.is_key_down(pg.K_p):
                    self.game_state = Game.STATE_PLAY_AGAIN

            elif self.game_state == Game.STATE_PLAY_AGAIN:
                self.engine.clear_screen()
                self.__init__(self.engine.config, self.fpath_base_rez)
                self.game_state = Game.STATE_PLAY

            self.engine.blit()

            self.was_space_hit = False            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game_state = Game.STATE_QUIT
                    break;
                if event.type == pg.KEYUP:
                    if event.key == pg.K_SPACE:                    
                        self.was_space_hit = True
   

        pg.quit()


    # dsd do i want to make some kind of standardized input system - that wraps pygame's - mouse and keyboard etc
    ###############################################################################
    #
    # override me! and call me with super
    #
    ###############################################################################
    def get_player_input(self):

        self.key_pressed_dict = pg.key.get_pressed()

                

    ###############################################################################
    #
    ###############################################################################
    def is_key_down(self, key: int):

        if self.key_pressed_dict[key]:
            return True
        
        return False


    ###############################################################################
    #
    # override me! and call me with super
    #
    ###############################################################################
    def update(self):  

        dt = time.time() - self.time_last
        self.time_last = time.time()

        if self.game_state != Game.STATE_PLAY:
            return False

        return True


    ###############################################################################
    #
    # override me! and call me with super
    #
    ###############################################################################
    def draw_background(self):  
        pass


    # dsd support cover art!
    ###############################################################################
    #
    ###############################################################################
    def __draw_menu(self):  

        pos = pg.math.Vector2(0, 0) 

        if self.menu_mode == Game.MENU_MODE_MAIN:

            self.engine.draw_rect_gradient(self.engine.config.menu_background_color_top, self.engine.config.menu_background_color_bottom, self.engine.screen_rect, SiDirection.VERTICAL)
    
            # title
            pos.x = self.engine.screen_res.x * 0.5
            pos.y = self.engine.screen_res.y * 0.25
            self.engine.draw_text(pos, pg.Color(255,255,255), self.engine.config.title, self.engine.font_engine_large)

            # play
            pos.x = self.engine.screen_res.x * 0.5
            pos.y = self.engine.screen_res.y * 0.6
            self.engine.draw_text(pos, pg.Color(0, 255, 0), "P - Play", self.engine.font_engine_small)

            # intructions
            pos.x = self.engine.screen_res.x * 0.5
            pos.y = self.engine.screen_res.y * 0.65
            self.engine.draw_text(pos, pg.Color(255, 255, 0), "I - Instructions", self.engine.font_engine_small)

             # credits
            pos.x = self.engine.screen_res.x * 0.5
            pos.y = self.engine.screen_res.y * 0.7
            self.engine.draw_text(pos, pg.Color(255, 255, 0), "C - Credits", self.engine.font_engine_small)

             # author
            pos.x = self.engine.screen_res.x * 0.5
            pos.y = self.engine.screen_res.y * 0.9
            self.engine.draw_text(pos, pg.Color(255, 255, 255), "©   " + self.engine.config.author + "   " + self.engine.config.year, self.engine.font_engine_medium)

        elif self.menu_mode == Game.MENU_MODE_INSTRUCTIONS:

            self.engine.draw_rect_gradient(self.engine.config.menu_background_color_top, self.engine.config.menu_background_color_bottom, self.engine.screen_rect, SiDirection.HORIZONTAL)

            self.blit_text(self.engine.screen, self.engine.config.instructions, (100, 100), self.engine.font_engine_small, pg.Color(255, 255, 255))

            pos.x = self.engine.screen_res.x * 0.5
            pos.y = self.engine.screen_res.y * 0.95
            self.engine.draw_text(pos, pg.Color(255, 255, 0), "B - Back", self.engine.font_engine_small)

        elif self.menu_mode == Game.MENU_MODE_CREDITS:

            self.engine.draw_rect_gradient(self.engine.config.menu_background_color_bottom, self.engine.config.menu_background_color_top, self.engine.screen_rect, SiDirection.HORIZONTAL)

            text_credits = "Engine Font: DOOM Eternal by HK Fonts\n\n"
            text_credits += self.engine.config.credits
            self.blit_text(self.engine.screen, text_credits, (100, 100), self.engine.font_engine_small, pg.Color(255, 255, 255))

            pos.x = self.engine.screen_res.x * 0.5
            pos.y = self.engine.screen_res.y * 0.95
            self.engine.draw_text(pos, pg.Color(255, 255, 0), "B - Back",  self.engine.font_engine_small)

        else:
            SiLog.Unsupported(self.menu_mode)



    ###############################################################################
    # 
    # got this from:
    # https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame
    #
    #
    # dsd adjusted font looks real shitty
    #
    ###############################################################################
    def blit_text(self, surface, text, pos, font, color):
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = surface.get_size()
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.


    ###############################################################################
    # 
    # override me! and call me with super - if you want anything extra on game over 
    #
    ###############################################################################
    def draw_game_over(self):  
 

        pos = pg.math.Vector2(0, 0) 
    
        pos.x = self.engine.screen_res.x * 0.5
        pos.y = self.engine.screen_res.y * 0.2
        self.engine.draw_text(pos, pg.Color(255,255,255), "GAME OVER", self.engine.font_engine_large)

        pos.x = self.engine.screen_res.x * 0.5
        pos.y = self.engine.screen_res.y * 0.75
        self.engine.draw_text(pos, pg.Color(255, 255, 0), "Hit P to Play Again", self.engine.font_engine_medium)



    ###############################################################################
    #
    # override me!
    #
    ###############################################################################
    def draw_hud(self):  
        pass


