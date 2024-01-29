import raytracing as rt
import raytracing.thorlabs as thorlabs
import raytracing.eo as eo
from raytracing.figure import GraphicOf

from tkinter import *

from tkinter.messagebox import showerror, showwarning, showinfo
import tkinter.ttk as ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from functools import partial


class Viewer:
    def __init__(self):
        self.field_var = None
        self.lenses = []
        self.root = Tk()
        self.fig = None
        self.canvas = None
        self.entry = None
        self.popup = None
        self.menuButton = None


        self.root.geometry("1020x750")
        self.root.title("Lens viewer")

        self.frm = ttk.Frame(self.root, padding=10)
        self.frm.grid()

        self.build_viewer_window()

    def buildLensList(self):
        modules = [thorlabs, eo]

        for i, lens in enumerate(rt.CompoundLens.all()):
            for module in modules:
                try:
                    class_ = getattr(module, lens)
                    lens = class_()
                    self.lenses.append(lens)
                except:
                    pass

    def createMenu(self):
        self.popup = Menu(self.root, tearoff=0)
        for i, lens in enumerate(self.lenses):
            self.popup.add_command(label=lens.label, command=partial(self.item_plot, i))
        self.field_var = StringVar(value="Select lens")
        self.menuButton = ttk.Menubutton(textvariable=self.field_var,text='All lenses',menu=self.popup)
        self.menuButton.width = 30
        self.menuButton.grid(column=0, row=0)

    def build_viewer_window(self):
        self.buildLensList()
        self.createMenu()

        # a blank figure that will be replaced with the real figure
        self.fig = Figure(figsize=(10, 7), dpi=100)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        toolbar = NavigationToolbar2Tk(self.canvas, self.root, pack_toolbar=False)
        toolbar.update()

        self.canvas.get_tk_widget().grid(column=0, row=1)
        self.canvas.draw()

    def item_plot(self, index):
        try:
            lens = self.lenses[index]
            self.field_var.set(lens.label) # Reflect choice on screen

            graphic = GraphicOf(lens)
            self.fig = graphic.display() # hack

            self.canvas = FigureCanvasTkAgg(self.fig.figure, master=self.root)
            toolbar = NavigationToolbar2Tk(self.canvas, self.root, pack_toolbar=False)
            toolbar.update()

            self.canvas.get_tk_widget().grid(column=0, row=1)
            self.canvas.draw()

        except Exception as err:
            showerror("Error when retrieving data", err)


if __name__ == "__main__":
    app = Viewer()
    app.root.mainloop()
