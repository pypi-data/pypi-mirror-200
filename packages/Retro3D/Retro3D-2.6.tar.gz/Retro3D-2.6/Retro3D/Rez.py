from Retro3D import *


# dsd may need to unload resources - a new Rez is not enuf.. ?

# dsd break out sound playing system from rez

# dsd change it so the engine figures out the rez path since its standardized anyway....

###############################################################################
#
# NOTE: rez means 'resource'
#
###############################################################################
class Rez:

    ###############################################################################
    #
    ###############################################################################
    def __init__(self, fpath_base, engine:'Engine'):

        self.engine = engine

        # setup base paths
        base_fpath_art = fpath_base + "art" + os.sep 
        if os.path.isdir(base_fpath_art) == False:
            SiLog.Error("art path does not exist [" + base_fpath_art + "]")

        self.base_fpath_models = base_fpath_art + "models" + os.sep
        if os.path.isdir(self.base_fpath_models) == False:
            SiLog.Error("models path does not exist [" + self.base_fpath_models + "]")

        self.base_fpath_images = base_fpath_art + "images" + os.sep
        if os.path.isdir(self.base_fpath_images) == False:
            SiLog.Error("images path does not exist [" + self.base_fpath_images + "]")

        self.base_fpath_sound = fpath_base + "sound" + os.sep 
        if os.path.isdir(self.base_fpath_sound) == False:
            SiLog.Error("sound path does not exist [" + self.base_fpath_sound + "]")

        self.base_fpath_fonts = fpath_base + "fonts" + os.sep 
        if os.path.isdir(self.base_fpath_fonts) == False:
            SiLog.Error("fonts path does not exist [" + self.base_fpath_fonts + "]")

        self.music = None
        self.dict_sounds = dict()
        self.dict_models = dict()
        self.dict_images = dict()



    ###############################################################################
    #
    ###############################################################################
    def set_music(self, fname):
        
        if self.engine.is_sound_active == False:
            return

        pg.mixer.music.load(self.base_fpath_sound + fname)


    ###############################################################################
    #
    ###############################################################################
    def play_music(self):

        if self.engine.is_sound_active == False:
            return

        #dsd wtf - don't see any return from music load to know if it failed
        #           now i have to do this crappy try/catch
        #           thanks fuckers
        #           either that or i can't read shitty pythonic docs...
        try:
            pg.mixer.music.play(-1)
        except:
            SiLog.Message("no music loaded")   
  


    ###############################################################################
    #
    ###############################################################################
    def stop_music(self):

        if self.engine.is_sound_active == False:
            return

        pg.mixer.music.stop()



    ###############################################################################
    #
    ###############################################################################
    def add_sound(self, fname:str):

        if self.engine.is_sound_active == False:
            return

        self.dict_sounds[fname] = pg.mixer.Sound(self.base_fpath_sound + fname)


    ###############################################################################
    #
    ###############################################################################
    def play_sound(self, fname:str):

        if self.engine.is_sound_active == False:
            return

        #dsd if debug these types of checks for speed - 
        if fname not in self.dict_sounds:
            SiLog.Error("sound has not been added [" + fname + "]")
            return

        pg.mixer.Sound.play(self.dict_sounds[fname])



    ###############################################################################
    #
    ###############################################################################
    def create_font(self, fname:str, size:int):
        return pg.font.Font(self.base_fpath_fonts + fname, size)



    
    ###############################################################################
    #
    ###############################################################################
    def add_model(self, fname:str):
        self.dict_models[fname] = Model(self.base_fpath_models + fname)


    ###############################################################################
    #
    ###############################################################################
    def get_model(self, fname:str):
 
        # dsd if debug these types of checks for speed - 
        if fname not in self.dict_models:
            SiLog.Error("model has not been added [" + fname + "]")
            return

        return self.dict_models[fname]


    ###############################################################################
    #
    ###############################################################################
    def add_image(self, fname:str):
        self.dict_images[fname] = pg.image.load(self.base_fpath_images + fname)

    ###############################################################################
    #
    ###############################################################################
    def get_image(self, fname:str):

        # dsd if debug these types of checks for speed - 
        if fname not in self.dict_images:
            SiLog.Error("image has not been added [" + fname + "]")
            return

        return self.dict_images[fname]
