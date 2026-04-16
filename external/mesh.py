import numpy as np
import time
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

def generate_nodes(nx: int, ny: int, lx: float , ly: float ) -> np.ndarray:
    x = np.linspace(0.0, lx, nx)
    y = np.linspace(0.0, ly, ny)

    #print(x)
    #print(y)

    nodes = []

    for j in range(ny):
        for i in range(nx):
            nodes.append([x[i], y[j]])
        
    #print(nodes)

    return np.array(nodes, dtype=float)

def generate_elements(nx: int, ny: int) -> np.ndarray:
    elements = []

    for j in range(ny -1):
        for i in range(nx-1):
            n0 = j*nx + i
            n1 = n0 + 1
            n2 = n0 + nx
            n3 = n2 + 1

            elements.append([n0, n1, n3])
            elements.append([n0, n3, n2])

    return np.array(elements, dtype=int)

def triangle_area(coords):
    x1,y1 = coords[0]
    x2,y2 = coords[1]
    x3,y3 = coords[2]

    area = 0.5 * abs((x2-x1)*(y3-y1) - (x3-x1)*(y2-y1))

    return area

def local_stiffness(coords):
    x1,y1 = coords[0]
    x2,y2 = coords[1]
    x3,y3 = coords[2]

    area = triangle_area(coords)

    b = np.array([y2-y3, y3-y1, y1-y2])
    c = np.array([x3-x2, x1-x3, x2-x1])

    ke = np.zeros((3,3))

    for i in range(3):
        for j in range(3):
            ke[i,j] = (b[i] * b[j] + c[i] * c[j])/(4.0 * area)

    return ke

def assemble_global_stiffness_dense(nodes, elements):
    n_nodes = len(nodes)
    K = np.zeros((n_nodes,n_nodes))

    for element in elements:
        coords = nodes[element]
        ke = local_stiffness(coords)

        for i in range(3):
            for j in range(3):
                K[element[i], element[j]] += ke[i,j]

    return K

def assemble_global_stiffness_sparse(nodes, elements):
    n_nodes = len(nodes)
    K = lil_matrix((n_nodes, n_nodes))

    for element in elements:
        coords = nodes[element]
        ke = local_stiffness(coords)

        for i in range(3):
            for j in range(3):
                K[element[i], element[j]] += ke[i,j]

    return K




