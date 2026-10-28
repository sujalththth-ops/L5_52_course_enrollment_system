
# Static Code Analysis — Issues

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Unsafe expression evaluation | Security | Actual line | `eval()` can execute arbitrary expressions. | Replace with validated numeric input. |
| Mutable default argument | Code quality / bug risk | Actual line | The default list may be shared between calls. | Use `None` and initialize inside the function. |
| Broad exception handling | Reliability | Actual line | Unexpected errors are silently ignored. | Catch the specific expected exception. |
| Shell command execution | Security | Actual line | Shell execution is unnecessary for printing a message. | Replace with `print()`. |
