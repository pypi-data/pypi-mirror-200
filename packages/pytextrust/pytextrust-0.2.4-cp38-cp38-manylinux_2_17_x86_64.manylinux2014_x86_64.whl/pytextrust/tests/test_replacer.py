from pytextrust.replacer import replace_literal_patterns


def test_basic_replacer():
    literal_patterns = ["uno", "dos"]
    replacements = ["1", "2"]
    text_to_replace = ["es el numero uno o el dos yo soy el -uno #uno puno"]
    text_list, n_reps = replace_literal_patterns(literal_patterns=literal_patterns,
                                                 replacements=replacements,
                                                 text_to_replace=text_to_replace,
                                                 is_bounded=True,
                                                 case_insensitive=True)
    assert n_reps == 4, "Number of replacements is not OK"
    assert text_list == [
        "es el numero 1 o el 2 yo soy el -1 #1 puno"], "Replaced text is not OK"
