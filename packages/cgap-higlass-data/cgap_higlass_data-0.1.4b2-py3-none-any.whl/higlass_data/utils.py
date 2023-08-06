
def does_tool_exist(name):
    """Check whether `name` is on PATH and marked as executable."""
    from shutil import which

    return which(name) is not None