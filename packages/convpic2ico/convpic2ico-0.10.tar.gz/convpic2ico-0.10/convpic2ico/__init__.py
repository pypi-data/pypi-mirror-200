import inspect
import os
import subprocess
import tempfile
from copy import deepcopy
from PIL import Image
from touchtouch import touch


def copy_func(f):
    if callable(f):
        if inspect.ismethod(f) or inspect.isfunction(f):
            g = lambda *args, **kwargs: f(*args, **kwargs)
            t = list(filter(lambda prop: not ("__" in prop), dir(f)))
            i = 0
            while i < len(t):
                setattr(g, t[i], getattr(f, t[i]))
                i += 1
            return g
    dcoi = deepcopy([f])
    return dcoi[0]


def create_icon(imagepath, magickpath="magick"):
    fo = os.path.dirname(imagepath)
    pic = Image.open(imagepath)
    pic2 = pic.resize((256, 256))

    temppic, refu = get_tmpfile(suffix=f".bmp")
    try:
        pic2.save(temppic)
    except Exception:
        pic2.convert("RGB").save(temppic)
    origimagepath = imagepath
    origimagepathfilename = origimagepath.split(os.sep)[-1]
    origimagepathfilenamenoex = ".".join(origimagepathfilename.split(".")[:-1])
    imagepath = temppic

    nameiconfile = os.path.normpath(os.path.join(fo, "tmptmpappicon_color.ico"))
    nameiconfile_bw = os.path.normpath(os.path.join(fo, "tmptmpappicon_bw.ico"))

    write_icon_file(imagepath, nameiconfile, nameiconfile_bw, magickpath=magickpath)
    nameiconfileren = os.path.join(
        os.path.dirname(nameiconfile), f"{origimagepathfilenamenoex}.ico"
    )
    nameiconfile_bwren = os.path.join(
        os.path.dirname(nameiconfile_bw), f"{origimagepathfilenamenoex}_bw.ico"
    )


    try:
        if os.path.exists(nameiconfileren):
            try:
                os.remove(nameiconfileren)
            except Exception:
                pass
        os.rename(nameiconfile, nameiconfileren)
    except Exception as fe:
        print(fe)
        pass
    #os.rename(nameiconfile_bw, nameiconfile_bwren)

    try:
        refu()
    except Exception as fe:
        print(fe)
        pass

    return nameiconfile  # , nameiconfile_bw
    # return nameiconfile, nameiconfile_bw


class FlexiblePartialOwnName:
    r"""
    FlexiblePartial(
            remove_file,
            "()",
            True,
            fullpath_on_device=x.aa_fullpath,
            adb_path=adb_path,
            serialnumber=device,
        )
    """

    def __init__(
        self, func, funcname: str, this_args_first: bool = True, *args, **kwargs
    ):
        self.this_args_first = this_args_first
        self.funcname = funcname
        try:
            self.f = copy_func(func)
        except Exception:
            self.f = func
        try:
            self.args = copy_func(list(args))
        except Exception:
            self.args = args

        try:
            self.kwargs = copy_func(kwargs)
        except Exception:
            try:
                self.kwargs = kwargs.copy()
            except Exception:
                self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        newdic = {}
        newdic.update(self.kwargs)
        newdic.update(kwargs)
        if self.this_args_first:
            return self.f(*self.args, *args, **newdic)

        else:
            return self.f(*args, *self.args, **newdic)

    def __str__(self):
        return self.funcname

    def __repr__(self):
        return self.funcname


def _get_remove_file(file):
    return FlexiblePartialOwnName(os.remove, f"os.remove({repr(file)})", True, file)


def get_tmpfile(suffix=".bin"):
    tfp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    filename = tfp.name
    filename = os.path.normpath(filename)
    tfp.close()
    touch(filename)
    return filename, _get_remove_file(filename)


def write_icon_file(imagepath, nameiconfile, nameiconfile_bw, magickpath="magick"):
    magickpath = os.path.normpath(magickpath)
    magick_convert_command = f'"{magickpath}" convert'
    different_sizes = [16, 32, 128, 256]
    iconcmd = magick_convert_command
    todelete = []
    for size in different_sizes:
        t, dt = get_tmpfile(".png")
        t = os.path.normpath(f"{os.sep}".join(t.split(os.sep)[:-1]))
        path = os.path.normpath(os.path.join(t, f"{size}x{size}_temppic.png"))
        todelete.append(path)
        magick_convert_command1 = (
            f"{magick_convert_command} {imagepath} -resize {size}x{size} {path}"
        )
        subprocess.run(magick_convert_command1, shell=True)
        iconcmd = iconcmd + f" {imagepath}"

    iconcmd = iconcmd + f" {nameiconfile}"
    subprocess.run(iconcmd, shell=True)
    # magick_convert_command2 = (
    #    f'"{magickpath}" convert {nameiconfile} -colorspace Gray {nameiconfile_bw}'
    # )
    # subprocess.run(magick_convert_command2,shell=True)

    for path in todelete:
        try:
            os.remove(path)
        except Exception as Fehler:
            print(Fehler)

    return imagepath, nameiconfile, nameiconfile_bw
