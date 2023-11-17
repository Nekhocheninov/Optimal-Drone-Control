import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

c_x0  = 0.0434  # коэффициент минимального лобового сопротивления
c_y0  = 0.23    # коэффициент подъемной силы при нулевом угле тангажа
c_ya  = 5.6106  # коэффициент производной первого порядка по углу атаки
S     = 0.55    # площадь крыла в метрах^2
l     = 2.8956  # размах  крыла в метрах
m     = 13.5    # масса самолета при полных баках в килограммах
e     = 0.75    # коэффициент Освальда
g     = 9.80665 # ускорение свободного падения
u     = np.radians(10) # угол тангажа     в градусах
o     = np.radians(10) # траекторный угол в градусах
m_c   = 0.0002  # секундный расход топлива при максимальной тяге в кг в секунду
P_max = 70      # максимальное значение тяги двигателя в Ньютонах
V_t0  = 20      # начальная скорость в метрах в секунду
V_T   = 50      # конечная  скорость в метрах в секунду
H_t0  = 50      # текущая   высота   в метрах
H_T   = 1000    # конечная  высота   в метрах

time_values = np.arange(0, 10.1, 0.1)
t_span = (0, 10) # Время

# плотность воздуха
def air_density(height):
    T0 = 288.15    # стандартная температура на уровне моря в Кельвинах
    P0 = 101325    # стандартное давление    на уровне моря в Паскалях
    L  = 0.0065    # градиент температуры в Кельвинах на метр
    R  = 287.05    # универсальная газовая постоянная в Дж/(кг·К)
    M  = 0.0289644 # молярная масса воздуха в кг/моль
    # Расчет температуры на заданной высоте
    # Расчет давления    на заданной высоте
    # Расчет плотности по уравнению состояния газа
    T = T0 - L * height
    P = P0 * (1 - L * height / T0) ** (9.8 * M / (R * L))
    rho = P / (R * T)
    return rho

# Функция управления тягой при наборе высоты
def control_P(H, V):
    return (c_x0 + c_ya * (u - o)**2 * S / (np.pi * e * l**2)) * S * air_density(H) * V**2 / 2 + m * g * np.sin(o)

# Функция управления углом атаки при наборе скорости
def control_a(H, V, P):
    return (m * g - c_y0 * S * air_density(H) * V**2 / 2) / (c_ya * S * air_density(H) * V**2 / 2 + P)

# Функции, представляющие систему дифференциальных уравнений при наборе высоты
def system_H(t, y, V):
    o, H, m = y
    do = t * ((control_P(H, V) * (u - o) + (c_y0 + c_ya * (u - o)) * S * air_density(H) * V**2 / 2) / (m * V) - (g * np.cos(o) / V))
    dH = t * V * np.sin(o)
    dm = t * (-m_c)
    return [do, dH, dm]

# Функции, представляющие систему дифференциальных уравнений при наборе скорости
def system_V(t, y, H):
    V, x, m = y
    dV = t * (P_max - (c_x0 + (c_ya * control_a(H, V, P_max)**2 * S) / (np.pi * e * l**2) * S * air_density(H) * V**2 / 2)) / m
    dx = t * V
    dm = t * (-m_c)
    return [dV, dx, dm]

initial_conditions_V = [V_t0, 0, m]
solution_H = solve_ivp(lambda t, y: system_V(t, y, H_t0), t_span, initial_conditions_V, t_eval = time_values)
plt.plot(solution_H.t, solution_H.y[0], label='o(t)')
plt.plot(solution_H.t, solution_H.y[1], label='H(t)')
plt.plot(solution_H.t, solution_H.y[2], label='m(t)')
plt.show()

initial_conditions_H = [o, H_t0, m]
solution_V = solve_ivp(lambda t, y: system_H(t, y, V_t0), t_span, initial_conditions_H, t_eval = time_values)
plt.plot(solution_V.t, solution_V.y[0], label='V(t)')
plt.plot(solution_V.t, solution_V.y[1], label='x(t)')
plt.plot(solution_V.t, solution_V.y[2], label='m(t)')
plt.show()