# 2D Heat Conduction — FEM with DOLFINx + Gmsh

Transient heat conduction on a rectangular plate. Left edge is held at 100°, right edge at 0°, top and bottom are insulated. The solution evolves from a uniform cold plate toward a linear steady-state temperature profile.

![Heat conduction animation](animation.mp4)

## Dependencies

Runs inside the official [DOLFINx Docker image](https://hub.docker.com/r/dolfinx/dolfinx), which bundles DOLFINx, PETSc, MPI, and Gmsh.

```
docker pull dolfinx/dolfinx:stable
```

## Running

From the repo root:

```
docker run --rm -ti -v ${PWD}:/work -w /work dolfinx/dolfinx:stable python3 heat_ex.py
```

Output: `heat_ex.xdmf` + `heat_ex.h5`. Open `heat_ex.xdmf` in [ParaView](https://www.paraview.org/) to visualize. When loading, use **Rescale to Data Range Over All Timesteps** to set the colorbar correctly.

## Files

| File | Description |
|------|-------------|
| `heat_ex.py` | Main simulation script |
| `plate.geo` | Gmsh geometry and mesh definition |
| `convergence_test.py` | O(h²) convergence verification using a structured mesh |
| `manufactured_solution.py` | Method of manufactured solutions — verifies the weak form against a known exact answer |
| `run.bat` | Shortcut: `.\run` instead of typing the full docker command |

## Verification

Two verification scripts are included. Both run the same way as the main script:

```
docker run --rm -ti -v ${PWD}:/work -w /work dolfinx/dolfinx:stable python3 convergence_test.py
docker run --rm -ti -v ${PWD}:/work -w /work dolfinx/dolfinx:stable python3 manufactured_solution.py
```

`convergence_test.py` checks that the L2 error halves at rate ~2.0 as the mesh refines, which is the expected behavior for P1 elements. `manufactured_solution.py` solves a problem with a known exact solution and reports how closely the solver matches it.
