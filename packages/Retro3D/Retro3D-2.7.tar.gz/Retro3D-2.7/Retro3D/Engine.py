from Retro3D import *




###############################################################################
#
# Author:  Deepak (I can't belive I'm programming Python) Deo
# Date:    Jan 3, 2023
#
###############################################################################
class Engine:

    VERSION = 2.7

    DISPLAY_LIST_WIREFRAME          = 1
    DISPLAY_LIST_SHADED             = 2
    DISPLAY_LIST_SHADED_OUTLINE     = 3



    #dsd there's probably a pythonic non-looping way to do this
    ###############################################################################
    #
    ###############################################################################
    @staticmethod
    @njit(fastmath=True)
    def AreAllVertsVisible(list_verts: list, screen_res_x: float, screen_res_y: float):
        for v in list_verts:
            if v[0] <= 0 or v[0] >= screen_res_x:
                return False;
            if v[1] <= 0 or v[1] >= screen_res_y:
                return False;

        return True;


    ###############################################################################
    #
    ###############################################################################
    def __init__(self, config: ConfigGame):

        SiLog.KeyVal("starting Retro3D", Engine.VERSION)

        # using pygame (pg) for drawing to the screen
        pg.init()
    
        # verify sound will work
        # pg.mixer.music.load crashes if not devices deteced. wonderful :/
        self.is_sound_active = True
        try:
            pg.mixer.init()
        except:
            SiLog.Message("no sound device detected") 
            self.is_sound_active = False
     
        self.config = config  

        self.screen_res = pg.math.Vector2(self.config.screen_resolution.x, self.config.screen_resolution.y)
        self.screen = pg.display.set_mode([self.config.screen_resolution.x, self.config.screen_resolution.y])

        self.screen_rect = pg.Rect(0, 0, self.config.screen_resolution.x, self.config.screen_resolution.y)

        self.light = light = LightDirectional(config.light_direction)

        self.FPS = 60
        self.clock = pg.time.Clock()
        self.frame_rate_last_frame_ticks = 0
        self.delta_time = 0.0

        self.camera = Camera(pg.math.Vector3(0, 0, 0))
        self.projection = Projection(self, self.config.screen_resolution)

        # must add objects to one of these lists if you want them drawn
        self.display_list_wireframe = list()
        self.display_list_shaded = list()
        self.display_list_shaded_outline = list()

        
        base_path_rez = os.path.dirname(__file__) + os.sep + "rez" + os.sep 

        # load engine fonts
        base_path_font = base_path_rez + "fonts" + os.sep 
        font_name = base_path_font + "EternalLogo.ttf"

        self.font_engine_large = pg.font.Font(font_name, 100)
        self.font_engine_medium = pg.font.Font(font_name, 45)
        self.font_engine_small = pg.font.Font(font_name, 25)

    ###############################################################################
    #
    ###############################################################################
    def add_display_object(self, obj: Object, display_list_type: int):

        if display_list_type == Engine.DISPLAY_LIST_WIREFRAME:
            self.display_list_wireframe.append(obj)
            obj.set_display_list(self.display_list_wireframe)
        elif display_list_type == Engine.DISPLAY_LIST_SHADED:
            self.display_list_shaded.append(obj)
            obj.set_display_list(self.display_list_shaded)
        elif display_list_type == Engine.DISPLAY_LIST_SHADED_OUTLINE:
            self.display_list_shaded_outline.append(obj)
            obj.set_display_list(self.display_list_shaded_outline)
        else:
            SiLog.Unsupported(display_list_type);
    
 
    ###############################################################################
    #
    ###############################################################################
    def remove_display_object(self, obj: Object):

        if obj.get_display_list() == None:
            SiLog.Error("missing display list!")
            return

        obj.get_display_list().remove(obj)
          

    ###############################################################################
    #
    ###############################################################################
    def clear_screen(self):

        # always clear screen to black
        self.screen.fill(pg.Color(0, 0, 0))


    ###############################################################################
    #
    ###############################################################################
    def update(self):

        # update delta_time    
        t = pg.time.get_ticks()
        self.delta_time = (t - self.frame_rate_last_frame_ticks) / 1000.0
        self.frame_rate_last_frame_ticks = t

        # precalc camera matrix
        camera_matrix = self.camera.calc_camera_matrix()

        if len(self.display_list_wireframe) > 0:
            self.__display(camera_matrix, self.display_list_wireframe, Engine.DISPLAY_LIST_WIREFRAME)

        if len(self.display_list_shaded) > 0:
            self.__display(camera_matrix, self.display_list_shaded, Engine.DISPLAY_LIST_SHADED)

        if len(self.display_list_shaded_outline) > 0:
            self.__display(camera_matrix, self.display_list_shaded_outline, Engine.DISPLAY_LIST_SHADED_OUTLINE)

    ###############################################################################
    #
    ###############################################################################
    def __display(self, camera_matrix: Matrix, display_list: list, display_list_type: int):

        camera_forward = [self.camera.forward.x, self.camera.forward.y, self.camera.forward.z, 0]
        camera_pos = [self.camera.pos.x, self.camera.pos.y, self.camera.pos.z, 1]


        for obj in display_list:

            # move verts to world space
            #              
            # NOTE: the mat_world array of arrays looks like this for a pos 0,0,0 and rot 0,0.2,0
            #       array[
            #               [0.99980001,    0,  -0.01999867,    0]
            #               [         0,    1,            0,    0]
            #               [0.01999867,    0,   0.99980001,    0]
            #               [         0,    0,            0,    1]
            #            ]
            #
            #        but should be thought of as transposed to understand the mat mult
            #        [ 0.99980001,      0,  0.01999867,     0]
            #        [          0,      1,           0,     0]
            #        [-0.01999867,      0,  0.99980001,     0]
            #        [          0,      0,           0,     1]
            #
            #        for another example consider this:
            #
            #           vertex    = np.array([2, 0, -2, 0])
            #           world_mat = np.array([[2, 0, -2, 0],
            #                                 [0, 1,  0, 0],
            #                                 [3, 0,  5, 0],
            #                                 [0, 0, 0, 1]])
            #
            #           new_vertex = np.matmul(vertex, world_mat)
            #
            #           in a standard mult - you'd think of the vertex as a vertical col.
            #           but here it's a row - which means we need to mult by the cols of world_mat
            list_vertex = np.matmul(obj.model.list_vertex, obj.mat_world)

            # copy the list to keep original world vertices
            list_vertex_world = list_vertex[:]

            # move normals to world space 
            # NOTE: need normals even if not drawing normals since code
            #       is using the normal to cull any polygons that are not
            #       facing the camera. also needed for lighting
            # NOTE: removing position info from matrix for normal calcs - akin to moving to camera space... :/
            mat = obj.mat_world.copy()
            mat[3][0] = 0.0
            mat[3][1] = 0.0
            mat[3][2] = 0.0
            list_normal = np.matmul(obj.model.list_face_normal, mat)

            # move verts to camera space   
            list_vertex = np.matmul(list_vertex, camera_matrix)

            # move verts to unit cube via perspective projection
            list_vertex = np.matmul(list_vertex, self.projection.projection_matrix)

            # perspective divide
            #       list_vertex is n rows of [x y z w]
            #       the below line of code is just doing this:
            #       for v in list_vertex:
            #           v[0] /= v[3];       # x / w
            #           v[1] /= v[3];       # y / w
            #           v[2] /= v[3];       # z / w
            #           v[3] /= v[3];       # w / w
            list_vertex /= list_vertex[:, -1].reshape(-1, 1)

            # dsd this is where we could clip verts that are outside of the unit cube...

            # unit_cube -> screen
            list_vertex = np.matmul(list_vertex, self.projection.to_screen_matrix)

            # store this before moving down to 2d
            list_vertex_screen = list_vertex[:]

            # create a new list with just the x/y of the verts
            # since, in the end, all we are doing is drawing a 2d image...
            list_vertex = list_vertex[:, :2]
           
            #draw faces
            for face_idx, face_info in enumerate(obj.list_face_info):
                             
                # skip drawing if any of the 3 verts are behind the camera
                is_out_of_view = False
                for v in list_vertex_screen:
                    if v[2] == 0.0:
                        is_out_of_view = True
                        break
                if is_out_of_view == True:
                    continue

                # this below code is just doing this
                # color = face_info[0]
                # face = face_info[1]
                color, list_vertex_index = face_info

                # this below code is just doing this
                # list_verts = []
                # for vert_idx in list_vertex_index:
                #     list_verts.append(list_vertex[vert_idx])
                # list_polygon_vertex = []
                # list_polygon_vertex.append(list_verts)
                list_polygon_vertex = list_vertex[list_vertex_index]

                # any of the 3 vertices will do
                vertex_world = list_vertex_world[list_vertex_index][0]


                if Engine.AreAllVertsVisible(list_polygon_vertex, self.screen_res.x, self.screen_res.y):

                    # only draw the face if it's in the view of the camera
                    # using dot product for this

                    # v1 = cam to face
                    v1 = camera_pos - vertex_world 
                    v1 = v1/np.linalg.norm(v1)
                    dp = np.dot(v1, camera_forward)

                    if dp < 0.0:

                        #only draw if poly is facing the camera

                        # NOTE: normals are already normalized since we are just rotating a normalized vector
                        v1 = list_normal[face_idx]

                        # get vector from face to the camera
                        v2 = vertex_world - camera_pos
                        v2 = v2/np.linalg.norm(v2)

                        dp = np.dot(v1,v2)

                        if dp < 0.0:

                            # now that we know tri is being drawn, calc dp for lighting
                            dp = v1[0]*self.light.direction[0] + v1[1]*self.light.direction[1] + v1[2]*self.light.direction[2]
                            dp = (1.0 - dp) * 0.5
                            face_color = self.__calc_face_color(color, dp)

                            # convert vertices from 4 components [x y z w] to 2 components [x y]   
                            v0 = [list_polygon_vertex[0][0], list_polygon_vertex[0][1]]
                            v1 = [list_polygon_vertex[1][0], list_polygon_vertex[1][1]]
                            v2 = [list_polygon_vertex[2][0], list_polygon_vertex[2][1]]

                            # NOTE: polygon draw with 0 means fill 0 otherwise it means thickness of line (int)
                            if display_list_type == Engine.DISPLAY_LIST_WIREFRAME:
                                pg.draw.line(self.screen, color, v0, v1, 2)
                                pg.draw.line(self.screen, color, v1, v2, 2)
                                pg.draw.line(self.screen, color, v2, v0, 2)
                            elif display_list_type == Engine.DISPLAY_LIST_SHADED:
                                pg.draw.polygon(self.screen, face_color, list_polygon_vertex, 0)  
                            elif display_list_type == Engine.DISPLAY_LIST_SHADED_OUTLINE:
                                pg.draw.polygon(self.screen, face_color, list_polygon_vertex, 0)  
                                pg.draw.line(self.screen, pg.Color('white'), v0, v1, 1)
                                pg.draw.line(self.screen, pg.Color('white'), v1, v2, 1)
                                pg.draw.line(self.screen, pg.Color('white'), v2, v0, 1)
                            else:
                                SiLog.Unsupported(display_list_type);


                        if obj.draw_normals:
                            self.__draw_normals(list_vertex_world, list_vertex_index, list_normal, face_idx)



    ###############################################################################
    #    
    ###############################################################################
    def __calc_face_color(self, face_color: pg.Color, dp: float):

        col = pg.Color(face_color)

        if dp > 1.0:
            dp = 1.0
        elif dp < 0.0:
            dp = 0.0

        col.r = int(col.r * dp)
        col.g = int(col.g * dp)
        col.b = int(col.b * dp)

        return col



    ###############################################################################
    #    
    ###############################################################################
    def __draw_normals(self, list_vertex_world: list, list_vertex_index: list, list_normal: list, face_idx: int):

        tx = 0.0
        ty = 0.0
        tz = 0.0
 
        for vertex in list_vertex_world[list_vertex_index]: 
            tx += vertex[0]
            ty += vertex[1]
            tz += vertex[2]

        num = list_vertex_world[list_vertex_index].shape[0]
        tx /= num
        ty /= num
        tz /= num

        pos_start = []
        pos_start.append(tx)
        pos_start.append(ty)
        pos_start.append(tz)
        pos_start.append(1.0)

        pos_end = pos_start[:]
        pos_end[0] += (list_normal[face_idx][0] * 1.0)
        pos_end[1] += (list_normal[face_idx][1] * 1.0)
        pos_end[2] += (list_normal[face_idx][2] * 1.0)
        pos_end[3] = 1.0

        pos_start = np.matmul(pos_start, self.camera.calc_camera_matrix())
        pos_start = np.matmul(pos_start, self.projection.projection_matrix)
        pos_start[0] /= pos_start[3]
        pos_start[1] /= pos_start[3]
        pos_start[2] /= pos_start[3]
        pos_start[3] /= pos_start[3]
        pos_start = np.matmul(pos_start, self.projection.to_screen_matrix)
        pos_start = pos_start[:2]

        pos_end = np.matmul(pos_end, self.camera.calc_camera_matrix())
        pos_end = np.matmul(pos_end, self.projection.projection_matrix)
        pos_end[0] /= pos_end[3]
        pos_end[1] /= pos_end[3]
        pos_end[2] /= pos_end[3]
        pos_end[3] /= pos_end[3]
        pos_end = np.matmul(pos_end, self.projection.to_screen_matrix)
        pos_end = pos_end[:2]

        pg.draw.line(self.screen, pg.Color('yellow'), pos_start, pos_end, 3)



    ###############################################################################
    #
    ###############################################################################
    def draw_rect_gradient(self, color_top: pg.Color, color_bottom: pg.Color, target_rect: pg.Rect, gradient_direction: 'SiDirection'):
    
        # draw colors to a tiny rectangle
        tiny_rect = pg.Surface((2,2)) 

        if gradient_direction == SiDirection.VERTICAL:
            pg.draw.line(tiny_rect, color_top, (0,0), (1,0))  
            pg.draw.line(tiny_rect, color_bottom, (0,1), (1,1))          
        else:
            pg.draw.line(tiny_rect, color_top, (0,0), (0,1))  
            pg.draw.line(tiny_rect, color_bottom, (1,0), (1,1))          

        # scale rectangle up and use smoothing
        tiny_rect = pg.transform.smoothscale(tiny_rect, (target_rect.width, target_rect.height))

        self.screen.blit(tiny_rect, target_rect) 
     
        
    #dsd move into Si since Si assumes pygame!
    ###############################################################################
    #
    ###############################################################################
    def draw_text(self, pos:pg.math.Vector2, color:pg.Color, text:str, font:pg.font.Font):    

        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (pos.x, pos.y)
        self.screen.blit(text_surface, text_rect)

    ###############################################################################
    #
    ###############################################################################
    def blit(self):

        pg.display.set_caption(str(self.clock.get_fps()))
        pg.display.flip()
        self.clock.tick(self.FPS)




