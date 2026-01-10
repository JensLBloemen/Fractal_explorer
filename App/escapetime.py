import numpy as np
import numba

@numba.njit
def mandelbrot_escape_times(C, max_iter=200, R=2):
    h, w = C.shape
    iters = np.zeros((h, w), dtype=np.int32)

    for i in range(h):
        for j in range(w):
            c = C[i, j]
            z = 0.0 + 0.0j

            for n in range(max_iter):
                z = z*z + c
                if (z.real*z.real + z.imag*z.imag) > R*R:
                    iters[i, j] = n
                    break
            else:
                iters[i, j] = max_iter

    return iters


@numba.njit
def julia_set(C, XY, max_iter=200, R=500):
    h, w = XY.shape
    iters = np.zeros((h, w), dtype=np.int32)
    for i in range(h):
        for j in range(w):
            z = XY[i, j]
            for n in range(max_iter):
                z = z*z + C
                if (z.real * z.real + z.imag * z.imag) > R * R:
                    iters[i, j] = n
                    break
            else:
                iters[i, j] = max_iter
    return iters    
