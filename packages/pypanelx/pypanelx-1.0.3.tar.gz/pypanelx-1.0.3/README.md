# __PyPanelX Project__
The goal for this project it's to write a full python panel cli with tools for what it's call "Data Hoarding" or backups if you think in another ways(?)
## __Tools?__
Yes, tools or addons that you can write thanks to modular construction of PyPanel
## __List of tools:__
- __iltools:__ Using the powerfull [Instaloader Python Module](https://instaloader.github.io/as-module.html) i write this for a better archiving of a instagram media.
- __meditor:__ [***Option 4***] (Currently working only in windows): this is a monaco-editor and electron executable, whith save option `(Ctrl or CMD + S)`  (send a POST Req to a flask server)
- __serviceWorker:__ [***Option 4***]: will be a flask based server for handle DB, Files and other kind of things.

## __Usage:__
### From __pypi:__
```
pip install pypanelx
```
### __Build and install by yourself:__
```
git clone https://github.com/jamesphoenixcode/pypanelxl.git
cd pypanelx
pip install setuptool wheel
python setup.py sdist bdist_wheel
```
### __Install__ in your __system:__
```
pip install ./dist/pypanelx-1.0.3-py3-none-any.whl
```
### __Then:__
```
instaloader -l userNameUsedToDownload
pypanelx
```
Files will be downloaded inside __"pypanelMedia, pypanelFiles"__ in the directory where pypanel has been executed.

`thanks to coffee and weed i write the most base code in one sunday (03/26/2023)`