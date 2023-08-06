# fe-openedx-alerts

A command line tool that send alerts if any Open edX service failasticsearch service is active



## Python version

Python: 3.9.16


## Poetry Configuration

```bash
# https://test.pypi.org/
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi PYPI_TEST_TOKEN
```


## Open edX Instance

```bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
export PATH=/home/ubuntu/.pyenv/bin:$PATH
pyenv install 3.9.16
pyenv global 3.9.16

/home/ubuntu/.pyenv/versions/3.9.16/bin/pip3 install fe-openedx-alerts
```
