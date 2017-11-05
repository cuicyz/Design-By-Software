#!/usr/bin/env python
import sys
print("error text",file=sys.stderr)
print("the command line arguments")
for x in sys.argv:
    print(x)

print("the input")
text = sys.stdin.read()
print(text)
exit(2)