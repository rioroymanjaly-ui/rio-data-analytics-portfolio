"""Reproducible synthetic supplier-fulfilment analytics. No live RUIYA records."""
import csv, random, sqlite3, json
from datetime import date,timedelta
from pathlib import Path

SUPPLIERS=["IN-ALPHA","IN-BETA","DE-OMEGA","PL-DELTA","CZ-GAMMA","IN-KAPPA"]
COUNTRY={"IN-ALPHA":"India","IN-BETA":"India","DE-OMEGA":"Germany","PL-DELTA":"Poland","CZ-GAMMA":"Czechia","IN-KAPPA":"India"}
PRODUCTS=["Automotive brackets","Machined fittings","Stamped panels","Fasteners"]
FIELDS=["order_id","order_date","supplier_id","origin","product","units","promised_days","actual_days","quality_issue","quoted_cost_eur","actual_cost_eur"]

def generate(n=1800,seed=260617):
    rng=random.Random(seed);base=date(2026,3,1);rows=[]
    for i in range(n):
        supplier=SUPPLIERS[i%len(SUPPLIERS)]
        origin=COUNTRY[supplier]
        order_day=base+timedelta(days=min(5,i//300)*30+rng.randrange(28))
        late=rng.random()<(0.31 if supplier in ("IN-BETA","IN-KAPPA") else 0.14 if supplier=="IN-ALPHA" else 0.08)
        delay=rng.randint(2,14) if late else 0
        lead=7+(9 if origin=="India" else 3)+rng.randint(0,7)+delay
        quality=rng.random()<(0.095 if supplier=="IN-BETA" else 0.025)
        qty=rng.randint(10,70)
        quoted=round(qty*rng.uniform(19,53),2)
        variance=rng.uniform(0.04,0.15) if late else rng.uniform(-0.025,0.025)
        rows.append(dict(order_id=f"ORD-{i+1:05}",order_date=order_day.isoformat(),supplier_id=supplier,
           origin=origin,product=rng.choice(PRODUCTS),units=qty,
           promised_days=20 if origin=="India" else 13,actual_days=lead,
           quality_issue=int(quality),quoted_cost_eur=round(quoted,2),
           actual_cost_eur=round(quoted*(1+variance),2)))
    return rows

def validate(rows):
    ids=set()
    for row in rows:
        oid=row["order_id"]
        if not oid or oid in ids:raise ValueError("duplicate or empty order ID")
        ids.add(oid)
        if int(row["units"])<=0 or int(row["actual_days"])<0 or int(row["promised_days"])<=0:
            raise ValueError("invalid quantity or delivery period")
        if float(row["actual_cost_eur"])<0 or float(row["quoted_cost_eur"])<=0:
            raise ValueError("invalid cost")
        if int(row["quality_issue"]) not in (0,1):raise ValueError("invalid quality flag")
    return True

def summarize(rows):
    validate(rows)
    count=len(rows)
    if not count:raise ValueError("dataset must not be empty")
    lateness=lambda r:int(r["actual_days"]>r["promised_days"])
    late=sum(lateness(row) for row in rows)
    total_quoted=sum(row["quoted_cost_eur"] for row in rows)
    total_actual=sum(row["actual_cost_eur"] for row in rows)
    suppliers={}
    for row in rows:
        sid=row["supplier_id"]
        group=suppliers.setdefault(sid,[])
        group.append(row)
    return {
      "dataset":"fixed-seed synthetic order scenarios",
      "orders":count,"late_orders":late,
      "on_time_pct":round(100*(1-late/count),2),
      "quality_issue_pct":round(100*sum(r["quality_issue"] for r in rows)/count,2),
      "mean_lead_days":round(sum(r["actual_days"] for r in rows)/count,1),
      "quoted_eur":round(total_quoted,2),"actual_eur":round(total_actual,2),
      "cost_variance_pct":round(100*(total_actual/total_quoted-1),2),
      "suppliers":{sid:{
        "orders":len(group),
        "on_time_pct":round(100*(1-sum(lateness(r) for r in group)/len(group)),2),
        "quality_issue_pct":round(100*sum(r["quality_issue"] for r in group)/len(group),2)
      } for sid,group in suppliers.items()}
    }

def sql_scorecard(rows):
    validate(rows)
    db=sqlite3.connect(":memory:")
    db.execute("CREATE TABLE orders (supplier_id TEXT, promised_days INT, actual_days INT, quality_issue INT, quoted_cost_eur REAL, actual_cost_eur REAL)")
    db.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?)",[(r["supplier_id"],r["promised_days"],r["actual_days"],r["quality_issue"],r["quoted_cost_eur"],r["actual_cost_eur"]) for r in rows])
    result=db.execute("""SELECT supplier_id,COUNT(*),
       ROUND(100.0*AVG(CASE WHEN actual_days<=promised_days THEN 1.0 ELSE 0 END),2),
       ROUND(100.0*AVG(quality_issue),2) FROM orders GROUP BY supplier_id""").fetchall()
    db.close()
    return result

if __name__=="__main__":
    rows=generate();result=summarize(rows)
    folder=Path("output");folder.mkdir(exist_ok=True)
    with (folder/"synthetic_orders.csv").open("w",newline="") as fh:
        writer=csv.DictWriter(fh,fieldnames=FIELDS);writer.writeheader();writer.writerows(rows)
    (folder/"metrics.json").write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
    print("SQL supplier groups:",len(sql_scorecard(rows)))
