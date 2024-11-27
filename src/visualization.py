#  Copyright 2024 OPEN QUANTUM DESIGN
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from matplotlib import pyplot as plt
from matplotlib.ticker import AutoMinorLocator

import seaborn as sns

import numpy as np

########################################################################################

from src import Circuit
from src import PYNQCompiler

########################################################################################


def _prepare_wave(wave):
    _t = range(len(wave) + 1)
    t = []
    for j in range(len(_t) - 1):
        t.extend([_t[j], _t[j + 1]])
    t = np.array(t)

    wave = list(wave)

    state_map = {"l": 0, "h": 1}

    new_wave = []
    for state in wave:
        if state == ".":
            new_wave.extend([new_wave[-1], new_wave[-1]])
        else:
            new_wave.extend([state_map[state], state_map[state]])
    new_wave = np.array(new_wave)
    return t, new_wave


def draw_circuit(*, circuit: Circuit = None, compiled_circuit=None):
    if not (circuit is None or compiled_circuit is None):
        raise ValueError(
            "Inconsistency: circuit and compiled_circuit cannot be used simultaneously"
        )

    if circuit:
        compiled_circuit = PYNQCompiler().visit(circuit)

    fig = plt.figure(figsize=(16, 8))
    ax = fig.subplots(1, 1)

    T = len(compiled_circuit["signal"][0][1]["wave"])
    Nch = len(compiled_circuit["signal"][0]) - 1

    for i in range(Nch):
        t, wave = _prepare_wave(compiled_circuit["signal"][0][i + 1]["wave"])

        ax.plot(
            t,
            (Nch - i - 1) * 1.5 + wave,
            color=sns.color_palette("muted", n_colors=10, desat=0.8)[3],
        )

        ax.text(
            0,
            (Nch - i - 1) * 1.5 + 0.5,
            rf"ch{i}",
            ha="right",
            va="center",
        )

    ax.spines[["right", "left", "top", "bottom"]].set_visible(False)
    ax.set_xlim(0, T)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.xaxis.grid(True, which="major", ls="--")
    ax.xaxis.grid(True, which="minor", ls=":")
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position("top")
    ax.set_ylim(-0.1, (Nch - 1) * 1.5 + 1.1)
    ax.set_yticks([])

    return fig
