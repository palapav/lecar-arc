# Cache Comparison: ARC vs LeCaR

This repository contains a Python program (`run.py`) for evaluating the performance of two caching algorithms: ARC and LeCaR. This README provides instructions on how to run the program and interpret the results.

## Prerequisites

Make sure you have the following prerequisites installed on your system:

- Python 3.x
- A working virtual enviornment (see [here](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/)).
- Required Python libraries (install them using `pip install -r requirements.txt`)

## Usage

To run the program, use the following command:

```bash
python run.py <cache_capacity> <trace_file>
```

- <cache_capacity>: Integer representing the capacity of the cache.
- <trace_file>: The name of the trace file containing the request data.

## Example

```bash
python run.py 1000 my_trace_file.txt
```

Replace 1000 with your desired cache capacity and my_trace_file.txt with the actual trace file. If you would like to use one of our created trace files, for example, use the following instead of my my_trace_file.txt: traces/syn_workload1.txt

## Results

The program supports two caching algorithms: ARC and LeCaR. Both algorithms will be evaluated, and the results (hits, requests, hit ratio) will be displayed. Detailed evaluation results are presented in the evals folder. Code for these evaluations are presented outside of this folder (generate_eval_csv.py, phase_changes.py, syn_workload.py, etc.).

