from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

from matplotlib import pyplot as plt

from PyQt5.QtWidgets import QSizePolicy, QVBoxLayout



class MyMplCanavas(FigureCanvasQTAgg):
    def __init__(self, fig, parent=None):
        self.fig = fig
        FigureCanvasQTAgg.__init__(self, self.fig)
        FigureCanvasQTAgg.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

def prepare_canavas_and_toolbar(parent=None):
    parent.fig, parent.axes_left, parent.axes_right = plot_single_empty_graph()

    # этим мы создаем холст = figure - axes
    parent.canvas = MyMplCanavas(parent.fig)
    parent.toolbar = NavigationToolbar2QT(parent.canvas, parent)

    # эта строчка располагает виджеты один под другим с выравниванием по правой стороне
    parent.companovka_for_mpl = QVBoxLayout(parent.MplWidget)
    parent.companovka_for_mpl.addWidget(parent.canvas)
    parent.companovka_for_mpl.addWidget(parent.toolbar)

def plot_single_empty_graph():
    """функция создает axes, с которыми в дальнейшем и будем работать"""
    fig, (axes_left, axes_right) = plt.subplots(nrows=1, ncols=2, figsize=(10, 7), dpi=85, facecolor='white', frameon=True,
                             edgecolor='black', linewidth=3)
    fig.subplots_adjust(wspace=0.2, hspace=0.2, right=0.97, left=0.07, top=0.9, bottom=0.1)

    # наводим красоту на левом графике
    axes_left.grid(True, c='lightgrey', alpha=0.5)
    axes_left.set_title('DN', fontsize=20)
    axes_left.set_xlabel('Magnetic Field', fontsize=15)
    axes_left.set_ylabel('Signal', fontsize=15)

    # наводим красоту на правом графике
    axes_right.grid(True, c='lightgrey', alpha=0.5)
    axes_right.set_title('UP', fontsize=20)
    axes_right.set_xlabel('Magnetic Field', fontsize=15)
    axes_right.set_ylabel('Signal', fontsize=15)

    return fig, axes_left, axes_right
