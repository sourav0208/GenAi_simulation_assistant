# Simulation report 

## User Command

run a 40x40 fem simulation and compare dense vs sparse without generate plot and generate report

'' Parsed >Configuration

```json
{
    "solver": "fem",
    "nx": 40,
    "ny": 40,
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
- Runtime (s): 0.156456
- Nodes: None
- Elements: 3042

### Sparse Run
- Runtime (s): 0.133484
- Nodes: None
- Elements: 3042

## Generated Artifacts

- comparison_runtime.png
