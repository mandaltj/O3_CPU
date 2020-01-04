#!/usr/bin/env python2

import argparse
import os
import re

# Note: These are 100% made up! Seriously, don't believe this for real systems
size_constants = {
    'fetchWidth': lambda c: 1*c['fetchWidth'],
    'decodeWidth': lambda c: 3*c['decodeWidth']**1.5,
    'renameWidth': lambda c: 3*c['renameWidth']**2,
    'issueWidth': lambda c: .5*c['issueWidth']**2.5,
    'dispatchWidth': lambda c: 1*c['dispatchWidth'],
    'wbWidth': lambda c: 1*c['wbWidth'],
    'commitWidth': lambda c: 1*c['commitWidth']**1.5,
    'squashWidth': lambda c: 1*c['squashWidth'],

    'fetchBufferSize': lambda c: 0.5*c['fetchBufferSize'],

    'numIQEntries': lambda c: 0.5*c['numIQEntries'],
    'numROBEntries': lambda c: 0.05*c['numROBEntries']*c['issueWidth']**2,

    'LQEntries': lambda c: 0.5*c['LQEntries'],
    'SQEntries': lambda c: 0.5*c['SQEntries'],

    'numSimpleIntUnits': lambda c: 1*c['fuPool']['FUList'][0]['count'],
    'numComplexIntUnits': lambda c: 2*c['fuPool']['FUList'][1]['count'],
    'numFPUnits': lambda c: 5*c['fuPool']['FUList'][4]['count'],
    'numLoadUnits': lambda c: 1*c['fuPool']['FUList'][2]['count'],
    'numStoreUnits': lambda c: 1*c['fuPool']['FUList'][3]['count'],
}

fpu_insts = [
    'system.cpu.iq.FU_type_0::FloatAdd',
    'system.cpu.iq.FU_type_0::FloatCmp',
    'system.cpu.iq.FU_type_0::FloatCvt',
    'system.cpu.iq.FU_type_0::FloatMult',
    'system.cpu.iq.FU_type_0::FloatMultAcc',
    'system.cpu.iq.FU_type_0::FloatDiv',
    'system.cpu.iq.FU_type_0::FloatMisc',
    'system.cpu.iq.FU_type_0::FloatSqrt',
    'system.cpu.iq.FU_type_0::SimdAdd',
    'system.cpu.iq.FU_type_0::SimdAddAcc',
    'system.cpu.iq.FU_type_0::SimdAlu',
    'system.cpu.iq.FU_type_0::SimdCmp',
    'system.cpu.iq.FU_type_0::SimdCvt',
    'system.cpu.iq.FU_type_0::SimdMisc',
    'system.cpu.iq.FU_type_0::SimdMult',
    'system.cpu.iq.FU_type_0::SimdMultAcc',
    'system.cpu.iq.FU_type_0::SimdShift',
    'system.cpu.iq.FU_type_0::SimdShiftAcc',
    'system.cpu.iq.FU_type_0::SimdSqrt',
    'system.cpu.iq.FU_type_0::SimdFloatAdd',
    'system.cpu.iq.FU_type_0::SimdFloatAlu',
    'system.cpu.iq.FU_type_0::SimdFloatCmp',
    'system.cpu.iq.FU_type_0::SimdFloatCvt',
    'system.cpu.iq.FU_type_0::SimdFloatDiv',
    'system.cpu.iq.FU_type_0::SimdFloatMisc',
    'system.cpu.iq.FU_type_0::SimdFloatMult',
    'system.cpu.iq.FU_type_0::SimdFloatMultAcc',
    'system.cpu.iq.FU_type_0::SimdFloatSqrt',
]

# Note: These are 100% made up! Seriously, don't believe this for real systems
energy_constants = {
    'fetch': lambda c, s:
                10 * get_stat(s, 'system.cpu.fetch.CacheLines'),
    'decode': lambda c, s:
        size_constants['decodeWidth'](c) *
                1 * get_stat(s, 'system.cpu.decode.DecodedInsts'),
    'rename': lambda c, s:
        size_constants['renameWidth'](c) *
                0.5 * get_stat(s, 'system.cpu.rename.RenameLookups'),
    'issue': lambda c, s:
        size_constants['issueWidth'](c) * 1e-6 *
                0.1 * get_stat(s, 'system.cpu.iq.iqInstsAdded') *
                0.1 * get_stat(s, 'system.cpu.iq.iqInstsIssued'),
    's_int': lambda c, s:
                10 * get_stat(s, 'system.cpu.iq.FU_type_0::IntAlu '),
    'c_int': lambda c, s:
                20 * (get_stat(s, 'system.cpu.iq.FU_type_0::IntMult') +
                     get_stat(s, 'system.cpu.iq.FU_type_0::IntDiv')),
    'fpu': lambda c, s:
                50 * sum([get_stat(s, _) for _ in fpu_insts]),
    'mem': lambda c, s:
                5 * (get_stat(s, 'system.cpu.iq.FU_type_0::MemRead') +
                     get_stat(s, 'system.cpu.iq.FU_type_0::MemWrite')),
    'commit': lambda c, s:
        size_constants['commitWidth'](c) *
                0.5 * get_stat(s, 'system.cpu.commit.committedOps'),
    'rob': lambda c, s:
        size_constants['numROBEntries'](c) *
                0.02 * (get_stat(s, 'system.cpu.rob.rob_reads') +
                        get_stat(s, 'system.cpu.rob.rob_writes')),
    'regs': lambda c, s:
                20 * (get_stat(s, 'system.cpu.int_regfile_reads') +
                     get_stat(s, 'system.cpu.int_regfile_writes')) +
                30 * (get_stat(s, 'system.cpu.vec_regfile_reads') +
                      get_stat(s, 'system.cpu.vec_regfile_writes'))
}

def get_stat(stats, name):
    i = stats.find('Begin')
    i = stats.find('Begin', i+1) # Go to second dump
    i = stats.find(name, i) # find the stat
    # get the second thing in the line (ignore the repeated spaces)
    s = [_ for _ in stats[i+1:stats.find('\n', i)].split(' ') if _][1]

    return float(s)

def read_stats(outdir):
    with open(os.path.join(outdir, 'stats.txt')) as f:
        return f.read()

def read_config(outdir):
    import json
    with open(os.path.join(outdir, 'config.json')) as f:
        return json.load(f)

def calc_time(outdir):
    stats = read_stats(outdir)
    return get_stat(stats, 'sim_ticks')/1000 # in nanoseconds

def calc_size(outdir):
    config = read_config(outdir)
    cpu = read_config(args.outdir)['system']['cpu'][0]

    size = 0
    for key,func in size_constants.iteritems():
        size += func(cpu)

    return (50 + size/10)/10

def calc_dynamic_energy(outdir):
    config = read_config(outdir)
    stats = read_stats(outdir)
    cpu = read_config(args.outdir)['system']['cpu'][0]

    energy = 0
    for key,func in energy_constants.iteritems():
        energy += func(cpu, stats)

    return energy**0.8/1e9

disclaimer = """This is provided as an exercise only.
These are not realistic numbers. I literally made all of this up.
"""

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("outdir", help="The gem5 out directory to parse")
    args = parser.parse_args()

    print disclaimer

    time = calc_time(args.outdir)
    print "Your application took %0.0f ns" % (time)

    size = calc_size(args.outdir)
    print "Your core is %f mm^2" % (size)

    static_power = size**0.9 * 0.5

    dynamic_energy = calc_dynamic_energy(args.outdir)
    print "Your core consumed %f J" % \
        (dynamic_energy + static_power * time / 1e9)

    print "Your core dissipated %f Watts" % \
        (static_power + dynamic_energy/(time/1e9))
