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

# Project Structure

``` text
GenAi_simulation_assistant/
│
├── src/
│   ├── api/
│   ├── parsing/
│   ├── runners/
│   ├── reporting/
│   └── config/
    └── utils/
│
├── outputs/
│   ├── runs/
│   ├── checkpoints/
│   └── figures/
│
├── Dockerfile
├── requirements.txt
├── README.md
└── .github/
    └── workflows/
        └── ci.yml
│
├── render.yaml
```

------------------------------------------------------------------------

## Deployment

This project is deployed as a live cloud service using automated
Continuous Integration (CI) and Continuous Deployment (CD).

Every push to the `main` branch:

-   runs automated checks
-   builds a Docker image
-   deploys the service to the cloud

------------------------------------------------------------------------

## Live Cloud Demo

Base URL:

https://genai-simulation-assistant.onrender.com

Interactive API documentation:

https://genai-simulation-assistant.onrender.com/docs

Example request:

``` bash
curl -X POST https://genai-simulation-assistant.onrender.com/run-simulation -H "Content-Type: application/json" -d '{
  "command": "run a fem simulation with 20x20"
}'
```

------------------------------------------------------------------------

## Continuous Integration (CI)

This project uses GitHub Actions to automatically validate the codebase.

The CI pipeline performs:

-   dependency installation
-   Python syntax checks
-   linting
-   Docker image build verification

------------------------------------------------------------------------

## Continuous Deployment (CD)

Deployment workflow:

Developer Push\
↓\
GitHub Actions\
↓\
Docker Build\
↓\
Render Cloud Deployment\
↓\
Live API Service

------------------------------------------------------------------------

## Docker Containerization

The entire system runs inside a Docker container.

Benefits:

-   consistent runtime environment
-   reproducible builds
-   platform independence
-   simplified deployment

------------------------------------------------------------------------

## System Architecture

User\
↓\
HTTP Request\
↓\
FastAPI Service\
↓\
Command Parser\
↓\
Simulation Runner\
↓\
FEM / PINN Solver\
↓\
Results + Artifacts

------------------------------------------------------------------------

## Cloud Infrastructure

This service is deployed using:

-   Render cloud platform
-   Docker container runtime
-   GitHub-based deployment automation

------------------------------------------------------------------------

## Result Storage

Simulation results are generated dynamically during execution.

Typical output directory:

outputs/runs/`<timestamp>`{=html}/

Artifacts may include:

-   report.md
-   plots
-   figures
-   logs
-   model checkpoints

Note:

The public deployment uses a temporary filesystem.\
Large experiments should be executed locally for persistent storage.

------------------------------------------------------------------------

## API Usage

Primary endpoint:

POST /run-simulation

Example request:

{ "command": "run a pinn simulation with 20x20 and generate report" }

Example response:

{ "status": "completed", "run_dir": "outputs/runs/`<timestamp>`{=html}"
}

------------------------------------------------------------------------

## Performance Considerations

Recommended limits for cloud execution:

-   grid size ≤ 20x20\
-   epochs ≤ 500\
-   hidden_dim ≤ 32

For large simulations:

Run locally using Docker.

------------------------------------------------------------------------

## Testing and Validation

The system includes automated validation through:

-   CI pipeline checks
-   numerical verification
-   FEM reference comparison
-   reproducible simulation runs

------------------------------------------------------------------------
