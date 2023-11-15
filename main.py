import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

c_x0  = 0.0434  # коэффициент минимального лобового сопротивления
c_y0  = 0.23    # коэффициент подъемной силы при нулевом уголе тангажа
c_ya  = 5.6106  # коэффициент производной первого порядка по углу атаки
S     = 0.55    # площадь крыла в метрах^2
l     = 2.8956  # размах  крыла в метрах
m     = 13.5    # масса самолета при полных баках в килограммах
e     = 0.75    # коэффициент Освальда
g     = 9.80665 # ускорение свободного падения
u     = 10      # угол тангажа
o     = 0       # траекторный угол
m_c   = 0.0002  # секундный расход топлива при максимальной тяге в килограммах в секунду
P_max = 70      # максимальное значение тяги двигателя
V_t0  = 20      # начальная скорость в метрах в секунду
V_T   = 20      # конечная  скорость в метрах в секунду
H_t0  = 50      # текущая   высота   в метрах
H_T   = 1000    # конечная  высота   в метрах

# плотность воздуха
def air_density(height):
    T0 = 288.15    # стандартная температура на уровне моря в Кельвинах
    P0 = 101325    # стандартное давление    на уровне моря в Паскалях
    L  = 0.0065    # градиент температуры в Кельвинах на метр
    R  = 8.31447   # универсальная газовая постоянная в Дж/(моль·К)
    M  = 0.0289644 # молярная масса воздуха в кг/моль
    T = T0 - L * height                                   # Рассчет температуры на заданной высоте
    P = P0 * (1 - L * height / T0) ** (9.8 * M / (R * L)) # Рассчет давления    на заданной высоте
    rho = P / (R * T)                                     # Рассчет плотности по уравнению состояния газа
    return rho

# Функция управления тягой при наборе высоты
def control_P(H, V):
    return (c_x0 + c_ya * (u - o)**2 * S / (np.pi * e * l**2)) * S * air_density(H) * V**2 / 2 + m * g * np.sin(o)

# Функция управления углом атаки при наборе скорости
def control_a(H, V, P):
    return (m * g - c_y0 * S * air_density(H) * V**2 / 2) / (c_ya * S * air_density(H) * V**2 / 2 + P)

# Функции, представляющие систему дифференциальных уравнений при наборе высоты
def system_H(t, y):
    o, H, m, V = y
    do = t * ((control_P(H, V) * (u - o) + (c_y0 + c_ya * (u - o)) * S * air_density(H) * V**2 / 2) / (m * V) - (g * np.cos(o) / V))
    dH = t * V * np.sin(o)
    dm = t * (-m_c)
    return [do, dH, dm, V]

# Функции, представляющие систему дифференциальных уравнений при наборе скорости
def system_V(t, y):
    V, x, m, H = y
    dV = t * (P_max - (c_x0 + (c_ya * control_a(H, V, P_max)**2 * S) / (np.pi * e * l**2) * S * air_density(H) * V**2 / 2)) / m
    dx = t * V
    dm = t * (-m_c)
    return [dV, dx, dm, H]

t_span = (0, 5) # Время
initial_conditions_H = [o, H_t0, m, V_t0]

solution_H = solve_ivp(system_H, t_span, initial_conditions_H, t_eval=np.linspace(0, 5, 5))

print(system_H(1, initial_conditions_H))
print(solution_H.y[1])
plt.plot(solution_H.t, solution_H.y[0], label='o(t)')
plt.plot(solution_H.t, solution_H.y[1], label='H(t)')
plt.plot(solution_H.t, solution_H.y[2], label='m(t)')
plt.show()