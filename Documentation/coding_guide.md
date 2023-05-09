# Coding Guide
**Author:** Amela Pucic
**Date:** May 2023

## For examples take look into the [PEP 8- Syle Guide for Python](https://peps.python.org/pep-0008/)
## Code Layout
- Indentation
- Maximum Line Length are 79 characters
- Lines should break before a Binary Operator


## Naming Conventions 🐍
- descriptive names for variables, functions, classes
- snake_case
- Variable names start with lowercase letters
- Class names begin with upper case letters
- function names begin with lowercase letters
- global constants completely in capital letters

## Function Conventions
- Function description using ''' ''' Multi-Line Comments at the beginning of the function
  - (Optional) Description: 
  - Input: 
  - Output:
  - (Optional) additional Information:
- Metrics:
  - maximum number of function parameters: 5

## Comments
- keep it short and clear
- do not leave unnecessary code as comment
- use TODO comments

## Inclusion of MIT license in the source code
- use the [REUSE SOFTWARE](https://reuse.software/) format to declare license and copyright
  - [Documentation](https://reuse.readthedocs.io/en/latest/)
  - [Tutorial](https://reuse.software/tutorial/)
  - [API](https://api.reuse.software/info/git.fsfe.org/reuse/api)
- Each file needs to contain SPDX-FileCopyrightText and SPDX-License-Identifier tags in the header

   <pre><code>
   /*
   * SPDX-License-Identifier: MIT)
   * SPDX-FileCopyrightText: 2023 firstname lastname <email>
   * SPDX-FileCopyrightText: 2023 firstname lastname <email>
   */ </code></pre>


## GIT
- just push code that compiles
- Use only one account and one email
<pre><code>
//to check actual name or email
git config --list

//to change name or email
git config --local user.name "firstname lastname"
git config --local user.email "email"
</code></pre>
- Git Commit Sign-off
<pre><code>
git commit -m "Text" --signoff
</code></pre>
- Pair Programming
<pre><code>
git commit -a -m "Text
> Co-authored-by: firstname lastname <email>
> Co-authored-by: firstname lastname <email>
"
</code></pre>
