# OPlist - The Programmer's Search Engine

> This project sprung up as an idea - just like you would expect, though not in that fashion you are thinking of right now. The purpose, initially, was to understand how search engines work. But I suddenly lost interest in the mechanism of their operations, because it is an ancient and vast world and I am a relatively modern and knowledge-deficient programmer. Then **modesty** decides I offer this a gift to programmers...though not a perfect gift as some almost-perfect programmer's search engines out there. Don't be misled by the last sentence; this does its job and does it well, though _"flaws and flaws make a predefined flawless software a beautiful flaw"_.

**In one-liner; OPlist is a search engine that answers the programmer's questions in a funny satisfying way.**

## A WIND TOUR

There are some very funny ways that **OPlist** interacts with her users...

### #1/SEARCH SYNTAX

Her search syntax is the first; She bores a funny search rule that, if not understood, will only frustrate the programmer rather than bless him/her.

- Every search query assumes a *keyword* which defines how the search will be done. The default is `SEARCH`.
- This *keyword* must be capitalized (They are similar to SQL query syntax, but not as vast).
- There must come a slash (/) after the *keyword* to separate the keyword from its *disciple(s)*...
- Every keyword is being referred to as a **king**; Every *king* must have at least one *disciple*.
- The *disciple* must be within curly braces (`{}`) and must be separated from its *king* by blank space.
- Within the *disciple*'s environment there is a **head** and a **body**.
- The *head* specifies the keyword of the search (**confused?**; "See example below")
- The *body* dictates what to search for as regards the *head*.

#### SEARCH SYNTAX EXAMPLES

 > SEARCH/ {node 'how to install'}
**Note the above single quotes!** If you use double quotes, well I leave that to you to test out.
 > {node 'how to install'}
Here, the **king** was ignored since default is `SEARCH/`

**NOTE**: *More than one disciple is not allowed yet, but it will be included possibly in version 1.0.1

#### REASONS FOR A SEARCH SYNTAX

- Since machine learning techniques are not employed, it will be difficult to parse a search query that is not defined and depends on the user interacting with the **engine**, hence the **syntax**.
- With a search syntax, it will become easier to introduce the concept of **multiple** disciples in a later version.
- As programmers, we have to think programmatically... Do you agree? :smile:

## AUTHORS

OVECJOE <projectoplist@gmail.com>
