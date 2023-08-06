# -*- coding: utf-8 -*-

"""The graphical part of a QCArchive step"""

import logging
import tkinter as tk

from qcportal import PortalClient

import qcarchive_step  # noqa: F401
import seamm
from seamm_util import ureg, Q_, units_class  # noqa: F401
import seamm_widgets as sw

logger = logging.getLogger(__name__)


class TkQCArchive(seamm.TkNode):
    """
    The graphical part of a QCArchive step in a flowchart.

    Attributes
    ----------
    tk_flowchart : TkFlowchart = None
        The flowchart that we belong to.
    node : Node = None
        The corresponding node of the non-graphical flowchart
    namespace : str
        The namespace of the current step.
    tk_subflowchart : TkFlowchart
        A graphical Flowchart representing a subflowchart
    canvas: tkCanvas = None
        The Tk Canvas to draw on
    dialog : Dialog
        The Pmw dialog object
    x : int = None
        The x-coordinate of the center of the picture of the node
    y : int = None
        The y-coordinate of the center of the picture of the node
    w : int = 200
        The width in pixels of the picture of the node
    h : int = 50
        The height in pixels of the picture of the node
    self[widget] : dict
        A dictionary of tk widgets built using the information
        contained in QCArchive_parameters.py

    See Also
    --------
    QCArchive, TkQCArchive,
    QCArchiveParameters,
    """

    def __init__(
        self,
        tk_flowchart=None,
        node=None,
        canvas=None,
        x=None,
        y=None,
        w=200,
        h=50,
    ):
        """
        Initialize a graphical node.

        Parameters
        ----------
        tk_flowchart: Tk_Flowchart
            The graphical flowchart that we are in.
        node: Node
            The non-graphical node for this step.
        namespace: str
            The stevedore namespace for finding sub-nodes.
        canvas: Canvas
           The Tk canvas to draw on.
        x: float
            The x position of the nodes center on the canvas.
        y: float
            The y position of the nodes cetner on the canvas.
        w: float
            The nodes graphical width, in pixels.
        h: float
            The nodes graphical height, in pixels.

        Returns
        -------
        None
        """
        self.dialog = None

        self._qc_client = None
        self.have_client = None

        super().__init__(
            tk_flowchart=tk_flowchart,
            node=node,
            canvas=canvas,
            x=x,
            y=y,
            w=w,
            h=h,
        )

    @property
    def qc_client(self):
        """The Portal client."""
        if self.have_client is not None and self.have_client:
            return self._qc_client

        if self._qc_client is None:
            try:
                self._qc_client = PortalClient.from_file()
            except Exception as e:
                logger.warning(f"Error {e} attaching to QCArchive.")
                self.have_client = False
            else:
                self.have_client = True
        return self._qc_client

    def create_dialog(self):
        """
        Create the dialog. A set of widgets will be chosen by default
        based on what is specified in the QCArchive_parameters
        module.

        Parameters
        ----------
        None

        Returns
        -------
        None

        See Also
        --------
        TkQCArchive.reset_dialog
        """

        frame = super().create_dialog(title="QCArchive")
        # Shortcut for parameters
        P = self.node.parameters

        # Then create the widgets
        for key in P:
            self[key] = P[key].widget(frame)

        # And bindings to be responsive to changes
        for key in ("operation", "type of dataset"):
            self[key].bind("<<ComboboxSelected>>", self.reset_dialog)
            self[key].combobox.bind("<Return>", self.reset_dialog)
            self[key].combobox.bind("<FocusOut>", self.reset_dialog)

        # and lay them out
        self.reset_dialog()

    def reset_dialog(self, widget=None):
        """Layout the widgets in the dialog.

        Parameters
        ----------
        widget : Tk Widget = None

        Returns
        -------
        None

        See Also
        --------
        TkQCArchive.create_dialog
        """

        operation = self["operation"].get()
        dataset_type = self["type of dataset"].get()

        # Remove all the current widgets
        frame = self["frame"]
        for slave in frame.grid_slaves():
            slave.grid_forget()

        # Reconstruct based on current parameters
        widgets = []
        row = 0
        key = "operation"
        self[key].grid(row=row, column=0, sticky=tk.EW)
        widgets.append(self[key])
        row += 1

        if operation == "create new dataset":
            for key in (
                "type of dataset",
                "dataset",
                "description",
                "tags",
                "exist_ok",
            ):
                self[key].grid(row=row, column=0, sticky=tk.EW)
                widgets.append(self[key])
                row += 1
        elif operation == "add configuration":
            for key in ("type of dataset", "dataset"):
                self[key].grid(row=row, column=0, sticky=tk.EW)
                widgets.append(self[key])
                row += 1
        elif operation == "list entries":
            for key in ("type of dataset", "dataset"):
                self[key].grid(row=row, column=0, sticky=tk.EW)
                widgets.append(self[key])
                row += 1
        elif operation == "get entries":
            for key in (
                "type of dataset",
                "dataset",
                "structure handling",
                "subsequent structure handling",
            ):
                self[key].grid(row=row, column=0, sticky=tk.EW)
                widgets.append(self[key])
                row += 1

        sw.align_labels(widgets, sticky=tk.E)

        if operation == "create new dataset":
            datasets = []
        else:
            client = self.qc_client
            if client is not None:
                datasets = []
                for d in client.list_datasets():
                    if d["dataset_type"] == dataset_type:
                        datasets.append(d["dataset_name"])
                        self["dataset"].config(values=datasets)

    def right_click(self, event):
        """
        Handles the right click event on the node.

        Parameters
        ----------
        event : Tk Event

        Returns
        -------
        None

        See Also
        --------
        TkQCArchive.edit
        """

        super().right_click(event)
        self.popup_menu.add_command(label="Edit..", command=self.edit)

        self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
