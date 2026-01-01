# -*- coding: utf-8 -*-

import typing as T

from func_args.api import OPT

if T.TYPE_CHECKING: # pragma: no cover
    from ..nodes.base import T_NODE

def doc_content_to_markdown(
    content: T.Union[list["T_NODE"], T.Literal[OPT]],
    concat: str = "\n",
    ignore_error: bool = False,
) -> str:
    """
    For example blockquote
    """
    if content is OPT:
        return ""
    else:
        lst = list()
        for node in content:
            # print("----- Work on a new node -----")
            try:
                if isinstance(node, (NodeBulletList, NodeOrderedList, NodeCodeBlock)):
                    md = "\n" + node.to_markdown() + "\n"
                else:
                    md = node.to_markdown()
                # print(f"{node = }")
                # print(f"{md = }")
                lst.append(md)
            except Exception as e:  # pragma: no cover
                if ignore_error:
                    pass
                else:
                    raise e

    md = _strip_double_empty_line(concat.join(lst))
    return md