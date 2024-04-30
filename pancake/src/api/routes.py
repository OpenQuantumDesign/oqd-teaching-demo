import os

import io

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

import json

from matplotlib import pyplot as plt
import matplotlib

########################################################################################

from pancake.interface import Program
from pancake.visualization import draw_circuit

########################################################################################

PYNQ_FASTAPI_ENDPOINT = os.environ["PYNQ_FASTAPI_ENDPOINT"]

########################################################################################

router = APIRouter()

########################################################################################


@router.post("/run")
async def run(request: Request, program: Program):
    response = await request.app.state.async_client.request(
        "POST", PYNQ_FASTAPI_ENDPOINT + "/api/pynq/run", data=program.json()
    )
    return json.loads(response.content)


@router.post("/visualize")
async def run(request: Request, program: Program):
    plt.style.use("dark_background")

    matplotlib.rcParams["figure.figsize"] = (12, 8)
    matplotlib.rcParams["font.size"] = 20
    matplotlib.rcParams["text.usetex"] = True
    matplotlib.rcParams["mathtext.fontset"] = "stix"
    matplotlib.rcParams["font.family"] = "STIXGeneral"

    fig = draw_circuit(circuit=program.circuit)

    buf = io.BytesIO()
    fig.savefig(buf, format="svg", bbox_inches="tight", transparent=True)
    buf.seek(0)

    plt.close(fig)

    return StreamingResponse(buf, media_type="image/svg+xml")
