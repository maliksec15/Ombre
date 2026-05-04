"""python -m ombre — start the Ombre server."""
import sys
import os

if __name__ == "__main__":
    port = int(os.environ.get("OMBRE_PORT", 8080))
    import ombre
    ombre.start(port=port)
