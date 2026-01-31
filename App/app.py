import matplotlib.pyplot as plt
import numpy as np

from App.escapetime import mandelbrot_escape_times, julia_set


class App:
    def __init__(self, x_range, y_range, function, crit_points, figsize=(6, 6)):
        self.x_min, self.x_max = x_range
        self.y_min, self.y_max = y_range
        self.figsize = figsize
        self.function = function
        self.n = 2000
        self.C = 0 + 0j  # complex parameter for Julia
        self.crit_points = crit_points

        # will be created in run()
        self.fig = None
        self.ax = None
        self.ax2 = None
        self.img = None
        self.img2 = None

    def run(self):
        # Initial Mandelbrot grid
        x = np.linspace(self.x_min, self.x_max, self.n)
        y = np.linspace(self.y_min, self.y_max, self.n)
        X, Y = np.meshgrid(x, y)

        out = mandelbrot_escape_times(X + 1j * Y, self.function, self.crit_points)

        plt.ion()

        # ONE figure, TWO axes (side-by-side)
        self.fig, (self.ax, self.ax2) = plt.subplots(
            1, 2, figsize=(self.figsize[0] * 2, self.figsize[1])
        )

        # Connect events to the SAME canvas
        self.fig.canvas.mpl_connect("button_release_event", self.onClick)
        self.fig.canvas.mpl_connect("button_release_event", self.onClickJulia)

        # Mandelbrot image (left)
        self.img = self.ax.imshow(
            out,
            extent=[self.x_min, self.x_max, self.y_min, self.y_max],
            origin="lower",
            cmap="magma",
        )
        self.ax.set_title("Mandelbrot")

        # Initial Julia image (right), fixed view [-2,2]x[-2,2]
        xj = np.linspace(-2, 2, self.n)
        yj = np.linspace(-2, 2, self.n)
        Xj, Yj = np.meshgrid(xj, yj)

        self.img2 = self.ax2.imshow(
            julia_set(self.C, Xj + 1j * Yj, self.function),
            extent=[-2, 2, -2, 2],
            origin="lower",
            cmap="magma",
        )
        self.ax2.set_title("Julia (right-click Mandelbrot to set c)")

        # Optional: make layout nicer
        self.fig.tight_layout()

        plt.show(block=True)

    def onClickJulia(self, event):
        # Only react to clicks inside the Julia axes
        if event.inaxes != self.ax2:
            return

        # Example behavior: recompute Julia for the current zoom of Julia axes
        print("zoom Julia")
        xmin, xmax = self.ax2.get_xlim()
        ymin, ymax = self.ax2.get_ylim()

        x = np.linspace(xmin, xmax, self.n)
        y = np.linspace(ymin, ymax, self.n)
        X, Y = np.meshgrid(x, y)

        out = julia_set(self.C, X + 1j * Y, self.function)

        self.img2.set_data(out)
        self.img2.set_extent((xmin, xmax, ymin, ymax))
        self.ax2.figure.canvas.draw_idle()

    def onClick(self, event):
        # Only react to clicks inside the Mandelbrot axes
        if event.inaxes != self.ax:
            return

        # Right click -> set C and redraw Julia (in its current view)
        if event.button == 3:
            if event.xdata is None or event.ydata is None:
                return

            coord = event.xdata + 1j * event.ydata
            self.C = coord

            # Recompute Julia on current Julia zoom window (so zoom is preserved)
            xmin, xmax = self.ax2.get_xlim()
            ymin, ymax = self.ax2.get_ylim()

            x = np.linspace(xmin, xmax, self.n)
            y = np.linspace(ymin, ymax, self.n)
            X, Y = np.meshgrid(x, y)

            out = julia_set(coord, X + 1j * Y, self.function)

            self.fig.suptitle(
                f"Julia set for c={self.C.real:.3f}+{self.C.imag:.3f}i"
            )

            self.img2.set_data(out)
            self.img2.set_extent((xmin, xmax, ymin, ymax))
            self.ax2.figure.canvas.draw_idle()
            return

        # Left click (or any non-right click) -> recompute Mandelbrot for current zoom
        self.x_min, self.x_max = self.ax.get_xlim()
        self.y_min, self.y_max = self.ax.get_ylim()
        print(self.x_min, self.x_max, self.y_min, self.y_max)

        x = np.linspace(self.x_min, self.x_max, self.n)
        y = np.linspace(self.y_min, self.y_max, self.n)
        X, Y = np.meshgrid(x, y)

        out = mandelbrot_escape_times(X + 1j * Y, self.function, self.crit_points)

        self.img.set_data(out)
        self.img.set_extent((self.x_min, self.x_max, self.y_min, self.y_max))
        self.ax.figure.canvas.draw_idle()
