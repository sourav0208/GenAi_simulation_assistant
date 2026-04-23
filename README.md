# GenAI Simulation Assistant for FEM and PINN Workflows

This project implements a **GenAI-powered simulation assistant** that
allows users to run engineering simulations using natural language
commands.

------------------------------------------------------------------------

# Motivation

Engineering simulations are often executed through repetitive scripts
and manual configuration. This project demonstrates how **Generative
AI** can automate simulation workflows while maintaining numerical
correctness and reproducibility.

------------------------------------------------------------------------

# System Overview

User Command → LLM Parser → Simulation Runner → FEM / PINN Solver → Plot
/ Report → Stored Results

------------------------------------------------------------------------

# Example Commands

``` text
run a 50x50 fem simulation
run a 60x60 fem simulation and compare dense vs sparse
execute a pinn simulation on 40x40 with epochs=4000 and hidden_dim=64
simulate a fem with 50x50 and generate plot and report.
```

------------------------------------------------------------------------

# Example Outputs

## FEM Solution

![FEM Solution](outputs\figures\solution.png)

## Runtime Comparison

![Runtime Comparison](outputs\figures\comparison_runtime.png)

## PINN Loss History

![PINN Loss](outputs/figures/loss_history.png)

------------------------------------------------------------------------
