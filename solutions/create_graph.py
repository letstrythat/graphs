g = nx.DiGraph(
    # feed an adjacency list
    [
        ['A', 'A'], ['A', 'B'], ['A', 'C'],
        ['B', 'D'], ['B', 'F'],
        ['C', 'A'], ['C', 'E'], ['C', 'F'],
        ['D', 'B'],
        ['E', 'A'],
    ]
)

ax = plt.axes()
ax.set_axis_off()

# You may give a positioning strategy
nx.draw_networkx(g, ax=ax, pos=nx.kamada_kawai_layout(g))
g.edges
