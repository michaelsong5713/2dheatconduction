import gmsh
import numpy as np
import ufl
from mpi4py import MPI
from petsc4py import PETSc

from dolfinx import fem, io
from dolfinx.fem import petsc

try:
    from dolfinx.io import gmshio
except ImportError:
    from dolfinx.io import gmsh as gmshio

LENGTH = 1.0
HEIGHT = 0.5

K_COND = 1.0
RHO    = 1.0
CP     = 1.0

T_HOT  = 100.0
T_COLD = 0.0
T_INIT = 0.0

DT        = 0.005
NUM_STEPS = 100

DOMAIN_TAG = 1
LEFT_TAG   = 2
RIGHT_TAG  = 3
TOP_TAG    = 4
BOTTOM_TAG = 5

comm       = MPI.COMM_WORLD
model_rank = 0

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 0)

if comm.rank == model_rank:
    gmsh.open("plate.geo")
    gmsh.model.mesh.generate(2)

gmsh_out   = gmshio.model_to_mesh(gmsh.model, comm, model_rank, gdim=2)
domain     = gmsh_out.mesh
facet_tags = gmsh_out.facet_tags
gmsh.finalize()

tdim = domain.topology.dim
fdim = tdim - 1
domain.topology.create_connectivity(fdim, tdim)

V   = fem.functionspace(domain, ("Lagrange", 1))
uh  = fem.Function(V, name="Temperature")
u_n = fem.Function(V, name="Temperature_prev")
uh.x.array[:]  = T_INIT
u_n.x.array[:] = T_INIT

u, v   = ufl.TrialFunction(V), ufl.TestFunction(V)
dt     = fem.Constant(domain, PETSc.ScalarType(DT))
k      = fem.Constant(domain, PETSc.ScalarType(K_COND))
rho_cp = fem.Constant(domain, PETSc.ScalarType(RHO * CP))
f      = fem.Constant(domain, PETSc.ScalarType(0.0))

a = rho_cp / dt * u * v * ufl.dx + k * ufl.dot(ufl.grad(u), ufl.grad(v)) * ufl.dx
L = (rho_cp / dt * u_n + f) * v * ufl.dx

bilinear_form = fem.form(a)
linear_form   = fem.form(L)

left_dofs  = fem.locate_dofs_topological(V, fdim, facet_tags.find(LEFT_TAG))
right_dofs = fem.locate_dofs_topological(V, fdim, facet_tags.find(RIGHT_TAG))
bcs = [
    fem.dirichletbc(PETSc.ScalarType(T_HOT),  left_dofs,  V),
    fem.dirichletbc(PETSc.ScalarType(T_COLD), right_dofs, V),
]

A = petsc.assemble_matrix(bilinear_form, bcs=bcs)
A.assemble()

solver = PETSc.KSP().create(domain.comm)
solver.setOperators(A)
solver.setType(PETSc.KSP.Type.PREONLY)
solver.getPC().setType(PETSc.PC.Type.LU)

xdmf = io.XDMFFile(domain.comm, "heat_ex.xdmf", "w")
xdmf.write_mesh(domain)
xdmf.write_function(uh, 0.0)

t = 0.0
for step in range(NUM_STEPS):
    t += DT

    b = petsc.assemble_vector(linear_form)
    petsc.apply_lifting(b, [bilinear_form], [bcs])
    b.ghostUpdate(addv=PETSc.InsertMode.ADD_VALUES, mode=PETSc.ScatterMode.REVERSE)
    petsc.set_bc(b, bcs)

    solver.solve(b, uh.x.petsc_vec)
    uh.x.scatter_forward()
    b.destroy()

    u_n.x.array[:] = uh.x.array
    xdmf.write_function(uh, t)

xdmf.close()

lo = comm.allreduce(uh.x.array.min(), op=MPI.MIN)
hi = comm.allreduce(uh.x.array.max(), op=MPI.MAX)
if comm.rank == 0:
    print(f"Done: {NUM_STEPS} steps, t={t:.4f}s, range [{lo:.3f}, {hi:.3f}]")
