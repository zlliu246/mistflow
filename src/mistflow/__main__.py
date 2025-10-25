
import sys
import logging
from .runners.task_runner import TaskRunner
from .runners.workflow_runner import WorkflowRunner

# remove handlers from root handler as when we run "python -m something", 
# some congiguration happens to the root logger, making child loggers behave in strange ways
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def main():
    args = sys.argv[1:]
    if len(args) == 0:
        return print("hello from mistflow")

    if args[:2] == ["task", "run"]:
        task_path, input_json, *_ = args[2:]
        task_runner = TaskRunner(task_path)
        task_runner.install_dependencies()
        out = task_runner.run(input_json)
        print(out)

    if args[:2] == ["workflow", "run"]:
        workflow_full_name, input_json, *_ = args[2:]
        workflow_runner = WorkflowRunner(workflow_full_name, input_json)
        workflow_runner.install_dependencies()
        workflow_runner.run()

if __name__ == "__main__":
    main()