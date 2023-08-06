import winsdk.windows.media.ocr as ocr
import winsdk.windows.graphics.imaging as imaging
import winsdk.windows.storage.streams as streams
from flatten_everything import flatten_everything, ProtectedTuple
from kthread_sleep import sleep
import pandas as pd
from a_cv_imwrite_imread_plus import open_image_in_cv
from dataclasses import dataclass
from typing import List
from callpyfile import to_stdout
from pathos.multiprocessing import ProcessingPool as Pool
import time


@dataclass
class OcrWord:
    text: str
    left: float
    top: float
    width: float
    height: float


@dataclass
class OcrLine:
    words: List[OcrWord]


@dataclass
class OcrResult:
    lines: List[OcrLine]


class OcrBackend:
    def run_ocr(self, image) -> OcrResult:
        raise NotImplementedError()


def resa(engine, bitmap):
    result = engine.recognize_async(bitmap)
    while not result.status.value:
        sleep(0.1)
        continue
    return result


def get_installed_languages():
    return {
        engine.language_tag: ocr.OcrEngine.try_create_from_language(engine)
        for engine in ocr.OcrEngine.get_available_recognizer_languages()
    }


class WinRtBackend(OcrBackend):
    # Based on: https://github.com/wolfmanstout/screen-ocr/blob/master/screen_ocr/_winrt.py
    def __init__(self, language_tag: str = None):
        pass

    def run_ocr_async(self, image):
        language, ini, image = image
        try:
            engine = ocr.OcrEngine.try_create_from_language(
                get_installed_languages()[language]
            )
        except Exception as fe:
            engine = ocr.OcrEngine.try_create_from_user_profile_languages()
        image = open_image_in_cv(image, channels_in_output=4, bgr_to_rgb=True)
        bytesx = image.tobytes()
        data_writer = streams.DataWriter()
        bytes_list = bytearray(bytesx)

        del bytesx
        data_writer.write_bytes(bytes_list)

        del bytes_list
        bitmap = imaging.SoftwareBitmap(
            imaging.BitmapPixelFormat.RGBA8, image.shape[1], image.shape[0]
        )

        bitmap.copy_from_buffer(data_writer.detach_buffer())
        del data_writer
        result = resa(engine, bitmap)
        df = pd.DataFrame(
            list(
                flatten_everything(
                    [
                        [
                            ProtectedTuple(
                                (
                                    yy.text,
                                    yy.bounding_rect.x,
                                    yy.bounding_rect.y,
                                    yy.bounding_rect.width,
                                    yy.bounding_rect.height,
                                    xx.text,
                                )
                            )
                            for yy in xx.words
                        ]
                        for xx in result.get_results().lines
                    ]
                )
            )
        )
        df.columns = ["text", "left", "top", "width", "height", "sentence"]
        df["middle_x"] = df.left + (df.width // 2)
        df["middle_y"] = df.top + (df.height // 2)
        df["conf"] = 1
        df["start_x"] = df.left
        df["start_y"] = df.top
        df["end_x"] = df.left + df.width
        df["end_y"] = df.top + df.height
        df["im_index"] = ini
        try:
            result.close()
            del result
        except Exception as fe:
            pass
        return df


def get_dataframe(pi):
    aba = WinRtBackend()
    return aba.run_ocr_async(pi)


@to_stdout(kill_if_exception=True)
def start_winrt_ocr():
    pool = Pool(nodes=cpus)
    res = pool.amap(get_dataframe, imagelist)
    while not res.ready():
        time.sleep(0.05)
    allb = res.get()
    return allb


if __name__ == "__main__":
    dfs = start_winrt_ocr()
