# Simulation report 

## User Command

run a pinn simulation on 40x40 with generate report and generate plot

'' Parsed >Configuration

```json
{
    "solver": "pinn",
    "nx": 40,
    "ny": 40,
    "matrix_type": "sparse",
    "generate_plot": true,
    "generate_report": true,
    "compare_dense_sparse": false,
    "epochs": null,
    "hidden_dim": null
}
```

## Workflow Summary

- Workflow: pinn_single_run
- Status: completed
- Generate Plot: True
- Generate Report: True

## Results

- Solver: pinn
- Training Time (s): 110.2371597290039
- Hidden Dim: 64
- Adam Epochs: 5000
- Final Total Loss: 6.25702814431861e-05
- Final PDE Loss: 4.761765467264922e-06
- Final BC Loss: 1.156170242211374e-06

## Generated Artifacts

- No additional artifacts generated.
