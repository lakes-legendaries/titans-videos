"""Reorder frames to speed up animation"""

from subprocess import run


class Renumber:
    """Renumber frames to speed up animation
    
    Parameters
    ----------
    orig_count: int, optional, default=420
        original frame count
    new_count: int, optional, default=300
        new frame count
    input: str, optional, default='raw/Title'
        input filenames (without ####.png)
    output: str, optional, default='Title'
        output filenames (without ####.png)
    """
    def __init__(
        self,
        /,
        orig_count = 420,
        new_count = 300,
        *,
        fname: str = '/mnt/d/vframe/Title',
    ):
        for new_frame in range(new_count):
            old_frame = int(orig_count / new_count * new_frame)
            old_fname = f'{fname}{old_frame:04d}.png'
            new_fname = f'{fname}{new_frame:04d}.png'
            run(['cp', old_fname, new_fname])
        for old_frame in range(new_count, orig_count):
            run(['rm', f'{fname}{old_frame:04d}.png'])


if __name__ == '__main__':
    Renumber()
