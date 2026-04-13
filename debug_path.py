import sys, os
print("Current dir:", os.getcwd())
print("\nSys path:")
for p in sys.path:
    print(" ", p)

# Try the import manually
try:
    from src.parsing.command_parser import parse_simulation_command
    print("\n✅ Import works!")
except ImportError as e:
    print(f"\n❌ Import failed: {e}")