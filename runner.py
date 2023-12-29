import subprocess
from time import sleep

PYTHON_PATH = "/home/jamie/projects/shimmer/shimmer/bin/python"
SHIMMER_PATH = "/home/jamie/projects/shimmer/shimmer.py"

def main():
    result = subprocess.run(
        "ps aux | grep warner",
        stdout=subprocess.PIPE,
        shell=True,
    )
    output = result.stdout.decode("utf-8")
    if "python" not in output:
        warner = subprocess.run(
            f"nohup {PYTHON_PATH} {SHIMMER_PATH} &",
            shell=True,
        )
    sleep(5 * 60)

if __name__ == "__main__":
    while True:
        main()
