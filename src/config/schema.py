from dataclasses import dataclass
from typing import Optional

@dataclass
class SimulationConfig:
    solver: str = "fem"
    nx: int = 20
    ny: int = 20
    matrix_type: str = "sparse"
    generate_plot: bool = True
    generate_report: bool = True
    compare_dense_sparse: bool = False
    epochs: Optional[int] = None
    hidden_dim: Optional[int] = None