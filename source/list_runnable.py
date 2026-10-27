# list_runnable.py: list every module you can run with `python -m`
import os, sys

GUARDS = ('__name__ == "__main__"', "__name__ == '__main__'")
SKIP = {"test", "tests"}

def find_runnable(prefix=""):
    found = set()
    for root in filter(os.path.isdir, sys.path):
        for dirpath, dirnames, filenames in os.walk(root):
            # only descend into real packages (folders with __init__.py)
            dirnames[:] = [d for d in dirnames
                           if os.path.isfile(os.path.join(dirpath, d, "__init__.py"))]
            for fn in filenames:
                if not fn.endswith(".py"):
                    continue
                path = os.path.join(dirpath, fn)
                parts = os.path.relpath(path, root)[:-3].split(os.sep)
                if parts[-1] == "__main__":        # pkg/__main__.py → `python -m pkg`
                    parts = parts[:-1]
                name = ".".join(parts)
                if not name or not name.startswith(prefix) or SKIP & set(parts):
                    continue
                if fn == "__main__.py":
                    found.add(name)
                    continue
                try:
                    with open(path, encoding="utf-8", errors="ignore") as f:
                        src = f.read()
                except OSError:
                    continue
                if any(g in src for g in GUARDS):
                    found.add(name)
    return sorted(found)

if __name__ == "__main__":
    prefix = sys.argv[1] if len(sys.argv) > 1 else ""
    print("\n".join(find_runnable(prefix)))