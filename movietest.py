import cv2
import os

def save_frame_range(video_path, start_frame, stop_frame, step_frame,
                     dir_path, basename, ext='png'):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))

    for i in range(start_frame, stop_frame, step_frame):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if ret:
            frame = frame[146:293, 1750:1884]
            cv2.imwrite('{}_{}.{}'.format(base_path, str(i).zfill(digit), ext), frame)
        else:
            return

save_frame_range('movie.mp4',
                 2000, 3000, 12,
                 'result_range', 'img')
