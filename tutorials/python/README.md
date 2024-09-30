Python Installation

Install 3.12 on existing laptop

- Download release - python source code -  https://www.python.org/downloads/release/python-3120/


sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev

sudo apt-get install libssl-dev

tar -xf Python-3.12.6.tgz

cd Python-3.12.6

./configure --enable-optimizations --with-openssl=/usr/local/openssl

make -j4

make altinstall

