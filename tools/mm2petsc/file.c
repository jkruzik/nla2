#include <petscksp.h>

int main(int argc, char **args)
{
    Mat A;
    Vec b, x;
    PetscViewer viewer;
    char file[PETSC_MAX_PATH_LEN];
    PetscBool flg;
    PetscLogStage loadStage;
    PetscErrorCode ierr;

    PetscCall(PetscInitialize(&argc, &args, NULL, NULL));
    // Get binary file from command line
    PetscCall(PetscOptionsGetString(NULL, NULL, "-f", file, sizeof(file), &flg));
    PetscCheck(flg, PETSC_COMM_WORLD, PETSC_ERR_USER, "Must indicate binary file with the -f option");

    // Register logging stage for loading (-log_view)
    PetscCall(PetscLogStageRegister("load data", &loadStage));
    PetscCall(PetscLogStagePush(loadStage));

    // Load matrix and optionally right-hand side vector
    PetscCall(PetscViewerBinaryOpen(PETSC_COMM_WORLD, file, FILE_MODE_READ, &viewer));

    // Create and load matrix
    PetscCall(MatCreate(PETSC_COMM_WORLD, &A));
    PetscCall(MatSetFromOptions(A));
    PetscCall(MatLoad(A, viewer));

    // Create vectors compatible with A; x could be NULL
    PetscCall(MatCreateVecs(A, &b, &x));

    // Attempt to load right-hand side vector, ignore errors if not present
    PetscPushErrorHandler(PetscIgnoreErrorHandler, NULL);
    ierr = VecLoad(b, viewer);
    PetscPopErrorHandler();
    if (ierr) {
        // If loading b failed, initialize to a default vector
        PetscInt n;
        PetscCall(VecGetSize(b, &n));
        PetscCall(VecSet(b, 1.0 / PetscSqrtReal((PetscReal)n)));
    }
    VecView(b,NULL);
    PetscCall(PetscViewerDestroy(&viewer));
    PetscCall(PetscLogStagePop());

    // Clean up
    PetscCall(VecDestroy(&b));
    PetscCall(VecDestroy(&x));
    PetscCall(MatDestroy(&A));

    PetscCall(PetscFinalize());
    return 0;
}

