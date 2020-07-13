import numpy as np

def RK4(func, y0, t, args=(), filename=False):
    """
    Integrate a system of ordinary differential equations.
    
    y' = f(t, y), y(t_0) = y_0

    Parameters
    ----------
    func : callable
        Right-hand side of the system. The calling signature is ``fun(t, y)``.
    y0 : array
        Initial condition on y.
    t : array
        A sequence of time points for which to solve for y.
    args : tuple, optional
        Additional arguments to pass to the user-defined functions.
    filename : str
        write data in file.
    """
    n = len(t)
    y = y0
    f = open(filename, 'w')
    f.write("# column: t, y\n")
    f.write(str(t[0]))
    for i in y0:
        f.write(', ' + str(i))
    f.write('\n')
    for i in range(n - 1):
        h = t[i+1] - t[i]
        k1 = h * func(t[i], y, *args) 
        k2 = h * func(t[i] + 0.5 * h, y + 0.5 * k1, *args) 
        k3 = h * func(t[i] + 0.5 * h, y + 0.5 * k2, *args) 
        k4 = h * func(t[i] + h, y + k3, *args)
        y += (1.0 / 6.0)*(k1 + 2 * k2 + 2 * k3 + k4)
        f.write(str(t[i+1]))
        for i in y:
            f.write(', ' + str(i))
        f.write('\n')
    f.close()

if __name__ == "__main__":
    def lotkavolterra(t, z, a, b, c, d):
        x, y = z
        return np.array([a*x - b*x*y, -c*y + d*x*y])
    
    t = np.linspace(0, 15, 300)
    RK4(lotkavolterra, [10, 5], t, args=(1.5, 1, 3, 1), filename='ode.txt')