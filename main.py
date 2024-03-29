import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QSlider, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QGridLayout
from PySide6.QtGui import QIntValidator, QAction, QPixmap
from PySide6.QtCore import Qt, QEvent
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import model

class InfoWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Математическая постановка задачи")

        self.info_label_1 = QLabel("Движение летательного аппарата описывается системой дифференциальных уравнений:", self)
        self.info_label_2 = QLabel("где V– скорость; H – высота; t – время; α – угол атаки; ϑ – угол тангажа; θ – траекторный угол; cy0 – коэффициент подъемной силы при ϑ = 0; cx0 – коэффициент производной первого порядка по углу атаки; cyα – коэффициент минимального лобового сопротивления; P – тяга двигателя; mсек– секундный расход топлива при максимальной тяге; ρ(ℎ) – плотность воздуха; S – площадь крыла; l – размах крыла; e – коэффициент Освальда.\nПри достижении заданной высоты полета беспилотный летательный аппарат движется должен двигаться с неизменным траекторным углом, т.е. H = const, θ = 0.", self)
        self.info_label_1.setWordWrap(True)
        self.info_label_2.setWordWrap(True)

        pixmap = QPixmap("model.png")
        self.image_label = QLabel(self)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addWidget(self.info_label_1)
        layout.addWidget(self.image_label)
        layout.addWidget(self.info_label_2)

        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Оптимальное управление беспилотным летательным аппаратом для доставки грузов")
        self.menu_labels = {
            'Выход': 'Exit',
            'Открыть': 'Open',
            'Математическое описание': 'Mathematical description',
            'Русский': 'Russian',
            'Английский': 'English',
            'Программа' : 'Program',
            'Пример' : 'Example',
            'Упражнение' : 'Exercise',
            'Язык' : 'Language',
            'Exit': 'Выход',
            'Open': 'Открыть',
            'Mathematical description': 'Математическое описание',
            'Russian': 'Русский',
            'English': 'Английский',
            'Program' : 'Программа',
            'Example' : 'Пример',
            'Exercise' : 'Упражнение',
            'Language' : 'Язык'
        }
        self.current_menu = 0
        self.current_language = 'ru'

        central_widget = QWidget(self)
        self.status_label = QLabel(self)
        self.statusBar().addWidget(self.status_label, 1)
        self.setCentralWidget(central_widget)
        self.setup_ui(central_widget)
        self.info_window = InfoWindow()

    def setup_ui(self, central_widget):
        grid_layout = QGridLayout(central_widget)
        sliders_layout = QVBoxLayout()

        menubar = self.menuBar()
        file_menu = menubar.addMenu('Программа')
        menubar.addAction('Пример')
        menubar.addAction('Упражнение')
        language_menu = menubar.addMenu('Язык')
        file_menu.addAction('Открыть')
        file_menu.addAction('Математическое описание')
        file_menu.addAction('Выход')
        language_menu.addAction('Русский')
        language_menu.addAction('Английский')

        menubar.triggered[QAction].connect(self.menu_triggered)
        file_menu.triggered[QAction].connect(self.menu_triggered)
        language_menu.triggered[QAction].connect(self.menu_triggered)

        if self.current_language == 'ru':
            Labels_1 = ['Площадь крыла в метрах^2', 'Размах крыла в метрах', 'Масса дрона при пустых баках в килограммах',
                        'Масса дрона при полных баках в килограммах', 'Максимальное значение тяги двигателя в Ньютонах',
                        'Скорость расхода топлива килограммах в секунду', 'Текущая скорость в метрах в секунду',
                        'Текущая высота в метрах', 'Конечная высота в метрах', 'Масса груза в килограммах',
                        'Продолжительность полета в секундах', 'Момент времени сброса груза', 'Конечная высота после сброса груза в метрах']
        else:
            Labels_1 = ['Wing Area in Square Meters', 'Wingspan in Meters', 'Drone Mass with Empty Tanks in Kilograms',
                        'Drone Mass with Full Tanks in Kilograms', 'Maximum Engine Thrust in Newtons',
                        'Fuel Consumption Rate in Kilograms per Second', 'Current Speed in Meters per Second',
                        'Current Altitude in Meters', 'Final Altitude in Meters', 'Cargo Mass in Kilograms',
                        'Flight Duration in Seconds', 'Time of Cargo Release', 'Final Altitude after Cargo Release in Meters']

        Labels_2 = ['S', 'l', 'm_0', 'm_max', 'P_max', 'c', 'V_0', 'H_0', 'H_max', 'm_a', 't', 't_a', 'H_max_a']
        Variables = ['0.55', '2.8956', '8.5', '13.5', '20', '0.0045', '20', '10', '500', '2.0', '1300', '500', '800']

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
            label_1.setObjectName(f'label_1_{i + 1}')
            label_2 = QLabel(Labels_2[i] + ' =', central_widget)
            label_2.setFixedWidth(50)
            edit = QLineEdit(central_widget)
            edit.setFixedWidth(50)
            int_validator = QIntValidator()
            edit.setValidator(int_validator)
            slider = QSlider(Qt.Horizontal, central_widget)
            slider.setObjectName(f'horizontalSlider_{i + 1}')
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

            edit.setText(str(Variables[i]))

            edit.setToolTip(f"{toolTips[i]}")
            slider.setToolTip(f"{toolTips[i]}")

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

        self.figures, self.axes = plt.subplots(1, 1, figsize=(16, 6), sharex=True)
        self.figures.suptitle("Дальность полета", fontsize=14)
        self.figures.patch.set_edgecolor('gray')
        self.figures.patch.set_linewidth(2)
        #self.figures.delaxes(self.axes[2, 1])
        self.canvas = FigureCanvas(self.figures)

        grid_layout.addWidget(self.canvas, 0, 0, 1, 1)
        
        self.update_plot()

        label = QLabel("Параметры системы:", central_widget)
        label.setObjectName(f'label')
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("border: 0px solid black;")
        
        sliders_container = QWidget()
        sliders_container_layout = QVBoxLayout(sliders_container)
        sliders_container_layout.addWidget(label)
        sliders_container_layout.addLayout(sliders_layout)
        sliders_container.setStyleSheet("border: 1px solid gray;")

        grid_layout.addWidget(sliders_container, 0, 1, 1, 1)

        update_button = QPushButton("Применить параметры", central_widget)
        update_button.setObjectName(f'update_button')
        update_button.clicked.connect(self.update_plot)
        grid_layout.addWidget(update_button, 1, 1, 1, 1)

        description = QLabel("Данная математическая модель отображает дальность полета беспилотного летательного аппарата для доставки грузов при различных начальных значениях параметров полета.\nЗеленый пунктир отображает момент времени, когда беспилотник достиг заданной высоты полета; оранжевый пунктир отображает момент времени, когда груз был сброшен; красный пунктир отображает момент времени, когда у беспилотника кончилось топливо.\nНажмите на кнопку справа, чтобы обновить график.", central_widget)
        description.setWordWrap(True)
        description.setObjectName(f'description')
        description.setStyleSheet("border: 1px solid gray;")
        grid_layout.addWidget(description, 1, 0, 1, 1)

        central_widget.setLayout(grid_layout)
        self.setCentralWidget(central_widget)

    def eventFilter(self, source, event):
        if event.type() == QEvent.Enter:
            if isinstance(source, QLineEdit) or isinstance(source, QSlider):
                self.update_status_bar(f"{source.toolTip()}")
        elif event.type() == QEvent.Leave:
            self.update_status_bar("")
        return super().eventFilter(source, event)

    def update_status_bar(self, text):
        self.status_label.setText(text)

    def menu_triggered(self, action):
        if (action.text() == 'Выход') | (action.text() == 'Exit'):
            QApplication.quit()
        elif (action.text() == 'Математическое описание') | (action.text() == 'Mathematical description'):
            self.info_window.show()
        elif (action.text() == 'Открыть') | (action.text() == 'Open'):
            Variables = ['0.55', '2.8956', '8.5', '13.5', '20', '0.0045', '20', '10', '500', '2.0', '1300', '500', '800']
            ax = self.axes
            ax.clear()
            self.canvas.draw()
            self.current_menu = 0
            label = self.findChild(QLabel, f'description')
            if self.current_language == 'ru':
                label.setText('Данная математическая модель отображает дальность полета беспилотного летательного аппарата для доставки грузов при различных начальных значениях параметров полета.\nЗеленый пунктир отображает момент времени, когда беспилотник достиг заданной высоты полета; оранжевый пунктир отображает момент времени, когда груз был сброшен; красный пунктир отображает момент времени, когда у беспилотника кончилось топливо.')
            else:
                label.setText('This mathematical model displays the flight range of an unmanned aerial vehicle for delivering goods at various initial values ​​of flight parameters.\nThe green dotted line displays the moment in time when the drone reached a given flight altitude; the orange dotted line represents the point in time when the load was dropped; The red dotted line represents the point in time when the drone ran out of fuel.')
            self.update_edit(Variables)
        elif (action.text() == 'Пример') | (action.text() == 'Example'):
            Variables = ['0.55', '2.8956', '8.5', '13.5', '70', '0.0045', '20', '10', '500', '2.0', '1800', '900', '1000']
            ax = self.axes
            ax.clear()
            self.canvas.draw()
            self.current_menu = 1
            label = self.findChild(QLabel, f'description')
            if self.current_language == 'ru':
                label.setText('Данный пример основан на технических характеристиках Aerosonde.\nНажмите на кнопку справа, чтобы обновить график.')
            else:
                label.setText('This example is based on Aerosonde specifications.\nClick the button on the right to update the graph.')
            self.update_edit(Variables)
        elif (action.text() == 'Упражнение') | (action.text() == 'Exercise'):
            Variables = ['0.55', '2.8956', '8.5', '13.5', '20', '0.0045', '20', '10', '500', '2.0', '1800', '900', '1000']
            ax = self.axes
            ax.clear()
            self.canvas.draw()
            self.current_menu = 2
            label = self.findChild(QLabel, f'description')
            if self.current_language == 'ru':
                label.setText('Изменяя параметры крыла беспилотника необходимо достичь дальность полета выше 60,000.\nНажмите на кнопку справа, чтобы обновить график.')
            else:
                label.setText("By changing the parameters of the drone's wing, it is necessary to achieve a flight range above 60,000.\nClick the button on the right to update the graph.")
            for i in range(11):
                slider = self.findChild(QSlider, f'horizontalSlider_{i + 3}')
                edit = self.findChild(QLineEdit, f'horizontalEdit_{i + 3}')
                edit.setDisabled(True)
                slider.setDisabled(True)
                self.update_edit(Variables)
        elif (action.text() == 'Русский') | (action.text() == 'Russian'):
            if self.current_language != 'ru':
                self.figures.suptitle("Дальность полета", fontsize=14)
                self.setWindowTitle("Оптимальное управление беспилотным летательным аппаратом для доставки грузов")
                self.current_language = 'ru'
                self.changeMenu()
                self.changeLabelsLanguage()
        elif (action.text() == 'Английский') | (action.text() == 'English'):
            if self.current_language != 'en':
                self.figures.suptitle("Range of flight", fontsize=14)
                self.setWindowTitle("Optimal control of an unmanned aerial vehicle for cargo delivery")
                self.current_language = 'en'
                self.changeMenu()
                self.changeLabelsLanguage()
        if self.current_menu != 2:
            for i in range(11):
                slider = self.findChild(QSlider, f'horizontalSlider_{i + 3}')
                edit = self.findChild(QLineEdit, f'horizontalEdit_{i + 3}')
                edit.setDisabled(False)
                slider.setDisabled(False)
    
    def changeMenu(self):
        for menu in self.menuBar().actions():
            sub_menu = menu.menu()
            if sub_menu:
                for action in sub_menu.actions():
                    action_name = action.text()
                    new_text = self.menu_labels.get(action_name, action_name)
                    action.setText(new_text)
            menu_name = menu.text()
            new_text = self.menu_labels.get(menu_name, menu_name)
            menu.setText(new_text)
    
    def changeLabelsLanguage(self):
        if self.current_language == 'ru':
            Labels_1 = ['Площадь крыла в метрах^2', 'Размах крыла в метрах', 'Масса дрона при пустых баках в килограммах',
                        'Масса дрона при полных баках в килограммах', 'Максимальное значение тяги двигателя в Ньютонах',
                        'Скорость расхода топлива килограммах в секунду', 'Текущая скорость в метрах в секунду',
                        'Текущая высота в метрах', 'Конечная высота в метрах', 'Масса груза в килограммах',
                        'Продолжительность полета в секундах', 'Момент времени сброса груза', 'Конечная высота после сброса груза в метрах']
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
            update_lang = ['Параметы системы:', 'Применить параметры']
            label_description = ['Данная математическая модель отображает дальность полета беспилотного летательного аппарата для доставки грузов при различных начальных значениях параметров полета.\nЗеленый пунктир отображает момент времени, когда беспилотник достиг заданной высоты полета; оранжевый пунктир отображает момент времени, когда груз был сброшен; красный пунктир отображает момент времени, когда у беспилотника кончилось топливо.\nНажмите на кнопку справа, чтобы обновить график.',
                                 'Данный пример основан на технических характеристиках Aerosonde.\nНажмите на кнопку справа, чтобы обновить график.',
                                 'Изменяя параметры крыла беспилотника необходимо достичь дальность полета выше 60,000.\nНажмите на кнопку справа, чтобы обновить график.']
        else:
            Labels_1 = ['Wing Area in Square Meters', 'Wingspan in Meters', 'Drone Mass with Empty Tanks in Kilograms',
                        'Drone Mass with Full Tanks in Kilograms', 'Maximum Engine Thrust in Newtons',
                        'Fuel Consumption Rate in Kilograms per Second', 'Current Speed in Meters per Second',
                        'Current Altitude in Meters', 'Final Altitude in Meters', 'Cargo Mass in Kilograms',
                        'Flight Duration in Seconds', 'Time of Cargo Release', 'Final Altitude after Cargo Release in Meters']
            toolTips = ['Wing area affects lift and maneuverability. A larger area provides high payload capacity, while a smaller one increases maneuverability but reduces payload capacity and flight duration.',
                        'Wingspan affects lift and maneuverability. Greater wingspan contributes to payload capacity, while a smaller one enhances maneuverability and speed.',
                        'Drone mass with empty tanks',
                        'Drone mass with full tanks',
                        'Engine thrust affects the drones ability to carry loads and ascend. A higher maximum thrust usually allows the drone to climb to greater heights and carry heavier loads.',
                        'The speed at which the drones engine consumes fuel',
                        'The speed at which the drone initially travels',
                        'The height at which the drone is initially located',
                        'The height that the drone will not exceed',
                        'Cargo mass for drone delivery',
                        'Total drone flight duration for calculation',
                        'The time when the drone should release the cargo',
                        'The new value of the height that the drone will not exceed']
            update_lang = ['System parameters:', 'Apply parameters']
            label_description = ['This mathematical model displays the flight range of an unmanned aerial vehicle for delivering goods at various initial values ​​of flight parameters.\nThe green dotted line displays the moment in time when the drone reached a given flight altitude; the orange dotted line represents the point in time when the load was dropped; The red dotted line represents the point in time when the drone ran out of fuel.\nClick the button on the right to update the graph.',
                                 'This example is based on Aerosonde specifications.\nClick the button on the right to update the graph.',
                                 "By changing the parameters of the drone's wing, it is necessary to achieve a flight range above 60,000.\nClick the button on the right to update the graph."]
        for i in range(13):
            label_1 = self.findChild(QLabel, f'label_1_{i + 1}')
            label_1.setText(Labels_1[i] + ':')
            slider = self.findChild(QSlider, f'horizontalSlider_{i + 1}')
            edit = self.findChild(QLineEdit, f'horizontalEdit_{i + 1}')
            edit.setToolTip(f"{toolTips[i]}")
            slider.setToolTip(f"{toolTips[i]}")
        label_d = self.findChild(QLabel, f'description')
        if self.current_menu == 0:
            label_d.setText(label_description[0])
        elif self.current_menu == 1:
            label_d.setText(label_description[1])
        else:
            label_d.setText(label_description[2])
        label = self.findChild(QLabel, f'label')
        update_button = self.findChild(QPushButton, f'update_button')
        label.setText(update_lang[0])
        update_button.setText(update_lang[1])

    def update_plot(self):
        Edit_values = [float(self.findChild(QLineEdit, f'horizontalEdit_{i + 1}').text()) for i in range(13)]

        S, l, m_0, m_max, P_max, c, V_0, H_0, H_max, m_a, t, t_a, H_max_a = [float(value) for value in Edit_values[:13]]

        n_t = 100

        solution_1 = model.solve(0, t_a, n_t, S, l, m_max, m_0, m_a, c, P_max, V_0, H_0, H_max, 0.0, 0.0)
        yvalues_1 = [solution_1['pitch'], solution_1['velocity'], solution_1['altitude'], solution_1['fuel_mass'], solution_1['distance']]

        solution_2 = model.solve(t_a, t, n_t, S, l, solution_1['fuel_mass'][-1] - m_a, m_0, 0, c, P_max, solution_1['velocity'][-1], solution_1['altitude'][-1], H_max_a, solution_1['pitch'][-1], solution_1['distance'][-1])
        yvalues_2 = [solution_2['pitch'], solution_2['velocity'], solution_2['altitude'], solution_2['fuel_mass'], solution_2['distance']]
        
        #solution_2_a = model.solve(t_a, t, n_t, S, l, solution_1['fuel_mass'][-1], m_0, m_a, c, P_max, solution_1['velocity'][-1], solution_1['altitude'][-1], H_max_a, solution_1['pitch'][-1], solution_1['distance'][-1])
        #yvalues_2_a = [solution_2_a['pitch'], solution_2_a['velocity'], solution_2_a['altitude'], solution_2_a['fuel_mass'], solution_2_a['distance']]

        yvalues_3 = []
        for i in range(5):
            yvalues_3.append(model.concatenate(yvalues_1[i][:-1], yvalues_2[i]))
        xvalues_3 = model.concatenate(solution_1['solution'].t[:-1], solution_2['solution'].t)
        
        ylabels = ['Pitch (rad)', 'Speed (m/s)', 'Altitude (m)', 'Total Mass (kg)', 'Distance (m)']
        '''
        for i in range(2):
            for j in range(2):
                ax = self.axes[i, j]
                ax.clear()
                idx = i * 2 + j
                ax.plot(xvalues_3, yvalues_3[idx])
                if idx == 3:
                    ax.axhline (y = m_0, color='red', linestyle='--')
                #ax.plot(solution_2_a['solution'].t, yvalues_2_a[idx])
                ax.set_xlabel('Time (s)')
                ax.set_ylabel(ylabels[idx])
                ax.grid(True, linestyle='--', linewidth=0.8, alpha=0.7)
        '''
        print()
        f_0 = self.find_first_1(yvalues_3[3], m_0)
        h_1 = self.find_first_2(yvalues_1[2], H_max)
        h_2 = self.find_first_2(yvalues_2[2], H_max_a)
        ax = self.axes #ax = self.axes[2, 0]
        ax.clear()
        ax.plot(xvalues_3, yvalues_3[4])
        if f_0[0]:
            ax.axvline(x = xvalues_3[f_0[0]], color='red', linestyle='--')
        if h_1[0]:
            ax.axvline(x = xvalues_3[h_1[0]], color='g', linestyle='--')
        ax.axvline(x = t_a, color='orange', linestyle='--')
        if h_2[0]:
            ax.axvline(x = xvalues_3[len(yvalues_1[2])+h_2[0]], color='g', linestyle='--')
        #ax.plot(solution_2_a['solution'].t, yvalues_2_a[4])
        ax.set_xlabel('Time (s)')
        ax.set_ylabel(ylabels[4])
        ax.grid(True, linestyle='--', linewidth=0.8, alpha=0.7)
        if self.current_menu == 2:
            if yvalues_3[4][-1] > 60000:
                label = self.findChild(QLabel, f'description')
                if self.current_language == 'ru':
                    label.setText('Поздравляем, вы сделали это!')
                else:
                    label.setText("Congratulations, you've done it!")
        self.canvas.draw()
    
    def find_first_1(self, arr, target):
        for index, element in enumerate(arr):
            if element < target:
                return index, element
        return None, None 
    
    def find_first_2(self, arr, target):
        for index, element in enumerate(arr):
            if element > target:
                return index, element
        return None, None 

    def update_edit(self, Variables):
        for i in range(13):
            slider = self.findChild(QSlider, f'horizontalSlider_{i + 1}')
            edit = self.findChild(QLineEdit, f'horizontalEdit_{i + 1}')
            if i in [0, 1]:
                slider.setValue(float(Variables[i]) * 2)
            elif i in [2, 3, 4, 6, 9]:
                slider.setValue(float(Variables[i]) * 2)
            elif i == 5:
                slider.setValue(float(Variables[i]) * 8000)
            elif i in [7, 8, 10, 11, 12]:
                slider.setValue(float(Variables[i]))
            edit.setText(str(Variables[i]))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
