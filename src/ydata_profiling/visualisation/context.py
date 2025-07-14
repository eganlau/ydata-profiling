import contextlib
import warnings
from typing import Any
import platform
import os

import matplotlib
import seaborn as sns
from pandas.plotting import (
    deregister_matplotlib_converters,
    register_matplotlib_converters,
)


def configure_matplotlib_for_cjk():
    """
    Configure matplotlib to properly display Chinese characters in plots.
    """
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm
    
    system = platform.system()
    
    # Define font search priorities by platform
    if system == 'Darwin':  # macOS
        potential_fonts = [
            '/System/Library/Fonts/PingFang.ttc',
            '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
            '/Library/Fonts/Arial Unicode.ttf',
            '/System/Library/Fonts/STHeiti Light.ttc',
            '/System/Library/Fonts/Helvetica.ttc',
            '/Library/Fonts/Microsoft/SimHei.ttf',
            '/Library/Fonts/Microsoft/SimSun.ttf',
        ]
        fallback_fonts = ['PingFang SC', 'Arial Unicode MS', 'STHeiti', 'Helvetica', 'sans-serif']
    elif system == 'Windows':
        potential_fonts = [
            'C:\\Windows\\Fonts\\simhei.ttf',
            'C:\\Windows\\Fonts\\simsun.ttc',
            'C:\\Windows\\Fonts\\msyh.ttc'
        ]
        fallback_fonts = ['Microsoft YaHei', 'SimHei', 'Arial', 'sans-serif']
    elif system == 'Linux':
        potential_fonts = [
            '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
            '/usr/share/fonts/truetype/arphic/ukai.ttc',
            '/usr/share/fonts/truetype/arphic/uming.ttc',
        ]
        fallback_fonts = ['DejaVu Sans', 'Liberation Sans', 'sans-serif']
    else:
        potential_fonts = []
        fallback_fonts = ['DejaVu Sans', 'Liberation Sans', 'sans-serif']

    # Try to find an existing font file and get its name
    for path_option in potential_fonts:
        if os.path.exists(path_option):
            try:
                font_prop = fm.FontProperties(fname=path_option)
                font_name = font_prop.get_name()
                if font_name and font_name != 'unknown':
                    return [font_name] + fallback_fonts
            except Exception:
                continue
    
    # If no font files found, return fallbacks
    return fallback_fonts


@contextlib.contextmanager
def manage_matplotlib_context() -> Any:
    """Return a context manager for temporarily changing matplotlib unit registries and rcParams."""
    originalRcParams = matplotlib.rcParams.copy()

    # Get cross-platform font configuration
    cjk_fonts = configure_matplotlib_for_cjk()

    # Credits for this style go to the ggplot and seaborn packages.
    #   We copied the style file to remove dependencies on the Seaborn package.
    #   Check it out, it's an awesome library for plotting
    customRcParams = {
        "patch.facecolor": "#348ABD",  # blue
        "patch.antialiased": True,
        "font.size": 10.0,
        "figure.edgecolor": "0.50",
        # Seaborn common parameters
        "figure.facecolor": "white",
        "text.color": ".15",
        "axes.labelcolor": ".15",
        "legend.numpoints": 1,
        "legend.scatterpoints": 1,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.color": ".15",
        "ytick.color": ".15",
        "axes.axisbelow": True,
        "image.cmap": "Greys",
        "font.family": ["sans-serif"],
        "font.sans-serif": cjk_fonts,
        "grid.linestyle": "-",
        "lines.solid_capstyle": "round",
        # Seaborn darkgrid parameters
        # .15 = dark_gray
        # .8 = light_gray
        "axes.grid": True,
        "axes.facecolor": "#EAEAF2",
        "axes.edgecolor": "white",
        "axes.linewidth": 0,
        "grid.color": "white",
        # Seaborn notebook context
        "figure.figsize": [8.0, 5.5],
        "axes.labelsize": 11,
        "axes.titlesize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "grid.linewidth": 1,
        "lines.linewidth": 1.75,
        "patch.linewidth": 0.3,
        "lines.markersize": 7,
        "lines.markeredgewidth": 0,
        "xtick.major.width": 1,
        "ytick.major.width": 1,
        "xtick.minor.width": 0.5,
        "ytick.minor.width": 0.5,
        "xtick.major.pad": 7,
        "ytick.major.pad": 7,
        "backend": "agg",
        "axes.unicode_minus": False,
    }
    


    try:
        register_matplotlib_converters()
        matplotlib.rcParams.update(customRcParams)
        # sns.set_theme(style="white", font="STHeiti")        
        # Use the first font from our CJK font list for seaborn
        sns.set_theme(style="white", font=cjk_fonts[0])
        yield
    finally:
        deregister_matplotlib_converters()  # revert to original unit registries
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore", category=matplotlib.MatplotlibDeprecationWarning
            )
            matplotlib.rcParams.update(originalRcParams)  # revert to original rcParams
            
