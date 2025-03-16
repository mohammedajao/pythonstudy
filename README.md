Simple repo to learn how to code with python.

I decided to use web development principles I had previously learned.

Typing is a bit lazy. No tests. Not all dunder methods implemented.

I believe this should be compatible with Python 2.8+ (i think)

And yes, I know python 3.13 would've made my life much easier


Also includes a signal library for fun:

```python
... # skibidi imports here

foo = createSignal("")
brainrot = createComputedSignal(lambda: foo.get() + " is bussin")

def bar():
    if foo.get() == "pizza":
        print("Chat is this rizz")
    else:
        print("YURRRRR")

createEffect(bar)

print(brainrot.get())
foo.set("rice") # prints yurrrr
print(brainrot.get()) # prints rice is bussin
foo.set("pizza") # prints Chat is this rizz
print(brainrot.get()) # prints pizza is bussin
```

not everything in redux (i'm too lazy) but has the basics.
probbably should've done an iterative flattener with a mapReduce func and protocol binding for immer compat on action/builder reducers. add that if you wish