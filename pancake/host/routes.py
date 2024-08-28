from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from pydantic import parse_obj_as

import time

import io
from PIL import Image

########################################################################################

from pancake.interface import Program
from pancake.compiler import PYNQCompiler
from pancake.backend import EmulatorCompiler

########################################################################################

router = APIRouter()


@router.post("/run")
async def run(request: Request, program: Program):
    pattern_generator = request.app.state.overlay.pattern_generator

    compiled_program = PYNQCompiler().visit(program)

    pattern_generator.setup(
        compiled_program,
        stimulus_group_name="control",
    )

    for i in range(len(program.circuit.instructions) * 3):
        pattern_generator.step()
        time.sleep(1 / program.clock)

    pattern_generator.stop()
    pattern_generator.reset()

    result = EmulatorCompiler().visit(program)

    return {
        "status": "success",
        "result": {
            "real": result.squeeze().real.tolist(),
            "imag": result.squeeze().imag.tolist(),
        },
    }
