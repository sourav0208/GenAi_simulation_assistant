from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.parsing.ollama_parser import parse_simulation_command_llm
from src.runners.simulation_runner import run_simulation
from src.reporting.result_logger import save_run, _make_json_safe
from src.reporting.plot_generator import save_fem_solution_plot
from src.reporting.report_generator import generate_markdown_report

class SimulationRequest(BaseModel):
    command: str

class SimulationResponse(BaseModel):
    workflow: str
    status: str
    run_dir: str
    parsed_config: dict
    result: dict
    plot_generated: bool
    report_generated: bool

@asynccontextmanager
async def lifespan(app: FastAPI):

    yield

app = FastAPI(
    title="GenAI Simulation Assistant",
    version="0.1.0",
    lifespan= lifespan
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/run-simulation")
def run_simulation_endpoint(payload: SimulationRequest):
    try:
        command = payload.command
        config = parse_simulation_command_llm(command)
        result = run_simulation(config)

        run_dir = save_run(config, result)

        plot_generated = False
        report_generated = False

        if config.generate_plot:
            plot_path = save_fem_solution_plot(result, run_dir)
            plot_generated = plot_path is not None

        if config.generate_report:
            report_path = generate_markdown_report(command, config, result, run_dir)
            report_generated = report_path is not None

        safe_result = _make_json_safe(result)
        safe_config = _make_json_safe(config.__dict__)

        return SimulationResponse(
            workflow= result.get("workflow", "unknown"),
            status = result.get("status", "unknow"),
            run_dir= str(Path(run_dir)),
            parsed_config= safe_config,
            result=safe_result,
            plot_generated=plot_generated,
            report_generated=report_generated

        )
    
    except Exception as e:
        print("API ERROR:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))