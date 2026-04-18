# Simulation report 

## User Command

run fem of 60x60 and compare dense vs sparse and generate report and generate plot

'' Parsed >Configuration

```json
{
    "solver": "fem",
    "nx": 60,
    "ny": 60,
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
- Runtime (s): 0.853422
- Nodes: None
- Elements: 6962

### Sparse Run
- Runtime (s): 0.375843
- Nodes: None
- Elements: 6962

## Generated Artifacts

- comparison_runtime.png
