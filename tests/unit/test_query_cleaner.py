from helpers.query_cleaner import clean_query


def test_clean_query_removes_generic_words() -> None:
    assert clean_query("fichier population csv") == "population"


def test_clean_query_keeps_meaningful_words() -> None:
    assert clean_query("population par commune") == "population par commune"


def test_clean_query_lowercases() -> None:
    assert clean_query("Population 2014") == "population 2014"


def test_clean_query_all_generic_falls_back_to_original() -> None:
    assert clean_query("fichier excel") == "fichier excel"


def test_clean_query_handles_accents() -> None:
    assert clean_query("données population") == "population"
