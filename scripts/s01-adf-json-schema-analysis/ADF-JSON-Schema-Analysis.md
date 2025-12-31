# ADF JSON Schema Analysis

## Overview

- Total definitions: 82
- Node definitions (`*_node`): 62
- Mark definitions (`*_mark`): 16
- Other definitions: 4
- Unique type enum values: 64

## All Type Enum Values

64 unique type values:

- alignment
- annotation
- backgroundColor
- blockCard
- blockTaskItem
- blockquote
- bodiedExtension
- bodiedSyncBlock
- border
- breakout
- bulletList
- caption
- code
- codeBlock
- dataConsumer
- date
- decisionItem
- decisionList
- doc
- em
- embedCard
- emoji
- expand
- extension
- external
- file
- fragment
- hardBreak
- heading
- image
- indentation
- inlineCard
- inlineExtension
- layoutColumn
- layoutSection
- link
- listItem
- media
- mediaGroup
- mediaInline
- mediaSingle
- mention
- nestedExpand
- orderedList
- panel
- paragraph
- placeholder
- rule
- status
- strike
- strong
- sub
- subsup
- sup
- syncBlock
- table
- tableCell
- tableHeader
- tableRow
- taskItem
- taskList
- text
- textColor
- underline

## Implementation Order

Nodes sorted by dependencies (implement dependencies first):

1. **blockCard** - no dependencies
2. **bodiedExtension** - depends on: dataConsumer, fragment
3. **date** - no dependencies
4. **embedCard** - no dependencies
5. **emoji** - no dependencies
6. **extension** - depends on: dataConsumer, fragment
7. **hardBreak** - no dependencies
8. **inlineCard** - no dependencies
9. **inlineExtension** - depends on: dataConsumer, fragment
10. **layoutColumn** - no dependencies
11. **layoutSection** - depends on: breakout, layoutColumn
12. **layoutSection_full** - depends on: breakout, layoutColumn, layoutSection
13. **media** - depends on: annotation, border, link
14. **mediaGroup** - depends on: media
15. **mediaInline** - depends on: annotation, border, link
16. **mediaSingle** - depends on: link
17. **mediaSingle_full** - depends on: media, mediaSingle
18. **mention** - no dependencies
19. **nestedExpand** - no dependencies
20. **expand** - depends on: nestedExpand
21. **expand_root_only** - depends on: breakout, nestedExpand
22. **placeholder** - no dependencies
23. **rule** - no dependencies
24. **status** - no dependencies
25. **syncBlock** - depends on: breakout
26. **table_cell** - no dependencies
27. **table_header** - no dependencies
28. **table_row** - depends on: table_cell, table_header
29. **table** - depends on: fragment, table_row
30. **text** - no dependencies
31. **codeBlock** - depends on: text
32. **codeBlock_root_only** - depends on: breakout, text
33. **code_inline** - depends on: annotation, code, link, text
34. **formatted_text_inline** - depends on: annotation, backgroundColor, em, link, strike, strong, subsup, text, textColor, underline
35. **caption** - depends on: code_inline, date, emoji, formatted_text_inline, hardBreak, inlineCard, mention, placeholder, status
36. **inline** - depends on: code_inline, date, emoji, formatted_text_inline, hardBreak, inlineCard, inlineExtension, mediaInline, mention, placeholder, status
37. **decisionItem** - depends on: inline
38. **decisionList** - depends on: decisionItem
39. **heading** - depends on: alignment, indentation, inline
40. **mediaSingle_caption** - depends on: caption, media, mediaSingle
41. **paragraph** - depends on: alignment, indentation, inline
42. **blockTaskItem** - depends on: extension, paragraph
43. **taskItem** - depends on: inline
44. **taskList** - depends on: blockTaskItem, taskItem
45. **blockquote** - depends on: bulletList, codeBlock, extension, mediaGroup, mediaSingle_caption, mediaSingle_full, orderedList, paragraph
46. **bodiedSyncBlock** - depends on: blockCard, blockquote, breakout, bulletList, codeBlock, decisionList, embedCard, expand, heading, layoutSection, layoutSection_full, mediaGroup, mediaSingle, mediaSingle_caption, mediaSingle_full, orderedList, panel, paragraph, rule, table, taskList
47. **bulletList** - depends on: listItem
48. **doc** - depends on: blockCard, blockquote, bodiedExtension, bodiedSyncBlock, bulletList, codeBlock, codeBlock_root_only, decisionList, embedCard, expand, expand_root_only, extension, heading, layoutSection_full, mediaGroup, mediaSingle_caption, mediaSingle_full, orderedList, panel, paragraph, rule, syncBlock, table, taskList
49. **listItem** - depends on: bulletList, codeBlock, extension, mediaSingle_caption, mediaSingle_full, orderedList, paragraph, taskList
50. **orderedList** - depends on: listItem
51. **panel** - depends on: blockCard, bulletList, codeBlock, decisionList, extension, heading, mediaGroup, mediaSingle_caption, mediaSingle_full, orderedList, paragraph, rule, taskList

## Mark Definitions

16 mark types:

- alignment
- annotation
- backgroundColor
- border
- breakout
- code
- dataConsumer
- em
- fragment
- indentation
- link
- strike
- strong
- subsup
- textColor
- underline

## Recommended Implementation Phases

### Phase 1: Base Classes

- Base
- BaseNode
- BaseMark

### Phase 2: Marks

No internal dependencies, can be implemented in any order:

- MarkAlignment
- MarkAnnotation
- MarkBackgroundColor
- MarkBorder
- MarkBreakout
- MarkCode
- MarkDataConsumer
- MarkEm
- MarkFragment
- MarkIndentation
- MarkLink
- MarkStrike
- MarkStrong
- MarkSubsup
- MarkTextColor
- MarkUnderline

### Phase 3: Leaf Nodes

Nodes with no node dependencies:

- NodeBlockCard
- NodeDate
- NodeEmbedCard
- NodeEmoji
- NodeHardBreak
- NodeInlineCard
- NodeLayoutColumn
- NodeMention
- NodeNestedExpand
- NodePlaceholder
- NodeRule
- NodeStatus
- NodeTable_cell
- NodeTable_header
- NodeText

### Phase 4: Composite Nodes

Nodes with dependencies (implement in order):

- NodeBodiedExtension - needs: dataConsumer, fragment
- NodeExtension - needs: dataConsumer, fragment
- NodeInlineExtension - needs: dataConsumer, fragment
- NodeLayoutSection - needs: breakout, layoutColumn
- NodeLayoutSection_full - needs: breakout, layoutColumn, layoutSection
- NodeMedia - needs: annotation, border, link
- NodeMediaGroup - needs: media
- NodeMediaInline - needs: annotation, border, link
- NodeMediaSingle - needs: link
- NodeMediaSingle_full - needs: media, mediaSingle
- NodeExpand - needs: nestedExpand
- NodeExpand_root_only - needs: breakout, nestedExpand
- NodeSyncBlock - needs: breakout
- NodeTable_row - needs: table_cell, table_header
- NodeTable - needs: fragment, table_row
- NodeCodeBlock - needs: text
- NodeCodeBlock_root_only - needs: breakout, text
- NodeCode_inline - needs: annotation, code, link, text
- NodeFormatted_text_inline - needs: annotation, backgroundColor, em, link, strike, strong, subsup, text, textColor, underline
- NodeCaption - needs: code_inline, date, emoji, formatted_text_inline, hardBreak, inlineCard, mention, placeholder, status
- NodeInline - needs: code_inline, date, emoji, formatted_text_inline, hardBreak, inlineCard, inlineExtension, mediaInline, mention, placeholder, status
- NodeDecisionItem - needs: inline
- NodeDecisionList - needs: decisionItem
- NodeHeading - needs: alignment, indentation, inline
- NodeMediaSingle_caption - needs: caption, media, mediaSingle
- NodeParagraph - needs: alignment, indentation, inline
- NodeBlockTaskItem - needs: extension, paragraph
- NodeTaskItem - needs: inline
- NodeTaskList - needs: blockTaskItem, taskItem
- NodeBlockquote - needs: bulletList, codeBlock, extension, mediaGroup, mediaSingle_caption, mediaSingle_full, orderedList, paragraph
- NodeBodiedSyncBlock - needs: blockCard, blockquote, breakout, bulletList, codeBlock, decisionList, embedCard, expand, heading, layoutSection, layoutSection_full, mediaGroup, mediaSingle, mediaSingle_caption, mediaSingle_full, orderedList, panel, paragraph, rule, table, taskList
- NodeBulletList - needs: listItem
- NodeDoc - needs: blockCard, blockquote, bodiedExtension, bodiedSyncBlock, bulletList, codeBlock, codeBlock_root_only, decisionList, embedCard, expand, expand_root_only, extension, heading, layoutSection_full, mediaGroup, mediaSingle_caption, mediaSingle_full, orderedList, panel, paragraph, rule, syncBlock, table, taskList
- NodeListItem - needs: bulletList, codeBlock, extension, mediaSingle_caption, mediaSingle_full, orderedList, paragraph, taskList
- NodeOrderedList - needs: listItem
- NodePanel - needs: blockCard, bulletList, codeBlock, decisionList, extension, heading, mediaGroup, mediaSingle_caption, mediaSingle_full, orderedList, paragraph, rule, taskList