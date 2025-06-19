
import pytest
import tempfile
import os
from main import read_csv, filter_rows, aggregate_rows

CSV_CONTENT = """name,brand,price,rating
iphone 15 pro,apple,999,4.9
galaxy s23 ultra,samsung,1199,4.8
redmi note 12,xiaomi,199,4.6
poco x5 pro,xiaomi,299,4.4
"""

@pytest.fixture
def csv_file():
    with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.csv') as f:
        f.write(CSV_CONTENT)
        f.flush()
        yield f.name
    os.remove(f.name)

def test_read_csv(csv_file):
    rows = read_csv(csv_file)
    assert len(rows) == 4
    assert rows[0]['brand'] == 'apple'

def test_filter_rows_equal(csv_file):
    rows = read_csv(csv_file)
    filtered = filter_rows(rows, "brand=apple")
    assert len(filtered) == 1
    assert filtered[0]['name'] == 'iphone 15 pro'

def test_filter_rows_greater(csv_file):
    rows = read_csv(csv_file)
    filtered = filter_rows(rows, "price>1000")
    assert len(filtered) == 1
    assert filtered[0]['name'] == 'galaxy s23 ultra'

def test_filter_rows_less(csv_file):
    rows = read_csv(csv_file)
    filtered = filter_rows(rows, "rating<4.7")
    assert len(filtered) == 2
    names = {row['name'] for row in filtered}
    assert 'redmi note 12' in names
    assert 'poco x5 pro' in names

def test_aggregate_invalid_column(csv_file):
    rows = read_csv(csv_file)
    with pytest.raises(SystemExit):
        aggregate_rows(rows, "avg:shrte")

def test_filter_invalid_column(csv_file):
    rows = read_csv(csv_file)
    with pytest.raises(SystemExit):
        filter_rows(rows, "weabf=apple")

def test_filter_invalid_format(csv_file):
    rows = read_csv(csv_file)
    with pytest.raises(SystemExit):
        filter_rows(rows, "bererv")