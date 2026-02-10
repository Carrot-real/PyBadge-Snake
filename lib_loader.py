import sys
# Move '/lib' to the front of the search path
if '/lib' in sys.path:
    sys.path.remove('/lib')
sys.path.insert(0, '/lib')