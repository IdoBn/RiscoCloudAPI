# RiscoCloud api
This is a simple api that allows you to:
* login to your riscocloud account
* check the status of your detectors
* arm or disarm your detectors 

# Research
checkout the research here: [research.md]

# Usage
you can take a look at usage.py, it looks something like this:

```python
from risco_session import RiscoSession


def main():
	sess = RiscoSession()
	sess.authenticate("a@b.com", "******", 1234)

	print(sess.get_cp_state())
	print(sess.arm(2))
	print(sess.disarm(2))


if __name__ == '__main__':
	main()
```