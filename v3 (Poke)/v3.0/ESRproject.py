# это используется в информационном поле window2
version = "Poke v3.0\n" \
          "\n" \
          "7.01.24"
description_of_the_version = "Эта программа для сохранения нажатия.\n" \
                             "\n" \
                             "Загрузка данных:\n" \
                             "1. Кнопка Set file path -> Выбрать файлы для обработки.\n" \
                             "Note: он может быть всего один. А можно нажать ctrl a и выбрать все файлы в папке.\n" \
                             "Note: фильтр отсечёт папки, файлы < 50KB, файлы, где нет +99dn или +99up.\n" \
                             "2. Кнопка Load data.\n" \
                             "\n" \
                             "Обработка данных если активны метки:" \
                             "0. Метки активны, если нажаты галки в UP и DN рамках.\n" \
                             "1. Впишите числа в поля для центральной, правой и левой метки.\n" \
                             "Note: есть режим только центральной метки. Тогда в других должно быть пусто. " \
                             "Температуры находится по всем данным.\n" \
                             "2. Кнопка Draw. Она отрисует метки. Температура считается как среднее между правой и левой вертикалью.\n" \
                             "Note: Центральная метка нужно только для удобства.\n" \
                             "Note: сохранится только самая первая точка нажатия.\n" \
                             "Note: в одной итоговой строке сохранится частота, X Y и температуры DN, X Y и температуры UP," \
                             "их усреднение и температуры после калибровка по Oxford в 117\n" \
                             "Note: Данные сохранятся в директорию файлов. Его имя берется из поля results_file_name.\n" \
                             "\n" \
                             "Disclaimer:\n" \
                             "Программа написана сугубо для специфических файлов, которые выдает LabView.\n" \
                             "Далее файл удобно читается OriginPro*.\n" \
                             "* OriginPro 2018\n" \
                             "\n" \
                             "Дополнительно см. https://github.com/nikolaevgk/ESR_project\n" \
                             "Там же можно найти другие программы"

# это директория, которая сразу отображается в окне поиска файлов
directory_by_default = r"C:\Users\nikol\Desktop\LNEP data\ZnO Oct-Nov 2021 + Jul-Nov-Dec 2022 + Jan-Feb 2023\Z448\Z448 th45 base=500 jul2022\Immersion #1\HU DL nu3"

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QFileDialog, QWidget, QFormLayout, QTextEdit
from QtCreator_ESRproject import Ui_MainWindow

from Prepare_data_ESRproject import prepare_table_data_from_txt, put_table_in_qtable_wiget, convert_rows_to_columns
from Mpl_ESRproject import prepare_canavas_and_toolbar
from Fitting_ESRproject import *
from Load_data_ESRproject import *

import numpy as np


class MainWindow(QMainWindow, Ui_MainWindow, QWidget):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.widgets_adjust()

        # DN ####################################################################################################
        # здесь хранятся координаты клика мыши в формате списка из множеств (x, y)
        # чтобы различать по какому из графиков был произведён клик, введём отдельно DN и UP
        self.on_mouse_press_coordinate_list_DN = []

        # здесь данные из файла
        self.data_full_range_DN = []

        # здесь данные пика (после нормализации, данные пика до нормализации не используются)
        self.x_data_to_peak_fitting_DN = []
        self.y_data_to_peak_fitting_DN = []

        # здесь данные фона, которые будут фитироваться (до нормализации)
        self.x_data_for_background_DN = []
        self.y_data_for_background_DN = []

        # здесь данные фона, которые будут нормализоваться 
        self.x_data_cut_range_DN = []
        self.y_data_cut_range_DN = []

        # здесь данные моделирования фона
        self.y_calculated_background_cut_range_DN = []
        self.y_calculated_background_around_peak_DN = []

        # здесь данные от деления сырых данных пика на моделированный фон
        self.y_normalized_cut_full_range_DN = []

        # этот маркер нужен для кнопок Next и Prev, чтобы они понимали нужно ли отображать эти вертикали
        self.Central_line_status_DN = ""
        self.LR_lines_status_DN = ""

        self.Central_line_status_UP = ""
        self.LR_lines_status_UP = ""

        # это сырые данные, которые заполняются при нажатии на кнопку Load data
        self.data_voc_DN = {}

        # это список имен файлов, которые обрабатываются сейчас
        self.name_of_file_DN = ""

        # это для хранения параметров фитирования фона и пика
        self.params_of_background_DN = []
        self.params_of_peak_DN = []

        # Температура в Омах вблизи пика. Усреднение ровно там, из каких данных делалось фитирование
        self.temperature_resistance_around_peak_DN = 0
        self.temperature_around_peak_DN = 0

        # UP ####################################################################################################
        # здесь хранятся координаты клика мыши в формате списка из множеств (x, y)
        # чтобы различать по какому из графиков был произведён клик, введём отдельно DN и UP
        self.on_mouse_press_coordinate_list_UP = []

        # здесь данные из файла
        self.data_full_range_UP = []

        # здесь данные пика (после нормализации, данные пика до нормализации не используются)
        self.x_data_to_peak_fitting_UP = []
        self.y_data_to_peak_fitting_UP = []

        # здесь данные фона, которые будут фитироваться (до нормализации)
        self.x_data_for_background_UP = []
        self.y_data_for_background_UP = []

        # здесь данные фона, которые будут нормализоваться
        self.x_data_cut_range_UP = []
        self.y_data_cut_range_UP = []

        # здесь данные моделирования фона
        self.y_calculated_background_cut_range_UP = []
        self.y_calculated_background_around_peak_UP = []

        # здесь данные от деления сырых данных пика на моделированный фон
        self.y_normalized_cut_full_range_UP = []

        # этот маркер нужен в функции on_mouse_press() чтобы программа понимала, когда обрабатывается фон, а когда пик
        # так что есть всего два состояния "normalized graph" и "initial graph"
        self.programm_status_UP = ""

        # это сырые данные, которые заполняются при нажатии на кнопку Load data
        self.data_voc_UP = {}

        # это список имен файлов, которые обрабатываются сейчас
        self.name_of_file_UP = ""

        # это для хранения параметров фитирования фона и пика
        self.params_of_background_UP = []
        self.params_of_peak_UP = []

        # Температура в Омах вблизи пика. Усреднение ровно там, из каких данных делалось фитирование
        self.temperature_resistance_around_peak_UP = 0
        self.temperature_around_peak_UP = 0

        # for both ####################################################################################################
        # это список всех выбранных имен файлов
        self.list_for_plot = []

        # это устанавливает колонку для фитирования по умолчанию на X
        self.column_for_processing = 4

        # этот индекс меняется, когда меняются файлы для обработки. Кнопки Next, Next and Save.
        # при загрузке файлов (кнопка Load data) заполняется список из пар list_for_plot [(), (), ...]
        # по нему то и пробегает индекс self.data_index_for_processing
        self.data_index_for_processing = 0

        # здесь итоговые данные после фитирования. Они же и записываются в таблицу и файл
        self.export_list = {
            'header': ["F", "#run", " ", "B_DN", "R_DN", "T_R_DN", "T_DN", " ", "B_UP", "R_UP", "T_R_UP", "T_UP", " ",
                       "B_mean", "R_mean", "T_R_mean", "T_mean", " ", "name_of_file_DN", "name_of_file_UP"],
            'units': [], 'data': []}

        self.result_string_general = ""

    def widgets_adjust(self):
        """метод для привязки всех кнопок и текстовых полей к функциям"""

        # Кнопка выбора директории
        self.InitFilePathSetButton.setText("Set file path")
        self.InitFilePathSetButton.clicked.connect(self.load_init_data_file_dialog)

        # Кнопка для загрузки данных из выбранного набора файлов
        self.LoadButton.setText("Load data")
        self.LoadButton.clicked.connect(self.initial_import_data)

        # Кнопка Save and Next
        self.SaveNextButton.setText("Save and Next")
        self.SaveNextButton.clicked.connect(self.save_fitting_and_next_file)

        # Кнопка Save
        self.SaveButton.setText("Save")
        self.SaveButton.clicked.connect(self.save_fitting)

        # Кнопка Save
        self.delSave.clicked.connect(self.delSave_fitting)

        # Кнопка назад Previous file
        self.PreviousButton.setText("Previous file")
        self.PreviousButton.clicked.connect(self.previous_file)

        # Кнопка вперёд Next file
        self.NextButton.setText("Next file")
        self.NextButton.clicked.connect(self.next_file)

        # Поле ввода для пути к файлу
        self.InitFilePathField.setMaximumHeight(30)
        self.InitFilePathField.setMinimumHeight(30)

        # Поле настройки таблицы
        self.InitDataTable.setMinimumSize(300, 300)
        self.InitDataTable.setMaximumWidth(500)

        # Настройка поля для графика
        self.MplWidget.setMinimumSize(300, 300)
        self.MplWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Настройка элементов списка таблиц
        self.TableComboBox.addItems(["Table DOWN", "Table UP", "RESULT Table"])
        self.TableComboBox.activated[str].connect(self.TableComboBox_change_function)

        # Настройка элементов списка выбора столбца
        self.ColumnForPlotComboBox.addItems(["X", "Y", "R"])
        self.ColumnForPlotComboBox.activated[str].connect(self.ColumnForPlotComboBox_change_function)

        # Поле для ввода названия файла для сохранения - по умолчанию ставим 'results_file_name'
        self.ResFilePathField.setText(r'results_file_name')

        # соединяем кнопку информации с дополнительным окном
        self.InfoPushButton.clicked.connect(self.window2)

        # Кнопка для отрисовки вертикалей
        self.DrawLinesButton_DN.clicked.connect(self.draw_support_lines_DN)
        self.DrawLinesButton_UP.clicked.connect(self.draw_support_lines_UP)

        # Поля для ввода положения вертикальных линий DN
        self.CentralLineTextField_DN.setText(r'8.5')
        self.LeftLineTextField_DN.setText(r'8.4')
        self.RightLineTextField_DN.setText(r'8.6')

        self.CentralLineTextField_UP.setText(r'8.5')
        self.LeftLineTextField_UP.setText(r'8.4')
        self.RightLineTextField_UP.setText(r'8.6')

        # DN

        # Подсказка для нижнего текстового поля
        self.NameFileFieldDN.setToolTip('<h4>Имя файла для левого графика<h4>')

        # UP

        # Подсказка для нижнего текстового поля
        self.NameFileFieldUP.setToolTip('<h4>Имя файла для правого графика<h4>')

        # Функция подготовки графика
        prepare_canavas_and_toolbar(parent=self)

        # если бы не было этой строчки, то клик по графику не выводил бы координаты
        # можно было бы написать через if event.button() == Qt.LeftButton: в функции on_mouse_press(self, event)
        # и тогда бы координаты выводились от клика по рабочей области, но не от клика по графику
        self.canvas.mpl_connect('button_press_event', self.on_mouse_press)

    # 4 нажатия для фитирования фона и 2 нажатия для резонанса Фана
    def on_mouse_press(self, event):
        """ так мы привязываем действие мыши к функции
            Здесь == 3 значит лишь то, что клик произведён правой кнопкой"""
        if event.button == 3:

            # так мы понимаем, что клик был по левому графику
            if event.inaxes == self.axes_left:
                # Get the mouse click position relative to the graph
                x = event.xdata
                y = event.ydata
                on_mouse_press_coordinate = (round(x, 6), format(y, ".3e"))
                self.on_mouse_press_coordinate_list_DN.append(on_mouse_press_coordinate)
                self.axes_left.axvline(x)
                self.axes_left.axhline(y)
                self.canvas.draw()
                self.canvas.flush_events()
                print(f"Left button clicked at position DN: {self.on_mouse_press_coordinate_list_DN}")

            # так мы понимаем, что клик был по правому графику
            if event.inaxes == self.axes_right:
                # Get the mouse click position relative to the graph
                x = event.xdata
                y = event.ydata
                on_mouse_press_coordinate = (round(x, 6), format(y, ".3e"))
                self.on_mouse_press_coordinate_list_UP.append(on_mouse_press_coordinate)
                self.axes_right.axvline(x)
                self.axes_right.axhline(y)
                self.canvas.draw()
                self.canvas.flush_events()
                print(f"Left button clicked at position UP: {self.on_mouse_press_coordinate_list_UP}")

    def window2(self):
        self.window = QWidget()
        self.window.setWindowTitle("Information")
        self.window.setGeometry(400, 400, 1500, 700)
        self.new = QTextEdit(self.centralwidget)
        self.new.append(description_of_the_version)

        layout = QFormLayout(self.window)
        layout.addRow(version, self.new)

        self.window.show()

    def draw_support_lines_DN(self):
        # условие, чтобы не нажималась кнопка до загрузки данных
        if self.list_for_plot:
            print(self.list_for_plot[0])
            # условие, что график загрузился и есть куда ставить вертикали
            if self.checkBox_DN.isChecked():
                if self.list_for_plot[self.data_index_for_processing][0]:
                    self.clear_plot_DN()
                    self.plot_initial_data_DN()
                    # проверка, что центральная метка float
                    try:
                        x_central_line = float(self.CentralLineTextField_DN.toPlainText())
                        self.axes_left.axvline(x_central_line, color='r')
                        self.Central_line_status_DN = "Central line exists DN"

                        # условие, что поля правого и левого поля не пустые
                        if self.LeftLineTextField_DN.toPlainText() and self.RightLineTextField_DN.toPlainText():
                            # проверка, что поля правого и левого поля float
                            try:
                                x_left_line = float(self.LeftLineTextField_DN.toPlainText())
                                x_right_line = float(self.RightLineTextField_DN.toPlainText())
                                self.axes_left.axvline(x_left_line, color='r', linestyle="--")
                                self.axes_left.axvline(x_right_line, color='r', linestyle="--")
                                self.LR_lines_status_DN = "LR lines exist DN"


                            except ValueError:
                                print("LeftLineTextField_DN or RightLineTextField_DN is not float")

                    except ValueError:
                        print("CentralLineTextField_DN is not float")

                    self.fig.canvas.draw()
            else:
                self.clear_plot_DN()
                self.plot_initial_data_DN()

    def draw_support_lines_UP(self):
        # условие, чтобы не нажималась кнопка до загрузки данных
        if self.list_for_plot:
            # условие, что график загрузился и есть куда ставить вертикали
            if self.checkBox_UP.isChecked():
                if self.list_for_plot[self.data_index_for_processing][0]:
                    self.clear_plot_UP()
                    self.plot_initial_data_UP()
                    # проверка, что центральная метка float
                    try:
                        x_central_line = float(self.CentralLineTextField_UP.toPlainText())
                        self.axes_right.axvline(x_central_line, color='r')
                        self.Central_line_status_UP = "Central line exists UP"

                        # условие, что поля правого и левого поля не пустые
                        if self.LeftLineTextField_UP.toPlainText() and self.RightLineTextField_UP.toPlainText():
                            # проверка, что поля правого и левого поля float
                            try:
                                x_left_line = float(self.LeftLineTextField_UP.toPlainText())
                                x_right_line = float(self.RightLineTextField_UP.toPlainText())
                                self.axes_right.axvline(x_left_line, color='r', linestyle="--")
                                self.axes_right.axvline(x_right_line, color='r', linestyle="--")
                                self.LR_lines_status_UP = "LR lines exist UP"


                            except ValueError:
                                print("LeftLineTextField_UP or RightLineTextField_UP is not float")

                    except ValueError:
                        print("CentralLineTextField_UP is not float")

                    self.fig.canvas.draw()
            else:
                self.clear_plot_UP()
                self.plot_initial_data_UP()

    # калибровка температуры на Oxford в 117
    def temperature_calibration(self, temperature_resistance):
        if temperature_resistance > 120000:
            temperature_K = 10 ** (2.30902 - 0.43469 * np.log10(temperature_resistance))
        elif temperature_resistance > 20700:
            temperature_K = 6740.73426 - 5534.28254 * np.log10(temperature_resistance) + 1707.35367 * (
                np.log10(temperature_resistance)) ** 2 - 234.41767 * (
                                np.log10(temperature_resistance)) ** 3 + 12.08064 * (
                                np.log10(temperature_resistance)) ** 4
        else:
            temperature_K = 0
        return temperature_K

    # Set file path
    def load_init_data_file_dialog(self):
        """Эта функция вызывается кнопкой Set file path и существует, чтобы заполнять список self.list_for_plot
        то есть чтобы поместить в список имена всех файлов"""
        print("load_init_data_file_dialog")

        # у QFileDialog.getOpenFileNames() выход ([список строк имён файлов], 'All Files (*)')
        file_name_list = QFileDialog.getOpenFileNames(self, 'Choose data file for analysis', directory_by_default)[0]
        # это заполнит нам список self.list_for_plot отфильтрованным списком файлов
        self.list_for_plot = self.filter_data(file_name_list)

        # это чтобы без перезапуска программы можно было открывать и выбирать другие файлы в папке
        # но теперь при кнопки выбора директории придётся опять выбрать нужные файлы
        self.data_voc_DN = {}
        self.data_voc_UP = {}

        print("List for plot ", self.list_for_plot)

    def filter_data(self, files_list):
        """ Фильтрует все файлы меньше 50кб, сортируем файлы по UP и DN"""
        print("filter_data")

        filtered_files_by_size = filter_files_by_size(files_list)
        filtered_files_dn = filter_files_by_up_dn(filtered_files_by_size)[0]
        filtered_files_up = filter_files_by_up_dn(filtered_files_by_size)[1]
        return get_list_for_plot(filtered_files_dn, filtered_files_up)

    # Load data
    def initial_import_data(self):
        """ Функция вызывается при нажатии на кнопку Load data"""
        print("initial_import_data")

        # эта строчка при нажатии на кнопку Load data в середине обработки откроет файлы с самого начала
        self.data_index_for_processing = 0

        # эти 3 строчки условия очищают таблицу результатов, когда нажимается кнопка Load Data.
        # они не обязательны и их можно убрать, если хочется подряд обрабатывать данные из разных директорий
        self.export_list['data'].clear()
        self.result_string_general = ""
        self.InitDataTable.clear()

        self.import_data()

    def import_data(self):
        """ Импортируем данные с перебором условий чтобы файлы были не пустые"""
        print("import_data")

        # эти 2 строчки, чтобы при выполнении import_data не только чистилась таблицы, но и переключались
        # Items в ComboBox под таблицей
        self.TableComboBox.clear()
        self.TableComboBox.addItems(["Table DOWN", "Table UP", "RESULT Table"])

        # перебор по случаям self.list_for_plot c ([], ...), (... []) и нормальных пар (..., ...)
        # (..., ...)
        if self.list_for_plot:

            # эти строчки, чтобы новая метка сохранялась в списке нажатий на первом месте
            self.on_mouse_press_coordinate_list_DN = []
            self.on_mouse_press_coordinate_list_UP = []

            if self.list_for_plot[self.data_index_for_processing][0] and \
                    self.list_for_plot[self.data_index_for_processing][1]:
                self.load_data_DN()
                self.load_data_UP()

                self.clear_plot_DN()
                self.plot_initial_data_DN()

                self.clear_plot_UP()
                self.plot_initial_data_UP()

                # это условие, чтобы метки отображались после нажатия на NEXT
                if self.LR_lines_status_DN == "LR lines exist DN":
                    x_central_line = float(self.CentralLineTextField_DN.toPlainText())
                    x_left_line = float(self.LeftLineTextField_DN.toPlainText())
                    x_right_line = float(self.RightLineTextField_DN.toPlainText())
                    self.axes_left.axvline(x_central_line, color='r')
                    self.axes_left.axvline(x_left_line, color='r', linestyle="--")
                    self.axes_left.axvline(x_right_line, color='r', linestyle="--")
                    self.fig.canvas.draw()
                if self.Central_line_status_DN == "Central line exists DN" and not self.LR_lines_status_DN:
                    x_central_line = float(self.CentralLineTextField_DN.toPlainText())
                    self.axes_left.axvline(x_central_line, color='r')
                    self.fig.canvas.draw()

                if self.LR_lines_status_UP == "LR lines exist UP":
                    x_central_line = float(self.CentralLineTextField_UP.toPlainText())
                    x_left_line = float(self.LeftLineTextField_UP.toPlainText())
                    x_right_line = float(self.RightLineTextField_UP.toPlainText())
                    self.axes_right.axvline(x_central_line, color='r')
                    self.axes_right.axvline(x_left_line, color='r', linestyle="--")
                    self.axes_right.axvline(x_right_line, color='r', linestyle="--")
                    self.fig.canvas.draw()
                if self.Central_line_status_UP == "Central line exists UP" and not self.LR_lines_status_UP:
                    x_central_line = float(self.CentralLineTextField_UP.toPlainText())
                    self.axes_right.axvline(x_central_line, color='r')
                    self.fig.canvas.draw()

            # (... [])
            if self.list_for_plot[self.data_index_for_processing][0] and \
                    self.list_for_plot[self.data_index_for_processing][1] == []:
                self.load_data_DN()
                self.name_of_file_UP = ""
                self.NameFileFieldUP.setText("File UP is not exist")
                # график UP строится по данным с прошлого файла, но потом сразу очищается
                self.clear_plot_UP()
                self.clear_plot_DN()
                self.plot_initial_data_DN()

                if self.LR_lines_status_DN == "LR lines exist DN":
                    x_central_line = float(self.CentralLineTextField_DN.toPlainText())
                    x_left_line = float(self.LeftLineTextField_DN.toPlainText())
                    x_right_line = float(self.RightLineTextField_DN.toPlainText())
                    self.axes_left.axvline(x_central_line, color='r')
                    self.axes_left.axvline(x_left_line, color='r', linestyle="--")
                    self.axes_left.axvline(x_right_line, color='r', linestyle="--")
                    self.fig.canvas.draw()
                if self.Central_line_status_DN == "Central line exists DN" and not self.LR_lines_status_DN:
                    x_central_line = float(self.CentralLineTextField_DN.toPlainText())
                    self.axes_left.axvline(x_central_line, color='r')
                    self.fig.canvas.draw()

            # ([], ...)
            if self.list_for_plot[self.data_index_for_processing][1] and \
                    self.list_for_plot[self.data_index_for_processing][0] == []:
                self.load_data_UP()
                self.name_of_file_DN = ""
                self.NameFileFieldDN.setText("File DN is not exist")
                # график DN строится по данным с прошлого файла, но потом сразу очищается
                self.clear_plot_DN()
                self.clear_plot_UP()
                self.plot_initial_data_UP()

                if self.LR_lines_status_UP == "LR lines exist UP":
                    x_central_line = float(self.CentralLineTextField_UP.toPlainText())
                    x_left_line = float(self.LeftLineTextField_UP.toPlainText())
                    x_right_line = float(self.RightLineTextField_UP.toPlainText())
                    self.axes_left.axvline(x_central_line, color='r')
                    self.axes_left.axvline(x_left_line, color='r', linestyle="--")
                    self.axes_left.axvline(x_right_line, color='r', linestyle="--")
                    self.fig.canvas.draw()
                if self.Central_line_status_UP == "Central line exists UP" and not self.LR_lines_status_UP:
                    x_central_line = float(self.CentralLineTextField_UP.toPlainText())
                    self.axes_left.axvline(x_central_line, color='r')
                    self.fig.canvas.draw()



        else:
            print("file for analysis wasn't selected")

    # DN ####################################################################################################
    def load_data_DN(self):
        """ Идет по пути их текстовых полей, заполняет словарь данных data_voc_DN и таблицу"""

        self.name_data_file_DN()
        # file_path = self.InitFilePathField.toPlainText()

        # программа импортирует данные из пути, который получается при слиянии информации в текстовых блоках
        # так мы уверены, где лежат дынные, но приходится лишний раз сшивать данные из блоков
        directory = self.InitFilePathField.toPlainText()

        # из текстовых полей обратно восстанавливаем путь к файлу
        # так мы сшиваем данные для и подготавливаем данные в таблицу для DN
        file_name_DN = self.NameFileFieldDN.toPlainText()
        file_path_DN = "/".join([directory, file_name_DN])
        self.data_voc_DN = prepare_table_data_from_txt(file_path_DN, delimeter=',')
        # это название колонок в таблице данных
        self.data_voc_DN['header'] = ["B", " ", " ", " ", "X", "Y", " ", " ", " ", " ", "T", " ", "R", " ", "t", " ",
                                      " "]

        # это выводится в таблице по умолчанию - данные DN
        put_table_in_qtable_wiget(self.data_voc_DN['header'], self.InitDataTable, self.data_voc_DN['data'])

    def name_data_file_DN(self):
        """ Эта функция нужна в том случае, если есть только файл вниз
            Она узнает имя файла и заполняет поле над графиком"""

        # эта строчка позволяет написать имя директории в верхнее текстовое окно
        self.InitFilePathField.setText(
            get_name_of_file_from_path(self.list_for_plot[self.data_index_for_processing][0])[1])

        self.name_of_file_DN = get_name_of_file_from_path(self.list_for_plot[self.data_index_for_processing][0])[0]

        self.NameFileFieldDN.setText(self.name_of_file_DN)

        print("file for analysis: ", self.list_for_plot[self.data_index_for_processing])

    def clear_plot_DN(self):
        """ Функция для очистки графика DN"""

        self.axes_left.cla()
        self.axes_left.grid(True, c='lightgrey', alpha=0.5)
        self.axes_left.set_title('DN', fontsize=20)
        self.axes_left.set_xlabel('Magnetic Field', fontsize=15)
        self.axes_left.set_ylabel('Signal', fontsize=15)

    def plot_initial_data_DN(self):
        """ Функция для построения графика сразу после загрузки файлов"""

        x_data_full_range_DN = transformation_of_data(self.data_voc_DN['data'][0])
        y_data_full_range_DN = transformation_of_data(self.data_voc_DN['data'][self.column_for_processing],
                                                      1E6)

        self.axes_left.scatter(x_data_full_range_DN, y_data_full_range_DN, c='blue', s=20)
        self.fig.canvas.draw()

    # UP ####################################################################################################
    def load_data_UP(self):
        """ Идет по пути их текстовых полей, заполняет словарь данных data_voc_UP и таблицу"""

        self.name_data_file_UP()
        # file_path = self.InitFilePathField.toPlainText()

        # программа импортирует данные из пути, который получается при слиянии информации в текстовых блоках
        # так мы уверены, где лежат дынные, но приходится лишний раз сшивать данные из блоков
        directory = self.InitFilePathField.toPlainText()

        # из текстовых полей обратно восстанавливаем путь к файлу
        # так мы сшиваем данные для и подготавливаем данные в таблицу для UP
        file_name_UP = self.NameFileFieldUP.toPlainText()
        file_path_UP = "/".join([directory, file_name_UP])
        self.data_voc_UP = prepare_table_data_from_txt(file_path_UP, delimeter=',')

        # это название колонок в таблице данных
        self.data_voc_UP['header'] = ["B", " ", " ", " ", "X", "Y", " ", " ", " ", " ", "T", " ", "R", " ", "t", " ",
                                      " "]
        print(self.data_voc_UP['header'])
        # это выводится в таблице по умолчанию - данные UP
        put_table_in_qtable_wiget(self.data_voc_UP['header'], self.InitDataTable, self.data_voc_UP['data'])

    def name_data_file_UP(self):
        """ Эта функция нужна в том случае, если есть только файл вниз
            Она узнает имя файла и заполняет поле над графиком"""

        # эта строчка позволяет написать имя директории в верхнее текстовое окно
        self.InitFilePathField.setText(
            get_name_of_file_from_path(self.list_for_plot[self.data_index_for_processing][1])[1])

        self.name_of_file_UP = get_name_of_file_from_path(self.list_for_plot[self.data_index_for_processing][1])[0]

        self.NameFileFieldUP.setText(self.name_of_file_UP)

        print("file for analysis: ", self.list_for_plot[self.data_index_for_processing])

    def clear_plot_UP(self):
        """ Функция для очистки графика UP"""

        self.axes_right.cla()
        self.axes_right.grid(True, c='lightgrey', alpha=0.5)
        self.axes_right.set_title('UP', fontsize=20)
        self.axes_right.set_xlabel('Magnetic Field', fontsize=15)
        self.axes_right.set_ylabel('Signal', fontsize=15)

    def plot_initial_data_UP(self):
        """ Функция для построения графика сразу после загрузки файлов"""

        x_data_full_range_UP = transformation_of_data(self.data_voc_UP['data'][0])
        y_data_full_range_UP = transformation_of_data(self.data_voc_UP['data'][self.column_for_processing],
                                                      1E6)

        self.axes_right.scatter(x_data_full_range_UP, y_data_full_range_UP, c='blue', s=20)
        self.fig.canvas.draw()

    # for both ####################################################################################################
    # Save
    def save_fitting(self):
        """Функция, к которой привязана кнопка Save"""
        print("save_fitting")

        # в этой версии программы температура будет находиться здесь
        # Условие, что температура ноходится только после нажатия на кнопку Draw
        # Между правой и левой пунктирными вертикалями усредним температуру
        x_data_full_range_DN = transformation_of_data(self.data_voc_DN['data'][0])
        T_data_full_range_DN = transformation_of_data(self.data_voc_DN['data'][10])
        T_sum = 0
        T_counter = 0

        # условие находить температуру между вспомогательными метками, если они есть
        # иначе искать во всем диапазоне
        if self.LR_lines_status_DN == "LR lines exist DN":
            for ind in range(len(x_data_full_range_DN)):
                # Условие, что усреднение температуры происходит между центральными вертикалями
                if (x_data_full_range_DN[ind] > float(self.LeftLineTextField_DN.toPlainText())) and (
                        x_data_full_range_DN[ind] < float(self.RightLineTextField_DN.toPlainText())):
                    # Условие-фильтр выбросов температуры
                    if T_data_full_range_DN[ind] < 2000000:
                        T_sum += T_data_full_range_DN[ind]
                        T_counter += 1
        else:
            for ind in range(len(x_data_full_range_DN)):
                # Условие-фильтр выбросов температуры
                if T_data_full_range_DN[ind] < 2000000:
                    T_sum += T_data_full_range_DN[ind]
                    T_counter += 1


        if T_counter == 0:
            self.temperature_resistance_around_peak_DN = 0
            self.temperature_around_peak_DN = 0
        else:
            self.temperature_resistance_around_peak_DN = round(T_sum / T_counter, 3)
            self.temperature_around_peak_DN = self.temperature_calibration(self.temperature_resistance_around_peak_DN)

        # Между правой и левой пунктирными вертикалями усредним температуру
        x_data_full_range_UP = transformation_of_data(self.data_voc_UP['data'][0])
        T_data_full_range_UP = transformation_of_data(self.data_voc_UP['data'][10])
        T_sum = 0
        T_counter = 0
        # условие находить температуру между вспомогательными метками, если они есть
        # иначе искать во всем диапазоне
        if self.LR_lines_status_UP == "LR lines exist UP":
            for ind in range(len(x_data_full_range_UP)):
                # Условие, что усреднение температуры происходит между центральными вертикалями
                if (x_data_full_range_UP[ind] > float(self.LeftLineTextField_UP.toPlainText())) and (
                        x_data_full_range_UP[ind] < float(self.RightLineTextField_UP.toPlainText())):
                    # Условие-фильтр выбросов температуры
                    if T_data_full_range_UP[ind] < 2000000:
                        T_sum += T_data_full_range_UP[ind]
                        T_counter += 1
        else:
            for ind in range(len(x_data_full_range_UP)):
                # Условие-фильтр выбросов температуры
                if T_data_full_range_UP[ind] < 2000000:
                    T_sum += T_data_full_range_UP[ind]
                    T_counter += 1
        if T_counter == 0:
            self.temperature_resistance_around_peak_UP = 0
            self.temperature_around_peak_UP = 0
        else:
            self.temperature_resistance_around_peak_UP = round(T_sum / T_counter, 3)
            self.temperature_around_peak_UP = self.temperature_calibration(self.temperature_resistance_around_peak_UP)

        # Условие, чтобы кнопка нажималась только после нажатия на график
        if self.on_mouse_press_coordinate_list_DN or self.on_mouse_press_coordinate_list_UP:
            # Так мы добавляем к словарю результаты. Сам же словарь export_list понадобится в unsave, когда придется
            # удалять из него данные
            result_list = self.export_single_results_to_list()
            self.export_list['data'].append(result_list)

            # Так мы из численных результатов получаем строку
            result_string_local = result_list
            result_string_local = [str(x) for x in result_string_local]
            result_string_local = ", ".join(result_string_local)
            result_string_local = result_string_local + "\n"
            self.result_string_general += result_string_local

            self.save_to_file()

    def save_to_file(self):
        print("save_to_file")

        # Так мы сохраняем данные под именем из правого текстового поля
        if self.ResFilePathField.toPlainText():
            name_of_result_file = self.ResFilePathField.toPlainText()
        else:
            name_of_result_file = "results"

        # Так мы сохраняем данные в файл из директории, которая берётся из верхнего текстового поля
        directory_of_processing_files = self.InitFilePathField.toPlainText()
        results_file_path = "/".join([directory_of_processing_files, name_of_result_file])

        # это будет экспортировано
        header_for_saving = ",".join(self.export_list['header'])
        units_for_saving = "GHz, , , T, , Ohm, K, , T, , Ohm, K, , T, , Ohm, K, , , \n"
        result_string_general_with_header = header_for_saving + '\n' + units_for_saving + self.result_string_general
        with open(results_file_path + ".txt", "w") as file:
            file.write(result_string_general_with_header)

        # Это условие позволяет оперативно менять таблицу с результатами, когда мы смотрим на неё
        if self.TableComboBox.currentText() == "RESULT Table":
            converted_result_data = convert_rows_to_columns(self.export_list['data'])
            put_table_in_qtable_wiget(self.export_list['header'], self.InitDataTable, converted_result_data)

    def export_single_results_to_list(self):
        """ Эта функция формирует из ранее полученных данных список с результатами для рассматриваемого файло """
        print("export_single_results_to_list")

        result_list = []
        # так мы вписываем частоту и номер измерения
        if self.name_of_file_DN:
            frequency = split_name_of_file(self.name_of_file_DN)[0]
            run_number = split_name_of_file(self.name_of_file_DN)[1]
            result_list = [frequency, run_number]
        elif self.name_of_file_UP:
            frequency = split_name_of_file(self.name_of_file_UP)[0]
            run_number = split_name_of_file(self.name_of_file_UP)[1]
            result_list = [frequency, run_number]

        # если нет файла DN, то мы его заполним пропусками, а усреднение будет то же что и UP
        if (not self.name_of_file_DN) and self.name_of_file_UP:
            # эта строчка служит пробелом в данных, он станет пустой колонкой
            result_list.append("")
            B_peak_DN = ""
            R_peak_DN = ""
            T_resistance_DN = ""
            T_DN = ""
            result_list.append(B_peak_DN)
            result_list.append(R_peak_DN)
            result_list.append(T_resistance_DN)
            result_list.append(T_DN)

            result_list.append("")

            B_peak_UP = float(self.on_mouse_press_coordinate_list_UP[0][0])
            R_peak_UP = float(self.on_mouse_press_coordinate_list_UP[0][1])
            T_resistance_UP = self.temperature_resistance_around_peak_UP
            T_UP = self.temperature_around_peak_UP
            result_list.append(B_peak_UP)
            result_list.append(R_peak_UP)
            result_list.append(T_resistance_UP)
            result_list.append(T_UP)

            result_list.append("")

            B_peak_mean = float(self.on_mouse_press_coordinate_list_UP[0][0])
            R_peak_mean = float(self.on_mouse_press_coordinate_list_UP[0][1])
            T_resistance_mean = self.temperature_resistance_around_peak_UP
            T_mean = self.temperature_around_peak_UP
            result_list.append(B_peak_mean)
            result_list.append(R_peak_mean)
            result_list.append(T_resistance_mean)
            result_list.append(T_mean)

            result_list.append("")
            result_list.append("")
            result_list.append(self.name_of_file_UP)

        # если нет файла UP, то мы его заполним пропусками, а усреднение будет то же что и DN
        if self.name_of_file_DN and (not self.name_of_file_UP):
            # эта строчка служит пробелом в данных, он станет пустой колонкой
            result_list.append("")

            B_peak_DN = float(self.on_mouse_press_coordinate_list_DN[0][0])
            R_peak_DN = float(self.on_mouse_press_coordinate_list_DN[0][1])
            T_resistance_DN = self.temperature_resistance_around_peak_DN
            T_DN = self.temperature_around_peak_DN
            result_list.append(B_peak_DN)
            result_list.append(R_peak_DN)
            result_list.append(T_resistance_DN)
            result_list.append(T_DN)

            result_list.append("")

            B_peak_UP = ""
            R_peak_UP = ""
            T_resistance_UP = ""
            T_UP = ""
            result_list.append(B_peak_UP)
            result_list.append(R_peak_UP)
            result_list.append(T_resistance_UP)
            result_list.append(T_UP)

            result_list.append("")

            B_peak_mean = float(self.on_mouse_press_coordinate_list_DN[0][0])
            R_peak_mean = float(self.on_mouse_press_coordinate_list_DN[0][1])
            T_resistance_mean = self.temperature_resistance_around_peak_DN
            T_mean = self.temperature_around_peak_DN
            result_list.append(B_peak_mean)
            result_list.append(R_peak_mean)
            result_list.append(T_resistance_mean)
            result_list.append(T_mean)

            result_list.append("")
            result_list.append(self.name_of_file_DN)
            result_list.append("")

        if self.name_of_file_DN and self.name_of_file_UP:
            # эта строчка служит пробелом в данных, он станет пустой колонкой
            result_list.append("")

            B_peak_DN = float(self.on_mouse_press_coordinate_list_DN[0][0])
            R_peak_DN = float(self.on_mouse_press_coordinate_list_DN[0][1])
            T_resistance_DN = self.temperature_resistance_around_peak_DN
            T_DN = self.temperature_around_peak_DN
            result_list.append(B_peak_DN)
            result_list.append(R_peak_DN)
            result_list.append(T_resistance_DN)
            result_list.append(T_DN)

            result_list.append("")

            B_peak_UP = float(self.on_mouse_press_coordinate_list_UP[0][0])
            R_peak_UP = float(self.on_mouse_press_coordinate_list_UP[0][1])
            T_resistance_UP = self.temperature_resistance_around_peak_UP
            T_UP = self.temperature_around_peak_UP
            result_list.append(B_peak_UP)
            result_list.append(R_peak_UP)
            result_list.append(T_resistance_UP)
            result_list.append(T_UP)

            result_list.append("")

            B_peak_mean = round((B_peak_DN + B_peak_UP) / 2, 3)
            R_peak_mean = round((R_peak_DN + R_peak_UP) / 2, 6)
            T_resistance_mean = round((T_resistance_DN + T_resistance_UP) / 2, 3)
            T_mean = round((T_DN + T_UP) / 2, 3)
            result_list.append(B_peak_mean)
            result_list.append(R_peak_mean)
            result_list.append(T_resistance_mean)
            result_list.append(T_mean)

            result_list.append("")
            result_list.append(self.name_of_file_DN)
            result_list.append(self.name_of_file_UP)

        return result_list

    # Next
    def next_file(self):
        """Функция, к которой привязана кнопка Next"""
        # Это условие, чтобы не зависнуть в конце списка
        if self.data_index_for_processing < len(self.list_for_plot) - 1:
            self.InitDataTable.clear()
            self.data_index_for_processing += 1
            self.import_data()

    # Previous file
    def previous_file(self):
        """Функция, к которой привязана кнопка Previous"""
        if self.data_index_for_processing > 0:
            self.InitDataTable.clear()
            self.data_index_for_processing -= 1
            self.import_data()

    # Save and Next
    def save_fitting_and_next_file(self):
        """Функция, к которой привязана кнопка Save and Next"""
        if self.list_for_plot:
            self.save_fitting()
            self.next_file()

    # del Save
    def delSave_fitting(self):
        """Функция, к которой привязана кнопка del Save"""

        # Условие, что при удалении последней строчки следует просто очистить таблицу, а не пытаться её отрисовать
        if len(self.export_list['data']) == 1:
            self.export_list['data'].clear()
            self.result_string_general = ""
            self.InitDataTable.clear()

        # Так мы удаляем данные построчно. Здесь как раз принципиально важно, что мы сохраняли результаты в отдельный словарь export_list
        if len(self.export_list['data']) > 1:
            self.export_list['data'] = self.export_list['data'][:-1]
            self.result_string_general = ""
            for ind in range(len(self.export_list['data'])):
                result_string_local = [str(x) for x in self.export_list['data'][ind]]
                result_string_local = ", ".join(result_string_local)
                result_string_local = result_string_local + "\n"
                self.result_string_general += result_string_local

            self.save_to_file()

    # TableComboBox
    def TableComboBox_change_function(self, text):
        """Функция, к которой привязана слайдер выбора таблицы"""

        # Условие and self.list_for_plot не дает программе вылететь, когда прожимается слайдер без загруженных данных
        if text == "Table DOWN" and self.list_for_plot:
            if self.list_for_plot[self.data_index_for_processing][0]:
                self.InitDataTable.clear()
                put_table_in_qtable_wiget(self.data_voc_DN['header'], self.InitDataTable, self.data_voc_DN['data'])
            else:
                self.InitDataTable.clear()

        if text == "Table UP" and self.list_for_plot:
            if self.list_for_plot[self.data_index_for_processing][1]:
                self.InitDataTable.clear()
                put_table_in_qtable_wiget(self.data_voc_UP['header'], self.InitDataTable, self.data_voc_UP['data'])
            else:
                self.InitDataTable.clear()

        if text == "RESULT Table" and self.export_list['data']:
            self.InitDataTable.clear()
            # приходится транспонировать, чтобы функция put_table_in_qtable_wiget() заработала
            converted_result_data = convert_rows_to_columns(self.export_list['data'])
            put_table_in_qtable_wiget(self.export_list['header'], self.InitDataTable, converted_result_data)

    # ColumnForPlotComboBox
    def ColumnForPlotComboBox_change_function(self, text):
        """Функция, к которой привязана слайдер выбора столбца для обработки"""
        if text == "X":
            self.column_for_processing = 4

        if text == "Y":
            self.column_for_processing = 5

        if text == "R":
            self.column_for_processing = 12


        self.on_mouse_press_coordinate_list_DN = []
        self.on_mouse_press_coordinate_list_UP = []
        self.clear_plot_DN()
        self.clear_plot_UP()
        if self.data_voc_DN:
            self.plot_initial_data_DN()
        if self.data_voc_UP:
            self.plot_initial_data_UP()



def main_application():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main_application()
