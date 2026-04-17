import time
import numpy as np
from external.fem_solver.helper import solve_problem
def run_fem_simulation(nx:int, ny:int, lx:float, ly:float, source:float, matrix_type: str) -> dict:
    if matrix_type not in {"dense", "sparse"}:
        raise ValueError(f"Unsupported FEM matrix_type: {matrix_type}")
    
    use_sparse = (matrix_type == "sparse")

    start_time = time.perf_counter()#

    nodes, elements, K, f, u = solve_problem(
        nx=nx,
        ny=ny,
        lx=1.0,
        ly=1.0,
        source=1.0,
        use_sparse=use_sparse
    )

    runtime_seconds = time.perf_counter() - start_time

    result = {
        "solver": "fem",
        "nx":nx,
        "ny":ny,
        "matrix_type": matrix_type,
        "use_sparse" : use_sparse,
        "status": "completed",
        "runtime_seconds": runtime_seconds,
        "num_elements": len(elements),
        "stiffness_shape": K.shape,
        "load_shape": f.shape,
        "solution_shape": u.shape,
        "solution_min": float(np.min(u)),
        "solution_max": float(np.max(u)),
        "solution_l2_norm": float(np.linalg.norm(u)),
        "nodes": nodes,
        "elements": elements,
        "solution": u
    }

    return result
