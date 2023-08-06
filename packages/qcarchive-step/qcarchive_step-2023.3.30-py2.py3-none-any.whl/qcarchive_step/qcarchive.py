# -*- coding: utf-8 -*-

"""Non-graphical part of the QCArchive step in a SEAMM flowchart
"""

import logging
from pathlib import Path
import pkg_resources

from qcportal import PortalClient
from qcportal.molecules import Molecule

import qcarchive_step
import molsystem
import seamm
from seamm_util import ureg, Q_  # noqa: F401
import seamm_util.printing as printing
from seamm_util.printing import FormattedText as __

# In addition to the normal logger, two logger-like printing facilities are
# defined: "job" and "printer". "job" send output to the main job.out file for
# the job, and should be used very sparingly, typically to echo what this step
# will do in the initial summary of the job.
#
# "printer" sends output to the file "step.out" in this steps working
# directory, and is used for all normal output from this step.

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter("QCArchive")

# Add this module's properties to the standard properties
path = Path(pkg_resources.resource_filename(__name__, "data/"))
csv_file = path / "properties.csv"
if path.exists():
    molsystem.add_properties_from_file(csv_file)


class QCArchive(seamm.Node):
    """
    The non-graphical part of a QCArchive step in a flowchart.

    Attributes
    ----------
    parser : configargparse.ArgParser
        The parser object.

    options : tuple
        It contains a two item tuple containing the populated namespace and the
        list of remaining argument strings.

    subflowchart : seamm.Flowchart
        A SEAMM Flowchart object that represents a subflowchart, if needed.

    parameters : QCArchiveParameters
        The control parameters for QCArchive.

    See Also
    --------
    TkQCArchive,
    QCArchive, QCArchiveParameters
    """

    def __init__(
        self, flowchart=None, title="QCArchive", extension=None, logger=logger
    ):
        """A step for QCArchive in a SEAMM flowchart.

        You may wish to change the title above, which is the string displayed
        in the box representing the step in the flowchart.

        Parameters
        ----------
        flowchart: seamm.Flowchart
            The non-graphical flowchart that contains this step.

        title: str
            The name displayed in the flowchart.
        extension: None
            Not yet implemented
        logger : Logger = logger
            The logger to use and pass to parent classes

        Returns
        -------
        None
        """
        logger.debug(f"Creating QCArchive {self}")

        super().__init__(
            flowchart=flowchart,
            title=title,
            extension=extension,
            logger=logger,
        )  # yapf: disable

        self._metadata = qcarchive_step.metadata
        self.parameters = qcarchive_step.QCArchiveParameters()
        self._qc_client = None
        self._dataset = None

    @property
    def version(self):
        """The semantic version of this module."""
        return qcarchive_step.__version__

    @property
    def git_revision(self):
        """The git version of this module."""
        return qcarchive_step.__git_revision__

    @property
    def qc_client(self):
        """The Portal client."""
        if self._qc_client is None:
            try:
                self._qc_client = PortalClient.from_file()
            except Exception as e:
                raise RuntimeError(f"Error {e} attaching to QCArchive.")
        return self._qc_client

    @property
    def dataset(self):
        """The dataset in QCArchive."""
        if self._dataset is None:
            P = self.parameters.current_values_to_dict(
                context=seamm.flowchart_variables._data
            )
            operation = P["operation"]
            ds_type = P["type of dataset"]
            dataset = P["dataset"]

            datasets = []
            for d in self.qc_client.list_datasets():
                if d["dataset_type"] == ds_type:
                    datasets.append(d["dataset_name"])

            if operation == "add configuration" and dataset not in datasets:
                self._dataset = self.qc_client.add_dataset(
                    ds_type,
                    name=dataset,
                    description="created by SEAMM",
                    default_tag="basis",
                )
            else:
                try:
                    self._dataset = self.qc_client.get_dataset(
                        ds_type, dataset_name=dataset
                    )
                except Exception as e:
                    raise RuntimeError(f"Error {e} getting dataset {dataset}.")
        return self._dataset

    def datasets(self, _type="all"):
        """The current datasets in QCArchive."""
        datasets = []
        if _type == "all":
            for d in self.qc_client.list_datasets():
                datasets.append((d["dataset_name"], d["dataset_type"]))
        else:
            for d in self.qc_client.list_datasets():
                if d["dataset_type"] == _type:
                    datasets.append(d["dataset_name"])

        return datasets

    def description_text(self, P=None):
        """Create the text description of what this step will do.
        The dictionary of control values is passed in as P so that
        the code can test values, etc.

        Parameters
        ----------
        P: dict
            An optional dictionary of the current values of the control
            parameters.
        Returns
        -------
        str
            A description of the current step.
        """
        if not P:
            P = self.parameters.values_to_dict()

        operation = P["operation"]
        if operation == "create new dataset":
            text = (
                f"Will create a new {P['type of dataset']}  dataset {P['dataset']} "
                f"in the {self.qc_client.server_name}"
            )
            if P["exist_ok"] == "yes":
                text += ", if it does not already exist."
            else:
                text += "."
        elif operation == "add configuration":
            text = (
                f"Will add the current configuration to the {P['type of dataset']} "
                f"dataset {P['dataset']} in the {self.qc_client.server_name}."
            )
        elif operation == "list entries":
            text = (
                f"Will list the entries in the {P['type of dataset']} "
                f"dataset {P['dataset']} in the {self.qc_client.server_name}."
            )
        elif operation == "get entries":
            text = (
                f"Will get the entries from the {P['type of dataset']} "
                f"dataset {P['dataset']} in the {self.qc_client.server_name}, "
                "creating a new system and configuration for each."
            )
        else:
            raise RuntimeError(f"Don't recognize the requested operation '{operation}'")
        return self.header + "\n" + __(text, **P, indent=4 * " ").__str__()

    def run(self):
        """Run a QCArchive step.

        Parameters
        ----------
        None

        Returns
        -------
        seamm.Node
            The next node object in the flowchart.
        """
        next_node = super().run(printer)
        # Get the values of the parameters, dereferencing any variables
        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )

        # Print what we are doing
        printer.important(__(self.description_text(P), indent=self.indent))

        # directory = Path(self.directory)
        # directory.mkdir(parents=True, exist_ok=True)

        operation = P["operation"]
        if operation == "create new dataset":
            datasets = self.datasets(P["type of dataset"])
            if P["dataset"] not in datasets:
                tags = [t.strip() for t in P["tags"].split(",")]
                self.qc_client.add_dataset(
                    P["type of dataset"],
                    name=P["dataset"],
                    description=P["description"],
                    tags=tags,
                )
                text = f"Created {P['type of dataset']} dataset {P['dataset']}."
                printer.important(__(text, indent=self.indent))
            elif P["exist_ok"]:
                text = (
                    f"The {P['type of dataset']} dataset {P['dataset']} already "
                    "existed, so not creating it again."
                )
                printer.important(__(text, indent=self.indent))
            else:
                raise RuntimeError(
                    f"The {P['type of dataset']} dataset {P['dataset']} exists already."
                )
        elif operation == "add configuration":
            # Get the current system and configuration
            system, configuration = self.get_system_configuration(None)

            qcschema = configuration.to_qcschema_dict()
            if "fragments" in qcschema:
                del qcschema["fragments"]
            molecule = Molecule(**qcschema)
            entry_name = f"{system.name}/{configuration.name}"
            self.dataset.add_entry(name=entry_name, molecule=molecule)
            text = f"Added {entry_name} to the dataset."
            printer.important(__(text, indent=self.indent))
        elif operation == "list entries":
            # for entry in self.dataset.iterate_entries():
            #     print(entry)
            entry_names = self.dataset.entry_names
            text = (
                f"There are {len(entry_names)} entries in the {P['type of dataset']} "
                f"dataset {P['dataset']}:\n"
            )
            for entry in entry_names:
                text += f"\t{entry}\n"
            printer.important(__(text, indent=self.indent, dedent=False, wrap=False))
        elif operation == "get entries":
            system_db = self.get_variable("_system_db")
            system, configuration = self.get_system_configuration(
                P, structure_handling=True
            )
            subsequent_as_configurations = (
                P["subsequent structure handling"] == "Create a new configuration"
            )
            first = True
            for entry in self.dataset.iterate_entries():
                json_data = entry.molecule.json()
                if first:
                    first = False
                else:
                    if subsequent_as_configurations:
                        configuration = system.create_configuration()
                    else:
                        system = system_db.create_system()
                        configuration = system.create_configuration()
                configuration.from_qcschema_json(json_data)
                if "/" in entry.molecule.name:
                    sysname, confname = entry.molecule.name.split("/", 1)
                    system.name = sysname.strip()
                    configuration.name = confname.strip()
                else:
                    system.name = entry.molecule.name.strip()
                    configuration.name = configuration.canonical_smiles

        # Add other citations here or in the appropriate place in the code.
        # Add the bibtex to data/references.bib, and add a self.reference.cite
        # similar to the above to actually add the citation to the references.

        return next_node
