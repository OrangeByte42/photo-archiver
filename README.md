# photography-scripts

"""
Flatten a directory of JPG files into a single directory.

Recursively find all JPG files under the current directory, move them to the root directory, and rename them using a prefix of their path of folder names joined by hyphens, followed by a sequential number with zero-padding of specified width.

Example:
    Root folder: xx1
        xx1/yy1/imgA.jpg
        xx1/yy1/imgB.jpg
        xx1/yy2/photo1.jpg

    Running script with digits=2 will produce in xx1:
        xx1-yy1-01.jpg
        xx1-yy1-02.jpg
        xx1-yy2-01.jpg
"""

