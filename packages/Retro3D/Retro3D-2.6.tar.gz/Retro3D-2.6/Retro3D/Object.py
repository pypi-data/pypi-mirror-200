from Retro3D import *



###############################################################################
#
###############################################################################
class Object:


    ###############################################################################
    #
    ###############################################################################
    def __init__(self):

        self.mat_world = np.array([[1.0, 0.0, 0.0, 0.0],
                                   [0.0, 1.0, 0.0, 0.0],
                                   [0.0, 0.0, 1.0, 0.0],
                                   [0.0, 0.0, 0.0, 1.0]])

        self.pos = pg.math.Vector3(0.0, 0.0, 0.0)
        self.rot = pg.math.Vector3(0.0, 0.0, 0.0)
        self.scale = 1.0
        self.forward = pg.math.Vector3(0.0, 0.0, 0.0)

        self.model = None
        self.list_face_normal = None

        self.draw_normals = False

        self.set_display_list(None)

        self.is_alive = True


    ###############################################################################
    #
    ###############################################################################
    def set_model(self, model: Model, face_color: pg.Color):

        self.model = model

        # face info
        #   color of face
        #       color belongs to obj so that diff objs can share the same 
        #       model but have diff colors
        #   indicies of the 4 vertices that make up the face
        #
        self.list_face_info = [(face_color, face) for face in model.list_face]
        


    ###############################################################################
    #
    ###############################################################################
    def set_pos(self, x, y, z):
        self.pos.x = x
        self.pos.y = y
        self.pos.z = z


    ###############################################################################
    #
    ###############################################################################
    def set_rot(self, x, y, z):
        self.rot.z = z



    ###############################################################################
    #
    ###############################################################################
    def set_scale(self, s):
        self.scale = s


    ###############################################################################
    #
    # should return True if dead/finished
    #
    ###############################################################################
    def update(self):
        
        self.mat_world = Matrix.RotateZ(self.rot.z)
        self.mat_world = np.matmul(self.mat_world, Matrix.Scale(self.scale))
        self.mat_world = np.matmul(self.mat_world,  Matrix.RotateX(self.rot.x))
        self.mat_world = np.matmul(self.mat_world,  Matrix.RotateY(self.rot.y))
        self.mat_world = np.matmul(self.mat_world,  Matrix.Translate(self.pos))

        self.forward.x = self.mat_world[2][0]
        self.forward.y = self.mat_world[2][1]
        self.forward.z = self.mat_world[2][2]

        return False



    ###############################################################################
    #
    ###############################################################################
    def get_display_list(self):
        return self.__display_list
        
    ###############################################################################
    #
    ###############################################################################
    def set_display_list(self, display_list:list):
        self.__display_list = display_list


        