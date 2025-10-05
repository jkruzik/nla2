## Installing PETSc
https://petsc.org/release/install/
- Distribution packages
- `pip install petsc petsc4py`
- Git (**recommended**)

### Installing PETSc from Git
```
git clone -b release https://gitlab.com/petsc/petsc.git petsc
cd petsc
```
Export environment variables (needed for installing Python modules):
```
export PETSC_DIR=`pwd`
export PETSC_ARCH=arch-dbg
export SLEPC_DIR=$PETSC_DIR/$PETSC_ARCH/externalpackages/git.slepc
```
Basic configuration:
```
./configure --download-mpich --download-fblaslapack --download-scalapack --download-metis --download-parmetis --download-mumps --download-superlu --download-superlu_dist --download-slepc --download-hypre --with-fortran-bindings=0
```
You can omit packages that you already have installed, e.g., `--download-mpich` and `--download-fblaslapack` if you have OpenMPI and OpenBLAS.
> [!TIP]
> Run `./configure --help` for all available options

Compile the library:
```
make all check
```

Install Python bindings (consider using venv):
```
 pip install petsc4py slepc4py
```
> [!TIP]
> Make an optimized build for timing measurements
> ```
>  export PETSC_ARCH=arch-opt
> ./configure --with-debugging=0 COPTFLAGS='-O3 -march=native -mtune=native' CXXOPTFLAGS='-O3 -march=native -mtune=native' FOPTFLAGS='-O3 -march=native -mtune=native' OTHER CONFIG OPTIONS
> ```
