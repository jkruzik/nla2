FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Install dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install build-essential gfortran cmake valgrind gdb bear \
    git python3-dev python3-pip \
    libopenmpi-dev openmpi-bin libopenblas-serial-dev libscalapack-openmpi-dev \
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install some dev tools
RUN pip install -U --break-system-packages ipykernel numpy scipy sympy matplotlib mpi4py

# Install PETSc
WORKDIR /opt
RUN git clone -b release https://gitlab.com/petsc/petsc.git && cd petsc && \
    ./configure \
      --with-cc=mpicc --with-cxx=mpicxx --with-fc=mpif90 \
      --download-metis \
      --download-parmetis \
      --download-mumps \
      --download-superlu \
      --download-superlu_dist \
      --download-slepc \
      --download-hypre \
      --with-fortran-bindings=0 && \
    make PETSC_DIR=$PWD PETSC_ARCH=arch-dbg all

# Build and install petsc4py
WORKDIR /opt/petsc
RUN PETSC_ARCH='arch-dbg' python3 -m pip install src/binding/petsc4py

# Environment variables
ENV PETSC_DIR=/opt/petsc
ENV PETSC_ARCH=arch-dbg
ENV PATH=$PETSC_DIR/$PETSC_ARCH/bin:$PATH

