
def distance(i1, i2):
    x1, y1 = pos[i1]
    x2, y2 = pos[i2]
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

g = nx.DiGraph()

# for each subway line
for line_nb, trip in trips.items():

    # for each different trip
    for trip_id in trip.drop_duplicates('route_id').trip_id:

        # Note:
        #   - we should use "trip_headsign" rather than "route_id"
        #     but the map gets confusing outside Paris
        #   - inside Paris, the graph we build here is still correct

        sequence = list(
            # get the list of stop_id in orders
            stop_times[line_nb]
            .query(f'trip_id == {trip_id}')
            .sort_values('stop_sequence')
            .stop_id
        )

        for first, second in zip(sequence[:-1], sequence[1:]):
            g.add_edge(
                first, second,
                # we store 'RER' or 'METRO' for printing it differently
                type=line_nb.split('_')[0],
                # add distance information
                distance=distance(first, second),
                # line_colors is provided as is
                color=line_colors[line_nb]
            )

# for each subway line
for line_nb, transfer in transfers.items():

    # parse the lines of the table in order
    for _, line in transfer.iterrows():

        first, second = line.from_stop_id, line.to_stop_id

        # add an edge for each connection if both nodes already exists in the
        # graph (remember there are a lot of bus stations we chose to ignore)
        if first in g.nodes and second in g.nodes:
            g.add_edge(
                first, second,
                type='CONNECTION',
                distance=distance(first, second),
                duration=line.min_transfer_time,
                color='#aaaaaa'
            )
            g.add_edge(
                second, first,
                type='CONNECTION',
                distance=distance(first, second),
                duration=line.min_transfer_time,
                color='#aaaaaa'
            )

