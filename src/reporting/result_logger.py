import json
import os
from datetime import datetime

def save_run(config, result):

    timestamp= datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    run_dir = os.path.join(
        "outputs",
        "runs",
        timestamp
    )

    os.makedirs(run_dir, exist_ok=True)

    config_path = os.path.join(run_dir, "config.json")
    result_path = os.path.join(run_dir, "results.json")

    with open(config_path, "w") as f:
        json.dump(_make_json_safe(result), f, indent=4)

    with open(result_path, "w") as f:
        json.dump(_make_json_safe(result), f, indent=4)

    print(f"\nRun saved to : {run_dir}")

    return run_dir

def _make_json_safe(obj):

    if isinstance(obj, dict):
        return{
            k: _make_json_safe(v)
            for k, v in obj.items()
        }
    
    if isinstance(obj, list):
        return[
            _make_json_safe(v)
            for v in obj
        ]
    
    try:
        json.dumps(obj)
        return obj
    
    except TypeError:
        return str(obj)
