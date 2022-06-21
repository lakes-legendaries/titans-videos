"""Make video clips (former gifs)"""

from __future__ import annotations

import os
from subprocess import run
from time import sleep


# set working directory
upload_dir = os.environ['UPLOAD_DIR']
os.chdir(upload_dir)

# parameters for clip extraction
params = {
    'elements': {
        'source': 'landing_video.h264.mp4',
        'start': '00:00:15.75',
        'duration': '00:00:05.00',
    },
    'interactive': {
        'source': 'landing_video.h264.mp4',
        'start': '00:00:22.00',
        'duration': '00:00:15.50',
    },
    'nowait': {
        'source': 'landing_video.h264.mp4',
        'start': '00:00:38.00',
        'duration': '00:00:11.00',
    },
    'constructed': {
        'source': 'landing_video.h264.mp4',
        'start': '00:01:04.50',
        'duration': '00:00:09.00',
    },
    'empire': {
        'source': 'empire_video.h264.mp4',
        'start': '00:01:11.50',
        'duration': '00:00:19.50',
        'speedup': 2,
    },
}


def crop(name: str, controls: dict[str, str]) -> str:
    """Crop video, return output filename"""
    ofname = f'{name}-cropped.mp4'
    run(
        [
            'ffmpeg',
            '-ss',
            controls['start'],
            '-i',
            controls['source'],
            '-t',
            controls['duration'],
            '-y',
            '-an',
            '-filter:v',
            'crop=1920:1000:0:0',
            ofname,
        ],
        capture_output=True,
        check=True,
    )
    return ofname


def speedup(ifname: str, speedup: int) -> str:
    """Speedup video, return output filename"""
    ofname = f'{ifname}-speedup.mp4'
    run(
        [
            'ffmpeg',
            '-i',
            ifname,
            '-y',
            '-filter:v',
            f"setpts=PTS/{speedup}",
            ofname,
        ],
        capture_output=True,
        check=True,
    )
    return ofname


def add_pause(ifname, ofname):
    """add pause to end of video"""
    run(
        [
            'ffmpeg',
            '-i',
            ifname,
            '-y',
            '-vf',
            'tpad=stop_mode=clone:stop_duration=2',
            ofname,
        ],
        capture_output=True,
        check=True,
    )


# perform extraction
if __name__ == '__main__':
    for name, controls in params.items():

        # try loop to clean up temporary files
        tmp_fname = []
        try:

            # create videos
            tmp_fname.append(crop(name, controls))
            if 'speedup' in controls:
                tmp_fname.append(
                    speedup(tmp_fname[-1], controls['speedup'])
                )
            std_fname = f'{name}_clip.mp4'
            add_pause(tmp_fname[-1], std_fname)

            # convert formats
            dir_path = os.path.dirname(os.path.realpath(__file__))
            run(
                [
                    dir_path + '/' + 'convert',
                    std_fname,
                    upload_dir,
                ],
                capture_output=True,
                check=True,
            )

        # clean up temporary files
        finally:
            while tmp_fname:
                os.remove(tmp_fname.pop())
