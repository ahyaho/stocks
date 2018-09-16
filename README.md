Test locally:
```
git clone https://github.com/ahyaho/stocks.git
cd stocks
virtualenv -p python3 .venv
source .venv/bin/activate
pip install -r requirements.txt
py.test tests
```

Test in Docker container:
```bash
git clone https://github.com/ahyaho/stocks.git
cd stocks
docker build -t stocks/calc .
docker container run -it stocks/calc /bin/sh
py.test tests/
```
