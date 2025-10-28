from typing import List

def execute(commands: List[str] | None):
    """Simulated safe executor. Replace later with real runner (SSM/K8s/etc.)."""
    outputs = []
    for cmd in commands or []:
        outputs.append(f"SIMULATED: {cmd}")
    return outputs
