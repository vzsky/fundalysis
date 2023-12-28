dir=$(pwd)
cd /usr/local
mkdir fundalysis
cd fundalysis

cp -r $dir/* .
pip3 install -r requirement

ln -s /usr/local/fundalysis/cli.py /usr/local/bin/fundalysis
