PYTHON_DIR="/home/${USER}/.wine/drive_c/users/${USER}/AppData/Local/Programs/Python/Python310"
MAIN_DIR="/home/${USER}/main"
WINE=wine64
WINEDEBUG=-all

.EXPORT_ALL_VARIABLES:

package: pyinstaller depedencies python
	cd ${MAIN_DIR} && ${WINE} ${PYTHON_DIR}/python.exe ${PYTHON_DIR}/Scripts/pyinstaller.exe main.py

pyinstaller: python pip
	cd ${PYTHON_DIR} && ${WINE} python.exe Scripts/pip.exe install pyinstaller

depedencies: pip
	cd ${PYTHON_DIR} && ${WINE} python.exe Scripts/pip.exe -r /home/${USER}/requirements.txt

pip: python
	cd ${PYTHON_DIR} && ${WINE} python.exe Scripts/pip.exe install --upgrade pip

python: python3.exe
	if ! [ -d ${PYTHON_DIR} ]; then\
		${WINE} python3.exe /quiet ; \
	fi

python3.exe:
	if ! [ -f "python3.exe" ]; then curl https://www.python.org/ftp/python/3.10.7/python-3.10.7-amd64.exe > python3.exe; fi

clean:
	rm python3.exe
	rm .cache
	rm .config
	rm .bash_history
	rm .local
	rmdir main
	rm -rf "/home/${USER}/.wine"
