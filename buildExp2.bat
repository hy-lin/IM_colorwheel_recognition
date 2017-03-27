mkdir dist
mkdir dist\Experiments
mkdir dist\Experiments\Experiment2
pyinstaller src\Experiments\Experiment2\continuousColorRecognition2.py -F -i src\Experiments\Experiment2\resources\uzh.ico --distpath dist\Experiments\Experiment2\
mkdir dist\Experiments\Experiment2\resources
copy src\Experiments\Experiment2\resources\*.* dist\Experiments\Experiment2\resources
mkdir dist\Experiments\Experiment2\Data
mkdir dist\Experiments\Experiment2\sdl_dll
copy src\Experiments\Experiment2\sdl_dll\*.* dist\Experiments\Experiment2\sdl_dll