# Functions — Extended Examples

Detailed walkthroughs showing function design principles in practice.

---

## Example: Decomposing a Long Function

### Before — 60-Line Monolith

```
generatePayroll(employees, month, year):
    report = []
    for emp in employees:
        if emp.status != "active": continue
        if emp.startDate > date(year, month, 1): continue
        
        basePay = emp.annualSalary / 12
        
        // overtime
        overtime = 0
        if emp.hoursWorked > 160:
            overtimeHours = emp.hoursWorked - 160
            overtimeRate = (emp.annualSalary / 2080) * 1.5
            overtime = overtimeHours * overtimeRate
        
        // deductions
        healthInsurance = 0
        if emp.plan == "single": healthInsurance = 200
        else if emp.plan == "family": healthInsurance = 500
        else if emp.plan == "premium": healthInsurance = 800
        
        retirement = 0
        if emp.retirementPct > 0:
            retirement = (basePay + overtime) * (emp.retirementPct / 100)
        
        // taxes
        gross = basePay + overtime
        taxable = gross - retirement
        federalTax = 0
        if taxable < 3000: federalTax = taxable * 0.10
        else if taxable < 7000: federalTax = 300 + (taxable - 3000) * 0.22
        else: federalTax = 1180 + (taxable - 7000) * 0.32
        stateTax = taxable * emp.stateTaxRate
        
        net = gross - healthInsurance - retirement - federalTax - stateTax
        
        record = {employee: emp.name, gross: gross, deductions: healthInsurance + retirement, taxes: federalTax + stateTax, net: net}
        report.add(record)
    
    return report
```

### Step 1 — Extract at the Highest Level

```
generatePayroll(employees, month, year):
    activeEmployees = filterEligibleEmployees(employees, month, year)
    return activeEmployees.map(emp -> calculatePaystub(emp))
```

The top-level function now reads like a recipe: filter eligible employees, calculate each paystub.

### Step 2 — Each Sub-Function Does One Thing

```
filterEligibleEmployees(employees, month, year):
    return employees.filter(emp ->
        emp.status == "active" and
        emp.startDate <= date(year, month, 1))

calculatePaystub(employee):
    gross = calculateGrossPay(employee)
    deductions = calculateDeductions(employee, gross)
    taxes = calculateTaxes(gross, deductions.retirement, employee.stateTaxRate)
    net = gross - deductions.total - taxes.total
    return Paystub(employee.name, gross, deductions, taxes, net)

calculateGrossPay(employee):
    basePay = employee.annualSalary / 12
    overtime = calculateOvertime(employee)
    return basePay + overtime

calculateOvertime(employee):
    if employee.hoursWorked <= 160: return 0
    overtimeHours = employee.hoursWorked - 160
    hourlyRate = employee.annualSalary / 2080
    return overtimeHours * hourlyRate * 1.5

calculateDeductions(employee, gross):
    health = healthInsuranceCost(employee.plan)
    retirement = gross * (employee.retirementPct / 100)
    return Deductions(health, retirement, total: health + retirement)

healthInsuranceCost(plan):
    costs = {"single": 200, "family": 500, "premium": 800}
    return costs[plan] or 0

calculateTaxes(gross, retirementDeduction, stateTaxRate):
    taxable = gross - retirementDeduction
    federal = calculateFederalTax(taxable)
    state = taxable * stateTaxRate
    return Taxes(federal, state, total: federal + state)

calculateFederalTax(taxableIncome):
    if taxableIncome < 3000: return taxableIncome * 0.10
    if taxableIncome < 7000: return 300 + (taxableIncome - 3000) * 0.22
    return 1180 + (taxableIncome - 7000) * 0.32
```

### What Changed

- **60 lines → 8 functions, each under 10 lines**
- **Step-down rule:** generatePayroll → calculatePaystub → calculateGrossPay → calculateOvertime
- **One thing per function:** each function has exactly one responsibility
- **No flag arguments:** healthInsuranceCost takes a plan, not a flag
- **Descriptive names:** calculateFederalTax tells you exactly what it does
- **Zero comments needed:** the function names ARE the documentation

---

## Example: Eliminating Flag Arguments

### Before

```
createFile(name, isTemp):
    if isTemp:
        path = tempDir + name
        file = File(path)
        file.setAutoDelete(true)
    else:
        path = dataDir + name
        file = File(path)
        file.setAutoDelete(false)
    return file
```

### After — Two Functions

```
createPermanentFile(name):
    return File(dataDir + name, autoDelete: false)

createTemporaryFile(name):
    return File(tempDir + name, autoDelete: true)
```

The flag argument was hiding two completely different functions inside one. The callers become clearer too: `createTemporaryFile("cache.dat")` is more readable than `createFile("cache.dat", true)`.

---

## Example: Command-Query Separation

### Violation

```
// This function both changes state AND returns a value
setUsername(user, newName):
    oldName = user.name
    user.name = newName
    database.update(user)
    return oldName
```

Callers can't tell if this is a query or a command:
```
result = setUsername(user, "Alice")  // Did something change? What's the result?
```

### Fixed — Separate Command and Query

```
// Query: returns information, no side effects
getCurrentUsername(user):
    return user.name

// Command: changes state, returns nothing
changeUsername(user, newName):
    user.name = newName
    database.update(user)
```

Now the intent is clear at every call site:
```
oldName = getCurrentUsername(user)  // clearly a query
changeUsername(user, "Alice")      // clearly a command
```
