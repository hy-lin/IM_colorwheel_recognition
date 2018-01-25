mkdir dist
mkdir dist\Experiments
mkdir dist\Experiments\Experiment3
pyinstaller src\Experiments\Experiment3\recallNrecognition.py -F -i src\Experiments\Experiment3\resources\uzh.ico --distpath dist\Experiments\Experiment3\
mkdir dist\Experiments\Experiment3\resources
copy src\Experiments\Experiment3\resources\*.* dist\Experiments\Experiment3\resources
mkdir dist\Experiments\Experiment3\Data