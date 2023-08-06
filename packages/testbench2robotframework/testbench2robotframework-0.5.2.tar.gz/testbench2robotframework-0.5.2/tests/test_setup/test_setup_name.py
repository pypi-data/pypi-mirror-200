import pytest
from robot.api.parsing import ModelVisitor, Token, get_model
from robot.parsing.model.blocks import File

from testbench2robotframework.json_reader import read_json
from testbench2robotframework.testbench2robotframework import (
    testbench2robotframework as tb2robot_write,
)

TEST_DATA_PATH = "tests/test_setup/test_data"
GENERATED_SUITE = "tests/test_setup/Generated/18__SetupAndTeardown"


class SetupNameValiator(ModelVisitor):
    def __init__(self, test_name: str, expected_setup_call: str) -> None:
        self.test_name = test_name
        self.expected_setup_call = expected_setup_call
        self.setup_visited = False

    def visit_File(self, file):
        self.generic_visit(file)
        if not self.setup_visited:
            raise RuntimeError(
                f"Could not find test '{self.test_name}' with setup '{self.expected_setup_call}'."
            )

    def visit_TestCase(self, test):
        if test.name == self.test_name:
            self.generic_visit(test)

    def visit_Setup(self, setup):
        self.setup_visited = True
        if self.expected_setup_call != setup.name:
            raise RuntimeError(
                f"Setup '{setup.name}' does not match with name '{self.expected_setup_call}'."
            )


def check_setup_name(robot_file: str, test_name: str, setup_name: str):
    robot_model = get_model(f'{GENERATED_SUITE}/{robot_file}')
    library_existence_validator = SetupNameValiator(test_name, setup_name)
    library_existence_validator.visit(robot_model)


def generate_robot_suites(json_report_path: str, config_path: str):
    configuration = read_json(config_path)
    tb2robot_write(json_report_path, configuration)


@pytest.mark.parametrize(
    "robot_file,test_name,expected_setup_name",
    [
        ("01__TCS_with_single_setup_and_teardown_step.robot", "itba-TC-2184-PC-21637", "Log"),
        (
            "02__TCS_with_multiple_setup_and_teardown_steps.robot",
            "itba-TC-2185-PC-21639",
            "Setup-itba-TC-2185-PC-21639",
        ),
    ],
)
def test_setup_name(robot_file, test_name, expected_setup_name):
    generate_robot_suites(f"{TEST_DATA_PATH}/json-report", f"{TEST_DATA_PATH}/config.json")
    check_setup_name(robot_file, test_name, expected_setup_name)
