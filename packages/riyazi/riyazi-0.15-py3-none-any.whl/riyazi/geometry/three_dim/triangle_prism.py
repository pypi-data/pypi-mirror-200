import Riyazi as a
import math
def v_triangular_prism(a, b, c, h):
    return (1/4) * h * math.sqrt(-a ** 4 + 2 * (a * b) ** 2 + 2 * (a * c) ** 2 - b ** 4 + 2 * (b * c) ** 2 - c ** 4)