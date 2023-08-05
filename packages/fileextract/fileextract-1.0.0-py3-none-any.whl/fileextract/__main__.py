import os
import sys
import glob
import json
import argparse

from fileextract.Controller import Controller
from fileextract.cmd.TSKCommand import TSKCommand
from fileextract.processor.Processor import Processor


def main(args_=None):
    """The main routine."""
    if args_ is None:
        args_ = sys.argv[1:]

    parser = argparse.ArgumentParser()   
    parser.add_argument("--config", "-c", type=str, required=True, help="Path to config file")
    args = parser.parse_args()

    f = open(args.config)
    c = json.load(f)

    ctrl = Controller()
    processor = Processor(c["logPath"])

    ctrl.printHeader()

    for raw in  c["raws"]:
        rawPaths = glob.glob(raw["path"])
        for rawPath in rawPaths:
            if(os.path.isfile(rawPath) and (".raw" in rawPath or ".dd" in rawPath)):
                print(" --> Target: " + rawPath)
                print("    ---")

                targetDir = rawPath + "_files"
                if(not os.path.isdir(targetDir)):
                    print("     Create: " + targetDir)
                    os.mkdir(targetDir)

                for file in raw["files"]:
                    print("    Extract: " + file)
                    target = os.path.join(targetDir, file.strip('/').strip('\\').split('/')[-1].split('\\')[-1])
                    cmd = TSKCommand.FCAT.substitute(offset=raw["offset"], filePath=file, imgPath=rawPath) + " > " + target
                    processor.process(cmd)
                print("    ---")
                print("")

    ctrl.printExecutionTime()

if __name__ == "__main__":
    sys.exit(main())
