import shutil
import os

extension_dir = 'extensions'

def unzip_to_extension():
    if not os.path.exists(extension_dir):
        os.mkdir(extension_dir)

    if not os.path.exists( os.path.join(extension_dir, 'mainfest.json') ):
        shutil.unpack_archive(os.path.join('drivers', 'browsec.zip'), extension_dir)

unzip_to_extension()