# Copyright 2014 BitPay, Inc.
# Distributed under the MIT/X11 software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import subprocess
import os
import json
import sys

def bctest(testDir, testObj, exeext):

	execprog = testObj['exec'] + exeext
	execargs = testObj['args']
	execrun = [execprog] + execargs
	stdinCfg = None
	inputData = None
	if "input" in testObj:
		filename = f"{testDir}/" + testObj['input']
		inputData = open(filename).read()
		stdinCfg = subprocess.PIPE

	outputFn = None
	outputData = None
	if "output_cmp" in testObj:
		outputFn = testObj['output_cmp']
		outputData = open(f"{testDir}/{outputFn}").read()
	proc = subprocess.Popen(execrun, stdin=stdinCfg, stdout=subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True)
	try:
		outs = proc.communicate(input=inputData)
	except OSError:
		print(f"OSError, Failed to execute {execprog}")
		sys.exit(1)

	if outputData and (outs[0] != outputData):
		print(f"Output data mismatch for {outputFn}")
		sys.exit(1)

	wantRC = testObj['return_code'] if "return_code" in testObj else 0
	if proc.returncode != wantRC:
		print(f"Return code mismatch for {outputFn}")
		sys.exit(1)

def bctester(testDir, input_basename, buildenv):
	input_filename = f"{testDir}/{input_basename}"
	raw_data = open(input_filename).read()
	input_data = json.loads(raw_data)

	for testObj in input_data:
		bctest(testDir, testObj, buildenv.exeext)

	sys.exit(0)

