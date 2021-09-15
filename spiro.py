import math
import turtle
import math
import sys, argparse, random
import numpy as np
from PIL import Image
from datetime import datetime
from fractions import _gcd


# a class that draws a SpiroGraph
class Spiro:
    def __init__(self, xc, yc, col, R, r, l):
        # create the turtle object
        self.t = turtle.Turtle()
        # set the cursor shape
        self.t.shape('turtle')
        # set the step indegrees
        self.step = 5
        # set the drawing complete flag
        self.drawingComplete = False

        # set the parameters
        self.setparams(xc, yc, col, R, r, l)

        # initialize the drawing
        self.restart()

    def setparams(self, xc, yc, col, R, r, l):
        self.xc = xc
        self.yc = yc
        self.R = int(R)
        self.r = int(r)
        self.l = l
        self.col = col
        # reduce r/R to its smallest form by dividing with the GCD
        gcdVal = _gcd(self.r, self.R)
        self.nRot = self.r // gcdVal
        # get ratio of radii
        self.k = r / float(R)
        self.t.color(*col)
        # store the current angle
        self.a = 0

    def restart(self):
        self.drawingComplete = False
        self.t.showturtle()
        # go to the first point
        self.t.up()
        R, k, l = self.R, self.k, self.l
        a = 0.0
        x = R * ((1 - k) * math.cos(a) + l * k * math.cos((1 - k) * a / k))
        y = R * ((1 - k) * math.sin(a) - l * k * math.sin((1 - k) * a / k))
        self.t.setpos(self.xc + x, self.yc + y)
        self.t.down()

    def draw(self):
        R, k, l = self.R, self.k, self.l
        for i in range(0, 360 * self.nRot + 1, self.step):
            a = math.radians(i)
            x = R * ((1 - k) * math.cos(a) + l * k * math.cos((1 - k) * a / k))
            y = R * ((1 - k) * math.sin(a) - l * k * math.sin((1 - k) * a / k))
            self.t.setpos(self.xc + x, self.yc + y)
        # drawing is now done so hide the turtle cursor
        self.t.hideturtle()

    def update(self):
        if self.drawingComplete:
            return

        self.a += self.step
        R, k, l = self.R, self.k, self.l
        a = math.radians(self.a)
        x = R * ((1 - k) * math.cos(a) + l * k * math.cos((1 - k) * a / k))
        y = R * ((1 - k) * math.sin(a) - l * k * math.sin((1 - k) * a / k))
        self.t.setpos(self.xc + x, self.yc + y)
        if self.a >= 360 * self.nRot:
            self.drawingComplete = True
            self.t.hideturtle()

class SpiroAnimator:
    def __init__(self, N):
        self.deltaT = 10
        self.width = turtle.window_width()
        self.height = turtle.window_height()
        # create the Spiro objects
        self.spiros = []
        for i in range(N):
            # generate random parameters
            rparams = self.genRandomParams()
            # set the spiro parameters
            spiro = Spiro(*rparams)
            self.spiros.append(spiro)
            turtle.ontimer(self.update(), self.deltaT)

    def genRandomParams(self):
        width, height = self.width, self.height
        R = random.randint(50, min(width, height) // 2)
        r = random.randint(10, 9 * R // 10)
        l = random.uniform(0.1, 0.9)
        xc = random.randint(-width // 2, width // 2)
        yc = random.randint(-height // 2, height // 2)
        col = (random.random(), random.random(), random.random())
        return (xc, yc, col, R, r, l)

    def restart(self):
        for spiro in self.spiros:
            spiro.clear()
            rparams = self.genRandomParams()
            spiro.setparams(*rparams)
            spiro.restart()

    def update(self):
        nComplete = 0
        for spiro in self.spiros:
            spiro.update()
            if spiro.drawingComplete:
                nComplete += 1

        # restart if all spiros are complete
        if nComplete == len(self.spiros):
            self.restart()
        # call the timer
        turtle.ontimer(self.update(), self.deltaT)

    def toggleTurtles(self):
        for spiro in self.spiros:
            if spiro.t.isvisible():
                spiro.t.hideturtle()
            else:
                spiro.t.showturtle()

    def saveDrawing(self):
        turtle.hideturtle()
        # generate unique filenames
        dateStr = (datetime.now()).strftime("%d%b%Y-%H%M%S")
        fileName = 'spiro-' + dateStr
        print('saving drawing to %s.eps/png' % fileName)
        # get the tkinter canvas
        canvas = turtle.getcanvas()
        # save the drawing as a postcript image
        canvas.postscript(file = fileName + '.eps')
        # use the Pillow module to convert the postscript image file to PNG
        img = Image.open(fileName + '.eps')
        img.save(fileName + '.png', 'png')
        # show the turtle cursor
        turtle.showturtle()

def main():
    print('generating spirograph...')
    description = """This program draws Spirographs using the Turtle module.
    When run with no arguments, this program draws random Spirographs.
    
    Terminology:
    
    R: radius of outer circle
    r: radius of inner circle
    l: ratio of hole distance to r
    """

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--sparams', nargs=3, dest='sparams', required=False, help="The three arguments in sparams: R, r, l.")

    args = parser.parse_args()
    turtle.setup(width=0.8)
    turtle.shape('turtle')

    turtle.title("Spirographs!")
    turtle.onkey(SpiroAnimator.saveDrawing, "s")
    turtle.listen()

    turtle.hideturtle()

    if args.sparams:
        params = [float(x) for x in args.sparams]
        col = (0.0, 0.0, 0.0)
        spiro = Spiro(0, 0, col, *params)
        spiro.draw()
    else:
        # create the animator object
        spiroAnim = SpiroAnimator(4)
        turtle.onkey(spiroAnim.toggleTurtles, "t")
        turtle.onkey(spiroAnim.restart, "space")

    turtle.mainloop()

if __name__ == '__main__':
    main()


