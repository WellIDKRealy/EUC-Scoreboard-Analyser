build: build-windows
clean: clean-windows

build-windows:
	guix shell -E DISPLAY --share=/tmp --share=WindowsBuild=/home/${USER} --expose=.=/home/${USER}/main -C -N -F --no-cwd -m windows-manifest.scm -- make

clean-windows:
	guix shell -E DISPLAY --share=/tmp --share=WindowsBuild=/home/${USER} --expose=.=/home/${USER}/main -C -N -F --no-cwd -m windows-manifest.scm -- make clean
