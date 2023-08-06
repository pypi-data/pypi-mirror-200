import cv2
import tempfile
import os

from typing import Union
from pathlib import Path
from uuid import uuid4
from intelliprove.api.exceptions import MediaException

def is_valid_image_path(im_path: Union[Path, str]) -> bool:
    im_path = Path(im_path) if isinstance(im_path, str) else im_path
    return im_path.is_file() and im_path.suffix.lower() in ('.png', '.jpg', '.jpeg')


def is_valid_video_path(vid_path: Union[Path, str]) -> bool:
    im_path = Path(vid_path) if isinstance(vid_path, str) else vid_path
    return im_path.is_file() and im_path.suffix.lower() in ('.mp4', '.m4v', '.h264', '.mov', '.avi')

def is_valid_video_codec(vid_path: Union[Path, str]) -> bool:
    im_path = str(vid_path) if isinstance(vid_path, Path) else vid_path
    cap = None
    try:
        cap = cv2.VideoCapture(im_path)
        h = int(cap.get(cv2.CAP_PROP_FOURCC))
        codec = chr(h&0xff) + chr((h>>8)&0xff) + chr((h>>16)&0xff) + chr((h>>24)&0xff)
        supported_codecs = (
            'mpeg-4',
            'mp4v',
            'mp4a',
            'hvec',
            'h264',
            'x264',
            'x265',
            'vp8',
            'vp9',
            'av1',
            'avc1'
        ) if os.environ.get('UNITTEST_MODE', 'off') == 'off' else (
            'h264',
            'x265'
        )
        
        return codec.lower() in supported_codecs
    except:
        return False
    
    finally:
        if cap:
            cap.release()


def get_first_video_frame(video_path: Union[Path, str]) -> Path:
    video_path = str(video_path)

    cap = cv2.VideoCapture(video_path)
    cap.open(video_path)
    success, image = cap.read()
    if not success:
        raise Exception(f'Could not read first frame from video. Video path: {video_path}')

    tempdir = tempfile.gettempdir()
    filename = f"{uuid4().hex}_video_frame.jpg"
    temppath = os.path.join(tempdir, filename)

    cv2.imwrite(temppath, image)

    return Path(temppath)


def check_file_size(path: Union[Path, str], format: str = "bytes") -> float:
    path = Path(path) if isinstance(path, str) else path
    if not path.exists() or not path.is_file():
        raise MediaException("The given path is not a valid path or is not a file.", path)

    size = float(os.path.getsize(path))
    if format.lower() == "kb":
        size /= 10e2
    elif format.lower() == "mb":
        size /= 10e4
    elif format.lower() == "gb":
        size /= 10e7

    return size
