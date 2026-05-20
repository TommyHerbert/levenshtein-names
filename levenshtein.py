from __future__ import annotations


def levenshtein(a: str, b: str) -> int:
    """Edit distance: insert, delete, substitute each cost 1; space is a character like any other."""
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


def shortest_levenshtein_distance(word_list: list[str], s: str) -> int:
    """
    Minimum edit distance from `s` to any string in `word_list`.
    """
    if not word_list:
        raise ValueError("word_list must be non-empty")
    return min(levenshtein(s, w) for w in word_list)


def shortest_levenshtein_distance_with_argmin(word_list: list[str], s: str) -> tuple[int, str]:
    """
    Minimum edit distance from `s` to any string in `word_list`, and one word that
    achieves it (the first in `word_list` order among ties).
    """
    if not word_list:
        raise ValueError("word_list must be non-empty")

    best: int | None = None
    winners: list[str] = []
    for w in word_list:
        d = levenshtein(s, w)
        if best is None or d < best:
            best = d
            winners = [w]
        elif d == best:
            winners.append(w)

    assert best is not None
    return best, winners


def shortest_phrase_levenshtein_with_argmin(
    word_list: list[str],
    s: str,
    *,
    max_words: int = 10,
) -> tuple[int, str]:
    """
    Minimum edit distance from `s` to any phrase made of 1..max_words words from
    `word_list`, joined by a single ASCII space between words. Words may repeat.
    Returns the distance and one such phrase (first in depth-first search order
    among ties). Space in the phrase counts as a character like any other.
    """
    if not word_list:
        raise ValueError("word_list must be non-empty")
    if max_words < 1:
        raise ValueError("max_words must be >= 1")

    len_s = len(s)
    best_d: int | None = None
    best_phrase: str | None = None

    def consider(phrase: str) -> None:
        nonlocal best_d, best_phrase
        L = len(phrase)
        if best_d is not None and abs(L - len_s) > best_d:
            return
        d = levenshtein(s, phrase)
        if best_d is None or d < best_d:
            best_d = d
            best_phrase = phrase

    def walk(parts: list[str]) -> None:
        if parts:
            consider(" ".join(parts))
        if len(parts) == max_words:
            return
        for w in word_list:
            parts.append(w)
            walk(parts)
            parts.pop()

    walk([])

    assert best_d is not None and best_phrase is not None
    return best_d, best_phrase


def shortest_phrase_levenshtein_distance(
    word_list: list[str],
    s: str,
    *,
    max_words: int = 10,
) -> int:
    """Same as ``shortest_phrase_levenshtein_with_argmin`` but returns only the distance."""
    d, _ = shortest_phrase_levenshtein_with_argmin(
        word_list, s, max_words=max_words
    )
    return d
