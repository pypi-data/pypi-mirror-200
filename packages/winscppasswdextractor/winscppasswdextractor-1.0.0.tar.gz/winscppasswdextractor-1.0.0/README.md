# WinSCP Password Extractor
WinSCP stores ssh session passwords in an encoded format in either the registry or a file called WinSCP.ini.
This python script searches in the winscp default locations to extract stored credentials.

These default file locations are:
- %APPDATA%\WinSCP.ini
- %USER%\Documents\WinSCP.ini

## Usage
You can either specify a file path if you know the exact path to an existing WinSCP.ini file or you let the tool itself look if any credentials are stored in the default locations.
```python3
python WinSCPPwdDump.py
python WinSCPPwdDump.py <path-to-file>
```

## About
This Tool is based on the work of [winscppasswd](https://github.com/anoopengineer/winscppasswd), the ruby winscp parser from [Metasploit-Framework](https://github.com/rapid7/metasploit-framework) and the awesome work from [winscppassword](https://github.com/dzxs/winscppassword).

They did the hard stuff
