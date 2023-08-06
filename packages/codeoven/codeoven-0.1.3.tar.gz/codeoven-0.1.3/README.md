## Introduction

If you're working on scientific calculations using C programming, you might find it tedious to prepare an interface to call it from Python. However, Codeoven offers a simple solution to this problem. All you have to do is add some comment lines to the original C source code, and Codeoven will do the rest. By decorating your code with `@oven` comment lines, the code will be compiled and executed so that it can communicate with your Python script through *stdio*.

Using Codeoven eliminates the need to prepare a separate interface to link your C code with Python. Instead, the `@oven` comment lines act as a bridge between the two programming languages. This approach has the added advantage of allowing the original source code to be run in any IDE, making debugging easier.

Here is a quick example. 

Assume that we have a source code *main.c* that adds up from 1 to n.

```c
#include <stdio.h>

int main(void)
{
  int i, total = 0;
  int n = 1; // @oven
  
  for(i = 1; i <= n; i++) 
  {
    total += i; 
  }
  
  printf("answer:%d\n", total); // @oven
  return 0;
}
```

The following Python script will compile and run main.c to get the sum of 1 to 10.

```python
from codeoven import Oven

oven = Oven("main.c")
result = oven.run({"n": 10})
print(result["answer"]) # -> print 55
```

Notice that the only modification required to the source code is the `@oven` comments on the lines corresponding to input and output.

In terms of the execution speed, the initial compilation and the communication between C and Python through *stdio* would be the major bottleneck.

## Usage

#### Loading your source code

```
oven = Oven("main.c")
```

#### Running your program

```
parameter_dict = {"a": 1, "b": 2.0, "c": [3.0, 4.0, 5.0]}
result = oven.run(parameter_dict)
```

#### Passing values from Python to C

##### Passing a scalar value

```c
// At declaration
int a = 1; // @oven

//At substitution
double b;
b = 2; // @oven
```

##### Passing an array

```c
double c[] = {0.0};
```

#### Passing value from C to Python

You can output the results of your calculation using `printf`:

```python
printf("key_name:%lf\n", value); // @oven
```

The format string must always be composed of a sequence of a key, a colon, a value, and a newline. As for the value, it can be a number, string tuple list, or dictionary, as long as it can be evaluated by Python's ast.literal_eval.

```c
printf("a_and_b:(%d, %lf)\n", a, b); // @oven
// This line passes 
```



```c
printf("time_series:(%d, %lf)\n", 0, x); // @oven
for(i = 0; i < n; i++)
	x += calculation(i, x);
	printf("time_series:(%d, %lf)\n", i+1, x); // @oven
```

If multiple outputs are made for the same key, the result is a list in the order of outputs.

#### Accessing the results

The return value of `run` is a dictionary. You can access it as usual. 

```
print(result["a"])
```

## Code modifiers

#### @oven

Input

```
int n = 1; // @oven
double array[] = {1.0, 2.0, 3.0}; // @oven
```

Output

```
printf("result:%d\n", n*n); // @oven
```

#### (Plan)@oven.assign  (new plan)-> @oven.as: or @oven:

Assign the value using a Python statement.

```
int array[] = {2, 3, 5}; // @oven
int n = 3; // @oven.assign:array.size
```

```
double map[][] = {{1.0, 2.0}, {2.0, 3.0}, {3.0, 4.0}}; // @oven
int n_x = 2; // @oven.assign:map.shape[0]
int n_y = 3; // @oven.assign:map.shape[1]
```

#### @oven.compile

The input specified by `@oven.compile` is embdedded directrly in the source code.

```
int n = 1; // @oven.compile

double array[] = {1.0, 2.0}; // @oven.compile
int n = 2; // @oven.assign:array.size
```

## Reference

#### class `codeoven.Oven`

##### **`codeoven.Oven(file_name:str)`**

- `file_name`: The file name of a source code to be processed

When an instance of Oven is created, the source code is loaded and parsed. At this stage, no new code is written out yet; the oven instance generates code when `run` or `burn` is executed.

##### **`oven.run(parameters:dict=None) -> dict`**

- `parameters`: Initialization or substitution statements commented with "@oven" in the C source code will be replaced using the value of the dictionary at runtime though *stdin*. The compilation will be done once for the first execution.

##### **`oven.burn(parameters:dict=None) -> dict`**

- `parameters`: Initialization or substitution statements commented with "@oven" in the C source code will be replaced using the value of the dictionary.

Each time the method `burn` is called, the new source code is output, compiled, and executed. No information exchange will be done at runtime, and all the parameters and data will be implemented in the source code.

## Examples

```c
#include <stdio.h>

int main(void)
{
  double data[] = [1, 3, 5]; // @oven
  int n = 3; // @over:data.size
  double result = 0;
  int i;
  for (i = 0; i < n; i++)
  {
    result += data[i];
  }
  printf("sum:%lf\n", result); // @oven
  return 0
}
```

```c
#include <stdio.h>

int main(void)
{
  double data = [[1, 2, 3], [2, 3, 4]]; // @oven.runtime
  int imax = 3; // @oven.assign:data.shape[0]
  int kmax = 2; // @oven.assign:data.shape[1]
  int i, k;
  for (i = 0; i <)
}
```



