import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import numpy as np

def save_fem_solution_plot(result: dict, run_dir: str) -> str | None:

    if result.get("workflow") == "fem_single_run":
        return _save_fem_single_plot(result, run_dir)
    
    if result.get("workflow") != "fem_single_run":
        return _save_fem_comparison_plots(result, run_dir)
    
    return None
    
    

def _save_fem_single_plot(result: dict, run_dir: str) -> str | None:
    fem_result = result["results"]

    nodes = np.asarray(fem_result["nodes"])
    elements = np.asarray(fem_result["elements"])
    solution = np.asarray(fem_result["solution"])

    x = nodes[:,0]
    y = nodes[:,1]

    triang = mtri.Triangulation(x,y,elements)

    plt.figure(figsize=(7,5))
    plt.tricontour(triang, solution, shading="gouraud")
    plt.colorbar(label="Solution u")
    plt.triplot(triang, color="black", linewidth=0.15, alpha=0.3)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(
        f"FEM Solution ({fem_result['matrix_type']}, {fem_result['nx']}x{fem_result['ny']})"
    )
    plt.tight_layout()

    plot_path = os.path.join(run_dir, "solution.png")
    plt.savefig(plot_path, dpi=600)
    plt.close()

    return plot_path


def _save_fem_comparison_plots(result: dict, run_dir:str) -> str | None:
    dense = result["results"]["dense"]
    sparse = result["results"]["sparse"]

    labels = ["dense", "sparse"]
    runtimes =[dense["runtime_seconds"], sparse["runtime_seconds"]]

    plt.figure(figsize=(7,5))
    plt.bar(labels, runtimes)
    plt.xlabel("Matrix Type")
    plt.ylabel("Runtime (s)")
    plt.title("FEM Dense vs Sparse Runtime Comparison")
    plt.tight_layout()

    plot_path = os.path.join(run_dir, "comparison_runtime.png")
    plt.savefig(plot_path, dpi=600)
    plt.close()

    return plot_path