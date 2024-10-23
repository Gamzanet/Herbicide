# with open("out.sample",'r') as f:
#     content = f.read()
#     traces_start = content.find('Traces:')
#     traces_end = content.find('\n\n', traces_start)
#     traces = content[traces_start:traces_end]
#     print(traces)

import re
with open('out.sample', 'r') as file:
    content = file.read()
    traces = re.findall(r'Traces:\n(.*?)(?=\n\n|\Z)', content, re.DOTALL)
    s = re.findall(r'^\[PASS\].*', content, re.MULTILINE)
    print(s)
#    for i, trace in enumerate(traces, 1):
#        print(f"Trace {i}:\n{trace}\n")
