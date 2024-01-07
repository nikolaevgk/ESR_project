from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt

def prepare_table_data_from_txt(path_to_data, delimeter = '\t'):
    r"""
    функция prepare_table_data_from_txt Версия 1.0
    Подготовка табличных данных из txt файла с разделителем \t (знак табуляции) по умолчанию
    Получаем словарь состоящий из
    1) header - заголовки столбцов
    2) units - единицы измерений для столбцов
    3) data - двумерный список с данными типа [[n11, n12, ..., n1i], ..., [nj1, nj2, ..., nji]]
    где i - колличество строк в исходных данных, j - колличество столбцов в исходных данных
    Читается весь файл, то есть все не пустые строки, при этом выделяется заголовок и строка единиц измерений по умолчанию 1 и 2
    соответственно, но также строки могут быть заданны пользователем при вызове функции
    """
    data = []
    # Читаем файл
    input_file = open(path_to_data, 'r', encoding='utf-8')
    read_data = input_file.readlines()
    input_file.close()
    # Если файл содержит данные то перебираем строки
    if len(read_data) > 0:
        header = []
        units = []
        for line in range(len(read_data)):
            # Если встречаем строку с номером загоовка переносим ее в заголовок
            # Добавляем данные из строки в массив данных
            data_line = read_data[line].replace(' ', '')
            data_line = (data_line.replace('\n','')).split(delimeter)
            # Данные устроены так, что каждая строка заканчивается ...data, data, data, \n
            #   так что split по запятой оставляет в конце пустой элемент. Именно его то мы и убираем len(data_line)-1 внизу
            # В этом цикле мы меняем тип элементов с str на float
            float_data_line = []
            for line_shape_index in range(len(data_line)-1):
                float_data_line.append(float(data_line[line_shape_index]))
            data.append(float_data_line)

        data = convert_rows_to_columns(data)
        data_table = {'header': header, 'units': units, 'data': data}

        return data_table

def convert_rows_to_columns(data_massive_to_convert):
    """
    Переформатирование рядов в колонки
    """
    data_massive_converted = []
    for y in range(len(data_massive_to_convert[0])):
        data_massive_converted.append([])
        for x in range(len(data_massive_to_convert)):
            data_massive_converted[y].append(data_massive_to_convert[x][y])
    return data_massive_converted

def put_table_in_qtable_wiget(header, table_wiget, data):
    """
    Function to plot table (на вход список заголовков и данные таблицы) into QTableWidget
    При помещении таблицы в QTableWidget отдельно показываются заголовки (строка заголовков)
    Нумеруются ряды (крайняя левая колонка)
    """
    table_wiget.setRowCount(len(data[0]))  # Устанавливаем колличество рядов для таблицы
    table_wiget.setColumnCount(len(data))  # Устанавливаем колличество колонок для таблицы
    table_wiget.setHorizontalHeaderLabels(header)  # Устанавливаем в качестве заголовков список шапки
    # table_wiget.verticalHeader().setVisible(False) эта строка позволяет убрать нумерацию строк
    # Добавление данных в таблицу
    for x in range(0, len(data)):
        for y in range(0, len(data[x])):
            table_wiget.setItem(y, x, QTableWidgetItem(str(data[x][y])))

    modify_cells(table_wiget)

def prepare_two_row_data(table, x=0, y=5):
    """
    Подготовка данных двух столбцов из табличного виджета QTableWidget по имени столбцов
    при возникновении ошибки функция возвращает пустой список иначе список со значениями требуемого ряда
    """
    column_one_container = []
    column_two_container = []

    try:
        for i in range(0, table.rowCount()):  # Перебираем ряды добовляя значения колонки с индексом x в список
            column_one_container.append(float(table.item(i, x).text()))
        for i in range(0, table.rowCount()):  # Перебираем ряды добовляя значения колонки с индексом y в список
            column_two_container.append(float(table.item(i, y).text()))
        return column_one_container, column_two_container
    except:
        return column_one_container, column_two_container

def modify_cells(TableWidget):
    """
    Функция изменяет отображение ячеек таблицы так, чтобы цифры отображались посередине и размеры ячейки подгонялись
    под размер поля, отведённого под таблицу
    """
    for row in range(TableWidget.rowCount()):
        for column in range(TableWidget.columnCount()):
            TableWidget.item(row, column).setTextAlignment(Qt.AlignCenter)
    # TableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


