import importlib, sys
sys.path.insert(0, r'C:\Users\soumy\ai-code-review-platform\services\repository-service')
app = importlib.import_module('app.main').app
for r in app.routes:
    t = type(r).__name__
    p = getattr(r, 'path', None) or getattr(r, 'prefix', None) or repr(r)
    m = getattr(r, 'methods', None)
    print(t, p, m)
