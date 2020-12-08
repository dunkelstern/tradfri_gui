PYTHON_VERSION=$(python -V|sed -e 's/Python \([0-9]*\.[0-9]*\)\..*/\1/')
export PYTHONOPTIMIZE=1

if [ "$1" = "" ] ; then
    MODE='--onefile'
else
    MODE="$1"
fi

pyinstaller \
    --name="TradfriGUI" \
    --add-data "$VIRTUAL_ENV/lib/python${PYTHON_VERSION}/site-packages/pytradfri/VERSION:pytradfri" \
    --add-data "icons/settings.png:icons" \
    --add-data "icons/settings@2x.png:icons" \
    $MODE \
    --noupx \
    -y src/main.py
