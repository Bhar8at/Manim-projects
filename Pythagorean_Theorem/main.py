from manim import *
import numpy as np


class RightAngledTriangle():
    def __init__(self, a ,b , pos, scale): 
        pos = np.array([i*scale for i in pos])  
        x = a*scale
        y = b*scale
        offset = 0.15
        self.vertices = [
            ORIGIN + pos ,
            np.array([x, 0, 0]) + pos,
            (np.array([x, y, 0]) + pos) ,
        ]
        # Create the triangle using the vertices
        self.triangle = Polygon(
            *(i for i in self.vertices),
            color = WHITE
        )
    
    def get_vertices(self):
        return self.vertices

class PythagoreanTheorem(Scene):

    def construct(self):
        offset = 0.25
        V_flip = np.array([0,1,0])
        H_flip = np.array([1,0,0])

        # Creating Triangles

        ## Bottom right
        t1 = RightAngledTriangle(4,4, [0, -3, -0], 0.5).triangle
        self.play(Create(t1))

        ## Bottom left
        t2 = t1.copy()
        t2.flip(V_flip)
        self.play(Create(t2),t2.animate.shift(t1.get_vertices()[0] - t2.get_vertices()[0]))

        ## Top right
        t3 = t1.copy()
        t3.flip(H_flip)
        self.play(t3.animate.shift(t1.get_vertices()[2] - t3.get_vertices()[2]))

        ## Top left
        t4 = t1.copy()
        t4.flip(H_flip)
        t4.flip(V_flip)
        self.play(t4.animate.shift(t2.get_vertices()[2] - t4.get_vertices()[2]))

        ## Filling the triangles
        self.play(*[triangle.animate.set_fill(BLUE, opacity=0.5) for triangle in [t1, t2, t3, t4]])
        self.wait(0.5)
        


        # Adding labels for all triangles
        ## Place 'a' and 'b' outside the square and 'c' inside the inner square
        t1_vertices = t1.get_vertices()
        t2_vertices = t2.get_vertices()
        t3_vertices = t3.get_vertices()
        t4_vertices = t4.get_vertices()

        a_labels = [
            Text("a", font_size=24).move_to((t1_vertices[0] + t1_vertices[1]) / 2 + np.array([0, -offset, 0])),
            Text("a", font_size=24).move_to((t2_vertices[1] + t2_vertices[2]) / 2 + np.array([-offset, 0, 0])),
            Text("a", font_size=24).move_to((t3_vertices[1] + t3_vertices[2]) / 2 + np.array([offset, 0, 0])),
            Text("a", font_size=24).move_to((t4_vertices[0] + t4_vertices[1]) / 2 + np.array([0, offset, 0])),     
        ]

        b_labels = [
            Text("b", font_size=24).move_to((t1_vertices[1] + t1_vertices[2]) / 2 + np.array([offset, 0, 0])),
            Text("b", font_size=24).move_to((t2_vertices[0] + t2_vertices[1]) / 2 + np.array([0, -offset, 0])),
            Text("b", font_size=24).move_to((t3_vertices[0] + t3_vertices[1]) / 2 + np.array([0, offset, 0])),
            Text("b", font_size=24).move_to((t4_vertices[1] + t4_vertices[2]) / 2 + np.array([-offset, 0, 0]))
            
        ]

        c_labels = [
            Text("c", font_size=24).move_to((t1_vertices[0] + t1_vertices[2]) / 2 - np.array([offset, -offset, 0])),
            Text("c", font_size=24).move_to((t2_vertices[0] + t2_vertices[2]) / 2 + np.array([offset, offset, 0])),
            Text("c", font_size=24).move_to((t3_vertices[0] + t3_vertices[2]) / 2 - np.array([offset, offset, 0])),
            Text("c", font_size=24).move_to((t4_vertices[0] + t4_vertices[2]) / 2 + np.array([+offset, -offset, 0]))
        ]

        # Animate all labels
        self.play(*[Write(label) for label in a_labels + b_labels + c_labels])
        self.wait(0.5)

        # Adding the C^2 text
        c_squared = Text("C^2", font_size=24).move_to(np.array([0, 0.5, 0]))
        self.play(*[Transform(label, c_squared.copy()) for label in c_labels])

        # Creating the square and removing c^2 label
        s = Square(4, color=WHITE).move_to(np.array([0, 0.5, 0]))
        self.play(Create(s))
        self.wait(1)
        self.play(FadeOut(i) for i in c_labels)  

        # Shifting triangles and labels to form squares
        self.play(t2.animate.shift(t3_vertices[0] - t2_vertices[2]),
                a_labels[1].animate.shift(t3_vertices[0] - t2_vertices[2]),
                b_labels[1].animate.shift(t3_vertices[0] - t2_vertices[2]))
        
        self.play(t4.animate.shift(np.array([0,-2,0])),
                  a_labels[3].animate.shift(np.array([0,-2,0])),
                b_labels[3].animate.shift(np.array([0,-2,0])))
        
        self.play(t1.animate.shift(np.array([-2,0,0])),
                a_labels[0].animate.shift(np.array([-2,0,0])),
                b_labels[0].animate.shift(np.array([-2,0,0])))
        
        # Transforming Labels for leftover area
        a_squared = Text("A^2", font_size=24).move_to(np.array([-1, 1.5, 0]))
        b_squared = Text("B^2", font_size=24).move_to(np.array([1, -0.50, 0]))
        a_labels = [a_labels[1],] + [a_labels[3],]
        self.play(*[Transform(label, a_squared.copy()) for label in a_labels],
                  *[Transform(label, b_squared.copy()) for label in b_labels[0:2]])
    
        # Revealing formula
        formula = Text("A^2 + B^2 = C^2", font_size=24).move_to(np.array([0, -3, 0]))
        self.play(Write(formula))
