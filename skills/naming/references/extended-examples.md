# Naming — Extended Examples

Detailed naming walkthroughs showing intent-revealing names in practice.

---

## Example: Renaming a Game Board

### Before

```
theList = []
for x in gameBoard:
    if x[0] == 4:
        theList.add(x)
return theList
```

What does this code do? Impossible to tell without context.

### After — Reveal Intent

```
flaggedCells = []
for cell in gameBoard:
    if cell.isFlagged():
        flaggedCells.add(cell)
return flaggedCells
```

Same logic, completely different readability. The names tell us: we're working with a game board, looking for flagged cells, collecting them into a list. No comments needed.

### The Transformation Steps

1. `theList` → `flaggedCells` — name reveals what the list contains, not that it IS a list
2. `x` → `cell` — name reveals domain concept
3. `x[0] == 4` → `cell.isFlagged()` — magic number becomes intent-revealing method
4. `gameBoard` stays — it's already a good domain name

---

## Example: Naming a Configuration System

### Bad Names (Real Code Patterns)

```
Manager:
    d: map          // what data?
    temp: string    // temporary what?
    flag: boolean   // what flag?
    
    doStuff(p1, p2):           // what stuff? what parameters?
        info = getInfo(p1)     // info about what?
        data = processData(p2) // what processing?
        if flag:
            handleIt(info, data) // handle what?
```

### Good Names

```
FeatureToggleConfiguration:
    toggles: map<string, boolean>
    defaultEnvironment: string
    isInitialized: boolean
    
    evaluateToggle(featureName, userContext):
        featureConfig = loadFeatureConfig(featureName)
        environmentRules = resolveEnvironmentRules(userContext)
        if isInitialized:
            applyToggleRules(featureConfig, environmentRules)
```

### Why Each Name Matters

- `Manager` → `FeatureToggleConfiguration` — "Manager" says nothing about what's managed. The new name tells you exactly what this class configures
- `d` → `toggles` — reveals it's a map of toggle states
- `temp` → `defaultEnvironment` — reveals the domain concept
- `flag` → `isInitialized` — boolean reads as a question
- `doStuff` → `evaluateToggle` — verb reveals the action
- `p1, p2` → `featureName, userContext` — parameters describe their purpose
- `getInfo` → `loadFeatureConfig` — reveals what info and where it comes from
- `processData` → `resolveEnvironmentRules` — reveals what processing occurs

---

## Example: Naming Parts of Speech

### Class Names — Nouns and Noun Phrases

```
// Bad: verbs or vague nouns
ProcessData        // verb — what does it process?
Helper             // noise — helper for what?
Utility            // noise — utility for what?
DataManager        // vague — manages what data how?

// Good: specific nouns
InvoiceCalculator       // what it is
CustomerRepository      // what it is and what it accesses
PaymentGateway          // what it is and what it connects to
ShippingRateEstimator   // what it is and what it computes
```

### Method Names — Verbs and Verb Phrases

```
// Bad: vague verbs or nouns
data()              // noun — does it get data? set data?
process()           // what kind of processing?
handle()            // handle what?
execute()           // too generic

// Good: specific verbs revealing intent
calculateMonthlyTotal()      // clear action and result
sendOrderConfirmation()      // clear action and target
validateEmailFormat()        // clear action and subject
retryFailedPayment()         // clear action and context
```

### Boolean Names — Questions That Read Naturally

```
// Bad: ambiguous meaning
status              // what status? true means what?
check               // check what?
flag                // flag for what?

// Good: reads as a yes/no question
isActive            // "if user isActive..."
hasPermission       // "if user hasPermission..."
canRetry            // "if transaction canRetry..."
shouldNotify        // "if order shouldNotify..."
wasProcessed        // "if payment wasProcessed..."
```

---

## Example: Avoiding Disinformation

### Misleading Type Names

```
accountList = getAccounts()   // Is it actually a List? What if it's a Set or Map?
// Better:
accounts = getAccounts()      // Don't encode the type in the name
```

### Similar Names That Confuse

```
// These exist in the same codebase:
getActiveAccount()
getActiveAccounts()
getActiveAccountInfo()
getActiveAccountData()

// A developer can't tell which to call without reading each implementation
// Better: each name should make its purpose clear
getActiveAccount()              // returns single Account entity
listActiveAccounts()            // returns collection of Account entities
getActiveAccountSummary()       // returns lightweight summary view
getActiveAccountWithTransactions()  // returns Account with loaded transactions
```

### Abbreviations That Mislead

```
// In different parts of the codebase:
genRpt()    // generate report? general repeat? generic receipt?
lstUsr()    // list users? last user? lost user?
chkPmt()    // check payment? chunk permit?

// Just spell it out:
generateReport()
listUsers()
checkPaymentStatus()
```
