Shoddy is a python utility for downloading files over the internet with the ability to stop a download and pick up where it left off at a later time.

This allows file downloads to be resumed after losing internet connection, switching networks, and between shutdowns. 

> python .\shoddy.py https[]()://releases.ubuntu.com/22.04.1/ubuntu-22.04.1-desktop-amd64.iso

>[+] Downloading file: ubuntu-22.04.1-desktop-amd64.iso<br>
>[+] File size: 3826.83136 MB<br>
>[+] Number of chunks set to: 512<br>
>[\*] Progress: [--->                ] 20%<br>
>[-] Script execution cancelled<br>
>[\*] Chunks completed: 103 / 512<br>

> python .\shoddy.py https[]()://releases.ubuntu.com/22.04.1/ubuntu-22.04.1-desktop-amd64.iso

>[\*] Partial File Found. Resuming Progress at chunk: 103 / 512<br>
>[+] Downloading file: ubuntu-22.04.1-desktop-amd64.iso<br>
>[+] File size: 3826.83136 MB<br>
>[+] Number of chunks set to: 512<br>
>[\*] Progress: [--->                ] 22%<br>