# NFT-video-toolset
This first version loops videos by duplicating then reversing the duplicate then combining. Simple tool for NFTs.

As seen in some of the collections here:
https://opensea.io/MattyJacks

Will add specific links later.








Bug Fixing:

If you get:

  File "c:\programming7\python-3-12-1\Lib\site-packages\moviepy\video\fx\resize.py", line 37, in resizer
    resized_pil = pilim.resize(newsize[::-1], Image.ANTIALIAS)
                                              ^^^^^^^^^^^^^^^
AttributeError: module 'PIL.Image' has no attribute 'ANTIALIAS'


Manually Fix the Code in moviepy:

Navigate to the moviepy library folder where the error originates. According to your error message, it's located here:
vbnet
Copy code
c:\programming7\python-3-12-1\Lib\site-packages\moviepy\video\fx\resize.py
Open this file and locate the following line:
python
Copy code
resized_pil = pilim.resize(newsize[::-1], Image.ANTIALIAS)
Replace Image.ANTIALIAS with Image.Resampling.LANCZOS:
python
Copy code
resized_pil = pilim.resize(newsize[::-1], Image.Resampling.LANCZOS)