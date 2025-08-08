SERVERS = [
    (0, "ac1118823fee"),
    (339, "ac1ddda8fee2"),
]  # ids = [0, 2^64)


def balancer(data):  # chooses node to send request
    h = hash(data.key)
    node_to_store = SERVERS.find_next_node(h)
    node_to_store.store(data)


def write(serf, data) -> bool:  # on storage node

    n_1 = self.get_next_node()
    n_2 = self.get_next_next_node()

    store = distach_store(data, [self, n_1, n_2])

    # get returns
    while store.ok_count() < 2:
        sleep(0.1)

    return True


def read(key) -> data:  # on storage node
    n_1 = self.get_next_node()
    n_2 = self.get_next_next_node()

    data = read_from(key, [self, n_1, n_2])

    ret_data = get_most_recent(
        data
    )  # olha o id (incremental) dos dados, retorna o mais alto => que será o mais recente

    return ret_data
