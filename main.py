import sys
sys.path.append(rf"C:\SOURAV\GenAi_simulation_assistant\src")
from src.parsing.command_parser import parse_simulation_command
from src.runners.simulation_runner import run_simulation
from src.parsing.ollama_parser import parse_simulation_command_llm
from src.reporting.result_logger import save_run
from src.reporting.plot_generator import save_fem_solution_plot

def main():
    command = input("Enter simulation command:")
    config = parse_simulation_command_llm(command)
    print("\nParsed configuration:")
    print(config)

    results = run_simulation(config=config)
    save_run(config, results)
    print("\n Simulation results:")
    print(results)

    run_dir = save_run(config, results)

    if config.generate_plot:
        plot_path = save_fem_solution_plot(results, run_dir)
        if plot_path is not None:
            print(f"Plot saved to: {plot_path}")

if __name__ == "__main__":
    main()