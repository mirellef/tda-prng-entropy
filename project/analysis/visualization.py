import matplotlib.pyplot as plt


def plot_embedding_2d(series, title="Embedding 2D"):

    plt.figure(figsize=(7, 7))

    plt.scatter(
        series[:-1],
        series[1:],
        s=3,
        alpha=0.4
    )

    plt.xlabel("x(t)")
    plt.ylabel("x(t+1)")
    plt.title(title)

    plt.tight_layout()
    plt.show()


def plot_point_cloud_3d(cloud, title="Point Cloud"):

    fig = plt.figure(figsize=(8, 6))

    ax = fig.add_subplot(
        111,
        projection="3d"
    )

    ax.scatter(
        cloud[:, 0],
        cloud[:, 1],
        cloud[:, 2],
        s=3,
        alpha=0.5
    )

    ax.set_xlabel("x(t)")
    ax.set_ylabel("x(t+τ)")
    ax.set_zlabel("x(t+2τ)")

    ax.set_title(title)

    plt.tight_layout()
    plt.show()