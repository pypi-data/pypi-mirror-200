# ColonPython

A programming language that transpiles to python. It has extremely similar syntax, but you are also able to call functions with only one argument using a colon (`:`) using the following syntax:
```python
function:argument
```

This allows for statements such as this in ColonPython:
```python
print:"hello"
```

or:
```python
str:1234
```

It allows you to call single-argument functions whilst shortening the time it takes to write them.

To use ColonPython, first install it using:
```shell
pip3 install colonpython
```

Then, to use it in your program, create a new python file and before putting in any code write:
```python
import colonpython
```

Please note that sometimes Python will detect what it thinks are syntax errors, even though the code will run. This means that some things are not possible. This problem has caused this project to split into two. ColonPython and ArrowPython. ColonPython is this project: adding a way to call functions with an argument using a colon (`:`), and is used by importing the module and running the code in the file. As python identifies incorrect python syntax before runtime and raises errors, ArrowPython intead lets you run code on external files. It has more non-Python features. If I could use them in the same was as ColonPython, I would, but I cannot as far as I am aware.

Sometimes, you may run into issues. The following code will run fine:
```python
indexes = ("hello", "world")

print(indexes[0:1]) # This returns the string "hello".
```

However, the following code will not:
```python
indexes = ("hello", "world")

start = 0
end = 1

print(indexes[start:end]) # Raises error.
```

Because of this I would reccomend the following:
```python
indexes = ("hello", "world")

start = 0
end = 1

print(indexes[slice(start:end)]) # Does not raise an error, returns the string "hello".
```

With that out of the way, this is an example of the popular FizzBuzz program in ColonPython:
```python
import colonpython

def fizbuzz:num:
    for fizzbuzz in range:num:
        if fizzbuzz % 3 == 0 and fizzbuzz % 5 == 0:
            print:"fizzbuzz"
            continue
        elif fizzbuzz % 3 == 0:
            print:"fizz"
            continue
        elif fizzbuzz % 5 == 0:
            print:"buzz"
            continue
        print:fizzbuzz

fizbuzz:51
```

Have fun coding!