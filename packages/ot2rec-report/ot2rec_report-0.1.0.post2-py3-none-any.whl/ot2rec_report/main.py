import argparse
import json
import logging
import os
import subprocess
from copy import deepcopy as dc
from enum import Enum, auto
from glob import glob

import nbformat
import papermill as pm
from icecream import ic
from magicgui import magicgui as mg

from ot2rec_report import utils
from ot2rec_report.templates import *
import pkg_resources

logging.basicConfig(level=logging.INFO)


def write_nb(nb_data, nb_path):
    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(nb_data, f)


class Choices(Enum):
    none = auto()
    workflow_diagram = auto()
    motioncor2 = auto()
    warp = auto()
    ctffind = auto()
    ctfsim = auto()
    exclude_bad_tilts = auto()
    imod_align = auto()
    imod_recon = auto()
    aretomo_align = auto()
    aretomo_recon = auto()
    savu_recon = auto()
    rlf_deconv = auto()


@mg(
    call_button="Create Ot2Rec Report",
    layout="vertical",
    result_widget=False,
    project_name={
        "label": "Project name*",
    },
    processes={
        "label": "Sections to include in report*",
        "tooltip": "Hold Ctrl to select several",
        "widget_type": "Select",
        "choices": Choices,
    },
    notes={"label": "Notes to add to report", "widget_type": "TextEdit"},
    to_html={
        "label": "Export to html",
    },
    to_slides={"label": "Export to Jupyter slides"},
)
def get_args_o2r_report(
    project_name="",
    processes=Choices.none,
    notes="",
    to_html=False,
    to_slides=False,
):
    return locals()


def read_ipynb(filename):
    fn = pkg_resources.resource_filename("ot2rec_report.templates", filename)

    with open(fn, "r") as f:
        return json.load(f)


def main(args=None):
    lookup_dict = {
        "workflow_diagram": read_ipynb("workflow_diagram.ipynb"),
        "motioncor2": read_ipynb("report_mc.ipynb"),
        "warp": read_ipynb("report_warp.ipynb"),
        "ctffind": read_ipynb("report_ctffind.ipynb"),
        "ctfsim": read_ipynb("report_ctfsim.ipynb"),
        "exclude_bad_tilts": read_ipynb("report_excludebadtilts.ipynb"),
        "imod_header": read_ipynb("report_imod_header.ipynb"),
        "imod_align": read_ipynb("report_imod_align.ipynb"),
        "imod_recon": read_ipynb("report_imod_recon.ipynb"),
        "aretomo_header": read_ipynb("report_aretomo_header.ipynb"),
        "aretomo_align": read_ipynb("report_aretomo_align.ipynb"),
        "aretomo_recon": read_ipynb("report_aretomo_recon.ipynb"),
        "savu_recon": read_ipynb("report_savu_recon.ipynb"),
        "rlf_deconv": read_ipynb("report_rlf_deconv.ipynb"),
    }

    if args is None:
        args = get_args_o2r_report.show(run=True)

    final_nb = dc(read_ipynb("report_main.ipynb"))
    node_list = [i.name for i in args.processes.value]

    # Check if AreTomo has been used
    at_list = list(i for i, s in enumerate(node_list) if "aretomo" in s)
    at_used = len(at_list) > 0
    if at_used:
        at_first_idx = at_list[0]

    # Add in cells to final notebook
    for idx, curr_proc in enumerate(node_list):
        if curr_proc == "imod_align":
            final_nb["cells"] += lookup_dict["imod_header"]["cells"]
        elif at_used and idx == at_first_idx:
            final_nb["cells"] += lookup_dict["aretomo_header"]["cells"]
        final_nb["cells"] += lookup_dict[curr_proc]["cells"]
        logging.info(f"Added {curr_proc}.")

    # Write out template notebook
    write_nb(final_nb, "./report_temp.ipynb")

    # Use papermill to populate empty notebook
    params = dict(
        proj_name=args.project_name.value,
        node_list=node_list,
        notes=args.notes.value,
    )

    pm.execute_notebook(
        "./report_temp.ipynb",
        "./report.ipynb",
        parameters=params,
    )

    logging.info("Report notebook created.")

    # Export HTML
    if args.to_html.value is True:
        cmd = [
            "jupyter-nbconvert",
            "--to",
            "html",
            "--TemplateExporter.exclude_input=True",
            "./report.ipynb",
        ]

        exp = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="ascii",
            check=True,
        )

        try:
            assert not exp.stderr
        except:
            print(exp.stderr)

    # Export slides
    if args.to_slides.value is True:
        cmd = [
            "jupyter-nbconvert",
            "./report.ipynb",
            "--to",
            "slides",
            "--TemplateExporter.exclude_input=True",
            "--SlidesExporter.reveal_theme=simple",
            "--SlidesExporter.reveal_scroll=True",
        ]

        exp = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="ascii",
            check=True,
        )

        try:
            assert not exp.stderr
        except:
            print(exp.stderr)
