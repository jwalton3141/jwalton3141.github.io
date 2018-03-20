---
layout: post
title: 3 useful Python decorators
image: https://jwalton3141.github.io/assets/background.png
---

It was around a year ago that I first came across the concept of a [decorator](https://wiki.python.org/moin/PythonDecorators) in Python. I was immediately intrigued: the use of a function of function appealed to me as a mathematician. However, other than the "time" example often used to advocate the use of decorators, I didn't immediately find much use for them.

Largely, I found that though many promoted the use of decorators, simple examples demonstrating their usefulness were scarce. A year later decorators have become part of my everyday workflow, and so I wanted to share three useful decorators I use regularly.

If you're unfamiliar with decorators [Stackoverflow provides a surprisingly good starting point](https://stackoverflow.com/a/1594484). As with all things Python a quick Google search will return a plethora of resources. This post is not intended to be an introduction to decorators, instead I hope to persuade you of their usefulness by way of three simple examples
.
## 1. Timer 2.0.1

Before I introduce this decorator you should note that if you wish to time fast, performance critical sections of code you should probably be using [ipython](https://ipython.org/)'s ```%timeit``` functionality, not the decorator I suggest below. The decorator I describe here is useful for longer runs.

The most common example I stumbled upon when reading about decorators was the "timer" example. This oft used example wraps any function and prints out the time it took to execute in seconds. When running scripts that take hours to complete, reading the run time in seconds is irritating. However, it's easy to alter this decorator to format the run time more intelligently.

I use the decorator below on a daily basis. This decorator prints and formats the run time depending on the length of the run. If the run takes less than an hour, the run time is printed in minutes and seconds. If the run takes longer than an hour, the run time is printed in hours and minutes.

```py
import time
from functools import wraps

def my_time(function):
    """ Wrapper used to time how long a function takes to execute, and intelligently print 
    run time.
    """

    # Preserve docstring (and other attributes) of function_to_time
    @wraps(function)
    def wrapper(*args, **kwargs):
        t0 = time.time()
        results = function(*args, **kwargs)
        t1 = time.time()

        # If function took over an hour, print time in hours and minutes
        if t1 - t0 > 60**2:
            print('This run took {:.0f} hr(s) {:.0f} min(s) to complete'.format((t1 - t0) // 60**2,
                  ((t1 - t0) % 60**2) // 60 ))
        else:
            print('This run took {:.0f} min(s) {:.0f} sec(s) to complete'.format((t1 - t0) // 60,
                  (t1 - t0) % 60))

        return results
    return wrapper
```

## 2. Completion alarm

Often I run scripts which take hours to complete. Instead of having to continually check up on my code, I wanted to be alerted (by way of sound) when my script completed. Cue our second decorator: the beeper.

I wrote the below decorator to play a sound once my run completes. This decorator allows you to concentrate on other work whilst your code runs, without the continual distraction of checking whether your run is complete.

You'll notice that this decorator utilises the library ```pygame```. [Pygame](https://www.pygame.org/wiki/about) is a large project which does so much more than playing sounds, and its use here is certainly overkill. However, after playing around with [snack](http://www.speech.kth.se/snack/), [pyaudio](https://people.csail.mit.edu/hubert/pyaudio/) and others, I found that Pygame was the easiest to get working straight out of the box.

Here I use the notification ```Amsterdam.ogg``` which I found in my ubuntu install at ```/usr/share/sounds/ubuntu/notifications```. Ensure that ```music.load()``` can find your desired sound file, either by way of an absolute or relative path.

```py
import pygame
from functools import wraps

def beeper(function):
    """ Decorator that plays a sound when function completes """

    @wraps(function)
    def wrapper(*args, **kwargs):
        results = function(*args, **kwargs)
        # Try play beeper
        try:
            pygame.mixer.init()
            pygame.mixer.music.load("/data/surf_scoter/infer/inputs/Amsterdam.ogg")
            pygame.mixer.music.play()
        # If can't play (for example: running script over ssh), don't flip
        except:
            pass
        return results
    return wrapper
```

## 3. Capture std_out

Many of my scripts print summaries and other information about their run. In addition to the ```my_time``` decorator introduced earlier, a single script may print from various different functions and places.

Sometimes, however, you may wish to print all this output to file for later reference. This could be done by altering all the print functions individually to write to file. However, this is not ideal and quickly becomes cumbersome for larger projects.

Instead, we can employ a decorator which captures all prints to ```std_out```. I first came across [this context manager on stack exchange](https://stackoverflow.com/a/16571630), where I found the following snippet:

```py
from functools import wraps
from io import StringIO
import sys

class Capturing(list):
    """ Used to capture printed output of running script. """
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        # Free up memory
        del self._stringio
        sys.stdout = self._stdout
```

With this snippet taken, it's easy for us to go ahead and wrap this context manager up into a decorator.

```py
def capture_stdout(function):
    """ Decorator to be used to capture stdout of function """
    # Preserve docstring (and other attributes) of function_to_listen
    @wraps(function)
    def wrapper(*args, **kwargs):
        with Capturing() as printed:
            results = function_to_listen(*args, **kwargs)
        return results, printed
    return wrapper
```

## Summary

The examples above were chosen to be of general use, rather than more technical decorators used for specific projects. With this you can hopefully start using the above introduced immediately. I hope you've now been convinced that decorators can be useful, and deserve the attention: so get decorating!
