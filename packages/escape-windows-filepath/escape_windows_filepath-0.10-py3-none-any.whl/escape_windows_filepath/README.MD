# Escaping file paths (Windows) without crying and losing one's mind

## pip install escape-windows-filepath

### Tested against Windows 10 / Python 3.10 / Anaconda 

```python
# How it is usually done:
import os
videopathraw = r"C:\baba ''bubu\bab xx\2020-11-23 13-05-26.mp4"
vlcpathraw = r"C:\Program Files\VideoLAN\VLC\vlc.exe"

# Quite frequently something like this surprisingly works, but in this example it doesn't:
videofilenotwellescaped = '"' + r"C:\baba ''bubu\bab xx\2020-11-23 13-05-26.mp4" + '"'
vlcpathnotwellescaped = '"' + r"C:\Program Files\VideoLAN\VLC\vlc.exe" + '"'
escapedcmdnotgood = rf"{vlcpathnotwellescaped} {videofilenotwellescaped}"
print(f"{escapedcmdnotgood=}")
os.system(escapedcmdnotgood)

# Output:
# escapedcmdnotgood='"C:\\Program Files\\VideoLAN\\VLC\\vlc.exe" "C:\\baba \'\'bubu\\bab xx\\2020-11-23 13-05-26.mp4"'
# 'C:\Program' is not recognized as an internal or external command,
# operable program or batch file.


from escape_windows_filepath import escape_windows_path

# The safest method is escaping evey single part (folder,file) of the path
videofileescaped = escape_windows_path(videopathraw)
vlcpath = escape_windows_path(vlcpathraw)
escapedcmd = rf"{vlcpath} {videofileescaped}"
print(f"{escapedcmd=}")
os.system(escapedcmd)
# Output
# escapedcmd='C:\\"Program Files"\\"VideoLAN"\\"VLC"\\"vlc.exe" C:\\"baba \'\'bubu"\\"bab xx"\\"2020-11-23 13-05-26.mp4"'
# And the video player opens

```