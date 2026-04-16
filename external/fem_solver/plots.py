import matplotlib.pyplot as plt
import matplotlib.tri as mtri

def plot_nodes(nodes):
    plt.figure()
    plt.scatter(nodes[:,0], nodes[:,1])

    for idx, (x,y) in enumerate(nodes):
        plt.text(x,y, str(idx))
    
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Mesh Nodes")
    plt.axis("equal")
    plt.show()


def plot_mesh(nodes, elements):
    triang = mtri.Triangulation(nodes[:,0], nodes[:,1], elements)

    plt.figure()
    plt.triplot(triang)
    plt.scatter(nodes[:,0], nodes[:,1], s=10)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Triangular Mesh")
    plt.axis("equal")
    plt.show()

def plot_solution(nodes, elements, u):
    triang = mtri.Triangulation(nodes[:,0], nodes[:,1], elements)

    plt.figure()
    contour = plt.tricontourf(triang, u, levels=20)
    plt.colorbar(contour, label="u")
    plt.triplot(triang, color="k", linewidth=0.5, alpha=0.5)

    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("FEM Solution")
    plt.axis("equal")
    plt.show()