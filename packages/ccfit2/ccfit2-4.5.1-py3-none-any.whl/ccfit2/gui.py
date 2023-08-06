"""
This module contains gui helper functions
"""


from tkinter import Tk, messagebox, Label, Entry, filedialog
from tkinter import Button as _Button
import os
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Button
import matplotlib.cm as cm
import matplotlib.colors as mpl_col
import numpy as np
import sys

from . import utils


def error_box(message: str, title: str = "Error") -> None:
    """
    Creates simple tkinter error box with specified text and title

    Parameters
    ----------
    message : str
        Text shown in body of window
    title : str
        Text shown in title of window

    Returns
    -------
    None
    """
    messagebox.showerror(title, message)
    sys.exit()

    return


def parse_sample_info(user_cfg: utils.UserConfig, mw_entry,
                      mass_entry, root: Tk) -> None:
    """
    Callback function for tkinter window for mass and molecular weight

    Parameters
    ----------
    user_cfg: utils.UserConfig
        Configuration object
    mw_entry : str
        string value of molecular weight from tkinter window
    mass_entry : str
        string value of sample mass from tkinter window
    root : Tk
        root object of current window

    Returns
    -------
    None
    """

    try:
        user_cfg.mass = float(mass_entry.get())
        user_cfg.mw = float(mw_entry.get())
    except ValueError:
        message = 'ValueError: The entries need to be numbers.'
        error_box(message)

    root.update()
    root.destroy()

    return


def mass_mw_entry(user_cfg: utils.UserConfig) -> None:
    """
    Creates tkinter window for user to input mass and molecular weight of
    sample

    Parameters
    ----------
    user_cfg: utils.UserConfig
        Configuration object

    Returns
    -------
    None
    """

    root = Tk()
    root.title("Sample information")
    root.geometry("310x150")

    # Move to centre of screen
    root.eval('tk::PlaceWindow . center')
    root.wait_visibility()

    mass_label = Label(
        root,
        text="Mass (mg):",
        justify='left',
        pady=5,
        height=2,
        anchor='w'
    )
    mass_entry = Entry(root, bd=1, width=14)
    mass_label.grid(row=0, column=0)
    mass_entry.grid(row=0, column=1)

    mw_label = Label(
        root,
        text="Molecular Weight (g/mol):",
        justify='left',
        pady=5,
        height=2
    )
    mw_entry = Entry(root, bd=1, width=14)
    mw_label.grid(row=1, column=0)
    mw_entry.grid(row=1, column=1)

    enter_button = _Button(
        root,
        text="Continue",
        command=lambda: parse_sample_info(
            user_cfg, mw_entry, mass_entry, root
        ),
        height=2
    )
    enter_button.grid(row=2, column=1)

    root.mainloop()

    return


def filename_entry(user_cfg: utils.UserConfig,) -> None:
    """
    Creates tkinter window for user to input mass and molecular weight of
    sample

    Parameters
    ----------
    user_cfg: utils.UserConfig
        Configuration object

    Returns
    -------
    None
    """

    root = Tk()
    root.withdraw()
    root.update()

    user_cfg.file_name = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title="Select file",
        filetypes=(
            ("dat files", "*.dat"),
            ("all files", "*.*")
        )
    )
    root.update()
    if not len(user_cfg.file_name):
        exit()

    root.update()
    root.destroy()

    return


def make_mpl_radiobuttons(pos: list[float], labels: list[str],
                          circle_radius: float, figure) -> RadioButtons:
    """
    Creates matplotlib radiobuttons on given figure

    Parameters
    ----------
    pos : list
        4 floats specifying left, bottom, width, height
    labels : list
        label for each radiobutton
    circle_radius : float
        radius of radiobutton circle

    Returns
    -------
    matplotlib.widgets.RadioButtons
        Set of radiobuttons for matplotlib figure window
    """

    rax = plt.axes(
        pos,
        facecolor='w',
        frameon=False,
        aspect='equal',
        figure=figure
    )
    radio = RadioButtons(
        rax,
        labels
    )

    for circle in radio.circles:
        circle.set_radius(circle_radius)
        circle.set_facecolor('white')

    return radio


def make_mpl_button(axis, text, colour):
    """
    Creates matplotlib button on given axis

    Parameters
    ----------
    axis : function
        Axis to which button is added
    text : str
        Text for body of button
    colour : str
        name of colour

    Returns
    -------
    matplotlib.widgets.Button
        Button for matplotlib figure window
    """

    button = Button(
        axis,
        text,
        color=colour,
        hovercolor='0.975'
    )

    return button


def sliders_reset(sliders):
    """
    Resets a list of sliders back to their original values

    Parameters
    ----------
    sliders : list[sliders]
        matplotlib sliders

    Returns
    -------
    None
    """
    for slider in sliders:
        slider.reset()
    return


class RadioToggleButtons(RadioButtons):

    def set_active(self, index):
        """
        Select button with number *index*.

        Callbacks will be triggered if :attr:`eventson` is True.
        """
        if index not in range(len(self.labels)):
            raise ValueError(f'Invalid RadioButton index: {index}')

        self.value_selected = self.labels[index].get_text()

        for i, p in enumerate(self.circles):
            if i == index:
                if p._facecolor == (0., 0., 1., 1.):
                    p.set_facecolor((0., 0., 0., 0.))
                else:
                    p.set_facecolor(self.activecolor)

        if self.drawon:
            self.ax.figure.canvas.draw()

        if self.eventson:
            self._observers.process('clicked', self.labels[index].get_text())

        return


def create_ac_temp_colorbar(ax, fig, temps: list[float], colors):
    """
    Creates colorbar for temperatues in AC plotting

    Parameters
    ----------

    ax : matplotlib axis object
        Axis to which colorbar is added
    fig : matplotlib fig object
        Figure to which colorbar is added
    temps : list[float]
        Temperatures in Kelvin
    colors : matplotlib cm object
        colormap used in plot

    Returns
    -------
    list
        Colourbar tick positions
    """
    n_temps = len(temps)

    # Make colourbar
    # Indexing starts at zero and ends at num_temps
    norm = mpl_col.BoundaryNorm(
        np.arange(0, n_temps+1),
        ncolors=colors.N
    )

    # Scalar mappable converts colourmap numbers into an image of colours
    sm = cm.ScalarMappable(cmap=colors, norm=norm)

    colorbar_ticks = np.arange(1, n_temps+1) - 0.5
    colorbar_labels = get_temp_colourbar_ticks(temps)

    cbar = fig.colorbar(
        sm,
        ticks=colorbar_ticks,
        orientation='horizontal',
        format='%.1f',
        cax=ax
    )

    ax.set_xticklabels(
        colorbar_labels,
        rotation=0,
        fontsize='smaller'
    )

    ax.minorticks_off()

    # Set colourbar label - technically title - above bar
    cbar.ax.set_title('T (K)', fontsize='smaller')

    return cbar


def get_temp_colourbar_ticks(temperatures: list[float]) -> list[float]:
    """
    Creates ticks for a temperature colourbar
    If there are fewer than 9 data points, show all from 1st to last all
    temp in temperatures.

    If there are between 9 and 17, slice every 3 and 4 points depending on
    even-odd.

    If there are more than 17, slice every 5 and 6 points depending on
    even-odd.

    Parameters
    ----------
    temperatures : list
        Floats of temperatures in Kelvin

    Returns
    -------
    list
        Colourbar tick positions
    """

    n_temps = len(temperatures)

    ticks = ["{:.1f}".format(tp) for tp in temperatures]

    if n_temps <= 8:
        step = 1
    elif 9 <= n_temps <= 17:
        if n_temps % 2 == 0:
            step = 3
        else:
            step = 4
    else:
        if n_temps % 2 == 0:
            step = n_temps//5
        else:
            step = n_temps//4

    # Swap numbers for blanks, and ensure start and end are present
    ticks = [ti if not it % step else '' for (it, ti) in enumerate(ticks)]
    ticks[0] = "{:.1f}".format(temperatures[0])
    ticks[-1] = "{:.1f}".format(temperatures[-1])

    return ticks
