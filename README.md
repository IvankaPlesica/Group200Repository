curl https://sh.rustup.rs -sSf | sh

"${SHELL}" <(curl -L micro.mamba.pm/install.sh)

apt install tesseract-ocr

apt-get install ccache

git clone https://github.com/tdurieux/EnergiBridge.git

sudo chgrp -R $USER /dev/cpu/*/msr;
sudo chmod g+r /dev/cpu/*/msr;

micromamba create -p .venv 'python==3.12'
micromamba activate .venv

uv pip install -r requirements.txt

cd datasets

uv run python run_paddle.py