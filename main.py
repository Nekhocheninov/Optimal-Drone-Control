import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QSlider, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import model

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Оптимальное управление беспилотным летательным аппаратом для доставки грузов")

        # Создаем вертикальную компоновку
        vbox = QVBoxLayout(self)

        # Создаем отдельный горизонтальный бокс для всех ползунков и меток
        all_sliders_box = QVBoxLayout()

        # Создаем 12 ползунков с метками
        for i in range(12):
            label = QLabel(f'Значение {i + 1}: 0', self)
            slider = QSlider(Qt.Horizontal, self)
            slider.setObjectName(f'horizontalSlider_{i + 1}')  # Set object name for the slider
            slider.setFocusPolicy(Qt.NoFocus)
            slider.valueChanged[int].connect(lambda value, l=label: self.change_value(value, l))

            # Создаем горизонтальную компоновку для каждого ползунка и метки
            hbox = QHBoxLayout()
            hbox.addWidget(label)
            hbox.addWidget(slider)

            # Добавляем горизонтальную компоновку в отдельный бокс
            all_sliders_box.addLayout(hbox)

        # Создаем графики
        self.figures, self.axes = plt.subplots(2, 2, figsize=(10, 8), sharex=True)
        self.canvas = FigureCanvas(self.figures)

        # Добавляем отдельный бокс в вертикальную компоновку
        vbox.addWidget(self.canvas)
        vbox.addLayout(all_sliders_box)

    def change_value(self, value, label):
        label.setText(f'Значение: {value}')
        # Обновляем графики при изменении значения ползунка
        self.update_plot()

    def update_plot(self):
        # Получаем значения всех ползунков
        slider_values = [self.findChild(QSlider, f'horizontalSlider_{i + 1}').value() for i in range(12)]

        flight_time = 10.0 / 10 * 15 * 60 # Время полета (в с)

        P_max = 30      # максимальное значение тяги двигателя в Ньютонах
        V_t0  = 15      # начальная скорость в метрах в секунду
        H_t0  = 10      # текущая   высота   в метрах
        H_T   = 500     # конечная  высота   в метрах

        S     = 0.55    # площадь крыла в метрах^2
        l     = 2.8956  # размах  крыла в метрах
        m     = 11.5    # масса самолета при полных баках в килограммах
        m0    = 6.5     # масса самолета при пустых баках в килограммах
        ma    = 2.0     # масса груза в килограммах

        c     = 0.0045  # Скорость расхода топлива килограммах в секунду

        solution = model.solve(flight_time, S, l, m, m0, ma, c, P_max, V_t0, H_t0, H_T)
        yvalues  = [solution['fuel_mass'],solution['velocity'],solution['altitude'],solution['pitch'],solution['distance']]
        ylabels  = ['Общая масса (кг)', 'Скорость (м/с)', 'Высота (м)', 'Тангаж (рад)', 'Расстояние (м)']
        # Очищаем графики и строим новые
        for i in range(2):
            for j in range(2):
                ax = self.axes[i, j]
                ax.clear()
                idx = i * 2 + j
                ax.plot(solution['solution'].t, yvalues[idx])
                ax.set_xlabel('Время (с)')
                ax.set_ylabel(ylabels[idx])
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Widget()
    window.show()
    sys.exit(app.exec())
