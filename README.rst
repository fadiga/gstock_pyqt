

GSTOCK ===

GSTOCK is a simple desktop application used to track expenses on accounts credited periodicaly.

It's main purpose is to be used at government agencies receiving bugets. It thus don't handle revenue.
Requirements

PyQT4
    sudo aptitude install python-qt4
SQLAlchemy 0.6.6 with SQLite

    pip install SQLAlchemy==0.6.6

    pip install pysqlite

    sudo aptitude install sqlite3
ReportLab 2.4
    pip install reportlab==2.4
gettext
    sudo aptitude install gettext
xlwt
    pip install xlwt==0.7.2

Windows

You need a working windows environment to build GSTOCK windows packageL

    nsis-2.46-setup.exe

    pywin32-210.win32-py2.6.exe

    py2exe-0.6.9.win32-py2.6.exe

    PyQt-Py2.6-x86-gpl-4.8.3-1.exe

    pysqlite-2.6.0.win32-py2.6.exe

    python-2.6.6.msi (add C:Python26 to PATH)

    xlwt-0.7.2.win32.exe

    reportlab-2.5.win32-py2.6.exe

    setuptools-0.6c11.win32-py2.6.exe

    easy_install SQLAlchemy==0.6.6
Once setup, create windows executable:

    copy ..\resources\microsoftdll\*.dll .

    copy ..\resources\microsoftdll\*.man* .

    python.exe setup-win.py py2exe

If you want a single executable (everything inside ; faster):

    set PY2EXEMODE=single ; python.exe setup-win.py py2exe 

Once windows binary is complete, create installer with:
    makensis.exe installer.nsi


