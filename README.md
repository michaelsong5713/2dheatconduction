# 2D Heat Conduction — FEM with DOLFINx + Gmsh

Transient heat conduction on a rectangular plate. Left edge is held at 100°, right edge at 0°, top and bottom are insulated. The solution evolves from a uniform cold plate toward a linear steady-state temperature profile.

<video src="https://github.com/michaelsong5713/2dheatconduction/raw/main/animation.mp4" controls muted loop width="100%"></video>

> If the player above doesn't load, [download/view `animation.mp4` directly](https://github.com/michaelsong5713/2dheatconduction/raw/main/animation.mp4).

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

