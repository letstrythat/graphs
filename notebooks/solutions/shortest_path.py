def shortest_path(g, source, target, method, **kwargs):
    """Finds the shortest path between source and target.

    Since many stations may match source and target, the method
    tries to all pairs and returns the shortest path.

    If errors are met, they are silenced unless no pair yields a
    shortest path.

    Returns a dictionary with various metrics and information
    useful for future explanations.

    """

    best_eval = np.inf
    best_result = None
    latest_exception = None

    for source_ in search_station(source):
        for target_ in search_station(target):
            try:
                with StatsPatch(g) as stats:
                    cur_attempt = method(
                        g, source=source_, target=target_,
                        **kwargs)
                    cur_eval = sum(
                        g[u][v].get(kwargs.get('weight', None), 1)
                        for u, v in zip(cur_attempt[:-1], cur_attempt[1:])
                    )
                    if cur_eval >= best_eval:
                        continue
                    best_eval = cur_eval
                    best_result = cur_attempt
                    best_stats = stats

            except nx.NetworkXNoPath as e:
                latest_exception = e

    if best_result is None:
        if latest_exception is not None:
            raise latest_exception
        return None

    return {
        'weight': best_eval,
        'path': [Station(id_) for id_ in best_result],
        'counter': best_stats.counter,
        'stats': best_stats
    }
