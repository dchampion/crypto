import sys, re, os
sys.path.append(re.sub("doc$", "src", os.path.dirname(os.path.abspath(__file__))))
sys.path.append(re.sub("doc$", "test", os.path.dirname(os.path.abspath(__file__))))