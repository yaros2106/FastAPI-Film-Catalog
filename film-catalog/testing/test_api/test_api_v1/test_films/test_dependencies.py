from api.api_v1.films.dependencies import UNSAFE_METHODS


def test_unsafe_methods_dont_contain_save_methods() -> None:
    save_methods = {
        "GET",
        "HEAD",
        "OPTIONS",
    }
    assert not UNSAFE_METHODS & save_methods
