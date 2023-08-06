# -*- coding: utf-8 -*-
"""
Control parameters for the QCArchive step in a SEAMM flowchart
"""

import logging
import seamm
import pprint  # noqa: F401

logger = logging.getLogger(__name__)


class QCArchiveParameters(seamm.Parameters):
    """
    The control parameters for QCArchive.

    You need to replace the "time" entry in dictionary below these comments with the
    definitions of parameters to control this step. The keys are parameters for the
    current plugin,the values are dictionaries as outlined below.

    Examples
    --------
    ::

        parameters = {
            "time": {
                "default": 100.0,
                "kind": "float",
                "default_units": "ps",
                "enumeration": tuple(),
                "format_string": ".1f",
                "description": "Simulation time:",
                "help_text": ("The time to simulate in the dynamics run.")
            },
        }

    parameters : {str: {str: str}}
        A dictionary containing the parameters for the current step.
        Each key of the dictionary is a dictionary that contains the
        the following keys:

    parameters["default"] :
        The default value of the parameter, used to reset it.

    parameters["kind"] : enum()
        Specifies the kind of a variable. One of  "integer", "float", "string",
        "boolean", or "enum"

        While the "kind" of a variable might be a numeric value, it may still have
        enumerated custom values meaningful to the user. For instance, if the parameter
        is a convergence criterion for an optimizer, custom values like "normal",
        "precise", etc, might be adequate. In addition, any parameter can be set to a
        variable of expression, indicated by having "$" as the first character in the
        field. For example, $OPTIMIZER_CONV.

    parameters["default_units"] : str
        The default units, used for resetting the value.

    parameters["enumeration"] : tuple
        A tuple of enumerated values.

    parameters["format_string"] : str
        A format string for "pretty" output.

    parameters["description"] : str
        A short string used as a prompt in the GUI.

    parameters["help_text"] : str
        A longer string to display as help for the user.

    See Also
    --------
    QCArchive, TkQCArchive, QCArchive QCArchiveParameters, QCArchiveStep
    """

    parameters = {
        "operation": {
            "default": "add configuration",
            "kind": "enum",
            "default_units": "",
            "enumeration": (
                "create new dataset",
                "add configuration",
                "list entries",
                "get entries",
            ),
            "format_string": "s",
            "description": "What to do:",
            "help_text": "What to do with the dataset in QCArchive.",
        },
        "type of dataset": {
            "default": "singlepoint",
            "kind": "enum",
            "default_units": "",
            "enumeration": ("singlepoint", "optimization"),
            "format_string": "s",
            "description": "Dataset type:",
            "help_text": "The type of the dataset.",
        },
        "dataset": {
            "default": "",
            "kind": "string",
            "default_units": "",
            "enumeration": tuple(),
            "format_string": "s",
            "description": "Dataset:",
            "help_text": "The name of the dataset.",
        },
        "exist_ok": {
            "default": "yes",
            "kind": "boolean",
            "default_units": "",
            "enumeration": ("yes", "no"),
            "format_string": "s",
            "description": "Ok if already exists:",
            "help_text": "Whether it is OK if the dataset already exists.",
        },
        "description": {
            "default": "",
            "kind": "string",
            "default_units": "",
            "enumeration": tuple(),
            "format_string": "s",
            "description": "Description:",
            "help_text": "The description of the dataset.",
        },
        "tags": {
            "default": "",
            "kind": "string",
            "default_units": "",
            "enumeration": tuple(),
            "format_string": "s",
            "description": "Tags:",
            "help_text": "The tags for the new dataset, a comma separated list.",
        },
    }

    def __init__(self, defaults={}, data=None):
        """
        Initialize the parameters, by default with the parameters defined above

        Parameters
        ----------
        defaults: dict
            A dictionary of parameters to initialize. The parameters
            above are used first and any given will override/add to them.
        data: dict
            A dictionary of keys and a subdictionary with value and units
            for updating the current, default values.

        Returns
        -------
        None
        """

        logger.debug("QCArchiveParameters.__init__")

        super().__init__(
            defaults={
                **QCArchiveParameters.parameters,
                **seamm.standard_parameters.structure_handling_parameters,
                **defaults,
            },
            data=data,
        )
