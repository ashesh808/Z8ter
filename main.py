import logging
from z8ter.core import Z8ter
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

app = Z8ter()
if __name__ == "__main__":
    app.run()
