import os
from datetime import time
from external.pinn_solver.train import train_pinn

def run_pinn_simulation(nx:int, ny:int, epochs: int, hidden_dim:int) -> dict:

    experiment_name = f"pinn_nx{nx}_ny{ny}_ep{epochs}_hd{hidden_dim}"

    checkpoint_dir = os.path.join("outputs", "checkpoints")
    figure_dir = os.path.join("outputs", "figures")

    os.makedirs(checkpoint_dir, exist_ok=True)
    os.makedirs(figure_dir, exist_ok=True)

    checkpoint_path = os.path.join(checkpoint_dir, f"{experiment_name}.pt")

    n_interior = nx*ny
    n_boundary_per_side = max(nx,ny)
    
    pinn_output = train_pinn(
        n_interior=n_interior,
        n_boundary_per_side=n_boundary_per_side,
        hidden_dim=hidden_dim,
        num_hidden_layers=4,
        learning_rate=1e-3,
        adam_epochs=epochs,
        lambda_bc=50.0,
        use_lbfgs=True,
        lbfgs_steps=500,
        checkpoint_path=checkpoint_path,
        figure_dir=figure_dir,
        experiment_name=experiment_name

    )

    result = {
        "solver": "pinn",
        "nx": nx,
        "ny": ny,
        "n_interior": n_interior,
        "n_boundary_per_side": n_boundary_per_side,
        "hidden_dim": hidden_dim,
        "adam_epochs": epochs,
        "status": "completed",
        "training_time": pinn_output["training_time"],
        "final_total_loss": pinn_output["final_total_loss"],
        "final_pde_loss": pinn_output["final_pde_loss"],
        "final_bc_loss": pinn_output["final_bc_loss"],
        "checkpoint_path": checkpoint_path,
        "figure_dir": figure_dir,
        "loss_history_length": len(pinn_output["total_loss_history"]),
        "raw_output": pinn_output
    }

    return result
