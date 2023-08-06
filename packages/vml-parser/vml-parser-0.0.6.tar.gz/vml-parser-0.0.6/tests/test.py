import sys
sys.path.append("../src/vml_parser")
import vml 

with open("test.vml", "r") as f:
    lines = f.readlines()
    
data = vml.parse(lines)
print(data)
dump = vml.dump(data)
print(dump, file=open("out.vml", "w"))