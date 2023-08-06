#!/bin/python3
import sys
import os

class Element:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.hascheckbox = False
        self.ischecked = False
        if (name.startswith("[x]") or name.startswith("[ ]")):
            self.hascheckbox = True
            if name.startswith("[x]"):
                self.ischecked = True
            else:
                self.ischecked = False
            self.name = name[3:].strip()

    def append(self, child):
        self.children.append(child)

    def __str__(self):
        if self.hascheckbox:
            if len(self.children) == 0:
                return '{"' + self.name + '"' + ": " + str(self.children) + ', "checked":' + str(self.ischecked).lower() + "}"
            else:
                return '{"' + self.name + '"' + ": " + str(self.children) + ', "checked":' + str(self.ischecked).lower() + "}"

        else:
            if len(self.children) == 0:
                return '"' + self.name + '"'
            return '{"' + self.name + '"' + ": " + str(self.children) + "}"

    def __repr__(self):
        return str(self)


def parse(lines : list[str]) -> list[Element]:
    root = []
    for line in lines:
        if line.startswith("\n"):
            continue

        if not line.startswith("\t"):
            root.append(Element(line.strip()))
        else:
            # count tabs
            tabs = 0
            for char in line:
                if char == "\t":
                    tabs += 1
                else:
                    break
            elements = root
            for i in range(tabs - 1):
                elements = elements[-1].children

            elements[-1].append(Element(line.strip()))

    return root

def dump(obj : object, level: int = 0) -> list[str]:
    lines = []
    
    for element in obj:
        # check if element has children
        if len(element.children) == 0:
            # check if element has checkbox
            if element.hascheckbox:
                if element.ischecked:
                    lines.append("\t" * level + "[x] " + element.name + "\n")
                else:
                    lines.append("\t" * level + "[ ] " + element.name + "\n")
            else:
                lines.append("\t" * level + element.name + "\n")
        else:
            # check if element has checkbox
            if element.hascheckbox:
                if element.ischecked:
                    lines.append("\t" * level + "[x] " + element.name + "\n")
                else:
                    lines.append("\t" * level + "[ ] " + element.name + "\n")
            else:
                lines.append("\t" * level + element.name + "\n")
                
            # recursively call the function for children elements
            lines.extend(dump(element.children, level = level + 1))
        
    return "".join(lines)
    

def main():
    # check if this script is piped to stdin
    if not sys.stdin.isatty():
        # read from stdin
        lines = sys.stdin.readlines()
        # parse lines
        print(parse(lines))
        # exit
        sys.exit(0)

    # for every file passed as an argument
    for filename in sys.argv[1:]:
        # check if filename is a regular file
        if os.path.isfile(filename):
            with open(filename, "r") as f:
                lines = f.readlines()
            print(parse(lines))

if __name__ == "__main__":
    main()