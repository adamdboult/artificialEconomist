#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import subprocess
#print("This is python talking")
#sys.stdout.flush()


question = sys.argv[1]
#print(question)
os.chdir("./gpt-2")
#os.system("./src/generate_unconditional_samples.py --nsamples 1")
#os.system("./src/interactive_conditional_samples_AB.py --raw_text 'Example'")

result = subprocess.run(["./src/interactive_conditional_samples_AB.py", "--raw_text", question], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#print("Output:")
#decoded = result.decode("UTF-8")
#cleanResult = str(result.stdout)
#print(cleanResult)
#print(type(cleanResult))
#print(type(result.stdout))
print(result.stdout.decode("utf8"))
sys.stdout.flush()
sys.exit()
#print("Error:")

#print(result.stderr)

