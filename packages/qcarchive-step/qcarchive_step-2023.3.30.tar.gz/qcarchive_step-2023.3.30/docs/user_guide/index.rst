.. _user-guide:

**********
User Guide
**********

The QCArchive plug-in in SEAMM provides tools for creating datasets in QCArchive, adding
structures to them, and retrieving the structures back into SEAMM.

Overview of QCArchive Datasets
==============================
A *dataset* in QCArchive is a of molecules and records that help you submit and manage a
large number of computations. A dataset is made up of entries, one per molecule,
specifications for calculations, and records containing the results. You can think of a
dataset as a table, where the *entries* are rows of the table, and *specifications*
define the columns. Each cell is a record, in the parlance of QCArchive.

Below is an example illustrating this. The records are shown by their ID. For example,
record 18263 is an HF/sto-3g computation on water, and record 23210 is an MP2/cc-pvdz
computation on ethanol. 

.. table::

  ==============  ==============  =================  =============
    Entry           HF/sto-3g      B3LYP/def2-tzvp    MP2/cc-pvdz
  ==============  ==============  =================  =============
   **water**          18263        18277              18295
   **methane**        19722        19642              19867
   **ethanol**        20212        20931              23210
  ==============  ==============  =================  =============

Preliminaries
=============

To work with QCArchive, you need to a file `~/.qca/qcportal_config.yaml` containing the
address of the QCArchive server you are using and your credentials:: 

  address: https://validation.qcarchive.molssi.org
  username: <username>
  password: <password>

where `<username>` is your user name and `<password>`, password.

Examples
========

.. toctree::
   :glob:
   :maxdepth: 2
   :titlesonly:

   *

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
