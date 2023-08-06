# textwrapre

A Python package to split text into smaller blocks based on regular expressions. 
It's useful to split large texts into smaller ones that can't exceed a certain limit, 
but need to be split where a certain regular expression matches. 

### pip install textwrapre

## Usage

```python
from textwrapre import wrapre
import regex

text = r"""
Python was created in the early 1990s by Guido van Rossum at Stichting Mathematisch 
Centrum (CWI, see https://www.cwi.nl/) in the Netherlands as a successor of a 
language called ABC. Guido remains Python’s principal author, although it includes
many contributions from others.

In 1995, Guido continued his work on Python at the Corporation for 
National Research Initiatives 
(CNRI, see https://www.cnri.reston.va.us/) in Reston, 
Virginia where he released several versions of the software.

""".strip()

# Split the text using the default regex separator
splitted = wrapre(text, blocksize=150, raisewhenlonger=True, removenewlines_from_result=True)

for s in splitted:
    print(len(s), s)

# Split the text using a custom regex separator
splitted = wrapre(text, blocksize=50, regexsep=r"[\r\n\s]+", raisewhenlonger=True, removenewlines_from_result=False, flags=regex.I)

for s in splitted:
    print(len(s), s)

# Split the text and raise an exception when the blocks are bigger than the limit
splitted = wrapre(text, blocksize=20, regexsep=r"[\r\n\s]+", raisewhenlonger=True, flags=regex.I)



85 Python was created in the early 1990s by Guido van Rossum at Stichting Mathematisch  
79 Centrum (CWI, see https://www.cwi.nl/) in the Netherlands as a successor of a  
115 language called ABC. Guido remains Python’s principal author, although it includes many contributions from others. 
99 In 1995, Guido continued his work on Python at the Corporation for  National Research Initiatives  
115 (CNRI, see https://www.cnri.reston.va.us/) in Reston,  Virginia where he released several versions of the software.
---------------------
47 Python was created in the early 1990s by Guido 
46 van Rossum at Stichting Mathematisch 
Centrum 
38 (CWI, see https://www.cwi.nl/) in the 
49 Netherlands as a successor of a 
language called 
46 ABC. Guido remains Python’s principal author, 
45 although it includes
many contributions from 
46 others.
In 1995, Guido continued his work on 
49 Python at the Corporation for 
National Research 
24 Initiatives 
(CNRI, see 
44 https://www.cnri.reston.va.us/) in Reston, 
47 Virginia where he released several versions of 
13 the software.
---------------------
Traceback (most recent call last):
  File "C:\Program Files\JetBrains\PyCharm Community Edition 2022.3.3\plugins\python-ce\helpers\pydev\pydevconsole.py", line 364, in runcode
    coro = func()
  File "<input>", line 41, in <module>
  File "C:\ProgramData\anaconda3\envs\adda\textwrapre.py", line 73, in wrapre
    raise ValueError(
ValueError: Some blocks are bigger than the limit! Try again with another separator or a bigger limit!
```

## Parameters

```python
def wrapre(
    text: Union[str, bytes], 
    blocksize: int, 
    regexsep: str = r"[\r\n]", 
    raisewhenlonger: bool = True, 
    removenewlines_from_result: bool = False, 
    *args, 
    **kwargs
) -> List[Union[str, bytes]]:
    """
    Split a text into blocks of a given size using a regex expression.

    :param text: the text to be splitted
    :param blocksize: the maximum size of each block
    :param regexsep: the regex expression used as separator (default: r"[\r\n]")
    :param raisewhenlonger: whether or not to raise an exception when a block is bigger than the limit (default: True)
    :param removenewlines_from_result: whether or not to remove new lines from the result (default: False)
    :param *args: additional arguments passed to the regex.compile() function
    :param **kwargs: additional keyword arguments passed to the regex.compile() function
    :return: a list of blocks
    """
```