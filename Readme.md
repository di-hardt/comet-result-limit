# Comet result limit

According to [Comet's](https://uwpr.github.io/Comet/) documentation [`num_output_lines`](https://uwpr.github.io/Comet/parameters/parameters_202301/num_output_lines.html) and [`num_results`](https://uwpr.github.io/Comet/parameters/parameters_202301/num_results.html) are limitted to 100 PSMs. While the value of this parmeter is not validated and can be set higher, it has a significant impact on Comet's execution time. The sole purpose of this repository is to show this for an increasing number in a nice plot.

# Install

### Need Python, pip and setuptools?
```
conda env create -f environment.yml
conda activate comet_result_limit
```

### Python stuff is already installed
pip install .

## Usage
```
python time_comet.py
```
will execute Comet a couple of times, measure the execution time, put the identifications in this folder, and plots the execution times in `./executions-time.png`.

```
python time_comet.py browser
```
will open the plot also in the default internet browser.
