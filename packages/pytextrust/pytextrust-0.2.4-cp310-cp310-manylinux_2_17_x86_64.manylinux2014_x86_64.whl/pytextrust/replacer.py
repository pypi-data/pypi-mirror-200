from pytextrust.pytextrust import wrap_literal_replacer
from typing import List
from enum import Enum


class MatchKind(Enum):
    LeftmostLongest = "LeftmostLongest"
    Standard = "Standard"
    LeftmostFirst = "LeftmostFirst"


def replace_literal_patterns(literal_patterns: List[str], replacements: List[str], text_to_replace: List[str],
                             is_bounded: bool = True, case_insensitive: bool = True,
                             match_kind: MatchKind = MatchKind.LeftmostLongest, n_jobs: int = 1):
    """
    Function to replace literal patterns in texts. A literal pattern consists only in unicode characters, without
    anchors, repetitions, groups or any regex specific symbol, just literals.

    The list literal_patterns is searched and found over the provided text_to_replace list, substituting each
    literal in literal_patterns by its corresponding replacement in replacements list.

    Options:
    - is_bounded: if True, it forces the literal pattern to be bounded by non-words/numbers to be replaced
    - case_insensitive: if True, ignores case.
    - match_kind corresponds to different matching possibilities described here 
        https://docs.rs/aho-corasick/latest/aho_corasick/enum.MatchKind.html
    - n_jobs: -1 means to use all paralellization available, 1 just one thread, N to set to exactly N threads

    It returns the replaced texts and the numbers of total replacements on all texts provided.
    """
    text_list, n_reps = wrap_literal_replacer(patterns=literal_patterns,
                                              replacements=replacements,
                                              texts=text_to_replace,
                                              is_bounded=is_bounded,
                                              case_insensitive=case_insensitive,
                                              match_kind=match_kind.value,
                                              n_jobs=n_jobs)

    return text_list, n_reps
