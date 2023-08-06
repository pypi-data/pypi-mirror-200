from src.main import create_etl_structure, create_modular_structure, create_ml_project_structure, create_web_app_structure
from pathlib import Path
import shutil
import os
import pytest

@pytest.fixture
def output_path(tmpdir):
    path = Path(tmpdir.mkdir("project"))
    yield path
    shutil.rmtree(str(path))

def test_create_etl_structure(output_path: Path):
    create_etl_structure(str(output_path))
    assert (output_path / "src").is_dir()
    assert (output_path / "tests").is_dir()
    assert (output_path / "data").is_dir()
    assert (output_path / "src" / "extract").is_dir()
    assert (output_path / "src" / "transform").is_dir()
    assert (output_path / "src" / "load").is_dir()
    assert (output_path / "data" / "input").is_dir()
    assert (output_path / "data" / "intermediate").is_dir()
    assert (output_path / "data" / "output").is_dir()
    assert (output_path / "src" / "main.py").is_file()
    assert (output_path / "tests" / "test_extract.py").is_file()
    assert (output_path / "tests" / "test_transform.py").is_file()
    assert (output_path / "tests" / "test_load.py").is_file()
    assert (output_path / "README.md").is_file()
    assert (output_path / "requirements.txt").is_file()

def test_create_modular_structure(output_path: Path):
    module_names = ["utils", "services", "models"]
    create_modular_structure(str(output_path), module_names)
    assert (output_path / "src").is_dir()
    assert (output_path / "tests").is_dir()
    assert (output_path / "src" / "__init__.py").is_file()
    assert (output_path / "README.md").is_file()
    assert (output_path / "requirements.txt").is_file()

    for module_name in module_names:
        module_path = output_path / "src" / module_name
        assert (module_path).is_dir()
        assert (module_path / "__init__.py").is_file()
        assert (module_path / f"{module_name}.py").is_file()

        test_file_path = output_path / "tests" / f"test_{module_name}.py"
        assert (test_file_path).is_file()

def test_create_ml_project_structure(output_path: Path):
    create_ml_project_structure(str(output_path))
    assert (output_path / "src").is_dir()
    assert (output_path / "tests").is_dir()
    assert (output_path / "data").is_dir()
    assert (output_path / "src" / "data").is_dir()
    assert (output_path / "src" / "models").is_dir()
    assert (output_path / "src" / "main.py").is_file()
    assert (output_path / "src" / "data" / "preprocess.py").is_file()
    assert (output_path / "src" / "data" / "features.py").is_file()
    assert (output_path / "src" / "models" / "model.py").is_file()
    assert (output_path / "src" / "models" / "train.py").is_file()
    assert (output_path / "src" / "models" / "evaluate.py").is_file()
    assert (output_path / "tests" / "test_preprocess.py").is_file()
    assert (output_path / "tests" / "test_features.py").is_file()
    assert (output_path / "tests" / "test_model.py").is_file()
    assert (output_path / "tests" / "test_train.py").is_file()
    assert (output_path / "tests" / "test_evaluate.py").is_file()
    assert (output_path / "data" / "raw").is_dir()
    assert (output_path / "data" / "interim").is_dir()
    assert (output_path / "data" / "processed").is_dir()
    assert (output_path / "data" / "models").is_dir()
    assert (output_path / "README.md").is_file()
    assert (output_path / "requirements.txt").is_file()

def test_create_web_app_structure(output_path: Path):
    create_web_app_structure(str(output_path))
    assert (output_path / "src").is_dir()
    assert (output_path / "tests").is_dir()
    assert (output_path / "static").is_dir()
    assert (output_path / "templates").is_dir()
    assert (output_path / "src" / "main.py").is_file()
    assert (output_path / "src" / "views.py").is_file()
    assert (output_path / "src" / "forms.py").is_file()
    assert (output_path / "src" / "models.py").is_file()
    assert (output_path / "tests" / "test_views.py").is_file()
    assert (output_path / "tests" / "test_forms.py").is_file()
    assert (output_path / "tests" / "test_models.py").is_file()
    assert (output_path / "static" / "css").is_dir()
    assert (output_path / "static" / "js").is_dir()
    assert (output_path / "static" / "images").is_dir()
    assert (output_path / "templates" / "base.html").is_file()
    assert (output_path / "README.md").is_file()
    assert (output_path / "requirements.txt").is_file()