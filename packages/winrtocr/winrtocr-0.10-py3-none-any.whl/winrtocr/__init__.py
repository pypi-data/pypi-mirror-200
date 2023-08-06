import pandas as pd
import winsdk.windows.media.ocr as ocr
from PrettyColorPrinter import add_printer
import os
import sys
import pandas as pd
import cv2
import pathos
from callpyfile import run_py_file
from a_cv_imwrite_imread_plus import open_image_in_cv
add_printer(1)


here = os.path.abspath(os.path.dirname(__file__))
executefile = os.path.normpath(os.path.join(here, "call3.py"))


def winrtocr(
    pics,
    language="en-US",
    cpus=4,
):
    allpics = [
        (
            language,
            y,
            open_image_in_cv(x),
        )
        for y, x in enumerate(pics)
    ]

    dfa = run_py_file(
        variables={"imagelist": allpics, "cpus": cpus},
        pyfile=executefile,
        activate_env_command="",
        pythonexe=sys.executable,
        raise_exception=False,
    )
    return [x for x in zip(dfa, pics)]


def get_installed_languages():
    return {
        engine.language_tag: ocr.OcrEngine.try_create_from_language(engine)
        for engine in ocr.OcrEngine.get_available_recognizer_languages()
    }


def _winrt_ocr(imagelist, cpus=4, language="en-US", return_pic=False):
    if isinstance(imagelist, str):
        imagelist = [imagelist]
    imagelist = [open_image_in_cv(x, channels_in_output=4) for x in imagelist]
    fax = winrtocr(
        imagelist,
        language=language,
        cpus=cpus,
    )
    if not return_pic:
        return pd.concat([x[0] for x in fax], ignore_index=True)
    return fax


def winrt_ocr_df(
    imagelist,
    cpus=4,
    language="en-US",
):
    dfa = _winrt_ocr(imagelist, cpus=cpus, language=language, return_pic=False)
    for c in [
        "left",
        "top",
        "width",
        "height",
        "middle_x",
        "middle_y",
        "conf",
        "start_x",
        "start_y",
        "end_x",
        "end_y",
        "im_index",
    ]:
        try:
            dfa[c] = dfa[c].astype("Int64")
        except Exception:
            continue
    return dfa


def winrt_ocr_df_and_pics(
    imagelist,
    cpus=4,
    language="en-US",
):
    return _winrt_ocr(imagelist, cpus=cpus, language=language, return_pic=True)


class WinRTocr:
    def __init__(self, cpus=4, language="en-US"):
        self.language = language
        self.cpus = cpus

    @staticmethod
    def get_installed_languages():
        return list(get_installed_languages().keys())

    def get_ocr_df(self, imagelist):
        return winrt_ocr_df(
            imagelist,
            cpus=self.cpus,
            language=self.language,
        )

    def get_ocr_df_and_pics(self, imagelist):
        return winrt_ocr_df_and_pics(
            imagelist,
            cpus=self.cpus,
            language=self.language,
        )

