import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append("../src")
import ec

_a = -2
_b = 2
_Gx = -1.4029
_Gy = 1.4052

def plot_reals_by_doubling():
    _setup_reals_plot()

    xs, ys = [_Gx], [_Gy]
    x, y = _Gx, _Gy
    for i in range(1,4):
        x, y = _double(x, y, _a)

        plt.scatter(x, -y, color="black")
        plt.annotate(f"{-(1<<i)}P", [x+.1, -y+.1])

        plt.scatter(x, y, color="black")
        plt.annotate(f"{1<<i}P", [x+.1, y+.1])

        xs.extend([x, x])
        ys.extend([-y, y])

    plt.plot(xs, ys)

    plt.grid()
    plt.show()

def plot_reals_by_adding():
    _setup_reals_plot()

    xs, ys = [_Gx], [_Gy]
    x, y = _Gx, _Gy
    for i in range(1, 8):
        if i == 1:
            x, y = _double(x, y, _a)
        else:
            x, y = _add(_Gx, _Gy, x, y)

        plt.scatter(x, -y, color="black")
        plt.annotate(f"{-(i+1)}P", [x+.1, -y+.1])

        plt.scatter(x, y, color="black")
        plt.annotate(f"{i+1}P", [x+.1, y+.1])

        xs.extend([x, x])
        ys.extend([-y, y])

    plt.plot(xs, ys)

    plt.grid()
    plt.show()

def _setup_reals_plot():
    y, x = np.ogrid[-12:12:100j, -12:12:100j]
    plt.contour(x.ravel(), y.ravel(), pow(y, 2) - pow(x, 3) - _a*x - _b, [0])

    plt.scatter(_Gx, _Gy, color="black")
    plt.annotate("P", [_Gx-.2, _Gy+.2])

def _double(x, y, a):
    slope = ((3 * pow(x, 2)) + a) / (2 * y)
    x1 = pow(slope, 2) - 2 * x
    y1 = (slope * (x - x1)) - y
    return x1, y1

def _add(x1, y1, x2, y2):
    slope = (y2 - y1) / (x2 - x1)
    x3 = pow(slope, 2) - (x2 + x1)
    y3 = (slope * x2) - (slope * x3) - y2
    return x3, y3

def plot_ints():
    _setup_ints_plot()

    ec.new_curve(23,1,4,0,2,29,1,5)

    pt = ec._G
    plt.scatter(pt[0], pt[1], color="black")
    plt.annotate(f"({pt[0]},{pt[1]})", [pt[0], pt[1]])
    
    while pt != ec._i:
        pt = ec.add(ec._G, pt)
        plt.scatter(pt[0], pt[1], color="black")
        if pt != ec._i:
            plt.annotate(f"({pt[0]},{pt[1]})", [pt[0], pt[1]])

    plt.grid()
    plt.show()

def _setup_ints_plot():
    np.ogrid[0:30:100j, 0:30:100j]