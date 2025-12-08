# Numerical Linear Algebra 2
## Running the examples
The examples can be run locally or through GitHub Codespaces.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/jkruzik/nla2)

## Lesson 1
- Basics of floating-point arithmetic
- Introduction to the stability of numerical algorithms

**Recommended reading:**
- N. J. Higham, "Accuracy and Stability of Numerical Algorithms: Second Edition", 2002. Chapter 1 (especially Sections 1.1–1.8)
- D. Goldberg, "What every computer scientist should know about floating-point arithmetic", ACM Comput. Surv., vol. 23, no. 1, 1991.

## Lesson 2
- Solving linear systems:
    - [Show effect of conditioning](l02/1conditioning.ipynb)
    - [Show the need of pivoting](l02/2pivoting.ipynb)
- Introduction to MPI

**Recommended reading:**
- [Introduction to Parallel Programming with MPI](https://pdc-support.github.io/introduction-to-mpi/)
- Optionally: [Intermediate MPI](https://enccs.github.io/intermediate-mpi/)

## Lesson 3
- Finite Difference and its use to solve Laplace's/Poisson's equations in 1D/2D
- Introduction to PETSc: [ksp/tutorials/ex2.c](https://petsc.org/release/src/ksp/ksp/tutorials/ex2.c.html)

**Recommended reading:**
- T. Kozubek et al., "[Lineární algebra s Matlabem](https://mi21.vsb.cz/sites/mi21.vsb.cz/files/unit/linearni_algebra_s_matlabem.pdf)", 2012. Chapters 16 and 17, especially pp. 134-138
- [PETSc User Guide: Getting Started](https://petsc.org/release/manual/getting_started/)

## Lesson 4
- Introduction to PETSc and petsc4py

**Recommended reading:**
- [Writing PETSc programs in C, compiling, etc.](https://petsc.org/release/manual/getting_started/#writing-c-c-or-fortran-applications)
- [Basic vector operations](https://petsc.org/release/manual/vec/#basic-vector-operations)
- [Index sets](https://petsc.org/release/manual/vec/#low-level-vector-communication)
- [Parallel matrix layout](https://petsc.org/release/manual/mat/#parallel-aij-sparse-matrices)
- [Basic matrix operations](https://petsc.org/release/manual/mat/#basic-matrix-operations)
- [Linear systems up to preconditioners (included)](https://petsc.org/release/manual/ksp/)

## Lesson 5
- Recap of Eigenvalues and Eigenvectors
- Eigenvalues of difference equations, Markov matrices, and differential equations and their stability
- Introduction to SLEPc

**Recommended reading:**
- G. Strang - "Linear Algebra and Its Applications, 4th Edition", 2006. Sections 5.3-5.4
- [Eigenvectors and Eigenvalues: explained visually](https://setosa.io/ev/eigenvectors-and-eigenvalues/)
- [SLEPc - EPS: Eigenvalue Problem Solver](https://slepc.upv.es/release/documentation/manual/eps.html)
- [SLEPc: eps/ex1.c](https://slepc.upv.es/release/documentation/hands-on/hands-on1.html)
- [slepc4py: eps/ex1.py](https://slepc.upv.es/release/slepc4py/tutorial.html#commented-source-of-a-simple-example)


## Lesson 6
- Singular Values Decomposition (SVD)
- Compression with SVD

**Recommended reading:**
- Tebbens, J.D.; Hnětynková, I.; Plešinger, M.; Strakoš, Z.; Tichý, P. - "Analýza metod pro maticové výpočty: základní metody", 2012

## Lesson 7
- Principal Component Analysis (PCA)

**Recommended reading:**
- J. Jauregui - "[Principal component analysis with linear algebra](https://www.math.union.edu/~jaureguj/PCA.pdf)", 2002.

## Lesson 8
- PageRank

**Recommended reading:**
S. Brin and L. Page - "[The Anatomy of a Large-Scale Hypertextual
Web Search Engine](http://infolab.stanford.edu/pub/papers/google.pdf)", 1998.

## Lesson 9
- Orthonormal basis (Wavelet, Fourier)
- Orthogonalization (Gram-Schmidt)

**Recommended reading:**
- D. Horák - "[Diskrétní transformace](https://mi21.vsb.cz/modul/diskretni-transformace.html)", 2012.
- https://en.wikipedia.org/wiki/Gram%E2%80%93Schmidt_process

## Lesson 10
- Sparse direct solvers and matrix reorderings
- Quadratic cost function minimization
- Steepest descent

**Recommended reading:**
- J. Kružík - "[Improving Quadratic Programming Algorihtms](https://homel.vsb.cz/~kru0097/files/kruzik_phd.pdf#chapter.4)", 2024. Chapter 4

## Lesson 11
- Barzilai-Borwein step lengths
- Krylov Basis
- Conjugate Gradients

**Recommended reading:**
- J. Kružík - "[Improving Quadratic Programming Algorihtms](https://homel.vsb.cz/~kru0097/files/kruzik_phd.pdf#chapter.4)", 2024. Chapter 4
- E. Carson, J. Liesen, Z. Strakoš - "[Towards understanding CG and GMRES through examples](https://www.karlin.mff.cuni.cz/~strakos/download/2024_CarLieStr.pdf)", 2024.


## Lesson 12
 - GMRES and MINRES
**Recommended reading:**
- J. Kružík - "[Improving Quadratic Programming Algorihtms](https://homel.vsb.cz/~kru0097/files/kruzik_phd.pdf#chapter.4)", 2024. Chapter 4
- E. Carson, J. Liesen, Z. Strakoš - "[Towards understanding CG and GMRES through examples](https://www.karlin.mff.cuni.cz/~strakos/download/2024_CarLieStr.pdf)", 2024.

