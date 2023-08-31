# std imports
from pathlib import Path
import re
import subprocess
import sys
import timeit
from typing import List

# 3rd party modules
import plotly.graph_objects as pgo

FASTA_FILE_PATH: Path = Path('./target_decoy.fasta')
SPEC_FILE_PATH: Path = Path('./specs.mzML')

PARAMS_TEMPLATE_PATH: Path = Path('./comet.params')
COMET_BIN_PATH: Path = Path('./comet.linux.exe')
NUM_RESULTS: List[int] = [1, 5, 10, 100, 1000, 10000, 20000, 100000, 336860]
NUM_RESULT_REGEX: re.Pattern = re.compile(r"num_results = \d+")
NUM_OUTPUT_LINE_REGEX: re.Pattern = re.compile(r"num_output_lines = \d+")


def create_params_file(new_num_results: int) -> Path:
    """Creates new params file with adjusted num_results and num_output_lines
    Parameters
    ----------
    new_num_results : int
        Number of results

    Returns
    -------
    Path
        Path to new params file
    """
    with PARAMS_TEMPLATE_PATH.open("r") as f:
        content = f.read()
        content = NUM_RESULT_REGEX.sub(f"num_results = {new_num_results}", content)
        content = NUM_OUTPUT_LINE_REGEX.sub(f"num_output_lines = {new_num_results}", content)
    new_params_file_path: Path = PARAMS_TEMPLATE_PATH.parent.joinpath(f"comet.params.{new_num_results}")
    with new_params_file_path.open("w") as f:
        f.write(content)

    return new_params_file_path

def run_comet(params_file_path: Path, num_results: int):
    subproc = subprocess.Popen(
        [
            f"./{COMET_BIN_PATH}",
            f"-P{params_file_path}",
            f"-D{FASTA_FILE_PATH}",
            f"-Nidents.{num_results}",
            str(SPEC_FILE_PATH)
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    _ = subproc.communicate()


def main():
    timings: List[float] = []
    for num_res in NUM_RESULTS:
        print(f"######> num_results: {num_res}")
        params_file_path = create_params_file(num_res)
        timing = timeit.timeit(lambda: run_comet(params_file_path, num_res), number=1)
        timings.append(timing)
        print(timing, 's')
    fig = pgo.Figure()
    fig.add_trace(pgo.Bar(
        x=[str(i) for i in NUM_RESULTS], # convert num_results to string to the axis is not scaling
        y=timings,
        marker_color='blue'
    ))
    fig.update_layout(
        title='Comet execution time for various `num_results` & `num_output_lines`',
        xaxis_title='`num_results` & `num_output_lines`',
        yaxis_title='Seconds'

    )
    fig.write_image('execution-times.png')
    if len(sys.argv) > 1 and sys.argv[1] == 'browser':
        fig.show()

if __name__ == '__main__':
    main()
