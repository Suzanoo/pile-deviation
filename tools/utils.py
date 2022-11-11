import numpy as np
import pandas as pd

def board_cast(x, p):
    coor = np.empty(shape=1)
    for i in range(len(x)):
        # broadcasting
        # https://numpy.org/doc/1.20/user/theory.broadcasting.html
        temp = x[i]+ p[:, np.newaxis]
        temp = temp.flatten()
        coor = np.concatenate((coor, temp), axis=None)
        # add None: see
        # https://plotly.com/python/shapes/
        coor = np.concatenate((coor, None), axis=None)
    return coor[1:-1]

def create_df(x, y, px, py):
    x = board_cast(x, px)
    y = board_cast(y, py)
    df = pd.DataFrame({
        'x' : x,
        'y' : y,
    })
    return df

'''p = 40
px = np.array([p/2, -p/2, -p/2, p/2, p/2]) #[p1, p2, p3, ..., p1] local x-coordinate, m
py = np.array([p/2, p/2, -p/2, -p/2, p/2])

X = [60,-60]
Y = [0, 0]

ex = [5, 2]
ey = [0, -5]

X_new = np.array(X) + np.array(ex)
Y_new = np.array(Y) + np.array(ey)

rx = X_new.sum()
ry = Y_new.sum()
unit_vector = np.array([rx, ry])
R = np.linalg.norm(unit_vector)

unit_vector.reshape(-1, 2)
unit_vector.T

df1 = create_df(X, Y, px, py)
df2 = create_df(X_new, Y_new, px, py)'''


