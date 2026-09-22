import csv
import os

def create_legacy_csv():
    headers = [
        "program", "perspective", "direction", "leg", "carrier_status", 
        "message_key", "alert_key"
    ] + [f"STEP_{i}" for i in range(11)]
    
    rows = [
        ["AG", "BUYER", "INBOUND", "LEG1", "DELIVERED", "MSG-101", "ALT-001", "STEP-01", "STEP-02", "STEP-03", "", "", "", "", "", "", "", ""],
        ["GSP", "SELLER", "OUTBOUND", "LEG2", "IN_TRANSIT", "MSG-102", "", "STEP-01", "STEP-02", "", "", "", "", "", "", "", "", ""],
        ["STANDARD", "BUYER", "INBOUND", "LEG1", "EXCEPTION", "MSG-103", "ALT-002", "STEP-01", "STEP-02", "STEP-EX", "", "", "", "", "", "", "", ""],
    ]
    
    with open("repo/MAIN.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def create_dictionaries():
    messages = [
        ["KEY", "TEXT"],
        ["MSG-101", "Your item has been delivered to the authentication center."],
        ["MSG-102", "Your item is on the way to the global shipping hub."],
        ["MSG-103", "There is a delay in shipping your item."],
        ["MSG-999", "A test message."]
    ]
    with open("repo/KEY_MESSAGE.csv", "w", newline="") as f:
        csv.writer(f).writerows(messages)
        
    steps = [
        ["KEY", "TEXT"],
        ["STEP-01", "Order Placed"],
        ["STEP-02", "Shipped"],
        ["STEP-03", "Delivered"],
        ["STEP-EX", "Delayed"]
    ]
    with open("repo/KEY_STEP.csv", "w", newline="") as f:
        csv.writer(f).writerows(steps)
        
    alerts = [
        ["KEY", "TEXT"],
        ["ALT-001", "Action required: review authentication results."],
        ["ALT-002", "Shipping delayed due to weather."]
    ]
    with open("repo/KEY_ALERT.csv", "w", newline="") as f:
        csv.writer(f).writerows(alerts)

if __name__ == "__main__":
    create_legacy_csv()
    create_dictionaries()
    print("Mock data generated in repo/")
