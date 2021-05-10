import warnings
import matplotlib as mpl


class ConfigDict(dict):
    """Dictionary that raises KeyError when trying to create new keys."""

    def __setitem__(self, key, val):
        """Raises:
        KeyError: If 'key' is not an existing key in the dictionary.
        """
        if key not in self.keys():
            raise KeyError(
                f"Key '{key}' is not a valid key. " f"Valid keys: {[*self.keys()]}."
            )
        else:
            super().__setitem__(key, val)


def update_rcparams(
    fontfamily="monospace",
    fontsize=12,
    labelsize="medium",
    titlesize="large",
    titlepad=30,
    facecolor="white",
    edgecolor="black",
    linewidth=1,
    xmargin=0,
    ymargin=0,
    xtickmajorsize=0,
    ytickmajorsize=0,
    pcolormeshsnap=True,
    dpi=100,
    rc_params_dict=None,
):
    """Wrapper around mpl.rcParams dict to easily set some key settings."""
    rc_params_dict = rc_params_dict or {}
    rcmod = ConfigDict(mpl.rcParams)
    rcmod["font.family"] = fontfamily
    rcmod["font.size"] = fontsize
    rcmod["axes.labelsize"] = labelsize
    rcmod["axes.titlesize"] = titlesize
    rcmod["axes.titlepad"] = titlepad
    rcmod["axes.facecolor"] = facecolor
    rcmod["axes.edgecolor"] = edgecolor
    rcmod["axes.linewidth"] = linewidth
    rcmod["axes.xmargin"] = xmargin
    rcmod["axes.ymargin"] = ymargin
    rcmod["xtick.major.size"] = xtickmajorsize
    rcmod["ytick.major.size"] = ytickmajorsize
    rcmod["pcolormesh.snap"] = pcolormeshsnap
    rcmod["figure.dpi"] = dpi
    rcmod.update(rc_params_dict)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", mpl.cbook.MatplotlibDeprecationWarning)
        mpl.rcParams.update(rcmod)
