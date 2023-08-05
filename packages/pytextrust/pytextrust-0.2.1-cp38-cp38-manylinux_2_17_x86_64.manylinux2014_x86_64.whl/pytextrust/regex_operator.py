from pydantic import BaseModel
from pytextrust import pytextrust
from typing import List, Dict, Union
import json
import regex as re
from pytextrust.constants import get_logger
from enum import Enum

logger = get_logger()

DEFAULT_REGEX_CHUNKSIZE = 30


class ParallelismConfig(Enum):
    ByPatternChunks = "ByPatternChunks"
    ByTextChunks = "ByTextChunks"


class RegexProcessDefinition(BaseModel):
    patterns: List[str]
    texts: List[str]
    text_n_char: List[int] = None
    substitute_bound: bool = True
    case_insensitive: bool = True
    unicode: bool = False
    substitute_latin_char: bool = False
    regexset_size_limit: int = int(3e8)
    regexset_dfa_size_limit: int = int(3e8)
    regexset_chunk_size: int = DEFAULT_REGEX_CHUNKSIZE
    n_threads: int = 1
    parallelism_config: ParallelismConfig = ParallelismConfig.ByPatternChunks

    def perform_rust_regex(self):
        if self.text_n_char is None:
            self.text_n_char = [len(val) for val in self.texts]
        results_dict = json.loads(pytextrust.wrap_regex_full_find(self.json()))

        return results_dict


def apply_patterns_to_texts(patterns: List[str], texts: List[str],
                            substitute_bound: bool = True,
                            unicode: bool = False, substitute_latin_char: bool = True,
                            case_insensitive: bool = True,
                            regexset_size_mb_limit: int = int(3e2),
                            regexset_dfa_size_mb_limit: int = int(3e2),
                            regexset_chunk_size: int = DEFAULT_REGEX_CHUNKSIZE,
                            n_threads: int = 1,
                            parallelism_config: ParallelismConfig = ParallelismConfig.ByPatternChunks,
                            verbose: bool = True, skip_rust_invalid: bool = False):
    """
    """
    assert (not unicode) or (unicode and (not substitute_latin_char)
                             ),    "substitute_latin_char has only sense when unicode is False"

    if verbose:
        logger.info(
            f"Performing regex match and find over: \n - Patterns: {len(patterns)}\n - Texts: {len(texts)}"
            f"\n - Regex compile max size: {regexset_size_mb_limit} MBs"
            f"\n - Regex DFA max size: {regexset_dfa_size_mb_limit} MBs"
            f"\n - Number of threads: {n_threads}"
        )

    jan = RegexProcessDefinition(patterns=patterns,
                                 texts=texts,
                                 unicode=unicode,
                                 case_insensitive=case_insensitive,
                                 substitute_bound=substitute_bound,
                                 substitute_latin_char=substitute_latin_char,
                                 regexset_size_limit=int(
                                     regexset_size_mb_limit * 1e6),
                                 regexset_dfa_size_limit=int(
                                     regexset_dfa_size_mb_limit * 1e6),
                                 regexset_chunk_size=regexset_chunk_size,
                                 n_threads=n_threads,
                                 parallelism_config=parallelism_config)

    results_dict = jan.perform_rust_regex()
    n_invalid_regex = len(results_dict['invalid_pattern_indexes'])
    if n_invalid_regex > 0 and not skip_rust_invalid:
        logger.info(
            f"Applying python regex package with {n_invalid_regex} patterns")
        results_dict = apply_python_regex(patterns=results_dict['invalid_pattern_indexes'],
                                          texts=texts,
                                          prev_results=results_dict,
                                          case_insensitive=case_insensitive)

    return results_dict


def apply_python_regex(patterns: Union[List, Dict], texts: List[str], prev_results: Dict = None,
                       case_insensitive: bool = True):
    """ Apply python regex over previous dictionary results with "match_results" field
    """
    if prev_results is None:
        prev_results = {'match_results': {}}
    if isinstance(patterns, list):
        patterns = {str(k): (patterns[k], ) for k in range(len(patterns))}

    for pattern_index in patterns:
        pattern = patterns[pattern_index][0]
        flags_to_apply = re.IGNORECASE if case_insensitive else None
        compiled_pattern = re.compile(pattern, flags=flags_to_apply)

        for text_index, text in enumerate(texts):
            match_gen = compiled_pattern.finditer(text)
            matches_list = [list(val.span()) for val in match_gen]
            if len(matches_list) > 0:
                string_text_index = str(text_index)
                string_pattern_index = str(pattern_index)
                if string_text_index not in prev_results['match_results']:
                    prev_results['match_results'][string_text_index] = {}
                prev_results['match_results'][string_text_index][string_pattern_index] = matches_list

    return prev_results


def reduce_result(match_results: Dict, patterns_index_seq: List[str] = None, text_index_seq: List[str] = None):
    """ Reduce result to provided indexes for the texts and the patterns into a tabular transformable
    list of dictionaries
    """
    new_result = []
    for raw_text_str_index in match_results:
        text_int_index = int(raw_text_str_index)
        matches = match_results[raw_text_str_index]
        if text_index_seq is not None:
            text_index = text_index_seq[text_int_index]
        else:
            text_index = text_int_index

        for raw_pattern_str_index in matches:
            pattern_int_index = int(raw_pattern_str_index)
            if patterns_index_seq is not None:
                pattern_index = patterns_index_seq[pattern_int_index]
            else:
                pattern_index = pattern_int_index
            pattern_matches = matches[raw_pattern_str_index]

            for match in pattern_matches:
                value_dict = {'text_index': text_index,
                              'pattern_index': pattern_index,
                              'start': match[0],
                              'end': match[1]}
                new_result.append(value_dict)
    return new_result


def check_matches_eq(a_matches, b_matches, patterns_list, text_list):
    """ Checks equality between matches results"""

    text_indexes = set(a_matches['match_results'].keys()).union(
        set(b_matches['match_results'].keys()))
    for text_index in text_indexes:
        a_dict = a_matches['match_results'].get(text_index, {})
        b_dict = b_matches['match_results'].get(text_index, {})
        pattern_indexes = set(a_dict.keys()).union(set(b_dict.keys()))

        for pattern_index in pattern_indexes:

            a_pattern_matches = a_dict.get(pattern_index, [])
            b_pattern_matches = b_dict.get(pattern_index, [])
#             print(a_pattern_matches)
            if len(a_pattern_matches) != len(b_pattern_matches):
                print(
                    f"- Text: {text_list[int(text_index)]} \n- Pattern {patterns_list[int(pattern_index)]}")
                print(f"A matches: {a_pattern_matches}")
                print(f"B matches: {b_pattern_matches}")
                print("\n")
