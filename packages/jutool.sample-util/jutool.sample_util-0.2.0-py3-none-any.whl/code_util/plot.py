import matplotlib.pyplot as plt


def draw_line_chart(path: str, labels: [], points: []):
    # x = [x[0] for x in points]
    # y = [x[1] for x in points]
    plt.cla()
    y = points

    plt.plot(y)
    plt.xlabel(labels[0])
    plt.ylabel(labels[1])

    plt.savefig(path)

    plt.close()
