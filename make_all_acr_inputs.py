import subprocess as sp
from typing import List, Tuple
projects: List[Tuple[str, int]] = [
    # ("Express", 27),
    # ("Shields", 4),
    # ("Bower", 3),
    # ("Hexo", 12),
    # ("Karma", 22),
    # ("Hessian.js", 9),
    ("Eslint", 333),
    # ("Node-redis", 7),
    # ("Pencilblue", 7),
    # ("Mongoose", 29),
]

if __name__ == "__main__":
    for project, num_bugs in projects:
        for i in range(117, 204):
            checkout_cmd = ["python3", "acr_input.py", "-p", project, "-b", str(i)]
            result = sp.run(checkout_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error running command: {checkout_cmd}")
                print(f"Error output: {result.stderr}")
            else:
                print(f"Successfully ran command: {checkout_cmd}")