# snp

Utility for saving inputs and outputs of Python functions for refactoring.

## Usage

```python
import snp

# Save the inputs and outputs of this function
# to the `/tmp` directory
@snp.snap('/tmp')
def original(a, b, c):
    return a + b * c

# Test a modified function by specifying
# the save directory and the module path
# for the original function
@snp.test('/tmp', '__main__.original')
def modified(a, b, c):
    d = b * c
    return a + d

# Call the original function to
# save inputs and outputs
original(2,5,8)

# Now when you call the modified function,
# it will load the original arguments
# and check that the output matches
modified()

# If we defined a function that was incorrect:
@snp.test('/tmp', '__main__.original')
def modified_broken(a, b, c):
    d = b * c + 2
    return a + d

# This will raise an assertion error
modified_broken()
```
