import engine as e

def test_start():
    b = e.new_board()
    assert sum(1 for x in b if x == 1) == 12 and sum(1 for x in b if x == -1) == 12
    assert len(e.get_moves(b, 1)) == 7

def test_forced_capture():
    b = [0] * 64
    b[5 * 8 + 2], b[4 * 8 + 3] = 1, -1          # human at (5,2), AI at (4,3), (3,4) empty
    ms = e.get_moves(b, 1)
    assert len(ms) == 1 and ms[0]["caps"] == [4 * 8 + 3]

def test_pruning_same_result_fewer_nodes():
    b = e.new_board()
    s1, s2 = e.Searcher(True), e.Searcher(False)
    v1 = s1.search(b, 4, float("-inf"), float("inf"), -1)
    v2 = s2.search(b, 4, float("-inf"), float("inf"), -1)
    assert v1 == v2 and s1.nodes < s2.nodes
    print("nodes with pruning:", s1.nodes, "without:", s2.nodes)

if __name__ == "__main__":
    test_start(); test_forced_capture(); test_pruning_same_result_fewer_nodes(); print("all tests passed")
