import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent

def build_callstring(max_time: float):
    result = "dump_reachable_search_space("
    if max_time is not None:
        result += f"max_time={max_time}"
    result +=  ")"
    return result

def generate_state_space(domain: str, problem: str, max_time: str = None):
    command = [
        "python3",
        Path(HERE / 'scorpion/fast-downward.py').resolve(),
        "--keep-sas-file",
        Path(domain).resolve(),
        Path(problem).resolve(),
        "--translate-options",
        "--dump-static-predicates",
        "--dump-predicates",
        "--dump-constants",
        "--dump-static-atoms",
        "--dump-goal-atoms",
        "--search-options",
        "--search",
        build_callstring(max_time)]
    print(f'Executing "{" ".join(map(str, command))}"')
    with open("run.log", "w") as file:
        subprocess.run(command, stdout=file,text=True)
