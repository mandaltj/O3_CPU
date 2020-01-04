1) The out-of-order CPU model config file is config_scripts/O3_cpu.py . This file generates an out of order processor with various parameters that can be configured.
   Use the following command for arguments that can be passed to the O3_cpu.py:
   $../gem5/build/X86/gem5.opt config_scripts/O3_cpu.py --help

2) The 'parsec_benchmarks' directory contains the following benchmarks:
   a) blackscholes
   b) bodytrack
   c) canneal
   d) dedup 
   e) freqmine
   f) streamcluster

   The ones marked 'Error' are not working. For every other you can find their corresponding binaries and inputs in their respective directory.

3) Each of the benchmark has its specific input options. Hence, each of the benchmark has its respective shell script. Each of the script also takes in arguments 
   to be passed to O3_cpu.py. For example, to run 'blackscholes' benchmark use the following command:
   $./blackscholes 4 16 16 64 192
   All other shell scripts of other benchmarks have the same command style.

4) The shell script 'regression_job.sh' runs a specific benchmark sequentially with the provided parameters. It takes in 1 input parameters which are passed onto O3_cpu.py
   $./regression_job.sh blackscholes  <- This will run all the different configured PARAM values one after the another and dump the results only for blackscholes
   benchmark. For running a different benchmark, we can pass different name of the benchmark.	 
