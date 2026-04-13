import re
from src.config.schema import SimulationConfig

def parse_simulation_command(command: str) -> SimulationConfig:

    text = command.lower().strip()

    config = SimulationConfig()

    if "pinn" in text:
        config.solver = "pinn"
    elif "fem" in text:
        config.solver = "fem"

    mesh_match = re.search(r'(\d+)\s*x\s*(\d+)', text)
    if mesh_match:
        config.nx = int(mesh_match.group(1))
        config.ny = int(mesh_match.group(2))

    if " dense vs sparse" in text or "compare dense vs sparse" in text:
        config.compare_dense_sparse = True
        config.matrix_type = "both"
    elif "dense" in text:
        config.matrix_type = "dense"
    elif "sparse" in text:
        config.matrix_type = "sparse"

    if "no plot" in text or "without plot" in text:
        config.generate_plot = False
    elif "report" in text:
        config.generate_report = True

    epochs_match = re.search(r'epochs?\s*(=|to)?\s*(\d+)', text)
    if epochs_match:
        config.epochs = int(epochs_match.group(2))

    hidden_dim_match = re.search(r'hidden[_\s-]?dim\s*(=|to)?\s*(\d+)', text)
    if hidden_dim_match:
        config.hidden_dim = int(hidden_dim_match.group(2))

    validate_config(config)

    return config

def validate_config(config: SimulationConfig) -> None:

    if config.solver not in {"fem", "pinn"}:
        raise ValueError(f"Unsupported solver: {config.solver}")
    
    if config.nx <=0 or config.ny <=0:
        raise ValueError("mesh dimension nx and ny must be positive integerts.")
    
    if config.matrix_type not in {"dense", "sparse", "both"}:
        raise ValueError(f"invalid matrix_type: {config.matrix_type}")
    
    if config.solver == "pinn":
        if config.compare_dense_sparse:
            raise ValueError("Dense/sparse matrix comparision is only valid for FEM worlflows.")