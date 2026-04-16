import numpy as np
from external.fem_solver.mesh import triangle_area
def find_boundary_nodes(nodes, lx: float, ly: float, tol = 1e-12):
    boundary_nodes = []

    for i , (x,y) in enumerate(nodes):
        if(
            abs(x -0.0) < tol
            or abs(x-lx) < tol
            or abs(y-0.0) < tol
            or abs(y - ly) < tol
        ):
            boundary_nodes.append(i)

    return boundary_nodes


def apply_dirichlet(K, f, boundary_nodes, value = 0.0):

    for node in boundary_nodes:
        K[node,:] = 0.0
        K[node, node] = 1.0
        f[node] = value

    return K,f

def apply_dirichlet_sparse(K, f, boundary_nodes, value = 0.0):
    f = f.copy()

    for node in boundary_nodes:
        K.rows[node] = [node]
        K.data[node] = [1.0]
        f[node] = value

    return K,f



def local_load(coords, source=1.0):
    area = triangle_area(coords)
    fe = source * area/3.0 *np.ones(3)
    return fe

def assemble_global_load(nodes, elements, source=1.0):
    n_nodes = len(nodes)
    f = np.zeros(n_nodes)
    for element in elements:
        coords = nodes[element]
        fe = local_load(coords, source)

        for i in range(3):
            f[element[i]] += fe[i]

    return f
