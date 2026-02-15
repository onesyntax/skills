# Refactoring Suggestions — Extended Examples

Full before/after refactoring walkthroughs showing the thought process from smell identification through the fix.

---

## Example: Refactoring a Report Generator (Multiple Smells)

### The Code

```
ReportGenerator:
    db: DatabaseConnection
    emailService: EmailService
    pdfLib: PdfLibrary

    generateReport(reportType, startDate, endDate, format, recipientEmail,
                   includeCharts, chartType, pageSize, orientation, watermark):
        // Get data
        if reportType == "sales":
            data = db.query("SELECT * FROM sales WHERE date BETWEEN ? AND ?", startDate, endDate)
        else if reportType == "inventory":
            data = db.query("SELECT * FROM inventory WHERE updated BETWEEN ? AND ?", startDate, endDate)
        else if reportType == "customers":
            data = db.query("SELECT * FROM customers WHERE created BETWEEN ? AND ?", startDate, endDate)
        else:
            throw Error("Unknown report type: " + reportType)

        // Process data
        rows = []
        totalAmount = 0
        for record in data:
            if reportType == "sales":
                row = {
                    date: formatDate(record.date),
                    customer: record.customerName,
                    amount: formatCurrency(record.amount),
                    status: record.status
                }
                totalAmount += record.amount
            else if reportType == "inventory":
                row = {
                    product: record.productName,
                    quantity: record.quantity,
                    warehouse: record.warehouseLocation,
                    lastUpdated: formatDate(record.updatedAt)
                }
            else if reportType == "customers":
                row = {
                    name: record.name,
                    email: record.email,
                    joined: formatDate(record.createdAt),
                    totalOrders: record.orderCount
                }
            rows.add(row)

        // Format output
        if format == "pdf":
            doc = pdfLib.createDocument(pageSize, orientation)
            if watermark != nil: doc.setWatermark(watermark)
            doc.addTitle(reportType + " Report")
            doc.addTable(rows)
            if includeCharts:
                if chartType == "bar": doc.addBarChart(data)
                else if chartType == "pie": doc.addPieChart(data)
                else if chartType == "line": doc.addLineChart(data)
            output = doc.render()
        else if format == "csv":
            output = ""
            for row in rows:
                output += row.values().join(",") + "\n"
        else if format == "html":
            output = "<html><body><h1>" + reportType + " Report</h1><table>"
            for row in rows:
                output += "<tr>"
                for value in row.values():
                    output += "<td>" + value + "</td>"
                output += "</tr>"
            output += "</table></body></html>"

        // Send
        if recipientEmail != nil:
            emailService.send(recipientEmail, reportType + " Report", output)

        return output
```

### Smell Identification

1. **Long Function** (Bloater) — 60+ lines doing four different things
2. **Long Parameter List** (Bloater) — 10 parameters
3. **Switch/If Chains** (OO Abuser) — three repeated switch-on-reportType blocks
4. **Divergent Change** (Change Preventer) — this class changes when: report types change, output formats change, email delivery changes, chart types change
5. **Feature Envy** — PDF formatting section knows too much about PdfLibrary internals
6. **Primitive Obsession** — reportType as string, format as string, dates as raw values

### Step-by-Step Refactoring

**Step 1: Extract Methods (fix Long Function)**

```
generateReport(reportType, startDate, endDate, format, recipientEmail,
               includeCharts, chartType, pageSize, orientation, watermark):
    data = fetchData(reportType, startDate, endDate)
    rows = processData(reportType, data)
    output = formatOutput(format, reportType, rows, data, includeCharts,
                          chartType, pageSize, orientation, watermark)
    deliverReport(recipientEmail, reportType, output)
    return output
```

Better, but the parameters are still a mess and the switches are still there.

**Step 2: Introduce Parameter Object (fix Long Parameter List)**

```
ReportRequest = {
    type: ReportType,      // enum, not string
    dateRange: DateRange,
    format: OutputFormat,
    recipient: Email?,
    chartOptions: ChartOptions?,
    pageOptions: PageOptions?
}

DateRange = {start, end}
ChartOptions = {enabled, type}
PageOptions = {size, orientation, watermark}

generateReport(request):
    data = fetchData(request.type, request.dateRange)
    rows = processData(request.type, data)
    output = formatOutput(request, rows, data)
    deliverReport(request.recipient, request.type, output)
    return output
```

**Step 3: Replace Conditional with Polymorphism (fix Switch/If Chains)**

```
interface ReportDataSource:
    fetch(dateRange): List<Record>
    processRow(record): Row

SalesDataSource implements ReportDataSource:
    fetch(dateRange): return db.query("SELECT * FROM sales WHERE ...", dateRange)
    processRow(record): return {date: formatDate(record.date), customer: record.customerName, ...}

InventoryDataSource implements ReportDataSource:
    fetch(dateRange): return db.query("SELECT * FROM inventory WHERE ...", dateRange)
    processRow(record): return {product: record.productName, quantity: record.quantity, ...}

CustomerDataSource implements ReportDataSource:
    fetch(dateRange): return db.query("SELECT * FROM customers WHERE ...", dateRange)
    processRow(record): return {name: record.name, email: record.email, ...}
```

**Step 4: Extract Class for Output Formatting (fix Divergent Change)**

```
interface ReportFormatter:
    format(title, rows, chartOptions): Output

PdfFormatter implements ReportFormatter:
    format(title, rows, chartOptions):
        doc = pdfLib.createDocument(pageOptions.size, pageOptions.orientation)
        if pageOptions.watermark: doc.setWatermark(pageOptions.watermark)
        doc.addTitle(title)
        doc.addTable(rows)
        if chartOptions.enabled: doc.addChart(chartOptions.type, data)
        return doc.render()

CsvFormatter implements ReportFormatter:
    format(title, rows, chartOptions):
        return rows.map(row -> row.values().join(",")).join("\n")

HtmlFormatter implements ReportFormatter:
    format(title, rows, chartOptions):
        return renderHtmlTable(title, rows)
```

**Step 5: Final Result**

```
ReportGenerator:
    dataSources: Map<ReportType, ReportDataSource>
    formatters: Map<OutputFormat, ReportFormatter>
    deliveryService: ReportDeliveryService

    generateReport(request):
        source = dataSources.get(request.type)
        data = source.fetch(request.dateRange)
        rows = data.map(record -> source.processRow(record))

        formatter = formatters.get(request.format)
        output = formatter.format(request.type.label + " Report", rows, request.chartOptions)

        if request.recipient:
            deliveryService.deliver(request.recipient, request.type, output)

        return output
```

**What changed:**
- 60+ line function → 6 lines
- 10 parameters → 1 parameter object
- 3 switch statements → polymorphism (zero switches)
- 1 god class → 5 focused classes
- Adding a new report type: create one new DataSource class (OCP)
- Adding a new format: create one new Formatter class (OCP)
- Each class has one reason to change (SRP)

---

## Example: Untangling Feature Envy

### The Code

```
InvoiceCalculator:
    calculateInvoice(customer, items, discountCode):
        subtotal = 0
        for item in items:
            price = item.product.basePrice
            if item.product.category == "electronics":
                price = price * 1.15  // electronics markup
            if item.product.isOnSale:
                price = price * (1 - item.product.saleDiscount)
            subtotal += price * item.quantity

        // Customer-specific discount
        if customer.membershipLevel == "gold":
            subtotal = subtotal * 0.9
        else if customer.membershipLevel == "platinum":
            subtotal = subtotal * 0.85

        // Discount code
        if discountCode != nil:
            discount = discountService.lookup(discountCode)
            if discount.type == "percentage":
                subtotal = subtotal * (1 - discount.value)
            else if discount.type == "fixed":
                subtotal = subtotal - discount.value

        tax = subtotal * customer.taxRate
        return subtotal + tax
```

### Smell: Feature Envy everywhere

`InvoiceCalculator` reaches into `product`, `customer`, and `discount` objects constantly. It knows their internal structure: `product.category`, `product.isOnSale`, `customer.membershipLevel`, `discount.type`.

### Refactored: Let Each Object Handle Its Own Concern

```
Product:
    effectivePrice():
        price = basePrice
        if category == "electronics": price = price * 1.15
        if isOnSale: price = price * (1 - saleDiscount)
        return price

Customer:
    applyMemberDiscount(amount):
        return amount * memberDiscountRate()

    memberDiscountRate():
        switch membershipLevel:
            "gold": return 0.9
            "platinum": return 0.85
            default: return 1.0

    calculateTax(amount):
        return amount * taxRate

Discount:
    apply(amount):
        switch type:
            "percentage": return amount * (1 - value)
            "fixed": return amount - value

// InvoiceCalculator is now simple coordination
InvoiceCalculator:
    calculateInvoice(customer, items, discountCode):
        subtotal = items.sum(item -> item.product.effectivePrice() * item.quantity)
        subtotal = customer.applyMemberDiscount(subtotal)
        if discountCode: subtotal = discountService.lookup(discountCode).apply(subtotal)
        tax = customer.calculateTax(subtotal)
        return subtotal + tax
```

Each object now manages its own business rules. InvoiceCalculator coordinates but doesn't reach into internals.

---

## Example: Removing Shotgun Surgery

### The Problem

Adding a new user field requires changes in 7 places:

```
Places that know about user fields:
1. User class (add field)
2. UserRepository (update SQL query)
3. UserValidator (add validation)
4. UserSerializer (add to JSON output)
5. UserDeserializer (parse from JSON input)
6. UserForm (add form field)
7. UserMigration (update database schema)
```

### The Fix: Consolidate Knowledge

```
// Define the field in ONE place with all its properties
UserField:
    name: "phoneNumber"
    type: String
    validation: matches("[0-9]{10}")
    dbColumn: "phone_number"
    required: false
    serializable: true

// Everything else derives from the field definition
User: fields auto-generated from UserField definitions
UserRepository: queries built from field.dbColumn
UserValidator: rules derived from field.validation
UserSerializer: output built from serializable fields
UserDeserializer: parsing built from field.type
```

Adding a new field: define ONE UserField. Everything else follows automatically.

This doesn't eliminate all 7 files, but it reduces the "add a field" change from 7 manual edits to 1 definition.

---

## Example: Strangling a God Class

### The Problem

A 2000-line `ApplicationService` that handles everything:

```
ApplicationService:
    // Authentication (300 lines)
    login(), logout(), resetPassword(), verifyEmail(), ...

    // User management (400 lines)
    createUser(), updateUser(), deleteUser(), listUsers(), ...

    // Order processing (500 lines)
    createOrder(), cancelOrder(), refundOrder(), ...

    // Reporting (400 lines)
    generateSalesReport(), generateInventoryReport(), ...

    // Notifications (200 lines)
    sendEmail(), sendSms(), sendPushNotification(), ...

    // Admin (200 lines)
    configureSystem(), managePermissions(), auditLog(), ...
```

### The Fix: Strangler Fig Pattern

Don't rewrite. Strangle gradually.

**Phase 1:** Extract AuthenticationService (lowest risk, clearest boundary)
```
AuthenticationService:
    login(), logout(), resetPassword(), verifyEmail()

ApplicationService:
    // Authentication — delegates to new service
    login(): return authService.login()
    logout(): return authService.logout()
    // ... everything else still here
```

**Phase 2:** Extract NotificationService (few dependencies)
```
NotificationService:
    sendEmail(), sendSms(), sendPushNotification()
```

**Phase 3:** Extract OrderService (higher risk, more dependencies)
**Phase 4:** Extract ReportService
**Phase 5:** Extract UserService
**Phase 6:** Extract AdminService

After all phases, `ApplicationService` is either empty (delete it) or a thin facade that delegates everything. At each phase, tests continue to pass because behavior is preserved — only structure changes.
