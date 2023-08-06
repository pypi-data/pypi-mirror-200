from typing import Union, List

import regex


def wrapre(
    text: Union[str, bytes],
    blocksize: int,
    regexsep: Union[str, bytes] = r"[\r\n]",
    raisewhenlonger: bool = True,
    removenewlines_from_result: bool = False,
    *args,
    **kwargs
) -> List[Union[str, bytes]]:
    """
    Splits a given `text` into blocks of size `blocksize`, using the `regexsep` pattern as the separator.

    If `raisewhenlonger` is True (default), raises a ValueError if any block is larger than `blocksize`.

    If `removenewlines_from_result` is True, removes any newline characters from the resulting blocks.

    *args and **kwargs are additional arguments that can be passed to the `regex.compile` function.

    Args:
        text (str/bytes): The text to be split into blocks.
        blocksize (int): The maximum size of each block.
        regexsep (str/bytes): The regular expression pattern used to separate the blocks. Defaults to r"[\r\n]".
        raisewhenlonger (bool, optional): Whether to raise an error if any block is larger than `blocksize`. Defaults to True.
        removenewlines_from_result (bool, optional): Whether to remove any newline characters from the resulting blocks. Defaults to False.
        *args: Additional arguments to be passed to the `regex.compile` function.
        **kwargs: Additional keyword arguments to be passed to the `regex.compile` function.

    Returns:
        list: A list of strings (or bytes, if `text` was a bytes object), where each element is a block of text of maximum size `blocksize`.

    Raises:
        ValueError: If `raisewhenlonger` is True and any block is larger than `blocksize`.

    """
    spannow = -1
    limit = blocksize
    allspansdone = []
    allf = text
    isbytes = isinstance(text, bytes)
    regexsepcom = regex.compile(regexsep, *args, **kwargs)

    while allf:
        oldlenallf = len(allf)
        newlenaffl = oldlenallf
        for ini, x in enumerate(
            regexsepcom.finditer(allf, concurrent=True, partial=False)
        ):
            spannowtemp = x.end()
            if spannowtemp < limit:
                spannow = spannowtemp
            else:
                allspansdone.append(allf[:spannow])
                allf = allf[spannow:]
                spannow = -1
                newlenaffl = len(allf)
                break
        if oldlenallf == newlenaffl:
            allspansdone.append(allf)
            if not isbytes:
                allf = ""
            else:
                allf = b""
    if not allspansdone:
        allspansdone.append(allf)

    if raisewhenlonger:
        if len([True for x in allspansdone if len(x) > limit]) != 0:
            raise ValueError(
                "Some blocks are bigger than the limit! Try again with another separator or a bigger limit!"
            )
    if removenewlines_from_result:
        if isbytes:
            newlinesbtypes = regex.compile(rb"[\r\n]+")
            allspansdone = [newlinesbtypes.sub(b" ", x) for x in allspansdone]
        else:
            newlinesbstr = regex.compile(r"[\r\n]+")

            allspansdone = [newlinesbstr.sub(" ", x) for x in allspansdone]
    return allspansdone

