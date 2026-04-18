from src.config.schema import SimulationConfig
from src.runners.fem_adapter import run_fem_simulation
from src.runners.pinn_adapter import run_pinn_simulation

def run_simulation(config: SimulationConfig) -> dict:
    if config.solver == "fem":
        return _run_fem_workflow(config)
    
    if config.solver == "pinn":
        return _run_pinn_workflow(config)
    
    raise ValueError(f"Unsupported solver type: {config.solver}")

def _run_fem_workflow(config: SimulationConfig) -> dict:
    if config.compare_dense_sparse:
        dense_result = run_fem_simulation(
            nx = config.nx,
            ny = config.ny,
            lx=1.0,
            ly=1.0,
            source=1.0,
            matrix_type="dense"
        )

        sparse_result = run_fem_simulation(
            nx = config.nx,
            ny = config.ny,
            lx=1.0,
            ly=1.0,
            source=1.0,
            matrix_type="sparse"

        )
        return{
            "workflow": "fem_dense_sparse_comparison",
            "status": "completed",
            "results": {
                "dense": dense_result,
                "sparse": sparse_result
            },
            "generate_plot": config.generate_plot,
            "generate_report": config.generate_report
        }
    
    single_result = run_fem_simulation(
        nx=config.nx,
        ny=config.ny,
        lx=1.0,
        ly=1.0,
        source=1.0,
        matrix_type=config.matrix_type
    )

    return{
        "workflow": "fem_single_run",
        "status": "completed",
        "results": single_result,
        "generate_plot": config.generate_plot,
        "generate_report": config.generate_report
    }

def _run_pinn_workflow(config: SimulationConfig) -> dict:
    epochs = config.epochs if config.epochs is not None else 5000
    hidden_dim = config.hidden_dim if config.hidden_dim is not None else 64

    pinn_result=run_pinn_simulation(
        nx=config.nx,
        ny=config.ny,
        epochs=epochs,
        hidden_dim = hidden_dim
    )

    return {
        "workflow": "pinn_single_run",
        "status": "completed",
        "results": pinn_result,
        "generate_plot": config.generate_plot,
        "generate_report": config.generate_report
    }