import json
import requests

from src.config.schema import SimulationConfig
from src.parsing.command_parser import parse_simulation_command
from src.parsing.command_parser import validate_config

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL = "qwen2.5:3b"

def parse_simulation_command_llm(command: str) -> SimulationConfig:

    prompt = f""" 
You are a simulation command parser.

Return ONLY valid JSON.

Schema:
{{
"solver": "fem or pinn",
"nx": integer,
"ny": integer,
"matrix_type": "dense or sparse or both",
"generate_plot": true or false,
"compare_dense_sparse": true or false,
"epochs": integer or null,
"hidden_dim": integer or null
}}

Defaults:

solver = "fem"
nx = 20
ny = 20
matrix_type = "sparse"
generate_plot = true
generate_report = true
compare_dense_sparse = false
epochs = null
hidden_dim = null

User command:
{command}

Return JSON only
"""
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        text = response.json()["response"].strip()

        parsed = json.loads(text)

        config = SimulationConfig(**parsed)

        validate_config(config=config)

        return config
    
    except Exception as e:
        print("Ollama pasring failed - using fallback parser")
        print(e)

        return parse_simulation_command(command)