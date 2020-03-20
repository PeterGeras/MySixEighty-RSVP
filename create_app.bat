@ECHO OFF

del mysixeighty-rsvp.exe
del mysixeighty-rsvp.spec
rmdir /q /s build
rmdir /q /s dist

pyinstaller --onefile mysixeighty-rsvp.py

del mysixeighty-rsvp.exe
move .\dist\mysixeighty-rsvp.exe .
del mysixeighty-rsvp.spec
rmdir /q /s build
rmdir /q /s dist

move mysixeighty-rsvp.exe Application.exe