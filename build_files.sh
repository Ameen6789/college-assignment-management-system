echo "BUILD START"
python3.12 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
python3.12 manage.py collectstatic --noinput

echo "BUILD END"
