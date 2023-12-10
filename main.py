import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QSlider, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QGridLayout
from PySide6.QtGui import QIntValidator, QAction
from PySide6.QtCore import Qt, QEvent
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import model

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Оптимальное управление беспилотным летательным аппаратом для доставки грузов")
        central_widget = QWidget(self)
        self.status_label = QLabel(self)
        self.statusBar().addWidget(self.status_label, 1)
        self.setCentralWidget(central_widget)
        self.setup_ui(central_widget)

    def setup_ui(self, central_widget):
        grid_layout = QGridLayout(central_widget)
        sliders_layout = QVBoxLayout()
        Labels_1 = ['Площадь крыла в метрах^2', 'Размах крыла в метрах', 'Масса дрона при пустых баках в килограммах',
                    'Масса дрона при полных баках в килограммах', 'Максимальное значение тяги двигателя в Ньютонах',
                    'Скорость расхода топлива килограммах в секунду', 'Текущая скорость в метрах в секунду',
                    'Текущая высота в метрах', 'Конечная высота в метрах', 'Масса груза в килограммах',
                    'Продолжительность полета в секундах', 'Момент времени сброса груза', 'Конечная высота после сброса груза в метрах']
        Labels_2 = ['S', 'l', 'm_0', 'm_max', 'P_max', 'c', 'V_0', 'H_0', 'H_max', 'm_a', 't', 't_a', 'H_max_a']
        Variables = ['0.55', '2.8956', '6.5', '11.5', '30', '0.0045', '15', '10', '500', '2.0', '1800', '900', '1000']

        toolTips = ['Площадь крыла влияет на подъемную силу и маневренность. Большая площадь обеспечивает высокую грузоподъемность, маленькая - повышает маневренность, но уменьшает грузоподъемность и продолжительность полета.',
                    'Размах крыла влияет на подъемную силу и маневренность. Больший размах способствует грузоподъемности, меньший — повышает маневренность и скорость.',
                    'Масса дрона при пустых баках',
                    'Масса дрона при полных баках',
                    'Тяга двигателя влияет на способность дрона нести грузы и подниматься в воздухе. Более высокая максимальная тяга обычно позволяет дрону подниматься на большие высоты и носить тяжелые грузы.',
                    'Скорость, с которой двигатель дрона расходует топливо',
                    'Скорость, которую дрон имеет изначально',
                    'Высота, на которой дрон находится изначально',
                    'Высота, которую дрон не будет превышать',
                    'Масса груза для доставки дроном',
                    'Общая продолжительность полета дрона для расчета',
                    'Момент времени, когда дрон должен сбросить груз',
                    'Новое значение высоты, которую дрон не будет превышать']

        for i in range(13):
            label_1 = QLabel(Labels_1[i] + ':', central_widget)
            label_2 = QLabel(Labels_2[i] + ' =', central_widget)
            label_2.setFixedWidth(50)
            edit = QLineEdit(central_widget)
            edit.setFixedWidth(50)
            int_validator = QIntValidator()
            edit.setValidator(int_validator)
            slider = QSlider(Qt.Horizontal, central_widget)
            edit.setObjectName(f'horizontalEdit_{i + 1}')
            slider.setFocusPolicy(Qt.NoFocus)
            slider.setMinimum(0)
            slider.setStyleSheet("border: 0px dashed black;")
            edit.setStyleSheet("border: 0px dashed black;")
            label_2.setStyleSheet("border: 0px dashed black;")
            label_1.setStyleSheet("border: 0px dashed black;")
            
            if i in [0, 1]:
                slider.setMaximum(20)
                slider.setSingleStep(1)
                slider.setValue(float(Variables[i]) * 2)
                slider.valueChanged[int].connect(lambda value, e=edit: e.setText(str(value / 2)))
            elif i in [2, 3, 4, 6, 9]:
                slider.setMaximum(200)
                slider.setSingleStep(1)
                slider.setValue(float(Variables[i]) * 2)
                slider.valueChanged[int].connect(lambda value, e=edit: e.setText(str(value / 2)))
            elif i == 5:
                slider.setMaximum(1000)
                slider.setSingleStep(1)
                slider.setValue(float(Variables[i]) * 8000)
                slider.valueChanged[int].connect(lambda value, e=edit: e.setText(str(value / 8000)))
            elif i in [7, 8, 10, 11, 12]:
                slider.setMaximum(5000)
                slider.setSingleStep(10)
                slider.setValue(float(Variables[i]))
                slider.valueChanged[int].connect(lambda value, e=edit: e.setText(str(value)))

            initial_value = Variables[i]
            edit.setText(str(initial_value))

            edit.setToolTip(f"Подсказка: {toolTips[i]}")
            slider.setToolTip(f"Подсказка: {toolTips[i]}")

            edit.installEventFilter(self)
            slider.installEventFilter(self)

            row_layout = QVBoxLayout()
            row_layout.addWidget(label_1)

            inner_layout = QHBoxLayout()
            inner_layout.addWidget(label_2)
            inner_layout.addWidget(edit)
            inner_layout.addWidget(slider)
            row_layout.addLayout(inner_layout)
            sliders_layout.addLayout(row_layout)

        self.figures, self.axes = plt.subplots(3, 2, figsize=(16, 6), sharex=True)
        self.figures.suptitle("Изменение параметров системы", fontsize=14)
        self.figures.patch.set_edgecolor('gray')
        self.figures.patch.set_linewidth(2)
        self.figures.delaxes(self.axes[2, 1])
        self.canvas = FigureCanvas(self.figures)

        grid_layout.addWidget(self.canvas, 0, 0, 1, 1)
        
        self.update_plot()

        label = QLabel("Параметы системы:", central_widget)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("border: 0px solid black;")
        
        sliders_container = QWidget()
        sliders_container_layout = QVBoxLayout(sliders_container)
        sliders_container_layout.addWidget(label)
        sliders_container_layout.addLayout(sliders_layout)
        sliders_container.setStyleSheet("border: 1px solid gray;")

        grid_layout.addWidget(sliders_container, 0, 1, 1, 1)

        update_button = QPushButton("Применить параметры", central_widget)
        update_button.clicked.connect(self.update_plot)
        grid_layout.addWidget(update_button, 1, 1, 1, 1)

        description = QLabel("Параметы системы:", central_widget)
        description.setStyleSheet("border: 1px solid gray;")
        grid_layout.addWidget(description, 1, 0, 1, 1)

        central_widget.setLayout(grid_layout)
        self.setCentralWidget(central_widget)

        menubar = self.menuBar()

        # Создание пунктов меню
        file_menu = menubar.addMenu('Программа')
        examples_menu = menubar.addMenu('Примеры')
        exercises_menu = menubar.addMenu('Упражнения')
        language_menu = menubar.addMenu('Язык')

        # Добавление действий в меню
        file_menu.addAction('Открыть')
        file_menu.addAction('Выход')

        examples_menu.addAction('Пример 1')
        examples_menu.addAction('Пример 2')

        exercises_menu.addAction('Упражнение 1')
        exercises_menu.addAction('Упражнение 2')

        language_menu.addAction('Русский')
        language_menu.addAction('Английский')

        # Создание обработчика события для выхода из программы
        file_menu.triggered[QAction].connect(self.menu_triggered)

    def eventFilter(self, source, event):
        if event.type() == QEvent.Enter:
            if isinstance(source, QLineEdit) or isinstance(source, QSlider):
                self.update_status_bar(f"{source.toolTip()}")
        elif event.type() == QEvent.Leave:
            self.update_status_bar("")  # Clear the tooltip when the mouse leaves
        return super().eventFilter(source, event)

    def update_status_bar(self, text):
        self.status_label.setText(text)

    def menu_triggered(self, action):
        if action.text() == 'Выход':
            QApplication.quit()
        elif action.text() == 'Общее описание':
            pass

    def update_plot(self):
        Edit_values = [float(self.findChild(QLineEdit, f'horizontalEdit_{i + 1}').text()) for i in range(13)]

        S, l, m_0, m_max, P_max, c, V_0, H_0, H_max, m_a, t, t_a = [float(value) for value in Edit_values[:12]]

        solution_1 = model.solve(t_a, S, l, m_max, m_0, m_a, c, P_max, V_0, H_0, H_max)
        solution_2 = model.solve(t-t_a, S, l, m_max, m_0, m_a, c, P_max, V_0, H_0, H_max)

        yvalues = [solution_1['pitch'], solution_1['velocity'], solution_1['altitude'], solution_1['fuel_mass'],
                   solution_1['distance']]
        ylabels = ['Тангаж (рад)', 'Скорость (м/с)', 'Высота (м)', 'Общая масса (кг)', 'Расстояние (м)']

        for i in range(2):
            for j in range(2):
                ax = self.axes[i, j]
                ax.clear()
                idx = i * 2 + j
                ax.plot(solution_1['solution'].t, yvalues[idx])
                ax.set_xlabel('Время (с)')
                ax.set_ylabel(ylabels[idx])
                ax.grid(True, linestyle='--', linewidth=0.8, alpha=0.7)
        ax = self.axes[2, 0]
        ax.clear()
        ax.plot(solution_1['solution'].t, solution_1['distance'])
        ax.set_xlabel('Время (с)')
        ax.set_ylabel(ylabels[4])
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
