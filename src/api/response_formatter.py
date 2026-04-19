import os

def format_api_response(config, result, run_dir):

    workflow = result.get("Workflow")
    status = result.get("status")

    summary = _build_summary(result)

    artifacts = _find_artifacts(run_dir)

    return{
        "workflow": workflow,
        "status": status,
        "run_dir": run_dir,
        "summary": summary,
        "artifacts": artifacts,
        "config": {
            "solver": config.solver,
            "nx": config.nx,
            "ny": config.ny,
            "matrix_type": config.matrix_type,
        },
    }

def _build_summary(result):

    workflow = result.get("workflow")

    if workflow == "fem_single_run":

        r = result["results"]

        return {
            "runtime_seconds": r.get("runtime_seconds"),
            "num_nodes": r.get("num_nodes"),
            "num_elements": r.get("num_elements"),
            "solution_min": r.get("solution_min"),
            "solution_max": r.get("solution_max"),
        }

    if workflow == "fem_dense_sparse_comparison":

        dense = result["results"]["dense"]
        sparse = result["results"]["sparse"]

        speedup = (
            dense["runtime_seconds"]
            / sparse["runtime_seconds"]
            if sparse["runtime_seconds"] > 0
            else None
        )

        return {
            "dense_runtime_seconds": dense["runtime_seconds"],
            "sparse_runtime_seconds": sparse["runtime_seconds"],
            "speedup": speedup,
        }

    if workflow == "pinn_single_run":

        r = result["results"]

        return {
            "training_time": r.get("training_time"),
            "final_total_loss": r.get("final_total_loss"),
            "final_pde_loss": r.get("final_pde_loss"),
            "final_bc_loss": r.get("final_bc_loss"),
        }

    return {}


def _find_artifacts(run_dir):

    files = os.listdir(run_dir)

    return {
        "report": "report.md" if "report.md" in files else None,
        "plot": _find_plot(files),
    }


def _find_plot(files):

    for f in files:

        if f.endswith(".png"):
            return f

    return None