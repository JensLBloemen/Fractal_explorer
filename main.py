from App.app import App
import numba

@numba.njit
def f(z, c):
    return z * z + c

if __name__ == "__main__":
    app = App([-2, 2], [-3, 3], f)
    app.run()