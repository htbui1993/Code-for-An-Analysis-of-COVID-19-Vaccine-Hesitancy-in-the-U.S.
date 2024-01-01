import os
import time
import glob
import numpy as np

if __name__ == "__main__":
    start_time = time.time()
    full_path = os.path.realpath(__file__)
    path, filename = os.path.split(full_path)

    #! Use draw.io to create figure 1 which is a flowchart

    #! Loop to create figures
    for i in glob.glob(f"{path}/fig*_code.py"):
        # Run the python file
        os.system(f"python '{i}'")

    print(f"Total time: {time.time() - start_time:.2f} seconds")
