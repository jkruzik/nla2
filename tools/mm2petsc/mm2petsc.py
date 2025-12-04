#!/usr/bin/env python3

import os
import sys
import scipy.io

dirs = os.environ["PETSC_DIR"]
sys.path.insert(0, dirs + "/lib/petsc/bin/")

import PetscBinaryIO

OUTPUT_DIR = "petscmats"

def convert(filename):
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    mat_name = filename.replace("/", ".")
    mat_name = mat_name.split(".")[-2]
    output_file = os.path.join(OUTPUT_DIR, mat_name + ".bin")

    files = [filename]
    vec_name = filename[:-4] + "_b" + filename[-4:]
    if os.path.isfile(vec_name):
        files.append(vec_name)

    with open(output_file, "w") as mfile:
        for f in files:
            print("Converting: " + f)
            A = scipy.io.mmread(f)
            if A.shape[1] != 1:
                PetscBinaryIO.PetscBinaryIO().writeMatSciPy(mfile, A)
            else:
                PetscBinaryIO.PetscBinaryIO().writeVec(mfile, A.todense())


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python " + sys.argv[0] + " pathToMatrixFile")
        sys.exit(1)
    convert(sys.argv[1])
