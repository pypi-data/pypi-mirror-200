# Converts an image to .ico - Windows 

## pip install convpic2ico

### Tested against Windows 10 / Python 3.10 / Anaconda 


```python
from convpic2ico import create_icon

coloredicon = create_icon(
    imagepath=r"C:\Users\hansc\Downloads\pinpng.com-anime-girl-face-png-6144106.png",
    magickpath=r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe",
)


coloredicon
Out[3]: 'C:\\Users\\hansc\\Downloads\\tmptmpappicon_color.ico'


```