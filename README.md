# mistflow

## run task
```
python3 -m mistflow task run mistflow.tasks.test.add100 '{"number": 6}'
```

## run workflow
```
python3 -m mistflow workflow run mistflow.workflows.test.number_magic2 '{"start_number": 3}'
```