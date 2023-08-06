from algs import NeedlemanWunsch, Hirshberg, DTW

def test_dtw():
    dtw = DTW()

    # print(dtw.get_alignment_indices([1, 2, 3], [1, 2, 3, 4]))

    x = [3, 1, 2, 2, 1]
    y = [2, 0, 0, 3, 3, 1, 0]
    print(dtw.get_alignment_path(x, y))
    # Warp path:  [(0, 0), (1, 1), (1, 2), (2, 3), (3, 4), (4, 5), (4, 6)]


def test_hirshberg():
    seq1 = "GATTACA"
    seq2 = "GCATGCU"

    # seq1 = ['G', 'A', 'TWW', 'T', 'AWW', 'C', 'A']
    # seq2 = ['G', 'CAA', 'A', 'T', 'XXG', 'C', 'U']

    # seq1 = 'AGTACGCA'
    # seq2 = 'TATGC'

    nw = NeedlemanWunsch(
        match_weight=2,
        mismatch_weight=-1,
        gap_weight=-2,
    )
    hr = Hirshberg(
        match_weight=2,
        mismatch_weight=-1,
        gap_weight=-2,
    )

    print("Needleman-Wunsch")
    a, b = nw.get_alignment(seq1, seq2)
    nw.print_alignment(a, b)

    print("Needleman-Wunsch")
    a, b = nw.get_alignment(seq1[::-1], seq2[::-1])
    nw.print_alignment(a, b)

    print("Hirshberg")
    a, b = hr.get_alignment(seq1, seq2)
    hr.print_alignment(a, b)

if __name__ == "__main__":
    # test_hirshberg()
    test_dtw()
