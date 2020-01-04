# -*- coding: utf-8 -*-
# Copyright (c) 2015 Jason Power
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors: Tapojyoti Mandal, Sanket Aggarwal, Dhiraj Kudva

"""
TJ:
This config file is supposed to be run with X86 ISA. This is based on the
gem5/configs/learning_gem5/part1/simple.py general script.
"""
GEM5_DIR = '../gem5'

'''
TJ:
General Python Libraries
argparse - For arguments passed to this python file
'''
import os
import argparse
import sys
sys.path.append(os.path.join(GEM5_DIR, 'configs/common'))

'''
TJ:
import the m5 (gem5) library created when gem5 is built
import all of the SimObjects with '*'
Options - For using generic command line arguments. gem5/configs/common/Options.py

from Caches import * - This is needed to use L1_ICache() and L1_DCache()
'''
import m5
from m5.objects import *
from Caches import *

'''
This dictionary is just to provide an example of what are the available parameters for the O3 CPU model.
The actual values are passed through --param1 to --param5
'''
O3_config = {
	#PARAM1
	'fetchWidth'		: 4, 	#8
	'decodeWidth'		: 4, 	#8
	'renameWidth'		: 4, 	#8
	'issueWidth'		: 4, 	#8
	'dispatchWidth'		: 4, 	#8
	'wbWidth'		: 4, 	#8 #Min 2
	'commitWidth'		: 4, 	#8
	'squashWidth'		: 4, 	#8
	#PARAM2
	'LQEntries'		: 16,	#32
	#PARAM3
	'SQEntries'		: 16,	#32
	#PARAM4
	'numIQEntries'		: 64, 	#64
	#PARAM5
	'numROBEntries'		: 192,	#192

}
#branchPred
#numPhysVecRegs

#LSQDepCheckShift = 0
#decodeToRenameDelay = 2
#renameToIEWDelay = 1
'''
================================================================================
Reading Command Line arguments for Python file and passing to 'process'
================================================================================
'''
parser = argparse.ArgumentParser(description='Config script for CPU model')
parser.add_argument('--exe', help='path to the executable' )
parser.add_argument('--options', default='', help='options to be passed to executable')
parser.add_argument('--clock', type=str, help='Clock Frequency in GHz')
parser.add_argument('--cpu_type', type=int, help='1 = TimingSimpleCPU; 2 = MinorCPU; 3 = O3 CPU;')
parser.add_argument('--param1', type=int, help='Check O3_cpu.py file for param1')
parser.add_argument('--param2', type=int, help='Check O3_cpu.py file for param2')
parser.add_argument('--param3', type=int, help='Check O3_cpu.py file for param3')
parser.add_argument('--param4', type=int, help='Check O3_cpu.py file for param4')
parser.add_argument('--param5', type=int, help='Check O3_cpu.py file for param5')

#parser.add_argument('--max_inst', type=int, default= , help='Use 1000000 for 1 Million Instruction Max')
args = parser.parse_args()

#print("Argument length:" + str(len(sys.argv)))
#print("Arguments:" + str(args))


"""
================================================================================
create the system we are going to simulate
================================================================================
"""
system = System()

# Set the clock fequency of the system (and all of its children)
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = args.clock+'GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# Set up the system
system.mem_mode = 'timing'                # Use timing accesses
system.mem_ranges = [AddrRange('8192MB')] # Create an address range


"""
================================================================================
                              CPU Configuration Code
================================================================================
args.cpu_type=1	TimingSimpleCPU
args.cpu_type=2	MinorCPU
args.cpu_type=3	DerivO3CPU

Adding I-Cache and D-Cache for CPU
Addign Interrupt Controller required for X86
"""
if args.cpu_type==1:
	system.cpu = TimingSimpleCPU()
elif args.cpu_type==2:
	system.cpu = MinorCPU()
elif args.cpu_type==3:
	system.cpu = DerivO3CPU()

# Adding ICache and DCache
icache = L1_ICache(size='32kB', assoc=1)
dcache = L1_DCache(size='256kB', assoc=4)
system.cpu.addPrivateSplitL1Caches(icache, dcache, None, None)
system.cpu.createInterruptController()

system.cpu.fetchWidth = args.param1
system.cpu.decodeWidth = args.param1
system.cpu.renameWidth = args.param1
system.cpu.issueWidth = args.param1
system.cpu.dispatchWidth = args.param1
system.cpu.wbWidth = args.param1
system.cpu.commitWidth = args.param1
system.cpu.squashWidth = args.param1

system.cpu.LQEntries = args.param2
system.cpu.SQEntries = args.param3

system.cpu.numIQEntries = args.param4
system.cpu.numROBEntries = args.param5

"""
================================================================================
							DDR Memory Config
================================================================================
"""
# Create a DDR3 memory controller and connect it to the membus
# tj: This is to create a main_memory. Check gem5/src/mem/DRAMCtrl.py
system.mem_ctrl = DDR3_1600_8x8()
system.mem_ctrl.range = system.mem_ranges[0]

"""
================================================================================
							Memory Bus
================================================================================
"""
# Create a memory bus, a coherent crossbar, in this case
system.membus = SystemXBar()

# Connect the System Port to the Memory Bus. Not Sure why this is needed!
system.system_port = system.membus.slave

# Connect all ports of CPU(system.cpu) to Memory Bus
system.cpu.connectAllPorts(system.membus)

# Connect the DRAM to the Memory Bus
system.mem_ctrl.port = system.membus.master

"""
================================================================================
					Process creation and Workload Assign
================================================================================
"""# Create a process for a simple "Hello World" application
process = Process()
# Set the command
# cmd is a list which begins with the executable (like argv)
if args.options!="":
	process.cmd = [args.exe] + args.options.split()
	#print("Check 0:{}".format(process.cmd))
else:
	process.cmd = [args.exe]
	#print("Check 1:{}".format(process.cmd))

# Set the cpu to use the process as its workload and create thread contexts
system.cpu.workload = process
system.cpu.createThreads()

# set up the root SimObject and start the simulation
root = Root(full_system = False, system = system)
# instantiate all of the objects we've created above
m5.instantiate()

print ("Beginning simulation!")
exit_event = m5.simulate()
print ('Exiting @ tick {} because {}'
        .format(m5.curTick(), exit_event.getCause()))
