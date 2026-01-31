from App.app import App
from Lib.pow_int import pow_int
import numba

@numba.njit
def f(z, c):
    return pow_int(z, 4) + c

critical_points = [complex(0, 0)]

if __name__ == "__main__":
    app = App([-2, 2], [-3, 3], f, critical_points)
    app.run()