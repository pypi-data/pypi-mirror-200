from contextlib import nullcontext

import cupy

def alltoallv(sendbuf, sdispls, recvbuf, debug=False):
    """
    sendbuf [[] [] []]
    sdispls [. . .]
    """
    source_block_ids = sendbuf._global_index_to_block_id(sdispls)
    source_bounds = sendbuf._bounds
    target_bounds = recvbuf._bounds

    for i in range(len(sendbuf._original_data)):
        gather_mask = (source_block_ids == i)
        for j in range(len(recvbuf._original_data)):
            scatter_mask = gather_mask[(target_bounds[j-1] if j else 0):target_bounds[j]]
            gather_indices_global = sdispls[(target_bounds[j-1] if j else 0):target_bounds[j]][scatter_mask]
            gather_indices_local = gather_indices_global - (source_bounds[i-1] if i else 0)
            assert sum(scatter_mask) == len(gather_indices_local)
            # gather
            with getattr(sendbuf._original_data[i], 'device', nullcontext()):
                buf = sendbuf._original_data[i][gather_indices_local]
            # scatter
            with getattr(recvbuf._original_data[j], 'device', nullcontext()):
                assert not debug or cupy.allclose(recvbuf._original_data[j][scatter_mask], cupy.asarray(buf))
                recvbuf._original_data[j][scatter_mask] = cupy.asarray(buf)