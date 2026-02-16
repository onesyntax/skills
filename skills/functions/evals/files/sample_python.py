import requests
import json
import os
from datetime import datetime

def process_orders(orders, db, config, notify=True, dry_run=False):
    results = []
    failed = []
    for order in orders:
        if order is None:
            continue
        if order.get("status") != "pending":
            continue
        if order.get("total", 0) <= 0:
            failed.append({"order": order, "reason": "invalid total"})
            continue

        # validate customer
        customer = db.query("SELECT * FROM customers WHERE id = %s", order["customer_id"])
        if not customer:
            failed.append({"order": order, "reason": "customer not found"})
            continue
        if customer["status"] == "banned":
            failed.append({"order": order, "reason": "customer banned"})
            continue

        # check inventory
        for item in order.get("items", []):
            stock = db.query("SELECT quantity FROM inventory WHERE sku = %s", item["sku"])
            if not stock or stock["quantity"] < item["quantity"]:
                failed.append({"order": order, "reason": f"insufficient stock for {item['sku']}"})
                break
        else:
            # calculate totals
            subtotal = sum(i["price"] * i["quantity"] for i in order["items"])
            tax = subtotal * config["tax_rate"]
            shipping = 0 if subtotal > config["free_shipping_threshold"] else config["shipping_rate"]
            total = subtotal + tax + shipping

            if abs(total - order["total"]) > 0.01:
                failed.append({"order": order, "reason": "total mismatch"})
                continue

            if not dry_run:
                # update inventory
                for item in order["items"]:
                    db.execute("UPDATE inventory SET quantity = quantity - %s WHERE sku = %s",
                              item["quantity"], item["sku"])

                # save order
                order["status"] = "processed"
                order["processed_at"] = datetime.now().isoformat()
                db.execute("INSERT INTO processed_orders VALUES (%s)", json.dumps(order))

                # notify
                if notify:
                    try:
                        requests.post(config["webhook_url"], json={
                            "event": "order_processed",
                            "order_id": order["id"],
                            "total": total
                        })
                    except:
                        pass

                # log
                with open(os.path.join(config["log_dir"], "orders.log"), "a") as f:
                    f.write(f"{datetime.now()} - Processed order {order['id']} for ${total}\n")

            results.append({"order_id": order["id"], "total": total, "status": "processed"})

    return {"processed": results, "failed": failed, "summary": {"total": len(results), "failed": len(failed)}}
