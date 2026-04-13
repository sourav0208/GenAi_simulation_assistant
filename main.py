from src.parsing.command_parser import parse_simulation_command

def main():
    command = input("Enter simulation command:")
    config = parse_simulation_command(command)
    print("\nParsed configuration:")
    print(config)

if __name__ == "__main__":
    main()