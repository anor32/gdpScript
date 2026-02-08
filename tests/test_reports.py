import pytest
import tempfile
import os
from reports import Report
from utils import path_normalizer


@pytest.fixture
def sample_csv_data():
    data = """country,year,gdp,gdp_growth,inflation
USA,2023,100,2.1,3.4
USA,2022,90,2.1,8.0
China,2023,80,5.2,2.5"""
    return data


@pytest.fixture
def temp_csv_file(sample_csv_data):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(sample_csv_data)
        temp_path = f.name
    yield temp_path
    os.unlink(temp_path)


@pytest.fixture
def report_with_data(temp_csv_file):
    report = Report(name="test")
    report.read_files([temp_csv_file])
    return report


def test_01_init():
    report = Report()
    assert report.name == ''
    assert report.headers is None
    assert report.rows is None


def test_02_init_with_name():
    report = Report(name="test")
    assert report.name == "test"


def test_03_read_files_single(temp_csv_file):
    report = Report()
    report.read_files([temp_csv_file])
    assert report.headers == ['country', 'year', 'gdp', 'gdp_growth', 'inflation']
    assert len(report.rows) == 3


def test_04_read_files_multiple(temp_csv_file):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("country,year,gdp\nJapan,2023,50")
        temp_path2 = f.name

    report = Report()
    report.read_files([temp_csv_file, temp_path2])
    assert len(report.rows) == 4
    os.unlink(temp_path2)



def test_06_read_files_empty_path():
    report = Report()
    report.read_files([""])
    assert report.rows == []


def test_07_read_files_invalid_path():
    report = Report()
    report.read_files(["."])
    assert report.rows == []


def test_08_sort_report_by_country(report_with_data):
    report_with_data.sort_report(0, reverse=False)
    assert report_with_data.rows[0][0] == "China"


def test_09_sort_report_by_gdp_desc(report_with_data):
    report_with_data.sort_report(2, reverse=True)

    assert report_with_data.rows[2][2] == "100"


def test_10_sort_report_empty():
    report = Report()
    result = report.sort_report(0)
    assert result == 'не созданы строки таблицы'


def test_11_create_report_gdp(report_with_data):
    report_with_data.create_report_gdp()
    assert report_with_data.headers == ['country', 'gdp']
    assert len(report_with_data.rows) == 2


def test_12_create_report_gdp_no_headers():
    report = Report()
    result = report.create_report_gdp()
    assert result == 'не созданы строки таблицы или заголовки'


def test_13_create_report_gdp_no_rows():
    report = Report(headers=['country', 'gdp'])
    result = report.create_report_gdp()
    assert result == 'не созданы строки таблицы или заголовки'


def test_14_create_report_gdp_missing_columns():
    report = Report(headers=['a', 'b'], rows=[['x', 'y']])
    result = report.create_report_gdp()
    assert result == "Отсутвуют колонки для отчета создание невозможно"


def test_15_create_report_gdp_calculation(report_with_data):
    report_with_data.create_report_gdp()
    results = dict(report_with_data.rows)
    assert results['USA'] == 95.0
    assert results['China'] == 80.0


def test_16_path_normalizer_valid():
    result = path_normalizer("data.csv")
    assert result.endswith("data.csv")


def test_17_path_normalizer_with_spaces():
    result = path_normalizer("  data.csv  ")
    assert result.endswith("data.csv")




def test_19_path_normalizer_invalid():
    result = path_normalizer("data.txt")
    assert result is False


def test_20_path_normalizer_empty():
    result = path_normalizer("")
    assert result is False


def test_21_path_normalizer_dot():
    result = path_normalizer(".")
    assert result is False


def test_22_create_report_gdp_sort_after(report_with_data):
    report_with_data.create_report_gdp()
    report_with_data.sort_report(1, reverse=True)
    gdp_values = [row[1] for row in report_with_data.rows]
    assert gdp_values == sorted(gdp_values, reverse=True)