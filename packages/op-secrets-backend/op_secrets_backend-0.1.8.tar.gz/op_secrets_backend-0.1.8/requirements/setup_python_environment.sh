#!/bin/bash -i

# install UBUNTU dependencies for pyenv
sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev python-openssl

# install pyenv
if command -v pyenv 1>/dev/null 2>&1;
then
  echo "INFO: pyenv already installed"
else
  curl https://pyenv.run | bash
  echo -e '\nexport PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
  echo -e '\nif command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc
  source ~/.bashrc
fi

# install python_version ($1) and activate virtualenv
pyenv install --skip-existing $1
pyenv global $1
sudo pip install --quiet pipenv
pipenv --venv
PIPENV_CHECK=$?
if [ $PIPENV_CHECK -eq 1 ];
then
  pipenv shell --python $1
else
  pipenv shell --python $1
fi
