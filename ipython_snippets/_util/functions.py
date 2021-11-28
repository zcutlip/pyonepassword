import pathlib


def snippet_dir():
    main_file = pathlib.Path(__file__)
    main_dir = main_file.parent.parent
    return main_dir


def scratch_dir():
    main_dir = snippet_dir()
    scratch = pathlib.Path(main_dir, "scratch")
    scratch.mkdir(exist_ok=True)
    return scratch
