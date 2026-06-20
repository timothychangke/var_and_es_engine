import var_engine


def test_toolchain_smoke_test() -> None:
    """
    Ensure that the package is properly installed in the environment and discoverable
    """
    assert var_engine.__version__ != "unknown"
