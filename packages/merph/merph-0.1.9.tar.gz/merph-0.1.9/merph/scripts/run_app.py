try:
    from merph.app import make_local_dashboard
except ImportError:
    _has_app = False
else:
    _has_app = True


def run_app():
    if not _has_app:
        raise ImportError("app has dependencies, try: pip install merph[app]")
    make_local_dashboard()
