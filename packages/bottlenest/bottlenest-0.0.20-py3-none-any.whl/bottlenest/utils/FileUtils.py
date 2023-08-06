import os
import shutil
from pathlib import Path


class FileUtils:
    @staticmethod
    def absPath(path):
        # this function should be the abs path relative to the project root
        # basePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        basePath = None
        while basePath is None:
            if os.path.exists(os.path.join(os.getcwd(), 'bottlenest')):
                basePath = os.getcwd() + '/bottlenest'
            else:
                os.chdir(os.path.join(os.getcwd(), '..'))
        # basePath = Path(__file__).parent.parent.parent
        # return os.path.join(basePath, path)
        return os.path.join(basePath, path)

    @staticmethod
    def copyDir(src, dst, symlinks=False, ignore=None):
        # copy dir
        # do not use for
        shutil.copytree(src, dst, symlinks, ignore)
