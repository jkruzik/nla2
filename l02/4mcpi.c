// ## Estimating Pi using Monte Carlo method
// https://en.wikipedia.org/wiki/Monte_Carlo_method#Overview
// compile with mpicc filename.c -o filename
// run with mpirun -n 2 ./filename

#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char** argv) {
  int rank, size;
  long long tosses_l, tosses = 1000000;
  long long count_l = 0, count = 0;
  double x, y;

  MPI_Init(&argc, &argv);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

  if (argc > 1) {
    tosses = (long long)atof(argv[1]); // allow user to pass N
  }

  // Divide work
  tosses_l = tosses / size;

  // Seed RNG differently for each rank
  srand(rank);

  for (long long i = 0; i < tosses_l; i++) {
    x = (double)rand() / RAND_MAX;
    y = (double)rand() / RAND_MAX;
    if (x*x + y*y <= 1.0) {
      count_l++;
    }
  }

  // Reduce counts from all processes
  MPI_Reduce(&count_l, &count, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);

  if (rank == 0) {
    printf("Estimated Pi = %.6f using %lld tosses and %d processes\n",
        (4. * count) / tosses, tosses, size);
  }

  MPI_Finalize();
  return 0;
}

