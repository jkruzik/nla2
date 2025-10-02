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
