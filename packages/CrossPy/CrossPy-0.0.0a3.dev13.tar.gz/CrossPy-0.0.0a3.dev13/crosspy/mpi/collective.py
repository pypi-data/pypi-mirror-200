import numpy

def alltoallv(sendbuf, sdispls, recvbuf):
    """
    sendbuf [[] [] []]
    sdispls [. . .]
    """
    source_block_ids = sendbuf._global_index_to_block_id(sdispls)
    assert len(source_block_ids) == len(sdispls)

    block_ids_argsort = numpy.argsort(source_block_ids, kind='stable')
    sorted_sdispls = sdispls[block_ids_argsort]
    sorted_block_ids = source_block_ids[block_ids_argsort]
    comm_bounds = numpy.diff(sorted_block_ids, append=-1).nonzero()[0] + 1
    gather_indices = lambda i: sorted_sdispls[(comm_bounds[i-1] % comm_bounds[-1]):comm_bounds[i]]

    target_block_ids = recvbuf._global_index_to_block_id(block_ids_argsort)
    gather_target_block_ids = lambda i: target_block_ids[(comm_bounds[i-1] % comm_bounds[-1]):comm_bounds[i]]

    target_bounds = recvbuf._bounds
    for j in range(len(recvbuf._original_data)):
        for i in range(len(comm_bounds)):
            target_block_ids_i = gather_target_block_ids(i)
            left = sum(target_block_ids_i < target_bounds[j])
            target_global_orders = block_ids_argsort[target_block_ids_i == j]
            target_local_indices = target_global_orders - (target_bounds[j-1] % target_bounds[-1])
            recvbuf._original_data[j][target_local_indices] = sendbuf._original_data[i][left: left+len(target_local_indices)]
    return
