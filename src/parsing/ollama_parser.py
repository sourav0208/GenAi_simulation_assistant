import os
import json
import requests

from src.config.schema import SimulationConfig
from src.parsing.command_parser import parse_simulation_command
from src.parsing.command_parser import validate_config


OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")

MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")

def apply_default_values(config):


    if config.generate_plot is None:
        config.generate_plot = True

    if config.generate_report is None:
        config.generate_report = True

    if config.matrix_type is None:
        config.matrix_type = "sparse"

    if config.compare_dense_sparse is None:
        config.compare_dense_sparse = False

    return config

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

Important interpretation rules:
- "no plot", "without plot", "do not generate plot" , "no generation plot", "nothing plotting" => generate_plot = false
- "no report", "without report", "do not generate report", "no generation report", "nothing reporting" => generate_report = false
- If the user does not explicitly disable plot, generate_plot must remain true
- If the user does not explicitly disable report, generate_report must remain true
- "dense" means matrix_type = "dense"
- "sparse" means matrix_type = "sparse"
- "compare dense and sparse" means compare_dense_sparse = true and matrix_type = "both"
- matrix_type must be exactly one of: "dense", "sparse" , "both"
- Never resturn values like: -"dense or sparse", "either dense or sparse"
- for PINN, use "sparse" unless the user explicitly asks for dense/sparse comparison.

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
        print("LLM raw parsed JSON:", parsed)
        parsed = sanitize_llm_output(parsed)
        print("parsed JSON after sanitise_llm_output:", parsed)

        config = SimulationConfig(**parsed)
        config = apply_command_overrides(command, config)
        print("config after override:", config)


        validate_config(config=config)

        return config
    
    except Exception as e:
        print("Ollama pasring failed - using fallback parser")
        print(e)

        return parse_simulation_command(command)
    
def normalize_command_text(command: str) -> str:
    cmd = command.lower()

    replacements = {
        "don't": "do not",
        "dont": "do not",
        "would not like": "do not",
        "i don't like": "do not",
        "i do not want": "do not",
        "please don't": "do not",
        "without": "no",
        "skip": "no",
        "disable": "no",
        "nad": "and",
        "dont": "do not",
        "don't": "do not",
        "omit": "skip",
        "disable": "skip",
    }

    for key, value in replacements.items():
        cmd = cmd.replace(key, value)

    return cmd
    

def apply_command_overrides(command: str, config: SimulationConfig) -> SimulationConfig:

    cmd = command.lower()
    cmd = normalize_command_text(cmd)

    # REPORT
    if "report" in cmd:
        if (
            "skip report" in cmd
            or "no report" in cmd
            or "without report" in cmd
            or "without generate report" in cmd
        ):
            config.generate_report = False
        elif (
            "generate report" in cmd
            or "do not skip report" in cmd
        ):
            config.generate_report = True

    # PLOT
    if "plot" in cmd:
        if (
            "skip plot" in cmd
            or "no plot" in cmd
            or "without plot" in cmd
            or "without generate plot" in cmd
        ):
            config.generate_plot = False
        elif (
            "generate plot" in cmd
            or "do not skip plot" in cmd
        ):
            config.generate_plot = True


    return config

def sanitize_llm_output(parsed: dict) -> dict:
    valid_matrix_types = {"dense", "sparse", "both"}

    matrix_type = parsed.get("matrix_type")

    if matrix_type not in valid_matrix_types:
        
        parsed["matrix_type"] = "sparse"

    if "generate_plot" not in parsed:
        parsed["generate_plot"] = True

    if "generate_report" not in parsed:
        parsed["generate_report"] = True

    if "compare_dense_sparse" not in parsed:
        parsed["compare_dense_sparse"] = False

    if "epochs" not in parsed:
        parsed["epochs"] = None

    if "hidden_dim" not in parsed:
        parsed["hidden_dim"] = None
        

    return parsed
  