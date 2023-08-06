## Python scripts for Windows Task Scheduler 2.0 from SaltStack

This is a copy of a `https://github.com/saltstack/salt/blob/master/salt/modules/win_task.py`
from `https://github.com/saltstack/salt` (Apache 2.0 Licence) as a separate repository.

## Installation and usage

`pip install https://github.com/dolamroth/py_win_task_scheduler/archive/refs/heads/main.zip`

## Changes made

According to requirement SaltStack's licence, here is a list of changes made to original script:

- class `Com` and exceptions `ArgumentValueError`, `CommandExecutionError` 
  are inserted in a single file, instead of import.
- Function `run_wait` made asynchronous with anyio, `anyio.sleep(1)` inserted within infinite loop,
  to make function cancellable with `anyio.CancelScope`
- Added extra error-key `-2147024891` in method `_save_task_definition`
- Definitions of `__virtual__` methods have been removed

## Licences

- Salt original licence: https://github.com/saltstack/salt/blob/master/LICENSE
- Salt NOTICE file: https://github.com/saltstack/salt/blob/master/NOTICE
