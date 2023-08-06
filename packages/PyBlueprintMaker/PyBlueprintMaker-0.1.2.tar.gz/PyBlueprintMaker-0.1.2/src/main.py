import argparse
import os

def create_etl_structure(output_path: str):
    # Create main directories
    os.makedirs(os.path.join(output_path, "src"))
    os.makedirs(os.path.join(output_path, "tests"))
    os.makedirs(os.path.join(output_path, "data"))
    
    # Create subdirectories for src
    os.makedirs(os.path.join(output_path, "src", "extract"))
    os.makedirs(os.path.join(output_path, "src", "transform"))
    os.makedirs(os.path.join(output_path, "src", "load"))

    # Create subdirectories for data
    os.makedirs(os.path.join(output_path, "data", "input"))
    os.makedirs(os.path.join(output_path, "data", "intermediate"))
    os.makedirs(os.path.join(output_path, "data", "output"))

    # Create initial files
    open(os.path.join(output_path, "src", "main.py"), "w").close()
    open(os.path.join(output_path, "tests", "test_extract.py"), "w").close()
    open(os.path.join(output_path, "tests", "test_transform.py"), "w").close()
    open(os.path.join(output_path, "tests", "test_load.py"), "w").close()
    open(os.path.join(output_path, "README.md"), "w").close()
    open(os.path.join(output_path, "requirements.txt"), "w").close()

def create_modular_structure(output_path: str, module_names: list):
    # Create main directories
    os.makedirs(os.path.join(output_path, "src"))
    os.makedirs(os.path.join(output_path, "tests"))

    # Create module directories and files
    for module_name in module_names:
        module_path = os.path.join(output_path, "src", module_name)
        os.makedirs(module_path)
        open(os.path.join(module_path, "__init__.py"), "w").close()
        open(os.path.join(module_path, f"{module_name}.py"), "w").close()

        test_file_path = os.path.join(output_path, "tests", f"test_{module_name}.py")
        open(test_file_path, "w").close()

    # Create additional files
    open(os.path.join(output_path, "src", "__init__.py"), "w").close()
    open(os.path.join(output_path, "README.md"), "w").close()
    open(os.path.join(output_path, "requirements.txt"), "w").close()

def create_ml_project_structure(output_path: str):
    # Create main directories
    os.makedirs(os.path.join(output_path, "src"))
    os.makedirs(os.path.join(output_path, "tests"))
    os.makedirs(os.path.join(output_path, "data"))

    # Create subdirectories for src
    os.makedirs(os.path.join(output_path, "src", "data"))
    os.makedirs(os.path.join(output_path, "src", "models"))

    # Create initial files
    open(os.path.join(output_path, "src", "main.py"), "w").close()
    open(os.path.join(output_path, "src", "data", "preprocess.py"), "w").close()
    open(os.path.join(output_path, "src", "data", "features.py"), "w").close()
    open(os.path.join(output_path, "src", "models", "model.py"), "w").close()
    open(os.path.join(output_path, "src", "models", "train.py"), "w").close()
    open(os.path.join(output_path, "src", "models", "evaluate.py"), "w").close()

    # Create test files
    open(os.path.join(output_path, "tests", "test_preprocess.py"), "w").close()
    open(os.path.join(output_path, "tests", "test_features.py"), "w").close()
    open(os.path.join(output_path, "tests", "test_model.py"), "w").close()
    open(os.path.join(output_path, "tests", "test_train.py"), "w").close()
    open(os.path.join(output_path, "tests", "test_evaluate.py"), "w").close()

    # Create data directories
    os.makedirs(os.path.join(output_path, "data", "raw"))
    os.makedirs(os.path.join(output_path, "data", "interim"))
    os.makedirs(os.path.join(output_path, "data", "processed"))
    os.makedirs(os.path.join(output_path, "data", "models"))

    # Create additional files
    open(os.path.join(output_path, "README.md"), "w").close()
    open(os.path.join(output_path, "requirements.txt"), "w").close()


def create_web_app_structure(output_path: str):
    # Create main directories
    os.makedirs(os.path.join(output_path, "src"))
    os.makedirs(os.path.join(output_path, "tests"))
    os.makedirs(os.path.join(output_path, "static"))
    os.makedirs(os.path.join(output_path, "templates"))

    # Create static directories
    os.makedirs(os.path.join(output_path, "static", "css"))
    os.makedirs(os.path.join(output_path, "static", "js"))
    os.makedirs(os.path.join(output_path, "static", "images"))

    # Create initial files
    open(os.path.join(output_path, "src", "main.py"), "w").close()
    open(os.path.join(output_path, "src", "views.py"), "w").close()
    open(os.path.join(output_path, "src", "forms.py"), "w").close()
    open(os.path.join(output_path, "src", "models.py"), "w").close()

    # Create test files
    open(os.path.join(output_path, "tests", "test_views.py"), "w").close()
    open(os.path.join(output_path, "tests", "test_forms.py"), "w").close()
    open(os.path.join(output_path, "tests", "test_models.py"), "w").close()

    # Create additional files
    open(os.path.join(output_path, "README.md"), "w").close()
    open(os.path.join(output_path, "requirements.txt"), "w").close()
    open(os.path.join(output_path, "templates", "base.html"), "w").close()





def main(output_path, structure, modules=None):
    if structure == "etl":
        create_etl_structure(output_path)
    elif structure == "modular":
        module_names = modules if modules else ["utils", "services", "models"]
        create_modular_structure(output_path, module_names)
    elif structure == "ml":
        create_ml_project_structure(output_path)
    elif structure == "web":
        create_web_app_structure(output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a project structure.")
    parser.add_argument("output_path", help="The desired output path for the project structure.")
    parser.add_argument("structure", help="The project structure to create: etl, modular, ml, web.")
    parser.add_argument("-m", "--modules", nargs="*", help="The list of module names for the 'modular' structure option.")


    args = parser.parse_args()

    main(args.output_path, args.structure, args.modules)
