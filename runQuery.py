import sys
import os
import subprocess

id_and_question = sys.argv[1]
result = subprocess.run(
    ["wget", "-qO-", "artificialeconomist_tensorflow:8008/" + id_and_question],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)
print(result)
print(result.stdout.decode("utf8"))
sys.stdout.flush()
sys.exit()
