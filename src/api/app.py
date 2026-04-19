from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.parsing.ollama_parser import parse_simulation_command_llm
from src.runners.simulation_runner import run_simulation
from src.reporting.result_logger import save_run, _make_json_safe
from src.reporting.plot_generator import save_fem_solution_plot
from src.reporting.report_generator import generate_markdown_report
from src.api.response_formatter import format_api_response

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

        print("WORKFLOW =", result.get("workflow"))
        print("RESULT KEYS =", result.keys())
        print("RESULTS KEYS =", result.get("results", {}).keys() if isinstance(result.get("results"), dict) else type(result.get("results")))

        if config.generate_plot:
            plot_path = save_fem_solution_plot(result, run_dir)
            plot_generated = plot_path is not None

        if config.generate_report:
            report_path = generate_markdown_report(command, config, result, run_dir)
            report_generated = report_path is not None

        response = format_api_response(
           config=config,
           result=result,
           run_dir=run_dir
        )
        return response
    
    except Exception as e:
        print("API ERROR:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))