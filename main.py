import sys
sys.path.append(rf"C:\SOURAV\GenAi_simulation_assistant\src")
from src.parsing.command_parser import parse_simulation_command
from src.runners.simulation_runner import run_simulation
from src.parsing.ollama_parser import parse_simulation_command_llm

def main():
    command = input("Enter simulation command:")
    config = parse_simulation_command_llm(command)
    print("\nParsed configuration:")
    print(config)

    results = run_simulation(config=config)
    print("\n Simulation results:")
    print(results)

if __name__ == "__main__":
    main()