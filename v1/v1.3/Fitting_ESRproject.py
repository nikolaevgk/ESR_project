import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq


def transformation_of_data(data, multiplier=0):
    """Эта функция принимает данные в виде списка, и переводит их в numpy массив.
        Если multiplier не ноль, то у тому же умножает их на multiplier.
        Это сделано потому, что scipy.optimize.leastsq работает с nd.array,
        А умножаются данные внизу на 1E6 потому что leastsq плохо работает с
        малыми значениями"""
    data = np.array(data)
    if multiplier != 0:
        multiplied_data = [value*(multiplier) for value in data]
        multiplied_data = np.array(multiplied_data)
        return multiplied_data
    else:
        return data


def fano_resonance_with_linear_background(params, x):
    """Эта функция принимает массив параметров и переменную x.
        Выдает расчет по формуле резонанса Фано с добавлением линейной функции"""
    a, b, c, q = params[0], params[1], params[2], params[3]
    x0, w = params[4], params[5]
    e = 2 * (x - x0) / w
    formula = a * ((e + q)**2) / (e**2 + 1) + b * x + c
    return formula
def fano_resonance_with_linear_background_residual(params, x, y):
    """Эта функция необходима для scipy.optimizeю.leastsq"""
    residual = y - fano_resonance_with_linear_background(params, x)
    return residual
def peak_fitting_Fano_resonance_with_linear_background(x_row_data, y_row_data, initial_params=(0, 0, 0, 0, 0, 1)):
    """Эта функция принимает два массива данных, принимает начальные парамаетры для модели,
        строит модель с leastsq и возвращает параметры фитинга"""
    initial_params = np.array(initial_params)
    x_row_data = transformation_of_data(x_row_data)
    y_row_data = transformation_of_data(y_row_data)

    fitting_result_parameters = leastsq(fano_resonance_with_linear_background_residual, initial_params,
                     args=(x_row_data, y_row_data))[0]

    return fitting_result_parameters


def fano_resonance(params, x):
    """Эта функция принимает массив параметров и переменную x.
        Выдает расчет по формуле резонанса Фано"""
    a, q = params[0], params[1]
    x0, w = params[2], params[3]
    e = 2 * (x - x0) / w
    formula = a * ((e + q)**2) / (e**2 + 1)
    return formula
def fano_resonance_residual(params, x, y):
    """Эта функция необходима для scipy.optimizeю.leastsq"""
    residual = y - fano_resonance(params, x)
    return residual
def peak_fitting_Fano_resonance(x_row_data, y_row_data, initial_params=(0, 0, 0, 1)):
    """Эта функция принимает два массива данных, принимает начальные парамаетры для модели,
        строит модель с leastsq и возвращает параметры фитинга"""
    initial_params = np.array(initial_params)
    x_row_data = transformation_of_data(x_row_data)
    y_row_data = transformation_of_data(y_row_data)

    fitting_result_parameters = leastsq(fano_resonance_residual, initial_params,
                     args=(x_row_data, y_row_data))[0]

    return fitting_result_parameters


def qubic_background_fitting(params, x):
    """Эта функция принимает массив параметров и переменную x.
        Выдает расчет кубическому полиному"""
    a, b, c, d = params[0], params[1], params[2], params[3]
    formula = a * x**3 + b * x**2 + c * x + d
    return formula
def qubic_background_fitting_residual(params, x, y):
    """Эта функция необходима для scipy.optimizeю.leastsq"""
    residual = y - qubic_background_fitting(params, x)
    return residual
def background_fitting_qubic_function(x_row_data, y_row_data, initial_params=(0, 0, 0, 0)):
    """Эта функция принимает два массива данных, принимает начальные парамаетры для модели,
        строит модель с leastsq и возвращает параметры фитинга"""
    initial_params = np.array(initial_params)
    x_row_data = transformation_of_data(x_row_data)
    y_row_data = transformation_of_data(y_row_data)

    fitting_result_parameters = leastsq(qubic_background_fitting_residual, initial_params,
                     args=(x_row_data, y_row_data))[0]

    return fitting_result_parameters


def linear_background_fitting(params, x):
    """Эта функция принимает массив параметров и переменную x.
        Выдает расчет по уравнению прямой"""
    a, b = params[0], params[1]
    formula = a * x + b
    return formula
def linear_background_fitting_residual(params, x, y):
    """Эта функция необходима для scipy.optimizeю.leastsq"""
    residual = y - linear_background_fitting(params, x)
    return residual
def background_fitting_linear_function(x_row_data, y_row_data, initial_params=(0, 0)):
    """Эта функция принимает два массива данных, принимает начальные парамаетры для модели,
        строит модель с leastsq и возвращает параметры фитинга"""
    initial_params = np.array(initial_params)
    x_row_data = transformation_of_data(x_row_data)
    y_row_data = transformation_of_data(y_row_data)

    fitting_result_parameters = leastsq(linear_background_fitting_residual, initial_params,
                     args=(x_row_data, y_row_data))[0]

    return fitting_result_parameters


def fitting_function(function_of_fitting, params, x_data, plot=False):
    """Эта функция принимает функцию, параметры для неё и данные для абсциссы.
        Возвращает массив с рассчитанными данными. Если нежно строит график"""
    y_calculated_data = [function_of_fitting(params, x) for x in x_data]
    if plot is True:
        plt.plot(x_data, y_calculated_data,
                 color="red", label='Background fitting')
    return np.array(y_calculated_data)

