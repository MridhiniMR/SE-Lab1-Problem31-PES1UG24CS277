# Lab 5: Static Code Analysis — Issue Report

**Project:** Event Management System  
**File analyzed:** `event_manager.py`  
**Tools used:** Pylint, Bandit, Flake8

## 1. Baseline analysis results

The analysis tools were run on the original, unmodified program before any fixes were applied.

| Tool | Baseline result |
|---|---|
| Pylint | 4.64/10 |
| Bandit | 4 findings: 1 High, 1 Medium, 2 Low |
| Flake8 | 4 style violations |

The original program also exhibited an unintended functional defect: the Tech Meetup and Alumni Dinner events shared the same guest list because of a mutable default argument.

## 2. Issues identified and fixes

*Line numbers refer to the original, unmodified `event_manager.py`.*

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Shell command execution | Security — High | 56 | Bandit B605 flagged `os.system()` because it executes a shell command constructed using the event name. Crafted input could alter the command. | Replaced `os.system()` with `subprocess.run()` using an argument list and `shell=False`. |
| Unsafe deserialization | Security — Medium | 51 | Bandit B301 flagged `pickle.load()`, which can execute arbitrary code when loading an untrusted pickle file. Bandit B403 also warned about importing pickle. | Replaced pickle persistence with JSON serialization and added basic handling for missing or invalid JSON files. |
| Shared mutable default argument | Correctness — Medium | 9 | Pylint W0102 flagged `guests=[]`. Both events shared the same list, causing Alumni Dinner to be incorrectly reported as full. | Changed the default to `None` and initialized a separate guest list for each event. |
| Ignored sorting parameter | Correctness — Medium | 39 | Pylint W0613 flagged the unused `sortOrder` parameter. The original function did not implement the requested sort direction. | Implemented ascending and descending sorting and handled invalid sorting options. |
| Missing-event handling | Robustness | 27, 39 | The original functions could raise `KeyError` when an event did not exist. | Added event-existence checks in the seat-counting and guest-reporting functions. |
| Empty lucky-draw list | Robustness | 72 | Selecting a winner from an empty guest list would raise an exception. | Added a check for an empty list before selecting a winner. |
| Naming convention violations | Maintainability | Multiple | Pylint C0103 identified camelCase function names and parameters that did not follow the recommended `snake_case` convention. | Renamed functions and parameters consistently and updated their call sites. |
| Missing documentation | Maintainability | Multiple | Pylint C0114 and C0116 identified missing module and function docstrings. | Added a module docstring and function docstrings. |
| Unnecessary `else` branch | Maintainability | 33 | Pylint R1705 identified an unnecessary `else` after a `return` statement. | Removed the unnecessary `else` branch. |
| Formatting violations | Style | 61, 66, 75, 79 | Flake8 reported E231, E225, E261 and E305 for spacing, inline-comment formatting and blank-line issues. | Corrected spacing and blank lines. |

## 3. Verification results

After the fixes, the program executed successfully and preserved its intended functionality.

| Verification | Initial result | Final result |
|---|---|---|
| Pylint score | 4.64/10 | 10.00/10 |
| Flake8 | 4 reported violations | No reported violations |
| Shared guest-list defect | Alumni Dinner incorrectly appeared full | Each event maintains its own guest list |
| Guest reporting | Sorting parameter was ignored | Supported sorting options are implemented |
| Persistence | Pickle serialization | JSON serialization |
| Missing-event handling | Could raise `KeyError` in affected functions | Explicitly handled |
| Empty lucky draw | Could fail on an empty list | Empty-list check added |

The original Bandit findings B605 and B301 were eliminated by replacing shell-based execution and pickle deserialization.

The latest available Bandit report still contains four Low-severity findings: B404, B603, B607 and B311. These relate to subprocess usage, the executable path, and the standard pseudorandom generator. They must be reviewed rather than reported as fully resolved.

## 4. Conclusion

The analysis identified security, correctness, maintainability and formatting issues in the original program. The fixes addressed the primary functional and security defects while preserving the event-management demonstration.

The Pylint score improved from 4.64/10 to 10.00/10, and Flake8 reported no remaining violations. The remaining Low-severity Bandit findings are documented for further review.
