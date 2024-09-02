from tkinter import *
from tkinter.messagebox import showerror, showwarning, showinfo

import tkinter.ttk as ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from functools import partial

import raytracing as rt
import raytracing.thorlabs as thorlabs
import raytracing.eo as eo
from raytracing.figure import GraphicOf


class App:
    app = None

    def __new__(cls, geometry=None):
        if cls.app is None:
            cls.app = super().__new__(cls)
        return cls.app

    def __init__(self, geometry=None):
        self.window = Window(geometry)

    def mainloop(self):
        self.window.widget.mainloop()


class BaseView:
    def __init__(self):
        self.widget = None
        self.parent = None

    def grid_into(self, parent, **kwargs):
        self.create_widget(master=parent.widget)
        self.parent = parent

        if self.widget is not None:
            self.widget.grid(kwargs)

    def pack_into(self, parent, **kwargs):
        self.create_widget(master=parent.widget)
        self.parent = parent

        if self.widget is not None:
            self.widget.pack(kwargs)

    @property
    def width(self):
        return self.widget["width"]

    @property
    def height(self):
        return self.widget["height"]


class Window(BaseView):
    def __init__(self, geometry=None, title="Viewer"):
        BaseView.__init__(self)

        if geometry is None:
            geometry = "1020x750"
        self.title = title

        self.widget = Tk()
        self.widget.geometry(geometry)
        self.widget.title(self.title)
        self.widget.columnconfigure(0, weight=1)
        self.widget.rowconfigure(1, weight=1)


class View(BaseView):
    def __init__(self, width, height):
        BaseView.__init__(self)
        self.original_width = width
        self.original_height = height

    def create_widget(self, master):
        self.widget = ttk.Frame(master, width=self.original_width, height=self.original_height)


class PopupMenu(BaseView):
    def __init__(self, menu_items=None, user_callback=None):
        BaseView.__init__(self)

        self.selected_index = None
        self.user_callback = user_callback
        self.menu_items = menu_items
        self.menu = None
        self.text = StringVar(value="Select menu item")

    def create_widget(self, master):
        self.menu = Menu(master, tearoff=0)
        self.widget = ttk.Menubutton(master, textvariable=self.text, text='All lenses', menu=self.menu)

        if self.menu_items is not None:
            self.add_menu_items(self.menu_items)

    def add_menu_items(self, menu_items, user_callback=None):
        self.menu_items = menu_items
        labels = menu_items
        for i, label in enumerate(labels):
            self.menu.add_command(label=label, command=partial(self.selection_callback, i))

    def selection_callback(self, selected_index):
        self.selected_index = selected_index
        self.text.set(value=self.menu_items[self.selected_index])

        if self.user_callback is not None:
            self.user_callback()


class Label(BaseView):
    def __init__(self, text=""):
        BaseView.__init__(self)
        self.text = text

    def create_widget(self, master):
        self.widget = ttk.Label(master, text=self.text)


class Entry(BaseView):
    def __init__(self, text=""):
        BaseView.__init__(self)
        self.value = StringVar()

    def create_widget(self, master):
        self.widget = ttk.Entry(master, textvariable=self.value, text=text)


class MatplotlibView(BaseView):
    def __init__(self, figure=None):
        BaseView.__init__(self)

        if figure is None:
            self.figure = Figure(figsize=(10.2, 5.5), dpi=100)
        else:
            self.figure = figure

        self.canvas = None
        self.toolbar = None

    def create_widget(self, master):
        self.canvas = FigureCanvasTkAgg(self.figure, master=master)
        self.widget = self.canvas.get_tk_widget()

        self.toolbar = NavigationToolbar2Tk(self.canvas, master, pack_toolbar=True)
        self.toolbar.update()


class ViewerApp(App):
    def __init__(self, geometry="1000x700"):
        App.__init__(self, geometry)

        self.top_frame = View(width=1000, height=100)
        self.label = None
        self.menu = None

        self.top_frame.grid_into(self.window, column=0, row=0, pady=20)
        self.bottom_frame = View(width=1000, height=700 - 100)
        self.bottom_frame.grid_into(self.window, column=0, row=1, pady=20)
        self.matplotlib_view = None
        self.replace_figure()

    def create_popupmenu(self, prompt, menu_items):
        self.label = Label(prompt)
        self.menu = PopupMenu(menu_items)
        self.label.grid_into(self.top_frame, column=0, row=0)
        self.menu.grid_into(self.top_frame, column=1, row=0)

    def replace_figure(self, figure=None):
        self.bottom_frame = View(width=1000, height=700 - 100)
        self.bottom_frame.grid_into(self.window, column=0, row=1, pady=20)
        self.matplotlib_view = MatplotlibView(figure)
        self.matplotlib_view.pack_into(self.bottom_frame, padx=10)

    @property
    def figure(self):
        return self.matplotlib_view.figure

    @figure.setter
    def figure(self, value):
        self.replace_figure(value)


class OpticalComponentViewer(ViewerApp):
    def __init__(self):
        ViewerApp.__init__(self, geometry="1020x750")
        self.lenses = {}
        self.build_lens_dict()

        self.create_popupmenu("Selectionnez qqch:", list(self.lenses.keys()))
        self.menu.user_callback = self.selection_changed

    def build_lens_dict(self):
        modules = [thorlabs, eo]

        for i, lens in enumerate(rt.CompoundLens.all()):
            for module in modules:
                try:
                    class_ = getattr(module, lens)
                    lens = class_()
                    f1, f2 = lens.effectiveFocalLengths()
                    label = "{0:s} [f={1:.1f} mm]".format(lens.label, f1)
                    self.lenses[label] = lens
                except:
                    pass

    def selection_changed(self):
        lens_label = self.menu.menu_items[self.menu.selected_index]
        lens = self.lenses[lens_label]

        graphic = GraphicOf(lens)
        graphic_figure = graphic.createFigure()
        graphic_figure.draw()
        self.figure = graphic_figure.figure


if __name__ == "__main__":
    app = OpticalComponentViewer()

    plot = app.figure.add_subplot()
    plot.plot([0, 1, 2, 3], [4, 5, 6, 7])

    app.mainloop()


# import raytracing as rt
# import raytracing.thorlabs as thorlabs
# import raytracing.eo as eo
# from raytracing.figure import GraphicOf
#
# from tkinter import *
#
# from tkinter.messagebox import showerror, showwarning, showinfo
# import tkinter.ttk as ttk
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# from functools import partial
#
#
# class Viewer:
#     def __init__(self):
#         self.field_var = None
#         self.lenses = []
#         self.root = Tk()
#         self.fig = None
#         self.canvas = None
#         self.entry = None
#         self.popup = None
#         self.menuButton = None
#
#         self.build_viewer_window()
#
#     def buildLensList(self):
#         modules = [thorlabs, eo]
#
#         for i, lens in enumerate(rt.CompoundLens.all()):
#             for module in modules:
#                 try:
#                     class_ = getattr(module, lens)
#                     lens = class_()
#                     self.lenses.append(lens)
#                 except:
#                     pass
#
#     def createMenu(self):
#         self.popup = Menu(self.root, tearoff=0)
#         for i, lens in enumerate(self.lenses):
#             f1, f2 = lens.effectiveFocalLengths()
#             label = "{0:s} [f={1:.1f}]".format(lens.label, f1)
#             self.popup.add_command(label=label, command=partial(self.item_plot, i))
#         self.field_var = StringVar(value="Select lens")
#         self.menuButton = ttk.Menubutton(textvariable=self.field_var,text='All lenses',menu=self.popup)
#         self.menuButton.width = 30
#         self.menuButton.grid(column=0, row=0)
#
#     def build_viewer_window(self):
#         self.root.geometry("1020x750")
#         self.root.title("Lens viewer")
#
#         self.frm = ttk.Frame(self.root, padding=10)
#         self.frm.grid()
#
#         self.buildLensList()
#         self.createMenu()
#
#         # a blank figure that will be replaced with the real figure
#         self.fig = Figure(figsize=(10.2, 7.5), dpi=100)
#
#         self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
#         toolbar = NavigationToolbar2Tk(self.canvas, self.root, pack_toolbar=False)
#         toolbar.update()
#
#         self.canvas.get_tk_widget().grid(column=0, row=1)
#         self.canvas.draw()
#
#     def item_plot(self, index):
#         try:
#             lens = self.lenses[index]
#             self.field_var.set(lens.label) # Reflect choice on screen
#
#             graphic = GraphicOf(lens)
#             self.fig = graphic.drawFigure() # hack
#
#             self.canvas = FigureCanvasTkAgg(self.fig.figure, master=self.root)
#             toolbar = NavigationToolbar2Tk(self.canvas, self.root, pack_toolbar=False)
#             toolbar.update()
#
#             self.canvas.get_tk_widget().grid(column=0, row=1)
#             self.canvas.draw()
#
#         except Exception as err:
#             showerror("Unable to display lens #",i," : ", err)
#
#
# if __name__ == "__main__":
#     app = Viewer()
#     app.root.mainloop()
