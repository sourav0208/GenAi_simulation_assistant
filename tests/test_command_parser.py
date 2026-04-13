from src.parsing.command_parser import parse_simulation_command

def test_basic_fem():
    cmd = "run a 50x50 fem simulation"
    config = parse_simulation_command(cmd)

    assert config.solver == "fem"
    assert config.nx == 50
    assert config.ny == 50
