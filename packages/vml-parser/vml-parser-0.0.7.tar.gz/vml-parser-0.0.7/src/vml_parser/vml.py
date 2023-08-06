#!/bin/python3
import sys
import os
import json

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
        
    def setchecked(self, checked):
        self.hascheckbox = True
        self.ischecked = checked

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


def parse(lines: list[str]) -> list[Element]:
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

def dump(obj: list[Element], level: int = 0) -> list[str]:
    lines = []

    for element in obj:
        # check if element has children
        if len(element.children) == 0:
            # check if element has checkbox
            if element.hascheckbox:
                if element.ischecked:
                    lines.append("\t" * level + "[x] " + element.name)
                else:
                    lines.append("\t" * level + "[ ] " + element.name)
            else:
                lines.append("\t" * level + element.name)
        else:
            # check if element has checkbox
            if element.hascheckbox:
                if element.ischecked:
                    lines.append("\t" * level + "[x] " + element.name)
                else:
                    lines.append("\t" * level + "[ ] " + element.name)
            else:
                lines.append("\t" * level + element.name)

            # recursively call the function for children elements
            lines += dump(element.children, level + 1)  

    return lines

def dumps(lines : list[str]) -> list[str]:
    def convert(obj) -> list[Element]:
        root = []

        if not isinstance(obj, list):
            obj = [obj]
        
        for item in obj:
            if isinstance(item, str):
                element = Element(item)
            if isinstance(item, dict):
                name = list(item.keys())[0]
                element = Element(name)
                children = item[name]
                element.children = convert(children)
                if "checked" in item.keys():
                    element.hascheckbox = True
                    element.ischecked = item["checked"]
            root.append(element)
        return root

    root = convert(json.loads("".join(lines)))
    data = dump(root)
    return data
                

def usage():
    print("Usage: vml [-d] <file.vml> [file2.vml] [file3.vml] ...")


def main():
    # check for arguments
    if len(sys.argv) == 1 and sys.stdin.isatty():
        usage()
        sys.exit(1)
    
    if len(sys.argv) > 1 and sys.stdin.isatty():
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            usage()
            sys.exit(0)

    # get dashed arguments
    dashed_args = []
    for arg in sys.argv[1::]:
        if arg.startswith("-"):
            dashed_args.append(arg)
        else:
            break
        
    # dump logic
    if "-d" in dashed_args or "--dump" in dashed_args:
        if not sys.stdin.isatty():
            lines = sys.stdin.readlines()

            for line in dumps(lines):
                print(line)

            sys.exit(0)

        for filename in sys.argv[1:]:
            if os.path.isfile(filename):
                with open(filename, "r") as f:
                    lines = f.readlines()

                for line in dumps(lines):
                    print(line)
        sys.exit(0)
        
    #parse logic
    else:
        if not sys.stdin.isatty():
            lines = sys.stdin.readlines()
            print(parse(lines))
            sys.exit(0)

        for filename in sys.argv:
            if os.path.isfile(filename):
                with open(filename, "r") as f:
                    lines = f.readlines()
                print(parse(lines))

if __name__ == "__main__":
    main()
