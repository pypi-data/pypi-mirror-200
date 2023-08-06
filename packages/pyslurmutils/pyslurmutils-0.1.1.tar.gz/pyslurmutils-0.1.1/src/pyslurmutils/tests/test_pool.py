from time import sleep


def test_pool_submit(slurm_pool):
    future1 = slurm_pool.submit(sleep, 0)
    future2 = slurm_pool.submit(sum, [1, 1])
    assert future2.result() == 2
    assert future1.result() is None


def test_pool_map(slurm_pool):
    results = [future for future in slurm_pool.map(sum, [[1, 1], [2, 2], [3, 3]])]
    assert results == [2, 4, 6]
