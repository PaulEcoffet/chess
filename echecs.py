#!/bin/env python3
# -*- encoding:utf-8 -*-
from terminal import Terminal

def main():
    try:
        interface = Terminal()
        interface.start()
    except KeyboardInterrupt:
        print("Bye bye")

if __name__ == "__main__":
    main()
