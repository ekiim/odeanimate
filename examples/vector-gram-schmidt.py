import matplotlib.pyplot as plt
from odeanimate.vector import Vector

def Gram(*non):
    orth=[]
    orth.append(non[0])
    for i in range(1,len(non)):
        a=[non[i].dot(orth[i-j])/(orth[i-j].euclidean_norm()*orth[i-j].euclidean_norm())*orth[i-j] for j in range(1,i+1)]
        x=non[i]-sum(a,start=Vector(0,0,0))
        orth.append(x)
    return orth

if __name__ == '__main__':
    non=[
        Vector(1, -1, 1),
        Vector(1, 0, 1),
        Vector(1, 1, 2)
        ]
    n=Gram(*non)
    print(n)
    a = n[0]
    b = n[1]
    c = n[2]
    a1 = non[0]
    b1 = non[1]
    c1 = non[2]
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(projection='3d')
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    ax.set_zlim(0, 4)
    ax.quiver([0],[0],[0], [a.values[0]], [a.values[1]], [a.values[2]], color='k')
    ax.quiver([0],[0],[0], [b.values[0]], [b.values[1]], [b.values[2]], color='k')
    ax.quiver([0],[0],[0], [c.values[0]], [c.values[1]], [c.values[2]], color='k')
    ax.quiver([0],[0],[0], [a1.values[0]], [a1.values[1]], [a1.values[2]], color='r')
    ax.quiver([0],[0],[0], [b1.values[0]], [b1.values[1]], [b1.values[2]], color='r')
    ax.quiver([0],[0],[0], [c1.values[0]], [c1.values[1]], [c1.values[2]], color='r')
    ax.view_init(10, 40)
