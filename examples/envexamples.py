import sys
import os

# append module root directory to sys.path
sys.path.insert(0,
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
