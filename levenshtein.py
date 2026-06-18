from __future__ import annotations


def distance(a: str, b: str) -> int:
    """inserting, deleting or changing a letter is one step"""
    m, n = len(a), len(b)
    prev = list(range(n + 1))
    for i in range(1, m + 1):
        cur = [i]
        ca = a[i - 1]
        for j in range(1, n + 1):
            cb = b[j - 1]
            sub_cost = 0 if ca == cb else 1
            cur.append(
                min(
                    cur[j - 1] + 1,
                    prev[j] + 1,
                    prev[j - 1] + sub_cost,
                )
            )
        prev = cur
    return prev[n]


def closest_words(word_list: list[str], s: str) -> tuple[int, list[str]]:
    """
    minimum edit distance from `s` to any string in `word_list`, and 
    all words that achieve it
    """
    if not word_list:
        raise ValueError("word_list must be non-empty")

    best: int | None = None
    winners: list[str] = []
    for w in word_list:
        d = distance(s, w)
        if best is None or d < best:
            best = d
            winners = [w]
        elif d == best:
            winners.append(w)

    assert best is not None
    return best, winners

