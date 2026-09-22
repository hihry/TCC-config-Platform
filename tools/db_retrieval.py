import duckdb
import glob
import json
import pandas as pd

def query_rules(sql_query):
    """
    Executes a DuckDB SQL query against the JSON configuration rules.
    The rules are accessible via a table named 'rules'.
    Available columns: program, rule_index, perspective, direction, leg, carrier_status, message_key, alert_key, stepper
    """
    conn = duckdb.connect(database=':memory:')
    
    # Load all rules into a flat dataframe for querying
    all_rules = []
    for file in glob.glob("repo/programs/*.json"):
        with open(file, "r") as f:
            data = json.load(f)
            for i, rule in enumerate(data["rules"]):
                flat_rule = {
                    "program": data["program"],
                    "rule_index": i,
                    "perspective": rule.get("perspective"),
                    "direction": rule.get("direction"),
                    "leg": rule.get("leg"),
                    "carrier_status": rule.get("carrier_status"),
                    "message_key": rule.get("message_key"),
                    "alert_key": rule.get("alert_key"),
                    "stepper": json.dumps(rule.get("stepper", []))
                }
                all_rules.append(flat_rule)
    
    df = pd.DataFrame(all_rules)
    try:
        conn.register('rules', df)
        result = conn.execute(sql_query).fetchdf()
        return result.to_dict('records')
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()
