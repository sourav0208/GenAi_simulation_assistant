# Simulation report 

## User Command

run a 100x100 fem simulation and compare dense vs sparse with generate report and generate plot

'' Parsed >Configuration

```json
{
    "solver": "fem",
    "nx": 100,
    "ny": 100,
    "matrix_type": "both",
    "generate_plot": true,
    "generate_report": true,
    "compare_dense_sparse": true,
    "epochs": null,
    "hidden_dim": null
}
```

## Workflow Summary

- Workflow: fem_dense_sparse_comparison
- Status: completed
- Generate Plot: True
- Generate Report: True

## Results

### Dense Run
- Runtime (s): 4.137555
- Nodes: None
- Elements: 19602

### Sparse Run
- Runtime (s): 0.693050
- Nodes: None
- Elements: 19602

## Generated Artifacts

- comparison_runtime.png
