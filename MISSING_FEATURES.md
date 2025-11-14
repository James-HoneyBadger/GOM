# Missing Features Analysis - Gulf of Mexico Rust Interpreter

**Analysis Date:** November 13, 2025  
**Current Version:** 0.2.0  
**Test Status:** 26/26 passing  
**Overall Completion:** ~55% (up from 28%)

---

## Executive Summary

After implementing the 5 critical priorities (expression evaluation, variables, functions, arrays, basic temporal keywords), the Rust interpreter has reached **~55% specification compliance**. This document identifies the **45% of features still missing** from the specification.

### Recent Progress

- ✅ Expression evaluation with operator precedence
- ✅ Variable declaration and assignment with mutability
- ✅ Function definition and execution
- ✅ Array operations with -1 indexing and float indices
- ✅ Basic previous/current keywords

### Categories of Missing Features

| Category | Missing Features | Priority | Estimated Effort |
|----------|------------------|----------|------------------|
| **Advanced Operators** | 4 features | HIGH | 2-3 weeks |
| **Variable Lifetimes** | 3 features | HIGH | 2-3 weeks |
| **Reactive Programming** | 2 features | MEDIUM | 3-5 weeks |
| **Async System** | 2 features | MEDIUM | 3-4 weeks |
| **Advanced Features** | 5 features | LOW | 4-6 weeks |
| **Quality of Life** | 3 features | LOW | 1-2 weeks |

**Total Missing:** 19 major features

---

## 🔴 HIGH PRIORITY - Core Language Features

### 1. Variable Lifetime Enforcement ❌

**Specification:**

- `const const name<5> = "Luke"!` - expires after 5 lines
- `const const name<20s> = "Luke"!` - expires after 20 seconds
- `const const name<Infinity> = "Luke"!` - persists across program runs

**Current Status:**

- ✅ Parsing: Complete (`VariableLifetime` enum exists)
- ✅ Storage structure: Ready
- ❌ Expiration tracking: Not implemented
- ❌ Line-based cleanup: Not implemented
- ❌ Time-based cleanup: Not implemented
- ❌ Infinity persistence: Partially done (storage exists)

**What's Missing:**

```rust
// Need to implement in interpreter loop:
fn check_expired_variables(&mut self) {
    let current_line = self.current_line_number;
    let current_time = SystemTime::now();
    
    for namespace in &mut self.namespaces {
        namespace.retain(|name, entry| {
            match entry {
                NamespaceEntry::Variable(var) => {
                    match var.lifetime {
                        VariableLifetime::Lines(expires_at_line) => {
                            current_line < expires_at_line
                        }
                        VariableLifetime::Time(expires_at_time) => {
                            current_time < expires_at_time
                        }
                        VariableLifetime::Forever => true,
                    }
                }
                _ => true,
            }
        });
    }
}
```

**Files to Modify:**

- `src/interpreter.rs` - Add cleanup in `execute_statement()` loop
- `src/builtin.rs` - Ensure Variable struct tracks creation time/line
- `src/storage.rs` - Implement Infinity persistence load/save

**Test Cases Needed:**

```gom
// Test line-based expiration
const const x<3> = 5!
print(x)!  // Works
print("line 2")!
print("line 3")!
print(x)!  // Error: x expired

// Test time-based expiration
const const y<2s> = "hello"!
print(y)!  // "hello"
sleep(3s)!
print(y)!  // Error: y expired

// Test Infinity persistence
const const z<Infinity> = "persistent"!
// Should survive program restart
```

**Estimated Effort:** 2-3 weeks
**Complexity:** Medium (requires timer management and file I/O)

---

### 2. Significant Whitespace Arithmetic ❌

**Specification:**

```gom
print(1 + 2*3)!  // 7  (2*3 first, then +1)
print(1+2 * 3)!  // 9  ((1+2) first, then *3)
```

**Current Status:**

- ❌ Whitespace detection in lexer: Not implemented
- ❌ Operator precedence override: Not implemented
- ✅ Basic operator precedence: Working (but ignores whitespace)

**What's Missing:**

1. Lexer must track whitespace between tokens
2. Parser must adjust precedence based on whitespace
3. Expression tree must respect whitespace-based grouping

**Implementation Approach:**

```rust
// In lexer.rs - track whitespace
pub struct Token {
    pub whitespace_before: usize,  // NEW
    pub whitespace_after: usize,   // NEW
    // ... existing fields
}

// In expression_tree.rs - precedence adjustment
fn get_operator_precedence(op: &Token, left_spacing: usize, right_spacing: usize) -> u8 {
    let base_precedence = match op.token_type {
        TokenType::Plus | TokenType::Minus => 1,
        TokenType::Star | TokenType::Slash => 2,
        // ...
    };
    
    // If operator has more whitespace on one side, reduce its precedence
    if left_spacing > right_spacing {
        base_precedence - 1  // Bind to right first
    } else if right_spacing > left_spacing {
        base_precedence - 1  // Bind to left first
    } else {
        base_precedence
    }
}
```

**Files to Modify:**

- `src/processor/lexer.rs` - Track whitespace in tokens
- `src/processor/expression_tree.rs` - Adjust precedence calculation
- `src/base.rs` - Update Token struct

**Test Cases Needed:**

```gom
print(1 + 2*3)!       // 7
print(1+2 * 3)!       // 9
print(1  +  2  *  3)! // 7 (equal spacing = normal precedence)
print(1+ 2 * 3)!      // 9 (right side has more space)
```

**Estimated Effort:** 2-3 weeks
**Complexity:** High (requires lexer/parser refactoring)

---

### 3. Number Name Parsing ❌

**Specification:**

```gom
print(one + two)!  // 3
print(twenty two + thirty three)!  // 55
```

**Current Status:**

- ❌ Number name recognition: Not implemented
- ❌ Compound number parsing: Not implemented
- ✅ Number type system: Working

**What's Missing:**

```rust
// In lexer.rs - recognize number names
fn parse_number_name(word: &str) -> Option<f64> {
    match word {
        "zero" => Some(0.0),
        "one" => Some(1.0),
        "two" => Some(2.0),
        // ... up to "ninety nine"
        _ => None,
    }
}

// Handle compound numbers: "twenty two" = 22
fn parse_compound_number(tokens: &[Token]) -> Option<(f64, usize)> {
    if tokens.len() < 2 { return None; }
    
    let tens = parse_number_name(&tokens[0].value)?;
    let ones = parse_number_name(&tokens[1].value)?;
    
    if tens >= 20.0 && tens < 100.0 && ones < 10.0 {
        Some((tens + ones, 2))  // consumed 2 tokens
    } else {
        None
    }
}
```

**Files to Modify:**

- `src/processor/lexer.rs` - Add number name dictionary
- `src/processor/expression_tree.rs` - Handle number names in expressions

**Test Cases Needed:**

```gom
print(one)!                 // 1
print(two + three)!         // 5
print(twenty two)!          // 22
print(ninety nine - one)!   // 98
```

**Estimated Effort:** 1-2 weeks
**Complexity:** Medium (dictionary lookup + compound parsing)

---

### 4. Four-Level Equality Operators ❌

**Specification:**

```gom
3.14 = "3.14"!    // true  (very loose)
3.14 == "3.14"!   // true  (loose)
3.14 === "3.14"!  // false (strict type check)

const const pi = 3.14!
print(pi ==== pi)!     // true  (same reference)
print(3.14 ==== 3.14)! // false (different literals)
print(3.14 ==== pi)!   // false (literal vs variable)
```

**Current Status:**

- ✅ `==`, `===`, `====` parsing: Complete
- ❌ `=` (single equals) comparison: Not implemented
- ❌ Differentiated comparison logic: Not implemented
- ✅ Basic equality: Working (treats all as `===`)

**What's Missing:**

```rust
// In evaluate_binary_operation()
match operator_type {
    OperatorType::E => {  // Single =
        // Very loose comparison: coerce both to numbers
        let left_num = coerce_to_number(&left);
        let right_num = coerce_to_number(&right);
        Ok(DreamberdValue::Boolean(
            DreamberdBoolean::new(Some(left_num == right_num))
        ))
    }
    OperatorType::Ee => {  // ==
        // Loose comparison: string "3.14" equals number 3.14
        let left_coerced = loose_coerce(&left);
        let right_coerced = loose_coerce(&right);
        Ok(DreamberdValue::Boolean(
            DreamberdBoolean::new(Some(left_coerced == right_coerced))
        ))
    }
    OperatorType::Eee => {  // ===
        // Strict comparison: types must match
        Ok(DreamberdValue::Boolean(
            DreamberdBoolean::new(Some(left == right))
        ))
    }
    OperatorType::Eeee => {  // ====
        // Identity comparison: same memory location
        let left_id = get_value_identity(&left);
        let right_id = get_value_identity(&right);
        Ok(DreamberdValue::Boolean(
            DreamberdBoolean::new(Some(left_id == right_id))
        ))
    }
}
```

**Files to Modify:**

- `src/interpreter.rs` - Implement four comparison levels in `evaluate_binary_operation()`
- `src/builtin.rs` - Add value identity tracking (memory addresses or unique IDs)

**Test Cases Needed:**

```gom
// Very loose (=)
print(3 = 3.14)!       // true
print("3" = 3)!        // true

// Loose (==)
print(3.14 == "3.14")! // true
print(3 == "3")!       // true

// Strict (===)
print(3.14 === "3.14")! // false
print(3 === 3)!         // true

// Identity (====)
const const x = 5!
const const y = 5!
print(x ==== x)!       // true
print(x ==== y)!       // false (different variables)
print(5 ==== 5)!       // false (different literals)
```

**Estimated Effort:** 1-2 weeks
**Complexity:** Medium (requires value identity tracking)

---

## 🟡 MEDIUM PRIORITY - Advanced Features

### 5. When Statement Reactive Execution ❌

**Specification:**

```gom
const var health = 10!
when (health === 0) {
   print("You lose")!
}
// Later...
health = 0!  // Triggers the when statement
```

**Current Status:**

- ✅ When statement parsing: Complete
- ✅ Initial condition evaluation: Working
- ✅ Variable dependency extraction: Working
- ❌ Mutation hooks: Not implemented
- ❌ Re-triggering on variable change: Not implemented

**What's Missing:**

```rust
// Need to add mutation hooks to assign_variable()
fn assign_variable(&mut self, name: &str, value: DreamberdValue) -> Result<(), DreamberdError> {
    // ... existing assignment logic ...
    
    // NEW: Trigger when statements watching this variable
    self.check_when_statements_for_variable(name)?;
    
    Ok(())
}

fn check_when_statements_for_variable(&mut self, var_name: &str) -> Result<(), DreamberdError> {
    let mut triggered_whens = Vec::new();
    
    // Find all when statements that depend on this variable
    for (idx, when_stmt) in self.when_statements.iter().enumerate() {
        if when_stmt.dependent_variables.contains(&var_name.to_string()) {
            // Re-evaluate the condition
            let condition_result = self.evaluate_expression(&when_stmt.condition)?;
            let condition_bool = db_to_boolean(&condition_result);
            
            if let DreamberdBoolean { value: Some(true), .. } = condition_bool {
                triggered_whens.push(idx);
            }
        }
    }
    
    // Execute triggered when statement bodies
    for idx in triggered_whens {
        let when_stmt = &self.when_statements[idx];
        self.interpret_code_statements(when_stmt.body.clone())?;
    }
    
    Ok(())
}
```

**Files to Modify:**

- `src/interpreter.rs` - Add mutation hooks in `assign_variable()`, `execute_index_assignment()`
- `src/builtin.rs` - Track mutable value changes (lists, objects)

**Test Cases Needed:**

```gom
// Basic when statement
const var score = 0!
when (score === 10) {
    print("You win!")!
}
score = 10!  // Should print "You win!"

// When with complex condition
const var health = 100!
const var shield = 50!
when (health + shield < 50) {
    print("Critical condition!")!
}
health = 30!  // Should trigger
shield = 10!  // Should not trigger (already triggered)

// When with mutable values
const var items = [1, 2, 3]!
when (items.length === 5) {
    print("Full inventory!")!
}
items[1.5] = 4!
items[2.5] = 5!  // Should print "Full inventory!"
```

**Estimated Effort:** 3-5 weeks
**Complexity:** High (requires comprehensive mutation tracking)

---

### 6. After Statement Event Matching ❌

**Specification:**

```gom
after "keydown:A" {
    print("A pressed")!
}

after "click" {
    print("Mouse clicked")!
}
```

**Current Status:**

- ✅ Event system infrastructure: Complete (rdev, channels)
- ✅ After statement parsing: Complete
- ✅ Event queue: Working
- ✅ trigger() builtin: Working
- ❌ Event pattern parsing: Not implemented
- ❌ Event matching logic: Not implemented
- ❌ Integration with main loop: Partial

**What's Missing:**

```rust
// Parse event patterns like "keydown:A" or "click"
fn parse_event_pattern(pattern: &str) -> EventPattern {
    let parts: Vec<&str> = pattern.split(':').collect();
    match parts[0] {
        "keydown" => {
            let key = parts.get(1).unwrap_or(&"");
            EventPattern::KeyDown(key.to_string())
        }
        "keyup" => {
            let key = parts.get(1).unwrap_or(&"");
            EventPattern::KeyUp(key.to_string())
        }
        "click" => EventPattern::MouseClick,
        "mousedown" => EventPattern::MouseDown,
        "mouseup" => EventPattern::MouseUp,
        _ => EventPattern::Unknown,
    }
}

// Match incoming events against patterns
fn matches_event_pattern(event: &InputEvent, pattern: &EventPattern) -> bool {
    match (event, pattern) {
        (InputEvent::KeyDown(k1), EventPattern::KeyDown(k2)) => {
            k2.is_empty() || k1 == k2
        }
        (InputEvent::MouseClick, EventPattern::MouseClick) => true,
        _ => false,
    }
}
```

**Files to Modify:**

- `src/interpreter.rs` - Implement event pattern parsing in `execute_after_statement()`
- `src/interpreter.rs` - Add event matching in `process_input_event()`
- `src/base.rs` - Define EventPattern enum

**Test Cases Needed:**

```gom
// Specific key events
after "keydown:A" {
    print("A pressed")!
}

// Any keydown
after "keydown" {
    print("Some key pressed")!
}

// Mouse events
after "click" {
    print("Clicked!")!
}

// Multiple handlers for same event
after "click" { print("Handler 1")! }
after "click" { print("Handler 2")! }
// Should print both when clicked
```

**Estimated Effort:** 2-3 weeks
**Complexity:** Medium (pattern parsing + matching logic)

---

### 7. Async Functions with Turn-Based Execution ❌

**Specification:**

```gom
async func count() {
    print(1)!
    print(3)!
}

count()!
print(2)!
// Output: 1, 2, 3
```

**Current Status:**

- ✅ Async keyword parsing: Complete
- ✅ `is_async` flag in functions: Tracked
- ❌ Turn-based execution scheduler: Not implemented
- ❌ Statement interleaving: Not implemented
- ❌ noop keyword handling: Not implemented

**What's Missing:**

```rust
// Turn-based scheduler
struct AsyncScheduler {
    running_functions: Vec<AsyncFunctionContext>,
    current_turn: usize,
}

struct AsyncFunctionContext {
    func: DreamberdFunction,
    statements: Vec<Statement>,
    current_statement: usize,
    local_namespace: HashMap<String, NamespaceEntry>,
}

impl Interpreter {
    fn execute_async_function(&mut self, func: &DreamberdFunction, args: Vec<DreamberdValue>) {
        // Add to scheduler instead of executing immediately
        let context = AsyncFunctionContext {
            func: func.clone(),
            statements: func.body.clone(),
            current_statement: 0,
            local_namespace: HashMap::new(),
        };
        self.async_scheduler.running_functions.push(context);
    }
    
    fn run_async_turn(&mut self) -> Result<(), DreamberdError> {
        if self.async_scheduler.running_functions.is_empty() {
            return Ok(());
        }
        
        let idx = self.async_scheduler.current_turn % 
                  self.async_scheduler.running_functions.len();
        let context = &mut self.async_scheduler.running_functions[idx];
        
        if context.current_statement < context.statements.len() {
            let stmt = context.statements[context.current_statement].clone();
            self.execute_statement(stmt)?;
            context.current_statement += 1;
        } else {
            // Function complete, remove from scheduler
            self.async_scheduler.running_functions.remove(idx);
        }
        
        self.async_scheduler.current_turn += 1;
        Ok(())
    }
}
```

**Files to Modify:**

- `src/interpreter.rs` - Add AsyncScheduler struct and turn-based execution
- `src/interpreter.rs` - Modify `evaluate_function_call()` to detect async
- `src/interpreter.rs` - Add `run_async_turn()` to main loop

**Test Cases Needed:**

```gom
// Basic async interleaving
async func count() {
    print(1)!
    print(3)!
}
count()!
print(2)!
// Output: 1, 2, 3

// Multiple async functions
async func a() { print("A1")! print("A2")! }
async func b() { print("B1")! print("B2")! }
a()!
b()!
// Output: A1, B1, A2, B2

// noop keyword
async func delayed() {
    print(1)!
    noop!
    print(4)!
}
delayed()!
print(2)!
print(3)!
// Output: 1, 2, 3, 4
```

**Estimated Effort:** 3-4 weeks
**Complexity:** High (requires execution scheduler)

---

### 8. Next Keyword with Future Values ❌

**Specification:**

```gom
const var score = 5!
after "click" { score = score + 1! }
print(await next score)!  // Waits until score changes, prints 6
```

**Current Status:**

- ❌ next keyword: Not implemented
- ❌ Future value promises: Not implemented
- ❌ await integration: Not implemented
- ✅ previous keyword: Working
- ✅ current keyword: Working

**What's Missing:**

```rust
// Promise type for future values
pub struct FutureValue {
    variable_name: String,
    waiting_for_change: bool,
    resolved_value: Option<DreamberdValue>,
}

impl Interpreter {
    fn evaluate_next_keyword(&mut self, var_name: &str) -> Result<DreamberdValue, DreamberdError> {
        // Create a promise that resolves when the variable changes
        let future = FutureValue {
            variable_name: var_name.to_string(),
            waiting_for_change: true,
            resolved_value: None,
        };
        
        // Register this promise to be resolved on next mutation
        self.future_promises.push(future);
        
        // Return a Promise value (needs await)
        Ok(DreamberdValue::Promise(DreamberdPromise::new(var_name.to_string())))
    }
    
    fn assign_variable(&mut self, name: &str, value: DreamberdValue) -> Result<(), DreamberdError> {
        // ... existing logic ...
        
        // Resolve any promises waiting for this variable
        for promise in &mut self.future_promises {
            if promise.variable_name == name && promise.waiting_for_change {
                promise.resolved_value = Some(value.clone());
                promise.waiting_for_change = false;
            }
        }
        
        Ok(())
    }
}
```

**Files to Modify:**

- `src/interpreter.rs` - Add `evaluate_next_keyword()` and promise tracking
- `src/builtin.rs` - Add Promise type (already defined but unused)
- `src/interpreter.rs` - Add await expression evaluation

**Test Cases Needed:**

```gom
// Basic next keyword
const var x = 5!
const const future_x = next x!  // Creates promise
x = 10!
print(await future_x)!  // 10

// next with events
const var clicks = 0!
after "click" { clicks = clicks + 1! }
print(await next clicks)!  // Waits for click, then prints 1

// Multiple next promises
const var score = 0!
const const next1 = next score!
const const next2 = next score!
score = 5!
print(await next1)!  // 5
score = 10!
print(await next2)!  // 10
```

**Estimated Effort:** 3-4 weeks
**Complexity:** High (requires promise system + async integration)

---

## 🟢 LOW PRIORITY - Quality of Life

### 9. Variable Overloading by Exclamation Count ❌

**Specification:**

```gom
const const name = "Lu"!!
const const name = "Luke"!
print(name)!  // "Lu" (more exclamation marks win)
```

**Current Status:**

- ✅ Confidence level parsing: Complete
- ❌ Priority-based variable lookup: Not implemented
- ✅ Variable overloading: Working (last definition wins)

**What's Missing:**

```rust
// Modify variable lookup to check confidence
fn lookup_variable(&self, name: &str) -> Option<&Variable> {
    // Search namespaces in reverse (innermost first)
    for namespace in self.namespaces.iter().rev() {
        if let Some(entry) = namespace.get(name) {
            if let NamespaceEntry::Variable(var) = entry {
                // NEW: Keep searching for higher confidence
                let mut best_var = var;
                let mut best_confidence = var.lifetime.confidence;
                
                // Check all namespaces for this variable
                for ns in &self.namespaces {
                    if let Some(NamespaceEntry::Variable(candidate)) = ns.get(name) {
                        if candidate.lifetime.confidence > best_confidence {
                            best_var = candidate;
                            best_confidence = candidate.lifetime.confidence;
                        }
                    }
                }
                
                return Some(best_var);
            }
        }
    }
    None
}
```

**Files to Modify:**

- `src/interpreter.rs` - Update `lookup_variable()` to respect confidence levels

**Test Cases Needed:**

```gom
const const x = 1!
const const x = 2!!
const const x = 3!!!
print(x)!  // 3 (highest confidence)

// Overriding with lower confidence doesn't work
const const y = "first"!!!
const const y = "second"!
print(y)!  // "first" (higher confidence)
```

**Estimated Effort:** 1 week
**Complexity:** Low (simple priority comparison)

---

### 10. Reverse Statement Execution ❌

**Specification:**

```gom
const const message = "Hello"!
print(message)!
const const message = "world"!
reverse!
// Executes in reverse: "world", print("world"), "Hello"
```

**Current Status:**

- ✅ Reverse statement parsing: Complete
- ❌ Statement reordering: Not implemented
- ❌ Execution direction tracking: Not implemented

**What's Missing:**

```rust
fn execute_reverse_statement(&mut self) -> Result<(), DreamberdError> {
    // Reverse the order of all statements before this point
    let reverse_idx = self.current_statement_index;
    
    // Get all statements up to this point
    let mut to_reverse: Vec<Statement> = self.statements[0..reverse_idx]
        .iter()
        .cloned()
        .collect();
    
    // Reverse them
    to_reverse.reverse();
    
    // Replace in statement list
    for (i, stmt) in to_reverse.iter().enumerate() {
        self.statements[i] = stmt.clone();
    }
    
    // Re-execute from the beginning
    self.current_statement_index = 0;
    
    Ok(())
}
```

**Files to Modify:**

- `src/interpreter.rs` - Implement `execute_reverse_statement()` with statement reordering

**Test Cases Needed:**

```gom
print("1")!
print("2")!
reverse!
// Output: 2, 1

// Multiple reverses
print("A")!
print("B")!
reverse!
print("C")!
reverse!
// Output: B, A, C, A, B (?)
```

**Estimated Effort:** 1-2 weeks
**Complexity:** Medium (requires statement list manipulation)

---

### 11. Delete Keyword Feature ❌

**Specification:**

```gom
delete 3!
print(2 + 1)!  // Error: 3 has been deleted

delete class!
class Player {}  // Error: class keyword deleted
```

**Current Status:**

- ✅ Delete statement parsing: Complete
- ✅ Variable deletion: Working
- ❌ Value deletion from global space: Not implemented
- ❌ Keyword deletion: Not implemented
- ❌ Error enforcement when using deleted items: Not implemented

**What's Missing:**

```rust
// Global deleted items registry
struct DeletedItems {
    values: HashSet<String>,      // "3", "true", "hello"
    keywords: HashSet<String>,     // "class", "function", etc.
}

impl Interpreter {
    fn execute_delete_statement(&mut self, target: ExpressionTreeNode) -> Result<(), DreamberdError> {
        match target {
            ExpressionTreeNode::Value(val) => {
                match val.token.token_type {
                    TokenType::Number => {
                        // Delete the number globally
                        self.deleted_items.values.insert(val.token.value.clone());
                    }
                    TokenType::String => {
                        // Delete the string or keyword
                        if is_keyword(&val.token.value) {
                            self.deleted_items.keywords.insert(val.token.value.clone());
                        } else {
                            self.deleted_items.values.insert(val.token.value.clone());
                        }
                    }
                    _ => {}
                }
            }
            _ => {}
        }
        Ok(())
    }
    
    // Check before using any value
    fn check_not_deleted(&self, value: &DreamberdValue) -> Result<(), DreamberdError> {
        let value_str = match value {
            DreamberdValue::Number(n) => format!("{}", n.value),
            DreamberdValue::String(s) => s.value.clone(),
            DreamberdValue::Boolean(b) => format!("{:?}", b.value),
            _ => return Ok(()),
        };
        
        if self.deleted_items.values.contains(&value_str) {
            return Err(DreamberdError::InterpretationError(
                format!("Cannot use deleted value: {}", value_str)
            ));
        }
        
        Ok(())
    }
}
```

**Files to Modify:**

- `src/interpreter.rs` - Add DeletedItems tracking
- `src/interpreter.rs` - Add checks in `evaluate_expression()`
- `src/processor/lexer.rs` - Check deleted keywords during tokenization

**Test Cases Needed:**

```gom
delete 3!
print(2 + 1)!  // Error: 3 was deleted

delete true!
if (true) { print("hi")! }  // Error: true was deleted

delete class!
class Foo {}  // Error: class keyword was deleted

delete delete!
delete 5!  // Error: delete was deleted
```

**Estimated Effort:** 2 weeks
**Complexity:** Medium (requires global state + error checks)

---

### 12. Indentation Enforcement ❌

**Specification:**

```gom
function main() => {
   print("Must be 3 spaces")!
}

   function also_valid() => {
print("Negative 3 spaces (-3 outdent)")!
   }
```

**Current Status:**

- ❌ Indentation tracking: Not implemented
- ❌ Multiple-of-3 validation: Not implemented
- ❌ Negative indentation support: Not implemented

**What's Missing:**

```rust
// In lexer.rs - track indentation
fn validate_indentation(line: &str, line_number: usize) -> Result<(), DreamberdError> {
    let leading_spaces = line.chars().take_while(|c| *c == ' ').count();
    
    if leading_spaces % 3 != 0 {
        return Err(DreamberdError::SyntaxError(
            format!("Line {}: Indentation must be a multiple of 3 spaces (found {})", 
                    line_number, leading_spaces)
        ));
    }
    
    Ok(())
}
```

**Files to Modify:**

- `src/processor/lexer.rs` - Add indentation validation before tokenization

**Test Cases Needed:**

```gom
function good() => {
   print("3 spaces OK")!
}

function bad() => {
  print("2 spaces")!  // Error
}

   function negative() => {
print("-3 spaces OK")!
   }
```

**Estimated Effort:** 1 week
**Complexity:** Low (simple validation)

---

### 13. String Interpolation Execution ❌

**Specification:**

```gom
const const name = "world"!
print("Hello ${name}!")!       // "Hello world!"
print("Hello £{name}!")!       // "Hello world!"
print("Price: ${5 + 3}")!      // "Price: 8"
```

**Current Status:**

- ✅ Interpolation token detection: Complete (lexer recognizes `${}`, `£{}`, etc.)
- ❌ Expression evaluation inside interpolation: Not fully implemented
- ❌ Regional currency symbol handling: Recognized but not executed

**What's Missing:**

The code in `src/interpreter.rs` around line 706 attempts interpolation but needs completion:

```rust
// Current code (partial)
match crate::processor::expression_tree::build_expression_tree("interpolation", tokens, &expr_str) {
    Ok(expr_tree) => {
        match self.evaluate_expression(&expr_tree) {
            Ok(value) => {
                // Convert value to string and insert
                let value_str = self.value_to_string(&value)?;
                result.push_str(&value_str);
            }
            Err(_) => {
                // Fallback to literal
                result.push_str(&format!("${{{}}}", expr_str));
            }
        }
    }
    Err(_) => {
        result.push_str(&format!("${{{}}}", expr_str));
    }
}

// Need to add regional currency support
fn get_interpolation_symbol() -> String {
    // Could detect locale, but spec says default to $
    // Support: $, £, ¥, €, etc.
    "$".to_string()
}
```

**Files to Modify:**

- `src/interpreter.rs` - Complete interpolation evaluation (around line 680-730)
- Test the existing code more thoroughly

**Test Cases Needed:**

```gom
const const x = 5!
print("Value: ${x}")!          // "Value: 5"
print("Math: ${2 + 3}")!       // "Math: 5"
print("Call: ${add(1, 2)}")!   // "Call: 3"

// Regional currencies
print("UK: £{x}")!             // "UK: 5"
print("Japan: ¥{x}")!          // "Japan: 5"
```

**Estimated Effort:** 1 week (mostly testing)
**Complexity:** Low (infrastructure exists, needs polish)

---

### 14. Signal System (use keyword) ❌

**Specification:**

```gom
const var signal = use(0)!
print(signal())!   // Get: 0
signal(5)!         // Set: 5
print(signal())!   // Get: 5
```

**Current Status:**

- ❌ use keyword: Not implemented
- ❌ Signal type: Not implemented
- ❌ Getter/setter syntax: Not implemented

**What's Missing:**

```rust
// Signal type
pub struct DreamberdSignal {
    value: Box<DreamberdValue>,
    subscribers: Vec<Box<dyn Fn(&DreamberdValue)>>,  // For reactivity
}

// use() builtin function
fn builtin_use(&mut self, args: Vec<DreamberdValue>) -> Result<DreamberdValue, DreamberdError> {
    if args.is_empty() {
        return Err(DreamberdError::NonFormattedError("use() requires initial value".to_string()));
    }
    
    Ok(DreamberdValue::Signal(DreamberdSignal {
        value: Box::new(args[0].clone()),
        subscribers: Vec::new(),
    }))
}

// Signal call evaluation
fn evaluate_signal_call(&mut self, signal: &DreamberdSignal, args: Vec<DreamberdValue>) -> Result<DreamberdValue, DreamberdError> {
    if args.is_empty() {
        // Getter: signal()
        Ok(*signal.value.clone())
    } else {
        // Setter: signal(new_value)
        signal.value = Box::new(args[0].clone());
        
        // Notify subscribers
        for subscriber in &signal.subscribers {
            subscriber(&signal.value);
        }
        
        Ok(DreamberdValue::Undefined(DreamberdUndefined))
    }
}
```

**Files to Modify:**

- `src/builtin.rs` - Add DreamberdSignal type
- `src/interpreter.rs` - Add `builtin_use()` function
- `src/interpreter.rs` - Handle signal calls in `evaluate_function_call()`

**Test Cases Needed:**

```gom
const var count = use(0)!
print(count())!      // 0
count(5)!
print(count())!      // 5

// Signals with reactivity (advanced)
const var score = use(0)!
when (score() > 10) {
    print("High score!")!
}
score(15)!  // Should trigger when statement
```

**Estimated Effort:** 2-3 weeks
**Complexity:** Medium (new type + reactive integration)

---

### 15. Class Single Instance Enforcement ❌

**Specification:**

```gom
class Player {
   const var health = 10!
}

const var player1 = new Player()!
const var player2 = new Player()!  // Error: Can't have more than one instance
```

**Current Status:**

- ✅ Class declaration: Working
- ✅ Constructor parsing: Complete
- ❌ Instance tracking: Not implemented
- ❌ Single instance enforcement: Not implemented

**What's Missing:**

```rust
// Track class instances
struct ClassRegistry {
    instances: HashMap<String, bool>,  // class_name -> has_instance
}

impl Interpreter {
    fn evaluate_constructor(&mut self, constructor: &ConstructorNode) -> Result<DreamberdValue, DreamberdError> {
        let class_name = &constructor.class_name.value;
        
        // Check if instance already exists
        if self.class_registry.instances.get(class_name) == Some(&true) {
            return Err(DreamberdError::InterpretationError(
                format!("Cannot create multiple instances of class '{}'", class_name)
            ));
        }
        
        // Lookup class definition
        let class_obj = self.lookup_variable(class_name)?;
        
        // Mark instance as created
        self.class_registry.instances.insert(class_name.clone(), true);
        
        // Create instance from class
        Ok(DreamberdValue::Object(class_obj.clone()))
    }
}
```

**Files to Modify:**

- `src/interpreter.rs` - Add ClassRegistry and instance tracking
- `src/interpreter.rs` - Implement `evaluate_constructor()` with enforcement

**Test Cases Needed:**

```gom
class Player {
    const var health = 10!
}

const var p1 = new Player()!  // OK
const var p2 = new Player()!  // Error

// Workaround: PlayerMaker pattern
class PlayerMaker {
    function makePlayer() => {
        class Player { const var health = 10! }
        return new Player()!
    }
}

const const maker = new PlayerMaker()!
const var p1 = maker.makePlayer()!  // OK
const var p2 = maker.makePlayer()!  // OK (different nested classes)
```

**Estimated Effort:** 1-2 weeks
**Complexity:** Medium (registry tracking)

---

### 16. Property Access (Dot Operator) ❌

**Specification:**

```gom
const const obj = { x: 5, y: 10 }!
print(obj.x)!  // 5

class Player {
    const var health = 100!
}
const var p = new Player()!
print(p.health)!  // 100
```

**Current Status:**

- ✅ Index node type exists
- ❌ Dot operator parsing: Not implemented
- ❌ Property access evaluation: Not implemented
- ❌ Object literal syntax: Not implemented

**What's Missing:**

```rust
// In lexer - recognize dot as operator
TokenType::Dot

// In expression_tree - parse property access
fn parse_property_access(tokens: &[Token]) -> Result<IndexNode, DreamberdError> {
    // obj.prop becomes Index(obj, "prop")
    let object = parse_primary(tokens[0])?;
    let property = tokens[2].value.clone();  // After the dot
    
    Ok(IndexNode {
        value: Box::new(object),
        index: Box::new(ExpressionTreeNode::Value(
            ValueNode::new(Token::string(property))
        )),
    })
}

// In interpreter - evaluate property access
fn evaluate_property_access(&mut self, obj: &DreamberdValue, prop_name: &str) -> Result<DreamberdValue, DreamberdError> {
    match obj {
        DreamberdValue::Object(o) => {
            o.namespace.get(prop_name)
                .cloned()
                .ok_or_else(|| DreamberdError::InterpretationError(
                    format!("Property '{}' not found", prop_name)
                ))
        }
        _ => Err(DreamberdError::InterpretationError(
            "Cannot access property on non-object".to_string()
        ))
    }
}
```

**Files to Modify:**

- `src/processor/lexer.rs` - Add Dot token type
- `src/processor/expression_tree.rs` - Parse dot operator as index
- `src/interpreter.rs` - Evaluate property access

**Test Cases Needed:**

```gom
// Object property access (once objects implemented)
const const point = { x: 5, y: 10 }!
print(point.x)!  // 5

// Class property access
class Counter {
    const var count = 0!
}
const var c = new Counter()!
print(c.count)!  // 0
c.count = 5!
print(c.count)!  // 5
```

**Estimated Effort:** 2-3 weeks
**Complexity:** Medium (requires object literal syntax too)

---

### 17. Import/Export Full Implementation ❌

**Specification:**

```gom
===== math.gom3 ==
function add(a, b) => a + b!
export add to "main.gom3"!

===== main.gom3 ==
import add!
print(add(2, 3))!  // 5
```

**Current Status:**

- ✅ Multi-file format parsing: Complete
- ✅ Import/Export AST nodes: Complete
- ❌ Cross-file variable sharing: Not implemented
- ❌ Export serialization: Not implemented
- ❌ File writing for exports: Not implemented

**What's Missing:**

```rust
fn execute_export_statement(&mut self, export: ExportStatement) -> Result<(), DreamberdError> {
    let var_name = &export.name;
    let target_file = &export.target_file;
    
    // Look up the variable to export
    let value = self.lookup_variable(var_name)?;
    
    // Serialize the value
    let serialized = serialize_value(value)?;
    
    // Write to target file's export section
    let export_data = format!("const const {} = {}!\n", var_name, serialized);
    
    // Append to target file (or create if doesn't exist)
    let mut file = OpenOptions::new()
        .create(true)
        .append(true)
        .open(target_file)?;
    
    file.write_all(export_data.as_bytes())?;
    
    Ok(())
}

fn execute_import_statement(&mut self, import: ImportStatement) -> Result<(), DreamberdError> {
    let var_name = &import.name;
    
    // Search for exported variable in all files
    // (In practice, would need export registry or file scanning)
    let value = load_exported_variable(var_name)?;
    
    // Add to current namespace
    self.define_variable(var_name.clone(), value)?;
    
    Ok(())
}
```

**Files to Modify:**

- `src/interpreter.rs` - Complete `execute_export_statement()` and `execute_import_statement()`
- `src/serialize.rs` - Ensure value serialization works for exports

**Test Cases Needed:**

```gom
===== lib.gom3 ==
const const PI = 3.14!
export PI to "main.gom3"!

function square(x) => x * x!
export square to "main.gom3"!

===== main.gom3 ==
import PI!
import square!
print(PI)!           // 3.14
print(square(5))!    // 25
```

**Estimated Effort:** 2-3 weeks
**Complexity:** Medium (file I/O + serialization)

---

### 18. Object Literal Syntax ❌

**Specification:**

```gom
const const point = { x: 5, y: 10 }!
print(point.x)!  // 5
```

**Current Status:**

- ❌ Object literal parsing: Not implemented
- ❌ Curly brace syntax: Not implemented
- ✅ Object type: Exists

**What's Missing:**

```rust
// In syntax_tree.rs - parse object literals
fn parse_object_literal(tokens: &[Token]) -> Result<ExpressionTreeNode, DreamberdError> {
    // Find matching {}
    let mut properties = HashMap::new();
    
    // Parse key: value pairs
    let mut i = 1;  // Skip opening {
    while tokens[i].token_type != TokenType::RBrace {
        let key = tokens[i].value.clone();
        // Expect :
        i += 2;
        let value_expr = parse_expression(&tokens[i..])?;
        properties.insert(key, value_expr);
        // Skip comma if present
        i += 1;
    }
    
    Ok(ExpressionTreeNode::Object(ObjectNode { properties }))
}
```

**Files to Modify:**

- `src/processor/lexer.rs` - Handle `{` and `}` (currently ignored?)
- `src/processor/expression_tree.rs` - Add ObjectNode type
- `src/processor/syntax_tree.rs` - Parse object literals
- `src/interpreter.rs` - Evaluate object literals

**Test Cases Needed:**

```gom
const const empty = {}!
const const point = { x: 5, y: 10 }!
print(point.x)!  // 5

const const nested = {
    name: "Player",
    pos: { x: 0, y: 0 }
}!
print(nested.pos.x)!  // 0
```

**Estimated Effort:** 2-3 weeks
**Complexity:** Medium (new syntax + evaluation)

---

### 19. Numbers as Variable Names ❌

**Specification:**

```gom
const const 5 = 4!
print(2 + 2)!  // 4 (because 5 = 4, so 2+2 uses the redefined 5... wait, this doesn't make sense)
```

**Current Status:**

- ❌ Number tokens as names: Not allowed
- ❌ Value reassignment: Not implemented

**Note:** This feature is intentionally absurd and low priority. The spec itself is unclear on how this should work. Consider skipping or implementing last.

**Estimated Effort:** 1-2 weeks (if implemented at all)
**Complexity:** High (breaks fundamental assumptions about language)

---

## Summary Tables

### Missing Features by Priority

| Priority | Feature | Effort | Complexity |
|----------|---------|--------|------------|
| 🔴 HIGH | Variable Lifetime Enforcement | 2-3 weeks | Medium |
| 🔴 HIGH | Significant Whitespace Arithmetic | 2-3 weeks | High |
| 🔴 HIGH | Number Name Parsing | 1-2 weeks | Medium |
| 🔴 HIGH | Four-Level Equality Operators | 1-2 weeks | Medium |
| 🟡 MEDIUM | When Statement Reactive Execution | 3-5 weeks | High |
| 🟡 MEDIUM | After Statement Event Matching | 2-3 weeks | Medium |
| 🟡 MEDIUM | Async Functions (Turn-Based) | 3-4 weeks | High |
| 🟡 MEDIUM | Next Keyword (Future Values) | 3-4 weeks | High |
| 🟢 LOW | Variable Overloading by Confidence | 1 week | Low |
| 🟢 LOW | Reverse Statement | 1-2 weeks | Medium |
| 🟢 LOW | Delete Keyword Feature | 2 weeks | Medium |
| 🟢 LOW | Indentation Enforcement | 1 week | Low |
| 🟢 LOW | String Interpolation (polish) | 1 week | Low |
| 🟢 LOW | Signal System (use keyword) | 2-3 weeks | Medium |
| 🟢 LOW | Class Single Instance | 1-2 weeks | Medium |
| 🟢 LOW | Property Access (Dot Operator) | 2-3 weeks | Medium |
| 🟢 LOW | Import/Export Full Implementation | 2-3 weeks | Medium |
| 🟢 LOW | Object Literal Syntax | 2-3 weeks | Medium |
| 🟢 LOW | Numbers as Variable Names | 1-2 weeks | High |

### Total Effort Estimation

- **High Priority (4 features):** 8-10 weeks
- **Medium Priority (4 features):** 13-19 weeks  
- **Low Priority (11 features):** 17-26 weeks

**Total:** 38-55 weeks (9-13 months) to reach 100% spec compliance

---

## Recommended Development Path

### Phase 1: Core Operators (Weeks 1-8)

1. Variable Lifetime Enforcement (2-3 weeks)
2. Four-Level Equality Operators (1-2 weeks)
3. Number Name Parsing (1-2 weeks)
4. Significant Whitespace Arithmetic (2-3 weeks)

**Result:** All core variable/operator features complete

### Phase 2: Reactive Programming (Weeks 9-16)

1. When Statement Reactive Execution (3-5 weeks)
2. After Statement Event Matching (2-3 weeks)

**Result:** Reactive programming fully functional

### Phase 3: Async System (Weeks 17-25)

1. Async Functions with Turn-Based Execution (3-4 weeks)
2. Next Keyword with Future Values (3-4 weeks)

**Result:** Complete async/await system

### Phase 4: Quality of Life (Weeks 26-40)

1. String Interpolation polish (1 week)
2. Indentation Enforcement (1 week)
3. Variable Overloading (1 week)
4. Delete Keyword Feature (2 weeks)
5. Class Single Instance (1-2 weeks)
6. Reverse Statement (1-2 weeks)
7. Signal System (2-3 weeks)
8. Property Access (2-3 weeks)
9. Object Literal Syntax (2-3 weeks)
10. Import/Export Full (2-3 weeks)

**Result:** 95% spec compliance

### Phase 5: Esoteric Features (Weeks 41-55)

1. Numbers as Variable Names (1-2 weeks, optional)

**Result:** 100% spec compliance

---

## Next Immediate Steps

Based on current progress (55% complete with strong foundation), the recommended next features are:

1. **Variable Lifetime Enforcement** - Critical for spec compliance
2. **Four-Level Equality** - Relatively easy, high spec value
3. **When Statement Reactivity** - Unlocks reactive programming
4. **String Interpolation Polish** - Nearly done, just needs testing

These four features would bring completion to **~65%** and unlock significant new capabilities.

---

*Generated: November 13, 2025*  
*Current Interpreter Version: 0.2.0*  
*Tests Passing: 26/26 (100%)*  
*Completion Status: 55% → Target: 100%*
