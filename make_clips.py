"""Make video clips (former gifs)"""

import os
from subprocess import run


# set working directory
upload_dir = os.environ['UPLOAD_DIR']
os.chdir(upload_dir)

# parameters for clip extraction
params = {
    'elements': {
        'source': 'landing_video.mp4',
        'start': '00:00:15.75',
        'duration': '00:00:05.00',
    },
    'interactive': {
        'source': 'landing_video.mp4',
        'start': '00:00:22.00',
        'duration': '00:00:15.50',
    },
    'nowait': {
        'source': 'landing_video.mp4',
        'start': '00:00:38.00',
        'duration': '00:00:11.00',
    },
    'constructed': {
        'source': 'landing_video.mp4',
        'start': '00:01:04.50',
        'duration': '00:00:09.00',
    },
    'empire': {
        'source': 'empire_video.mp4',
        'start': '00:01:11.50',
        'duration': '00:00:19.50',
        'speedup': 2,
    },
}

# perform extraction
for ofname, controls in params.items():
    tmp_fname = f"{ofname}-tmp.mp4"
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
            tmp_fname,
        ],
        capture_output=True,
        check=True,
    )
    if 'speedup' in controls:
        tmp_fname2 = 'speedup' + tmp_fname
        run(
            [
                'ffmpeg',
                '-i',
                tmp_fname,
                '-y',
                '-filter:v',
                f"setpts=PTS/{controls['speedup']}",
                tmp_fname2,
            ],
            capture_output=True,
            check=True,
        )
        os.remove(tmp_fname)
        tmp_fname = tmp_fname2
    run(
        [
            'ffmpeg',
            '-i',
            tmp_fname,
            '-y',
            '-vf',
            'tpad=stop_mode=clone:stop_duration=2',
            f'{ofname}_clip.mp4',
        ],
        capture_output=True,
        check=True,
    )
    os.remove(tmp_fname)
