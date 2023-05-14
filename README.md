Shoddy is a python utility for downloading files over the internet with the ability to stop a download and pick up where it left off at a later time.

This allows file downloads to be resumed after losing internet connection, switching networks, and between shutdowns. 

> python .\shoddy.py https[]()://old-releases.ubuntu.com/releases/22.04.1/ubuntu-22.04.1-desktop-amd64.iso

>[+] Downloading file: ubuntu-22.04.1-desktop-amd64.iso<br>
>[+] File size: 3826.83136 MB<br>
>[+] Number of chunks set to: 512<br>
>[|] Downloading: 20%
>[-] Script execution cancelled<br>
>[\*] Chunks completed: 103 / 512<br>

> python .\shoddy.py https[]()://old-releases.ubuntu.com/releases/22.04.1/ubuntu-22.04.1-desktop-amd64.iso

>[\*] Found existing download. Resuming Progress at chunk: 103 / 512<br>
>[+] Downloading file: ubuntu-22.04.1-desktop-amd64.iso<br>
>[+] File size: 3826.83136 MB<br>
>[+] Number of chunks set to: 512<br>
>[-] Downloading: 22%<br>