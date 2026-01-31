import numpy as np
import numba

@numba.njit
def mandelbrot_escape_times(C, f, crit_points, max_iter=200, R=2):
    h, w = C.shape
    iters = np.zeros((h, w), dtype=np.int32)

    for i in range(h):
        for j in range(w):
            c = C[i, j]

            for crit_point in crit_points:
                z = crit_point
                if iters[i, j] != 0:
                    break
                for n in range(max_iter):
                    z = f(z, c)
                    if (z.real*z.real + z.imag*z.imag) > R*R:
                        iters[i, j] = n
                        break
                else:
                    iters[i, j] = max_iter

    return iters


@numba.njit
def julia_set(c, XY, f, max_iter=200, R=500):
    h, w = XY.shape
    iters = np.zeros((h, w), dtype=np.int32)
    for i in range(h):
        for j in range(w):
            z = XY[i, j]
            for n in range(max_iter):
                z = f(z, c)
                if (z.real * z.real + z.imag * z.imag) > R * R:
                    iters[i, j] = n
                    break
            else:
                iters[i, j] = max_iter
    return iters    
