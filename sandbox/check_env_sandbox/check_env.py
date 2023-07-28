import os
import platform
import sys

def get_environment_details():
    print(f'Operating System: {platform.system()} {platform.release()}')
    print(f'Python Version: {platform.python_version()}')
    
    print('Python Path: ', sys.path)
    print('Environment Variables: ')
    for k, v in os.environ.items():
        print(f'{k}: {v}')

get_environment_details()

import subprocess

def get_ffmpeg_version():
    result = subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE)
    print('FFmpeg Version:')
    print(result.stdout.decode('utf-8'))

get_ffmpeg_version()

