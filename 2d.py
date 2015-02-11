import numpy as np
from vispy import gloo
from vispy import app
from vispy.util.transforms import perspective, translate, rotate
from scipy.spatial import Delaunay

# app.use_app('glut')

# Create vetices
n = 4
#points = np.random.randint(-10, 10, (n, 2)).astype(np.float32)
points = np.array([[0,0],[0,1],[1,1],[1.1,0]]).astype(np.float32)



#tri = Delaunay(points)
#a_position = points[tri.simplices]
a_position = points

tri = 0
#a_position = np.vstack(a_position)

#a_id = np.random.randint(0, 30, (n, 1))
#a_id = np.sort(a_id, axis=0).astype(np.float32)
#print a_id


VERT_SHADER = """
uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;
attribute vec2 a_position;
//attribute float a_id;
//varying float v_id;
void main (void) {
    //v_id = a_id;
    gl_Position = u_projection * u_view * u_model * vec4(a_position, 0.0,1.0);
}
"""

FRAG_SHADER = """
//varying float v_id;
void main()
{
    //float f = fract(v_id);
    // The second useless test is needed on OSX 10.8 (fuck)
    //if( (f > 0.0001) && (f < .9999) )
    //    discard;
    //else
    gl_FragColor = vec4(0,0,0,1);
}
"""


class Canvas(app.Canvas):

    # ---------------------------------
    def __init__(self):
        app.Canvas.__init__(self, keys='interactive')

        self.program = gloo.Program(VERT_SHADER, FRAG_SHADER)

        # Set uniform and attribute
        #self.program['a_id'] = gloo.VertexBuffer(a_id)
        self.program['a_position'] = gloo.VertexBuffer(a_position)

        self.view = np.eye(4, dtype=np.float32)
        self.model = np.eye(4, dtype=np.float32)
        self.projection = np.eye(4, dtype=np.float32)

        self.translate = 20
        translate(self.view, 0, 0, -self.translate)
        self.program['u_model'] = self.model
        self.program['u_view'] = self.view

        self.theta = 0
        self.phi = 0
        self.tic = 0

        self.timer = app.Timer('auto', connect=self.on_timer)

    # ---------------------------------
    def on_initialize(self, event):
        gloo.set_clear_color('white')
        gloo.set_state('translucent')

    # ---------------------------------
    def on_key_press(self, event):
        if event.text == ' ':
            if self.timer.running:
                self.timer.stop()
            else:
                self.timer.start()

    # ---------------------------------
    def on_timer(self, event):
        global a_position,tri,points
        #self.theta += .5
        #self.phi += .5
        #self.model = np.eye(4, dtype=np.float32)
        #rotate(self.model, self.theta, 0, 0, 1)
        #rotate(self.model, self.phi, 0, 1, 0)
        #self.program['u_model'] = self.model
        #if self.tic%60 == 0:
        random = np.random.randint(-5, 5, (1, 2)).astype(np.float32)
        #print any((random == x).all() for x in points)
        if not any((random == x).all() for x in points):
           points = np.append(points,random,axis=0)
           tri = Delaunay(points)
           a_position = points[tri.simplices]
           self.program['a_position'] = a_position
        
        #print a_position
        self.tic += 1
        self.update()

    # ---------------------------------
    def on_resize(self, event):
        width, height = event.size
        gloo.set_viewport(0, 0, width, height)
        self.projection = perspective(45.0, width / float(height), 1.0, 1000.0)
        self.program['u_projection'] = self.projection

    # ---------------------------------
    def on_mouse_wheel(self, event):
        self.translate += event.delta[1]
        self.translate = max(2, self.translate)
        self.view = np.eye(4, dtype=np.float32)
        translate(self.view, 0, 0, -self.translate)
        self.program['u_view'] = self.view
        self.update()

    # ---------------------------------
    def on_draw(self, event):
        gloo.clear()
        self.program.draw('line_strip')


if __name__ == '__main__':
    c = Canvas()
    c.show()
    app.run()