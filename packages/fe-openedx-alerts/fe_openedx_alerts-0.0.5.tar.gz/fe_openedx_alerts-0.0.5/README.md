# fe-openedx-alerts

A command line tool that send alerts if any Open edX service failasticsearch service is active


## Python version

Python: 3.9.16



## Poetry Configuration

```bash
# https://pypi.org/
poetry config pypi-token.pypi $PYPI_TOKEN

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

/home/ubuntu/.pyenv/versions/3.9.16/bin/pip3 install fe-openedx-alerts==0.0.5 -U

# How to execute the script
/home/ubuntu/.pyenv/versions/3.9.16/bin/python /home/ubuntu/.pyenv/versions/3.9.16/lib/python3.9/site-packages/fe_openedx_alerts/es_status.py

```



## Cronjob

```bash
mkdir /home/ubuntu/logs/

crontab -e


```

