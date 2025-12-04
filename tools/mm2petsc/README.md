# Matrix Market to PETSc Binary Converter

Contains a script for converting [SuiteSparse Matrix Collection](https://sparse.tamu.edu/) Matrix Market (`.mtx`) files into PETSc binary files and an example of loading the files in PETSc.

See also the PETSc FAQ:
https://petsc.org/release/faq/#how-can-i-read-in-or-write-out-a-sparse-matrix-in-matrix-market-harwell-boeing-slapc-or-other-ascii-format

---

## Extracting `.mtx` Files

To extract all `*.mtx` files from the tar archives located in the `mats` directory, run:

```sh
cd mats
for f in *.tar.gz; do tar -xvzf "$f" --strip-components=1; done
```

---

## Converting a Single `.mtx` File

Make sure the environment variable `PETSC_DIR` is set, then run:

```sh
python mm2petsc.py mats/matrix.mtx
```

The PETSc `.bin` files will be written to the **`petscmats`** directory (hardcoded as `OUTPUT_DIR` in the script).

If a matching right-hand side file exists, e.g., `matrix_b.mtx`, it will be converted as well and appended to the same `.bin` file.

---

## Bulk Conversion

To convert all `.mtx` files in the `mats` directory:

```sh
for f in mats/*.mtx; do python mm2petsc.py "$f"; done
```

---

## Loading the Converted Files

To load the PETSc matrix and, if available, the right-hand side, see `file.c`, which can be compiled using `make file`

