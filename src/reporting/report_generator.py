import os
import json

def generate_markdown_report(command: str, config, result:dict, run_dir: str) -> str:

    report_path = os.path.join(run_dir, "report.md")

    lines = []

    lines.append("# Simulation report \n")
    lines.append("## User Command\n")
    lines.append(f"{command}\n")

    lines.append("'' Parsed >Configuration\n")
    lines.append("```json")
    lines.append(json.dumps(config.__dict__, indent=4))
    lines.append("```\n")

    lines.append("## Workflow Summary\n")
    lines.append(f"- Workflow: {result.get('workflow', 'unknown')}")
    lines.append(f"- Status: {result.get('status', 'unknown')}")
    lines.append(f"- Generate Plot: {result.get('generate_plot')}")
    lines.append(f"- Generate Report: {result.get('generate_report')}\n")

    lines.append("## Results\n")
    lines.extend(_format_result_section(result))
    lines.append("")

    lines.append("## Generated Artifacts\n")
    artifact_lines = _find_artifacts(run_dir)
    lines.extend(artifact_lines)
    lines.append("")

    with open(report_path, "w", encoding="utf-") as f:
        f.write("\n".join(lines))

    return report_path

def _format_result_section(result: dict) -> list[str]:
    workflow = result.get("workflow", "")

    if workflow == "fem_single_run":
        fem = result["results"]
        return[
            f"- Solver: {fem.get('solver')}",
            f"- Matrix Type: {fem.get('matrix_type')}",
            f"- Mesh: {fem.get('nx')} x {fem.get('ny')}",
            f"- Runtime (s): {fem.get('runtime_seconds'):.6f}",
            f"- Number of Nodes: {fem.get('num_nodes')}",
            f"- Number of Elements: {fem.get('num_elements')}",
            f"- Solution Min: {fem.get('solution_min')}",
            f"- Solution Max: {fem.get('solution_max')}",
            f"- Solution L2 Norm: {fem.get('solution_l2_norm')}",
        ]
    
    if workflow == "fem_dense_sparse_comparison":
        dense = result["results"]["dense"]
        sparse = result["results"]["sparse"]
        return [
            "### Dense Run",
            f"- Runtime (s): {dense.get('runtime_seconds'):.6f}",
            f"- Nodes: {dense.get('num_nodes')}",
            f"- Elements: {dense.get('num_elements')}",
            "",
            "### Sparse Run",
            f"- Runtime (s): {sparse.get('runtime_seconds'):.6f}",
            f"- Nodes: {sparse.get('num_nodes')}",
            f"- Elements: {sparse.get('num_elements')}",
        ]

    if workflow == "pinn_single_run":
        pinn = result["results"]
        return [
            f"- Solver: {pinn.get('solver')}",
            f"- Training Time (s): {pinn.get('training_time')}",
            f"- Hidden Dim: {pinn.get('hidden_dim')}",
            f"- Adam Epochs: {pinn.get('adam_epochs')}",
            f"- Final Total Loss: {pinn.get('final_total_loss')}",
            f"- Final PDE Loss: {pinn.get('final_pde_loss')}",
            f"- Final BC Loss: {pinn.get('final_bc_loss')}",
        ]

    return ["- No structured result formatting available."]

def _find_artifacts(run_dir: str) -> list[str]:
    files = sorted(os.listdir(run_dir))
    artifact_lines = []

    for name in files:
        if name in {"config.json", "results.json", "report.md"}:
            continue
        artifact_lines.append(f"- {name}")

    if not artifact_lines:
        artifact_lines.append("- No additional artifacts generated.")

    return artifact_lines



    