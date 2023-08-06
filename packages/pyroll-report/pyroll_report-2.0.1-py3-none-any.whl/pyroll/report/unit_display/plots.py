from pathlib import Path

import jinja2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from pyroll.core import Unit, PassSequence, RollPass, Profile
from .. import utils
from pyroll.report.pluggy import hookimpl, plugin_manager

_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(Path(__file__).parent, encoding="utf-8")
)

_template = _env.get_template("plots.html")


@hookimpl(specname="unit_display")
def unit_plots_display(unit: Unit):
    plots = [
        utils.get_svg_from_figure(p) if isinstance(p, Figure) else p
        for p in plugin_manager.hook.unit_plot(unit=unit)
    ]

    return _template.render(plots=plots)


@hookimpl(specname="unit_plot")
def roll_forces_plot(unit: Unit):
    if isinstance(unit, PassSequence):
        fig, ax = utils.create_sequence_plot(unit)
        ax.set_ylabel(r"roll force $F$")
        ax.set_title("Roll Forces")

        units = list(unit)
        if len(units) > 0:
            indices, forces = np.transpose(
                [
                    (index, unit.roll_force)
                    for index, unit in enumerate(units)
                    if isinstance(unit, RollPass)
                ]
            )

            ax.bar(x=indices, height=forces, width=0.8)

            return fig


@hookimpl(specname="unit_plot")
def roll_torques_plot(unit: Unit):
    if isinstance(unit, PassSequence):
        fig, ax = utils.create_sequence_plot(unit)
        ax.set_ylabel(r"roll torque $M$")
        ax.set_title("Roll Torques")

        units = list(unit)
        if len(units) > 0:
            x, y = np.transpose(
                [
                    (index, unit.roll.roll_torque)
                    for index, unit in enumerate(units)
                    if isinstance(unit, RollPass)
                ]
            )

            ax.bar(x=x, height=y, width=0.8)

            return fig


@hookimpl(specname="unit_plot")
def strains_plot(unit: Unit):
    if isinstance(unit, PassSequence):
        fig, ax = utils.create_sequence_plot(unit)
        ax.set_ylabel(r"strain $\varphi_\mathrm{V}$")
        ax.set_title("Mean Equivalent Strains")

        units = list(unit)
        if len(units) > 0:
            def gen_seq():
                yield -0.5, units[0].in_profile.strain
                for i, u in enumerate(units):
                    yield i + 0.5, u.out_profile.strain

            x, y = np.transpose(
                list(gen_seq())
            )

            ax.plot(x, y, marker="x")

            return fig


@hookimpl(specname="unit_plot")
def filling_ratios_plot(unit: Unit):
    if isinstance(unit, PassSequence):
        fig, ax = utils.create_sequence_plot(unit)
        ax.set_ylabel(r"filling ratio $i$")
        ax.set_title("Filling Ratios")

        units = list(unit)
        if len(units) > 0:
            x, y = np.transpose(
                [
                    (index, unit.out_profile.filling_ratio)
                    for index, unit in enumerate(units)
                    if isinstance(unit, RollPass)
                ]
            )

            ax.bar(x=x, height=y, width=0.8)

            return fig


@hookimpl(specname="unit_plot")
def cross_sections_plot(unit: Unit):
    if isinstance(unit, PassSequence):
        fig, ax = utils.create_sequence_plot(unit)
        ax.set_ylabel(r"cross section $A_\mathrm{p}$")
        ax.set_title("Profile Cross-Sections")

        units = list(unit)
        if len(units) > 0:
            def gen_seq():
                yield -0.5, units[0].in_profile.cross_section.area
                for i, u in enumerate(units):
                    yield i + 0.5, u.out_profile.cross_section.area

            x, y = np.transpose(
                list(gen_seq())
            )

            ax.plot(x, y, marker="x")

            return fig


@hookimpl(specname="unit_plot")
def roll_pass_plot(unit):
    """Plot roll pass contour and its profiles"""

    if isinstance(unit, RollPass):
        fig: plt.Figure = plt.figure(constrained_layout=True, figsize=(4, 4))
        ax: plt.Axes
        axl: plt.Axes
        ax, axl = fig.subplots(nrows=2, height_ratios=[1, 0.3])
        ax.set_title("In- and Outcoming Profiles")

        ax.set_aspect("equal", "datalim")
        ax.grid(lw=0.5)

        for cl in unit.contour_lines:
            c = ax.plot(*cl.xy, color="k", label="roll surface")

        ipp = ax.fill(*unit.in_profile.cross_section.boundary.xy, alpha=0.5, color="red", label="in profile")
        opp = ax.fill(*unit.out_profile.cross_section.boundary.xy, alpha=0.5, color="blue", label="out profile")

        ipr = ax.fill(*unit.in_profile.equivalent_rectangle.boundary.xy, fill=False, color="red", ls="--",
                      label="in eq. rectangle")
        opr = ax.fill(*unit.out_profile.equivalent_rectangle.boundary.xy, fill=False, color="blue", ls="--",
                      label="out eq. rectangle")

        axl.axis("off")
        axl.legend(handles=c + ipp + opp + ipr + opr, ncols=2, loc="lower center")
        fig.set_constrained_layout(True)

        return fig
