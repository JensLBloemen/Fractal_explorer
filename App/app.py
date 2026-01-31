import matplotlib.pyplot as plt
import numpy as np

from App.escapetime import mandelbrot_escape_times, julia_set

class App:
    def __init__(self, x_range, y_range, function, figsize=(6, 6)):
        self.x_min, self.x_max = x_range
        self.y_min, self.y_max = y_range
        self.figsize = figsize
        self.function = function
        self.n = 2000
        self.C = 0

    def run(self):
        x = np.linspace(self.x_min, self.x_max, self.n)
        y = np.linspace(self.y_min, self.y_max, self.n)

        grid = np.meshgrid(x, y)
        X, Y = grid
        out = mandelbrot_escape_times(X + 1j*Y, self.function)


        plt.ion()
        self.fig, self.ax = plt.subplots(figsize = self.figsize)
        self.fig2, self.ax2 = plt.subplots(figsize=self.figsize)

        self.fig.canvas.mpl_connect('button_release_event', self.onClick)

        self.fig2.canvas.mpl_connect('button_release_event', self.onClickJulia)




        self.img = self.ax.imshow(out, 
                                  extent=[self.x_min, self.x_max,self.y_min,self.y_max],
                                  origin="lower",
                                  cmap="magma")
        
        self.img2 = self.ax2.imshow(julia_set(self.C, X + 1j*Y, self.function), 
                                  extent=[-2,2,-2,2],
                                  origin="lower")
        
        plt.show(block=True)

    def onClickJulia(self, event):
        print("zoom Julia")
        xmin, xmax = self.ax2.get_xlim()
        ymin, ymax = self.ax2.get_ylim()
        x = np.linspace(xmin, xmax, self.n)
        y = np.linspace(ymin, ymax, self.n)

        grid = np.meshgrid(x, y)
        X, Y = grid
        out = julia_set(self.C, X + 1j * Y, self.function)

        self.img2.set_data(out)
        self.img2.set_extent((xmin, xmax, ymin, ymax))
        self.ax2.figure.canvas.draw_idle()


    def onClick(self, event):
        if event.button == 3:
            coord = event.xdata + 1j* event.ydata
            self.C = coord

            x = np.linspace(-2, 2, self.n)
            y = np.linspace(-2, 2, self.n)

            grid = np.meshgrid(x, y)
            X, Y = grid


            out = julia_set(coord, X + 1j * Y, self.function)
            self.fig2.suptitle(f"Julia set for c={round(self.C.real,3)}+{round(self.C.imag,3)}i")

            self.img2.set_data(out)
            # self.img2.set_extent((self.x_min, self.x_max, self.y_min, self.y_max))
            self.ax2.figure.canvas.draw_idle()

            return

        self.x_min, self.x_max = self.ax.get_xlim()
        self.y_min, self.y_max = self.ax.get_ylim()
        print(self.x_min, self.x_max, self.y_min, self.y_max)


        x = np.linspace(self.x_min, self.x_max, self.n)
        y = np.linspace(self.y_min, self.y_max, self.n)

        grid = np.meshgrid(x, y)
        X, Y = grid
        out = mandelbrot_escape_times(X + 1j*Y, self.function)

        self.img.set_data(out)
        self.img.set_extent((self.x_min, self.x_max, self.y_min, self.y_max))
        self.ax.figure.canvas.draw_idle()
