from Retro3D import *



###############################################################################
#
###############################################################################
class ConfigGame:


    ###############################################################################
    #
    ###############################################################################
    def __init__(self):

        # set defaults for all fields
        self.screen_resolution = pg.math.Vector2(1600, 900)
        self.menu_background_color_top = pg.Color(100, 100, 100)
        self.menu_background_color_bottom = pg.Color(0, 0, 0)
        self.light_direction = pg.math.Vector3(1.0, 0.0, 0.0)

        self.title  = "Title"
        self.author = "Author"
        self.year = "1970"

        self.instructions = "No Instructions Yet"
        self.credits = "No Credits Yet"
