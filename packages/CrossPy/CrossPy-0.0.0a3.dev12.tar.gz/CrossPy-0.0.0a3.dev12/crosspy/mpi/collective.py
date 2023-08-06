import numpy

def alltoallv(sendbuf, sdispls, recvbuf):
    """
    sendbuf [[] [] []]
    sdispls [. . .]
    """
    block_ids = self._global_index_to_block_id(sdispls)
    assert len(block_ids) == len(sdispls)

    # index_argsort = numpy.argsort(block_ids)
    # sorted_block_ids = block_ids[index_argsort]
    # comm_bounds = numpy.diff(sorted_block_ids, append=-1).nonzero()[0] + 1
    # left = 0
    # for right in comm_bounds:
    #     block = self._original_data[sorted_block_ids[left]]
    #     with getattr(block, 'device', nullcontext()):
    #         block[list_[index_argsort[left:right]]]
    #         ...
    #     left = right

    bounds = numpy.diff(block_ids, append=-1).nonzero()[0] + 1
    assert bounds[-1] == len(block_ids)
    obj = []
    left = 0
    for right in bounds:
        # TODO lazy
        block = self._original_data[block_ids[left]]
        with getattr(block, 'device', nullcontext()):
            obj.append(block[sdispls[left:right]])
        left = right