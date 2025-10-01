Usage:

First install the following packages:

    curl https://sh.rustup.rs -sSf | sh

    "${SHELL}" <(curl -L micro.mamba.pm/install.sh)

    apt install tesseract-ocr

    apt-get install ccache

Then run the following commands to create a virtual environment to run our programs in:

    micromamba create -p .venv 'python==3.12'
    micromamba activate .venv

Optionally if you are running the EnergiBridge configuration

    sudo chgrp -R $USER /dev/cpu/*/msr;
    
    sudo chmod g+r /dev/cpu/*/msr;

Finally from our root folder you can run the following to get started:

    pip install -r requirements.txt

For the run itself, first let the laptop sit for 30 minutes, and afterwards just either of the following:
    
    sudo /home/username/micromamba/envs/.venv/bin/python experiment-runner RunnerConfig_EnergiBridge.py
    
    sudo /home/username/micromamba/envs/.venv/bin/python experiment-runner RunnerConfig_PowerJoular.py
