from PIL import Image


def create_gif(
    ifname: str,
    frames: list[int],
    ofname: str,
):
    """Create GIF

    Inputs frames are denoted as
    :code:`f'/mnt/d/vframe/{ifname}{frame:04d}.png'`

    Output frames are saved to
    :code:`f'/mnt/d/OneDrive/Titans Of Eden/website/media/{ofname}'`

    Parameters
    ----------
    ifname: str
        input root filename
    frames: array-like
        frames to inclue
    ofname: str
        output filename
    """
    frames = list(frames)
    for i in range(3):
        frames.append(frames[-1])
    images = (
        Image.open(fname).convert('RGB').convert('P')
        for fname in [
            f'/mnt/d/vframe/{ifname}{frame:04.0f}.png'
            for frame in frames
        ]
    )
    next(images).save(
        fp=f'/mnt/d/OneDrive/Titans Of Eden/website/media/{ofname}',
        format='GIF',
        append_images=images,
        include_color_table=True,
        save_all=True,
        duration=200,
        loop=0,
    )


if __name__ == '__main__':
    create_gif('Empire Anim', range(2010, 3200, 15), 'empire.gif')
    create_gif('Gif - Constructed', range(2970, 3511, 10), 'constructed.gif')
    create_gif('Gif - Interactive', range(900, 1250, 10), 'cycle.gif')
    create_gif('Gif - Interactive', range(1300, 2251, 10), 'interactive.gif')
