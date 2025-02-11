import math

def euler_method(_x0, _y0, _h, _x_final, _f):
    _x0=float(_x0)
    _y0=float(_y0)
    _h=float(_h)
    _x_final=float(_x_final)
    if _x0+100000*_h<_x_final:
        return [], [], False
    _x_values=[_x0]
    _y_values=[_y0]
    while _x0<_x_final:
        _y0+=_h*_f(_x0,_y0,math.e)
        _x0+=_h
        _x_values.append(round(_x0,8))
        _y_values.append(round(_y0,8))
    return _x_values, _y_values, True