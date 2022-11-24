from pathlib import Path
import os


pytests = Path('.tox').rglob('pytest.exe')

for p in pytests:
    print(p)
    os.system(p.absolute().as_posix())