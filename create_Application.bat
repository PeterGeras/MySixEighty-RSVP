@ECHO OFF

pyinstaller --onefile mysixeighty-rsvp.py

:: Remake Application folder
rmdir /q /s Application
md Application
move dist\mysixeighty-rsvp.exe Application\mysixeighty-rsvp.exe
md Application\drivers
copy drivers\geckodriver* Application\drivers
md Application\logs
copy NUL Application\logs\geckodriver.log
copy events_selection.xlsx Application\events_selection.xlsx

del mysixeighty-rsvp.spec
rmdir /q /s build
rmdir /q /s dist