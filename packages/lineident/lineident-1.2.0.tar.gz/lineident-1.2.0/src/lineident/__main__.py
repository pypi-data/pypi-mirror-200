import sys
import argparse

from lineident.Controller import Controller
from lineident.processor.Processor import Processor

def main(args_=None):
    """The main routine."""
    if args_ is None:
        args_ = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument("--path", "-p", type=str, required=True, help="Path to file which shall be searched")
    parser.add_argument("--method", "-m", type=str, choices=["and", "or"], required=True, help="Method to check for words. and/or")
    parser.add_argument("--words", "-w", type=str, required=True, help="CSV input e.g.: dog,cat,hello")
    parser.add_argument("--format", "-f", type=str, choices=["std", "ol"], default="std", help="Output format: std/ol")
    args = parser.parse_args()

    ctrl = Controller(args.path)
    ctrl.printHeader()

    p = Processor(args.path, args.method, args.words)
    results = p.process()

    ctrl.printOptions(p.words, args.method)
    ctrl.printResults(results, args.format)
    ctrl.printExecutionTime()
   

if __name__ == "__main__":
    sys.exit(main())
