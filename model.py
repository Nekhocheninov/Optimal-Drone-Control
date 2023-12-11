import numpy as np
from scipy.integrate import solve_ivp

# Плотность воздуха
def air_density(height):
    T0 = 288.15    # стандартная температура на уровне моря в Кельвинах
    P0 = 101325    # стандартное давление    на уровне моря в Паскалях
    L  = 0.0065    # градиент температуры в Кельвинах на метр
    R  = 287.05    # универсальная газовая постоянная в Дж/(кг·К)
    M  = 0.0289644 # молярная масса воздуха в кг/моль
    # Рассчет температуры на заданной высоте
    # Рассчет давления    на заданной высоте
    # Рассчет плотности по уравнению состояния газа
    T = T0 - L * height
    P = P0 * (1 - L * height / T0) ** (9.8 * M / (R * L))
    rho = P / (R * T)
    return rho

def func(height, velocity, S):
    return S * air_density(height) * velocity**2 / 2

# Система уравнений
def aircraft_model(t, y, S, l, P_max, H_T, m0, ma, c):
    m, v, h, theta, x = y

    g     = 9.80665 # ускорение свободного падения
    e     = 0.75    # коэффициент Освальда
    c_x0  = 0.0434  # коэффициент минимального лобового сопротивления
    c_y0  = 0.23    # коэффициент подъемной силы при нулевом уголе тангажа
    c_ya  = 5.6106  # коэффициент производной первого порядка по углу атаки

    u = np.radians(10)
    a = u - theta
    if m < (m0+ma):
        P_max = 0
        c = 0.0
    if (h > H_T) & (m > (m0+ma)):
        dt_dt = -theta
    else:
        dt_dt = 57.3 * ((((P_max * a) / 57.3) + (c_y0 + c_ya * a) * func(h, v, S)) / (m * v) - g * np.cos(theta) / v)
        if (dt_dt > 0) & (m <= (m0+ma)):
            dt_dt = 0
    dm_dt = -c
    dh_dt = v * np.sin(theta)
    dv_dt = (P_max - (c_x0 + (c_ya * a)**2 * S / (np.pi * e * l**2)) * func(h, v, S)) / m - g * np.sin(theta)
    dx_dt = v * np.cos(theta)

    return [dm_dt, dv_dt, dh_dt, dt_dt, dx_dt]

def solve(t_1, t_2, n_t, S, l, m, m0, ma, c, P_max, V_t0, H_t0, H_T, theta, x):

    # Временные точки для решения уравнения
    time_points = np.linspace(t_1, t_2, n_t)

    # Начальные значения массы, скорости, высоты, тангажа и расстояния
    initial_conditions = [m+ma, V_t0, H_t0, theta, x]

    # Решение системы уравнений
    solution = solve_ivp(
        lambda t, y: aircraft_model(t, y, S, l, P_max, H_T, m0, ma, c),
        y0 = initial_conditions,
        t_eval = time_points,
        t_span = (time_points[0], time_points[-1]),
        method='RK45',
        atol = 1e-8,
        rtol = 1e-8,
        dense_output = True
    )
    # Извлечение решений
    fuel_mass, velocity, altitude, pitch, distance  = solution.y[0], solution.y[1], solution.y[2], solution.y[3], solution.y[4]
    return {'solution':solution, 'fuel_mass':fuel_mass, 'velocity':velocity, 'altitude':altitude, 'pitch':pitch, 'distance':distance}

def concatenate(a, b):
    return np.concatenate((a, b))