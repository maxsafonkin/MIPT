import re
import uvicorn
from enum import StrEnum

from pydantic import BaseModel, StrictStr, StrictFloat
from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse


def _create_response(data: dict, status_code: int, success: bool) -> JSONResponse:
    payload = {"success": success, "data": data}
    return JSONResponse(content=payload, status_code=status_code)


"""Task 1"""

task1_router = APIRouter(prefix="/task1")


class SimpleOperations(StrEnum):
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"


_OPERATION_HANDLER = {
    SimpleOperations.ADD: lambda x, y: x + y,
    SimpleOperations.SUBTRACT: lambda x, y: x - y,
    SimpleOperations.MULTIPLY: lambda x, y: x * y,
    SimpleOperations.DIVIDE: lambda x, y: x / y,
}


@task1_router.post("/{operation}")
def execute_simple_operation(
    operation: SimpleOperations, operand_1: float, operand_2: float
) -> JSONResponse:
    try:
        operation_result = _OPERATION_HANDLER[operation](operand_1, operand_2)
        data = {"result": operation_result}
        return _create_response(data=data, status_code=200, success=True)
    except ZeroDivisionError:
        error_data = {"message": "Zero division error"}
        return _create_response(data=error_data, status_code=400, success=False)
    except Exception as exc:
        error_data = {"message": str(exc)}
        return _create_response(data=error_data, status_code=500, success=False)


"""Task 2"""

task2_router = APIRouter(prefix="/task2")


class Operand(BaseModel):
    name: StrictStr
    value: StrictFloat


ALLOWED_PATTERN = re.compile(r"^[A-Za-z0-9+\-*/().,\s ]+$")


def execute(operation: str, operands: list[Operand]) -> float:
    # P.S. i hope the developer will fix this vulnerable method

    if not ALLOWED_PATTERN.fullmatch(operation):
        raise ValueError("Invalid characters in expression")

    operands_dict = {o.name: o.value for o in operands}
    return eval(operation, {"__builtins__": None}, operands_dict)


@task2_router.post("/execute")
def execute_operation(operation: str, operands: list[Operand]) -> JSONResponse:
    try:
        execution_result = execute(operation=operation, operands=operands)
        data = {"result": execution_result}
        return _create_response(data=data, status_code=200, success=True)
    except Exception as exc:
        error_data = {"message": str(exc)}
        return _create_response(data=error_data, status_code=500, success=False)


def main():
    app = FastAPI()
    app.include_router(task1_router)
    app.include_router(task2_router)

    uvicorn.run(app=app, port=9876)


if __name__ == "__main__":
    main()
