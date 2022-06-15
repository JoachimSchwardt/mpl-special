# mpl-special
Special plotting tools using matplotlib

# setup
- add the path to the folder containing the files to your $PYTHONPATH

# how-to
You can import the files like any other python library.
The intended use is
```python
from mpl_special import special, annotate
special.setup(use_tex=True)    # if you want/have latex fonts
```

# list of features
- function to generate the correct figure size for including figures in latex documents without further rescaling
- embed x and y labels into the ticks
- enumerate subplots with captions (a, b, ... )
- plot standalone colorbars for a given heatmap
- annotate point clouds
