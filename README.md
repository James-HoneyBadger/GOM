# Gulf of Mexico Programming Language# Gulf of Mexico Interpreter# Gulf of Mexico Interpreter



An esoteric programming language interpreter with probabilistic variables, -1 array indexing, and temporal lifetimes.



## Quick StartAn interpreter for the Gulf of Mexico programming language - an esoteric language featuring exclamation mark terminators, -1-indexed arrays, four variable types, and many other delightful quirks.This is the interpreter for the perfect programming language. It is made in Python, for the sole reason that the interpreter can itself be interpreted. Future plans include creating a Gulf of Mexico interpreter in GulfOfMexico, so that the Gulf of Mexico Interpreter can be passed into the Gulf of Mexico Interpreter Interpreter, which is then interpreted by the Gulf of Mexico Interpreter Interpreter Interpreter (a.k.a. Python). This may or may not be created due to difficulty moving everything over and whatnot. I'll try though.



```bash

# Install

pip install -e .## Quick StartThis is incredibly slow. My implementation of Gulf of Mexico is suboptimal, which itself runs on a subperformant language (Python), which runs on a pretty fast language (C). However, speed was never a focus in creating my interpreter for Gulf of Mexico and shouldn't be - it's not a language meant for day-to-day use - it's a work of art.



# Run a program

python -m gulfofmexico script.gom

```bash## Architecture

# Start REPL

python -m gulfofmexico# Install



# Launch IDE (Qt or Web-based)pip install -e .The interpreter is a **monolithic Python implementation** (~2,900 lines in `gulfofmexico/interpreter.py`) that directly executes Gulf of Mexico code. It uses a three-stage pipeline:

python -m gulfofmexico.ide

```



## Core Features# Run a program1. **Lexer** (`processor/lexer.py`) - Tokenizes source code



### 1. Array Indexing Starts at -1gulfofmexico your_program.gom2. **Parser** (`processor/syntax_tree.py`) - Builds abstract syntax tree (AST)



Arrays/lists in Gulf of Mexico start at index -1, not 0:3. **Interpreter** (`interpreter.py`) - Directly executes AST using pattern matching



```# Interactive REPL

const numbers [-1, 0, 1, 2, 3]!

print(numbers[-1])!  // Prints: -1gulfofmexico**Note:** The `gulfofmexico/engine/` package contains an experimental modular architecture that is NOT used in production. The actual interpreter uses the original monolithic design in `interpreter.py`.

print(numbers[0])!   // Prints: 0

print(numbers[3])!   // Prints: 3

```

# Web-based IDE📖 **For detailed architecture documentation, see [ACTUAL_ARCHITECTURE.md](ACTUAL_ARCHITECTURE.md)**

### 2. Fractional Array Indexing

python -m gulfofmexico.ide --web

Insert elements between existing positions using fractional indexes:

```## Installation

```

const list [10, 20, 30]!

list[0.5] = 99!  // Inserts 99 between index 0 and 1

// list is now: [10, 20, 99, 30]## InstallationYou can install Gulf of Mexico from PyPi, by doing any the following:

```



### 3. Probabilistic Variables with Confidence

### From Source```

Variables have confidence levels (!, !!, !!!) that determine priority:

pip install GulfOfMexico 

```

const x 10!      // Confidence level 1```bashpip install "GulfOfMexico[input, globals]"

const x 20!!     // Confidence level 2 (overwrites level 1)

const x 30!!!    // Confidence level 3 (highest priority)git clone https://github.com/James-HoneyBadger/GOM.gitpip install "GulfOfMexico[input]"

print(x)!        // Prints: 30

```cd GOMpip install "GulfOfMexico[globals]"



### 4. Variable Lifetimespython -m venv .venv```



Variables can have temporal or line-based lifetimes:source .venv/bin/activate  # On Windows: .venv\Scripts\activate



```pip install -e .Each of these commands installs Gulf of Mexico with the respective dependencies. `input` installs the `pynput` package and allows the use of `after` statements and event watchers. `globals` installs `PyGithub` and allows you to declare `const const const` variables that are publically stored using GitHub. Note: to use the latter, you must enter a [Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) in the `GITHUB_ACCESS_TOKEN` environment variable.

// Temporal lifetime (5 seconds)

const temp <5.0> = 42!```



// Line-based lifetime (expires after 10 lines)## Usage

const shortLived 10 = 100!

```### Requirements



### 5. Three-Valued Boolean LogicNow that you have installed GulfOfMexico, you can run the REPL using the `$ GulfOfMexico` command, or you can run a file using `$ GulfOfMexico FILE`. Usage instructions here:



Booleans can be `true`, `false`, or `maybe`:- Python 3.10 or higher



```- Optional dependencies:```text

const certain true!

const uncertain maybe!  - `PySide6` or `PyQt5` for Qt-based GUI (not required for web IDE)usage: GulfOfMexico [-h] [-s] [file]

const wrong false!

  - `pynput` for input handling features

if maybe {

   print("This might execute")!  - `pygithub` for global variable featurespositional arguments:

}

```  file                  the file containing your Gulf of Mexico code



### 6. Flexible String Quoting## Language Features



Strings use quote count matching instead of traditional quoting:options:



```### Statement Terminators  -h, --help            show this help message and exit

const s1 "hello"!       // Single quotes each side

const s2 ""world""!     // Two quotes each side  -s, --show-traceback  show the full Python trackback upon errors

const s3 '"mixed"'!     // One single, one double each side

```All statements end with `!`:```



### 7. String Interpolation



Embed expressions in strings with `${}`:```gom### REPL and CLI (module entry)



```print("Hello, World!")!

const name "Alice"!

const age 30!const var x = 5!You can also use the Python module entry point, which runs the production interpreter and a robust REPL:

print("Hello, ${name}! You are ${age} years old.")!

// Prints: Hello, Alice! You are 30 years old.```

```

```bash

### 8. Next/Previous Value Tracking

Debug mode statements end with `?`:python -m gulfofmexico                 # Start interactive REPL

Access future and past values of variables:

python -m gulfofmexico path/to/file.gom  # Execute a .gom file

```

const x 10!```gompython -m gulfofmexico -c "print(123)!"   # Run inline code and exit

print(previous(x))!  // undefined initially

x = 20!print("Debug output")?python -m gulfofmexico -s path/file.gom   # Show full Python traceback on errors

print(previous(x))!  // Prints: 10

`````````



### 9. Reactive Programming with `when`



Execute code automatically when conditions become true:Multiple exclamation marks indicate confidence levels:REPL features:



```

var temperature 20!

```gom- Real execution path: tokenize → parse → interpret (no experimental engine)

when temperature > 30 {

   print("It's hot!")!const var important = 100!!- Persistent state across inputs (variables, watchers, public globals)

}

const var very_important = 200!!!- Multi-line input with auto-continuation

temperature = 35!  // Triggers the when statement

``````- Commands: `:help`, `:quit`, `:reset`, `:load <file>`, `:vars`



### 10. Async/Await Functions   `:history`, `:save <file> [all|last|<n>]`, `:open <file>`,



Functions can run asynchronously:### Variable Declarations   `:run <n>`, `:clip [last|<n>]`



```- `:run <n|last>`, `:clip [last|<n>]`

async function fetchData() => {

   // Async operationFour combinations of mutability:

   return 42!

}!Optional: Clipboard support in REPL



const result await(fetchData())!```gom

```

const const name = "Alice"!     // Cannot reassign or modify```bash

## Variable Modifiers

const var count = 0!            // Can modify, cannot reassignOptional: Clipboard support in REPL

### `const` - Immutable Value

var const limit = 100!          // Can reassign, cannot modify```

```

const x 10!var var value = 5!              // Can reassign and modify

x = 20!  // Error: cannot modify const

``````:clip` command will print the requested block so you can copy it manually.



### `var` - Mutable Reference`:clip` command will print the requested block so you can copy it manually.



```### Array Indexing

var x 10!

x = 20!  // OK### IDE (GUI)

```

Arrays start at **-1** (not 0):

### `const var` - Mutable Value, Immutable Reference

An experimental PySide6-based GUI IDE is included.

```

const var list [1, 2, 3]!```gom

list[0] = 99!   // OK: can modify elements

list = [4, 5]!  // Error: cannot reassignconst const scores = [3, 2, 5]!- Install GUI deps (Poetry extra): `poetry install -E ide`

```

print(scores[-1])!  // Prints: 3 (first element)- Or with pip: `pip install PySide6`

### `const const const` - Immutable Global

print(scores[0])!   // Prints: 2 (second element)- Launch:

Triple const creates globally shared immutable constants:

print(scores[1])!   // Prints: 5 (third element)

```

const const const PI 3.14159!``````bash

// Saved to ~/.gulfofmexico_runtime and optionally synced to GitHub

```python -m gulfofmexico.ide     # module entry



## Operators### Float Indexinggom-ide                        # via Poetry console script



### Arithmetic```

- `+` Addition / String concatenation

- `-` Subtraction / Negation / ReverseInsert elements at float indices:

- `*` Multiplication

- `/` DivisionIf PySide6 is not installed, the launcher prints a helpful message.

- `^` Exponentiation

```gom

### Comparison

- `<` Less thanvar var numbers = [1, 2, 3]!## TODO

- `>` Greater than

- `<=` Less than or equalnumbers[0.5] = 99!

- `>=` Greater than or equal

print(numbers)!  // [1, 99, 2, 3]- Add another expression type which is just the dot operator, used for indexing and accessing names

### Equality (Multiple Levels)

- `=` Approximate equality (fuzzy matching)```- Better debugging (pretty limited for the time being)

- `==` Regular equality

- `===` Strict equality (identity for mutables)- A much better standard library

- `====` Really strict equality (always identity)

### Functions- Allow for declaring basic objects with {} and other things.

### Logical

- `&` AND (short-circuits)- Add a way to deal with file objects

- `|` OR (short-circuits)

- `;` NOT (unary)Multiple function keywords (all equivalent):



### Inequality## Absent Features

- `;=` Not equal (approximately)

- `;==` Not equal (regular)```gom

- `;===` Not equal (strict)

- `;====` Not equal (really strict)function add(a, b) => {The goal of this project is to implement every feature from the Gulf of Mexico language. A list of features is in the README file of the project, linked [here](https://github.com/TodePond/GulfOfMexico---e-acc). Here is a working list of features that there is no chance I will implement (new features may be added - or I should say, removed - as I work on this project and realize I'm too stupid to implement them):



## Control Flow   return a + b!



### If Statements}!- DB3X: I am not going to even try to parse XML AND parse DB code.



```- Regex: Since type hints seem to not even do anything there is no point in implementing a Regex parser.

if condition {

   // codefunc multiply(x, y) => x * y!- "Variable Hoisting" (being able to declare variables with a negative lifetime): Given the fact that keywords can be renamed and reassigned in this language, it does not make sense to implement this as the following breaks:

}

```



### When Statements (Reactive)fun divide(a, b) => {    ```javascript



```   return a / b!    print(name)

when condition {

   // executes whenever condition becomes true}!    var const = "lol";

}

```    const const name<-2> = "Jake";



### After Statements (Scheduled)fn subtract(x, y) => x - y!    ```



``````

after <5.0> {

   print("5 seconds later")!    It is impossible to evaluate the expression on the right side of the `name` declaration after the print statement. Additionally, doing so doesn't account for possible renaming of keywords in the second line.

}

```### Booleans- Any sort of autocomplete requires more brainpower than I am willing to put in.



## Functions



### Regular FunctionsThree-valued boolean system:To my knowledge, everything else has been or will be implemented.



```

function add(a, b) => a + b!

```gom## Implemented Features

// Flexible keyword matching

fn multiply(a, b) => a * b!const const is_true = true!

func divide(a, b) => a / b!

```const const is_false = false!These are features that are implemented according to the [GulfOfMexico specification](https://github.com/TodePond/GulfOfMexico---e-acc) in this interpreter.



### Async Functionsconst const is_maybe = maybe!



``````### Exclamation Marks

async function slowOperation() => {

   // async code

   return result!

}!### StringsBe bold! End every statement with an exclamation mark!

```



## Classes and Objects

Multiple quote styles:```javascript

```

class Person {print("Hello world")!

   const name "Unknown"!

   var age 0!```gom```

   

   function greet() => {const const single = 'hello'!

      print("Hello, I'm ${name}")!

   }!const const double = "world"!If you're feeling extra-bold, you can use even more!!!

}!

const const triple = """multiline

const alice new Person()!

alice.name = "Alice"!string"""!```javascript

alice.age = 30!

alice.greet()!```print("Hello world")!!!

```

```

## Built-in Functions

Zero quotes (bare words):

### Type Conversion

- `Number(x)` - Convert to numberIf you're unsure, that's ok. You can put a question mark at the end of a line instead. It prints debug info about that line to the console for you.

- `String(x)` - Convert to string

- `Boolean(x)` - Convert to boolean```gom



### I/Oconst const name = hello!  // Equivalent to "hello"```javascript

- `print(...)` - Print values

- `read(path)` - Read file```print("Hello world")?

- `write(path, content)` - Write file

```

### Data Structures

- `Map()` - Create dictionary/mapString interpolation with regional currency symbols:

- `use(value)` - Create signal

You might be wondering what Gulf of Mexico uses for the 'not' operator, which is an exclamation mark in most other languages. That's simple - the 'not' operator is a semi-colon instead.

### Control

- `sleep(seconds)` - Pause execution```gom

- `exit()` - Exit program

const var name = "Alice"!```javascript

### Regex

- `regex_match(pattern, text)` - Test patternprint("Hello ${name}!")!       // $-styleif (;false) {

- `regex_findall(pattern, text)` - Find all matches

- `regex_replace(pattern, replacement, text)` - Replace matchesprint("Hello £{name}!")!       // £-style   print("Hello world")!



### Math Functionsprint("Hello €{name}!")!       // €-style}

All functions from Python's `math` module: `sin`, `cos`, `sqrt`, `log`, etc.

``````

### Word Numbers

- `zero` through `ninteen` - Numbers 0-19

- `twenty` through `ninety` - Returns function that adds tens place

  ```### Classes### Declarations

  const twentyThree twenty(three)!  // 23

  ```



## Debug Modifiers```gomThere are four types of declaration. Constant constants can't be changed in any way.



Add `?` after statements for debugging output:class Player {



```   const var health = 100!```javascript

const x 10?     // Level 1: Show value

const y 20??    // Level 2: Show value and names   const var score = 0!const const name = "Luke"!

const z 30???   // Level 3: Show value, names, and expression tree

const w 40????  // Level 4: Show everything}!```

```



## Import/Export

const var player = new Player()!Constant variables can be edited, but not re-assigned.

### Multi-File Programs

print(player)!

Split files using `=====` markers:

``````javascript

```

===== math_utils =====const var name = "Luke"!

function square(n) => n * n!

export square to main!### Conditionalsname.pop()!



===== main =====name.pop()!

import square!

print(square(5))!  // Prints: 25```gom```

```

const var x = 10!

## Installation

Variable constants can be re-assigned, but not edited.

### From Source

if (x > 5) {

```bash

git clone https://github.com/James-HoneyBadger/GOM.git   print("Greater than 5")!```javascript

cd GOM

pip install -e .}!var const name = "Luke"!

```

```name = "Lu"!

### Dependencies

```

Required:

- Python 3.10+### Import/Export

- requests 2.31.0

Variable variables can be re-assigned and edited.

Optional:

- pynput 1.7.6 (for keyboard/mouse input)```gom

- pygithub 2.2.0 (for global variable sync)

- PySide6 or PyQt5 (for Qt-based IDE)// export.gom```javascript



## IDEexport const const message = "Hello"!var var name = "Luke"!



Gulf of Mexico includes both Qt-based and web-based IDEs:export const var count = 42!name = "Lu"!



```bashname.push("k")!

# Launch IDE (tries Qt, falls back to web)

python -m gulfofmexico.ide// main.gomname.push("e")!



# Force web-based IDEimport message from "export.gom"!```

python -m gulfofmexico.ide --web

```print(message)!



The web IDE runs on `http://localhost:8080/ide` and includes:```### Immutable Data

- Syntax highlighting

- Example programs

- Save/Load functionality

- Execution with output capture### Reverse Statement**New for 2023!**<br>

- No dependencies (uses Python's built-in http.server)

Mutable data is an anti-pattern. Use the `const const const` keyword to make a constant constant constant. Its value will become constant and immutable, and will _never change_. Please be careful with this keyword, as it is very powerful, and will affect all users globally forever.

## Command-Line Usage

Undo variable assignments:

```bash

# Run a file```javascript

python -m gulfofmexico script.gom

```gomconst const const pi = 3.14!

# Inline code

python -m gulfofmexico -c "print(123)!"var var x = 5!```



# REPLprint(x)!  // 5

python -m gulfofmexico

x = 10!#### Notes About Implementation

# Show Python traceback on errors

python -m gulfofmexico -s script.gomprint(x)!  // 10

```

reverse!This is added by me (the interpreter)! I wanted to share how this works.

## Architecture

print(x)!  // 5

### Production Interpreter

```Thanks to [this repo](https://github.com/marcizhu/marcizhu) for helpful reference for issues and actions in Python.

All code execution flows through:

- `gulfofmexico/__init__.py` - Entry point with `run_file()`

- `gulfofmexico/interpreter.py` - Main execution engine (~2,900 lines)

- Pattern matching on statement types for execution### Temporal Keywords**Local Storage (Primary):** Immutable constants are stored locally in your home directory under `~/.GulfOfMexico_runtime/.immutable_constants` and `~/.GulfOfMexico_runtime/.immutable_constants_values/`. This ensures they persist across sessions and work offline.



### Experimental Components (Unused)



The following exist but are NOT used in production:Access variable history:**Global Storage (Optional):** When possible, constants are also shared globally via GitHub Issues API:

- `gulfofmexico/engine/` - Handler-based architecture proof-of-concept

- `gulfofmexico/plugin_system.py` - Plugin system (not implemented)

- Expression caching (not enabled)

```gom- On the user's side, open a GitHub issue with a title of the format `Create Public Global: {name};;;{confidence}` and the body containing the pickled version of the value.

## Language Specification

var var x = 10!- Then, run a GitHub workflow that puts the issue body into a file under `global_objects/` and add an entry to `public_globals.txt` that contains the `name;;;id;;;confidence`

Gulf of Mexico implements 92% of the original specification:

x = 20!- Finally, to retrieve these values, the content of each of these files is fetched and converted back into values.

**Implemented:**

- ✅ -1 array indexingx = 30!

- ✅ Fractional indexing

- ✅ Probabilistic variablesprint(current(x))!   // 30If GitHub is unavailable (no internet, no API token), the constants still work perfectly - they're just stored locally only.

- ✅ Temporal/line lifetimes

- ✅ Three-valued booleansprint(previous(x))!  // 20

- ✅ Flexible quoting

- ✅ String interpolation```### Naming

- ✅ next/previous tracking

- ✅ when statements

- ✅ async/await

- ✅ Classes### OperatorsBoth variables and constants can be named with any Unicode character or string.

- ✅ const const const globals

- ✅ Import/export

- ✅ Multiple equality levels

- ✅ 40+ built-in functions**Arithmetic:** `+`, `-`, `*`, `/`, `^` (exponentiation)```javascript



**Not Implemented:**const const firstAlphabetLetter = 'A'!

- ❌ Reverse time operator

- ❌ Some advanced plugin features**Comparison:** `>`, `<`, `>=`, `<=`, `==`, `!=`var const 👍 = True!

- ❌ Distributed execution

var var 1️⃣ = 1!

## Examples

**Logical:** `&` (AND), `|` (OR), `;` (NOT)```

### Hello World



```

print("Hello, World!")!**Division by zero returns `undefined`:**This includes numbers, and other language constructs.

```



### Fibonacci

```gom```javascript

```

function fib(n) => {const var result = 10 / 0!const const unchanging = const!

   if n <= 0 {

      return 0!print(result)!  // undefinedunchanging unchanging 5 = 4!

   }

   if n == 1 {```print(2 + 2 === 5)! //true

      return 1!

   }```

   return fib(n - 1) + fib(n - 2)!

}!### Delete Statement



print(fib(10))!### Arrays

```

Delete values from memory:

### Class Example

Some languages start arrays at `0`, which can be unintuitive for beginners. Some languages start arrays at `1`, which isn't representative of how the code actually works. Gulf of Mexico does the best of both worlds: Arrays start at `-1`.

```

class Counter {```gom

   var count 0!

   delete 3!```javascript

   function increment() => {

      count = count + 1!delete "hello"!const const scores = [3, 2, 5]!

      return count!

   }!delete true!print(scores[-1])! //3

}!

```print(scores[0])!  //2

const c new Counter()!

print(c.increment())!  // 1print(scores[1])!  //5

print(c.increment())!  // 2

```### Indentation```



### Reactive Programming



```**All indentation must be multiples of 3 spaces:****New for 2022!**<br>

var stock_price 100!

You can now use floats for indexes too!

when stock_price > 150 {

   print("Stock is high!")!```gom

}

function example() => {```javascript

when stock_price < 50 {

   print("Stock is low!")!   const var x = 5!const var scores = [3, 2, 5]!

}

   if (x > 0) {scores[0.5] = 4!

stock_price = 160!  // Triggers "Stock is high!"

stock_price = 45!   // Triggers "Stock is low!"      print("Positive")!print(scores)! //[3, 2, 4, 5]

```

   }!```

## License

}!

See LICENSE file for details.

```### When

## Contributing



This is an esoteric language project. Contributions welcome but expect unusual design decisions!

Tabs count as 2 spaces (intentionally awkward).In case you really need to vary a variable, the `when` keyword lets you check a variable each time it mutates.

## Author



James HoneyBadger

## Running Programs```javascript

const var health = 10!

### Command Linewhen (health = 0) {

   print("You lose")!

```bash}

# Run a file```

gulfofmexico program.gom

#### Technical Info

# Run with Python module

python -m gulfofmexico program.gomHi! It's me again. I took some creative liberty implementing the `when` statement, here's how it works:

```

- When defined, gather a list of names that are used in the expression of the statement.

### Interactive REPL- If a variable is detected, cause the when satement to watch that variable.

  - This is done in order to avoid watching names instead of variables when, say, a different variable with the same name is defined in a different scope.

```bash  - Speaking of scope, when statements for which changes are detected in a different scope (from that of definition) **use that scope within their code**.

gulfofmexico    - Looking back on my design decision, I am probably going to change this to make them always use the scope where they were defined.

```- Additionally, if a variable detected contains a mutable value, that mutable value is also watched, so the following code detects a change:



Features:    ```javascript

- Multi-line statement support    const var l = [1, 2, 3]!

- Arrow key navigation    when (l.length === 4) {

- Command history       print l!  

- Auto-completion    }

    const var l_alias = l!

### Web IDE    l_alias[1.5] = 4!  // triggers the when statement

    ```

```bash

python -m gulfofmexico.ide --webTherefore, the when statement can contain as complex an expression as desired. One small pitfall is that I've implemented it with recursion, which may cause performance issues (although I don't really care about performance, obvious in the fact that this is in Python).

```

### Lifetimes

Opens at `http://localhost:8080/ide`

GulfOfMexico has a built-in garbage collector that will automatically clean up unused variables (note: this is simply Python's garbage collector, I didn't implement anything). However, if you want to be extra careful, you can specify a lifetime for a variable, with a variety of units.

Features:

- Code editor with syntax awareness```javascript

- Save/load `.gom` files (Ctrl+S / Ctrl+O)const const name<2> = "Luke"! // lasts for two lines

- Run code (Ctrl+Enter)const const name<20s> = "Luke"! // lasts for 20 seconds

- Built-in examples```

- Error reporting

By default, a variable will last until the end of the program. But you can make it last in between program-runs by specifying a longer lifetime.

### Qt GUI IDE (if available)

```javascript

```bashconst const name<Infinity> = "Luke"! // lasts forever

python -m gulfofmexico.ide```

```

> Yes, this is a thing. It stores your variables and values to a folder in your home directory.

Note: Requires `PySide6` or `PyQt5`. Falls back to web IDE if Qt is unavailable.

### Loops

## Project Structure

Loops are a complicated relic of archaic programming languages. In GulfOfMexico, there are no loops.

```

gulfofmexico/### Booleans

├── __main__.py              # Entry point

├── base.py                  # Core types and errorsBooleans can be `true`, `false` or `maybe`.

├── builtin.py               # Built-in functions and values

├── constants.py             # Language constants```javascript

├── context.py               # Execution contextconst var keys = {}!

├── interpreter.py           # Main interpreterafter "keydown" { keys[event.key] = true! }

├── handlers.py              # Statement handlersafter "keyup" { keys[event.key] = false! }

├── repl.py                  # Interactive REPL

├── processor/function isKeyDown(key) => {

│   ├── lexer.py            # Tokenization   if (keys[key] = undefined) {

│   ├── syntax_tree.py      # AST generation      return maybe!

│   └── expression_tree.py  # Expression parsing   }

├── ide/   return keys[key]!

│   ├── web_ide.py          # Web-based IDE}

│   ├── app.py              # Qt GUI application```

│   ├── editor.py           # Code editor widget

│   └── highlighter.py      # Syntax highlighting**Technical info:** Booleans are stored as one-and-a-half bits.

└── plugins/

    └── example_custom_statement.py  # Plugin example### Arithmetic

```

GulfOfMexico has significant whitespace. Use spacing to specify the order of arithmetic operations.

## Development

```javascript

### Running Testsprint(1 + 2*3)! //7

print(1+2 * 3)! //9

```bash```

# Run a test file

python -m gulfofmexico test_features.gomUnlike some other languages, Gulf of Mexico allows you to use the caret (^) for exponentiation.



# Run examples```javascript

python -m gulfofmexico examples/hello.gomprint(1^1)! // 1

```print(2^3)! // 8

```

### Creating .gom Programs

You can also use the number name, for example:

1. Use `.gom` file extension

2. All statements end with `!````javascript

3. Use 3-space indentationprint(one+two)! // 3

4. Arrays start at index -1print  (twenty two  +  thirty three)!  // 55

5. Have fun with the quirks!```



## Examples> Yes, the second line is also valid. In an effort to preserve my sanity, I have limited this quirk to all numbers up to 99. After that, you're on your own.



See the `examples/` directory for sample programs:### Indents



- `hello.gom` - Hello WorldWhen it comes to indentation, Gulf of Mexico strikes a happy medium that can be enjoyed by everyone: All indents must be 3 spaces long.

- `calculator.gom` - Basic calculator

- `array_testing.gom` - Array manipulation```javascript

- `mandelbrot.gom` - Mandelbrot set generatorfunction main() => {

- `sierpinski.gom` - Sierpinski triangle   print("GulfOfMexico is the future")!

}

## Specification Compliance```



This interpreter implements **~92% of the Gulf of Mexico specification**, including:-3 spaces is also allowed.



✅ Exclamation mark terminators```javascript

✅ Four variable declaration types     function main() => {

✅ -1-indexed arrays with float indexingprint("GulfOfMexico is the future")!

✅ Multiple function keywords   }

✅ Three-valued booleans```

✅ String quote variations

✅ Import/export system> Note: Your code will err if you have indents that are not a multiple of three.

✅ Reverse statements

✅ Temporal keywords (previous/current)### Equality

✅ Delete statements

✅ Classes with constructorsJavaScript lets you do different levels of comparison. `==` for loose comparison, and `===` for a more precise check. Gulf of Mexico takes this to another level.

✅ Division by zero handling

You can use `==` to do a loose check.

See [LANGUAGE_REFERENCE.md](LANGUAGE_REFERENCE.md) for complete language documentation.

```javascript

## License3.14 == "3.14"! // true

```

See [LICENSE](LICENSE) file for details.

You can use `===` to do a more precise check.

## Credits

```javascript

Inspired by the [DreamBerd](https://github.com/TodePond/DreamBerd) programming language.3.14 === "3.14"! // false

```

Developed by James HoneyBadger.

You can use `====` to be EVEN MORE precise!

```javascript
const const pi = 3.14!
print(pi ==== pi)!  // true
print(3.14 ==== 3.14)!  // false
print(3.14 ==== pi)!  // false
```

If you want to be much less precise, you can use `=`.

```javascript
3 = 3.14! //true
```

### Functions

To declare a function, you can use any letters from the word `function` (as long as they're in order):

```javascript
function add (a, b) => a + b!
func multiply (a, b) => a * b!
fun subtract (a, b) => a - b!
fn divide (a, b) => a / b!
functi power (a, b) => a ** b!
union inverse (a) => 1/a!
```

### Dividing by Zero

Dividing by zero returns `undefined`.

```javascript
print(3 / 0)! // undefined
```

### Strings

Strings can be declared with single quotes or double quotes.

```javascript
const const name = 'Lu'!
const const name = "Luke"!
```

They can also be declared with triple quotes.

```javascript
const const name = "'Lu'"!
```

In fact, you can use any number of quotes you want.

```javascript
const const name = '""""Luke"""'"!
```

Even zero.

```javascript
const const name = Luke!
```

#### Technical Info

- To parse strings with many quotes, the interpreter scans the code for the shortest possible string.
- As soon as a pair of quote groups is found that is equal in terms of quote count on both sides, that is considered a string.
  - For example, `""""""` reads the two first double quotes, detects that there is a pair (`"` and `"`), and returns the corresponding empty string. This is repeated twice for the two remaining pairs of double quotes.
  - Therefore, to avoid premature detections of strings, simply create your starting quote with a single `'` and any number of `"`, like so: `'"""Hello world!'''''''`
- This is as complicated as it is in order to allow the declaration of empty strings without many problems.

### String Interpolation

Please remember to use your regional currency when interpolating strings.

```javascript
const const name = "world"!
print("Hello ${name}!")!
print("Hello £{name}!")!
print("Hello ¥{name}!")!
```

> Note: It was specified in the original repo to allow developers to follow their local typographical norms. While I think I could, that is not something I want to do and therefore I will not do it. Additionally, if the regional currency cannot be determined, the interpolation symbol defaults to the dollar sign.

### Types

Type annotations are optional.

```javascript
const var age: Int = 28!
```

By the way, strings are just arrays of characters.

```javascript
String == Char[]!
```

Similarly, integers are just arrays of digits. Hello again! Because of this, you can index into integers!

```javascript
const var my_number = 20!
my_number[-0.5] = 1!
print(my_number)!
```

If you want to use a binary representation for integers, `Int9` and `Int99` types are also available.

```javascript
const var age: Int9 = 28!
```

**Technical info:** Type annotations don't do anything, but they help some people to feel more comfortable.

### Previous

The `previous` keyword lets you see into the past!<br>
Use it to get the previous value of a variable.

```javascript
const var score = 5!
score = score + 1!
print(score)! // 6
print(previous score)! // 5
```

Similarly, the `next` keyword lets you see into the future!

```javascript
const var score = 5!
after ("click") { score = score + 1! }
print(await next score)! // 6 (when you click)
```

Additionally, the `current` keyword lets you see into the present!!

```javascript
const var score = 5!
print(current score)! // 5
```

### Exporting

Many languages allow you to import things from specific files. In GulfOfMexico, importing is simpler. Instead, you export _to_ specific files!

```java
===== add.gom3 ==
function add(a, b) => {
   return a + b!
}

export add to "main.gom3"!

===== main.gom3 ==
import add!
add(3, 2)!
```

### Classes

You can make classes, but you can only ever make one instance of them. This shouldn't affect how most object-oriented programmers work.

```javascript
class Player {
   const var health = 10!
}

const var player1 = new Player()!
const var player2 = new Player()! // Error: Can't have more than one 'Player' instance!
```

This is how you could do this:

```javascript
class PlayerMaker {
   function makePlayer() => {
      class Player {
         const var health = 10!
      }
      const const player = new Player()!
      return player!
   }
}

const const playerMaker = new PlayerMaker()!
const var player1 = playerMaker.makePlayer()!
const var player2 = playerMaker.makePlayer()!
```

### Delete

To avoid confusion, the `delete` statement only works with primitive values like numbers, strings, and booleans (I actually decided to implement it to delete those and also non-primitive things like variables - really, anything in the namespace).

```javascript
delete 3!
print(2 + 1)! // Error: 3 has been deleted
```

GulfOfMexico is a multi-paradigm programming language, which means that you can `delete` the keywords and paradigms you don't like.

```javascript
delete class!
class Player {} // Error: class was deleted
```

When perfection is achieved and there is nothing left to `delete`, you can do this:

```javascript
delete delete!
```

### Overloading

You can overload variables. The most recently defined variable gets used.

```javascript
const const name = "Luke"!
const const name = "Lu"!
print(name)! // "Lu"
```

Variables with more exclamation marks get prioritised.

```javascript
const const name = "Lu"!!
const const name = "Luke"!
print(name)! // "Lu"

const const name = "Lu or Luke (either is fine)"!!!!!!!!!
print(name)! // "Lu or Luke (either is fine)"
```

### Reversing

You can reverse the direction of your code.

```javascript
const const message = "Hello"!
print(message)!
const const message = "world"!
reverse!
```

### Class Names

For maximum compatibility with other languages, you can alternatively use the `className` keyword when making classes.

This makes things less complicated.

```javascript
className Player {
   const var health = 10!
}
```

In response to some recent criticism about this design decision, we would like to remind you that this is part of the JavaScript specification, and therefore - out of our control.

### Semantic naming

GulfOfMexico supports semantic naming.

```javascript
const const sName = "Lu"!
const const iAge = 29!
const const bHappy = true!
```

**New for 2023:** You can now make globals.

```javascript
const const g_fScore = 4.5!  // Interpreter maker here... idk if this is supposed to do anything, I could implement this easily if I had to
```

### Asynchronous Functions

In most languages, it's hard to get asynchronous functions to synchronise with each other. In GulfOfMexico, it's easy: Asynchronous functions take turns running lines of code.

```javascript
async funct count() {
   print(1)!
   print(3)!
}

count()!
print(2)!
```

You can use the `noop` keyword to wait for longer before taking your turn.

```javascript
async func count() {
   print(1)!
   noop!
   print(4)!
}

count()!
print(2)!
print(3)!
```

**Note:** In the program above, the computer interprets `noop` as a string and its sole purpose is to take up an extra line. You can use any string you want.

### Signals

To use a signal, use `use`.

```javascript
const var score = use(0)!
```

When it comes to signals, the most important thing to discuss is _syntax_.

In GulfOfMexico, you can set (and get) signals with just one function:

```javascript
const var score = use(0)!

score(9)! // Set the value
score()?  // Get the value (and print it)
```

### Copilot

It's worth noting that Github Copilot doesn't understand GulfOfMexico, which means that Microsoft won't be able to steal your code.

This is great for when you want to keep your open-sourced project closed-source.

### Highlighting

Syntax highlighting is now available for Gulf of Mexico in VSCode. To enable it, install a [highlighting extension](https://marketplace.visualstudio.com/items?itemName=fabiospampinato.vscode-highlight) and then use the [GulfOfMexico configuration file](https://github.com/TodePond/GulfOfMexico/blob/main/.vscode/settings.json).

This is what it looks like:

```
const const name = "Luke"!
print(name)! // "Luke"
```

**Please note:** The above code will only highlight correctly if you have the extension installed.

### Parentheses

Wait, I almost forgot!

Parentheses in Gulf of Mexico do nothing. They get replaced with whitespace.<br>
The following lines of code all do the same thing.

```javascript
add(3, 2)!
add 3, 2!
(add (3, 2))!
add)3, 2(!
```

Lisp lovers will love this feature. Use as many parentheses as you want!

```javascript
(add (3, (add (5, 6))))!
```

Lisp haters will also love it.

```javascript
(add (3, (add (5, 6)!
```

Due to certain design decisions, `"("` is replaced with `" "` while `")"` is replaced with `""`.
