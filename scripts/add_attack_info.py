import csv, json, sys
attack_path, csv_path = sys.argv[1], sys.argv[2]
def tname(p):
    return " ".join(w if w == "and" else w.capitalize() for w in p.split("-"))
info = {}
for o in json.load(open(attack_path, encoding="utf-8"))["objects"]:
    if o.get("type") != "attack-pattern":
        continue
    tid = next((r["external_id"] for r in o.get("external_references", []) if r.get("source_name") == "mitre-attack"), None)
    if not tid:
        continue
    status = "revoked" if o.get("revoked") else "deprecated" if o.get("x_mitre_deprecated") else "ok"
    tac = ";".join(tname(k["phase_name"]) for k in o.get("kill_chain_phases", []) if k.get("kill_chain_name") == "mitre-attack")
    if tid not in info or status == "ok":
        info[tid] = (o.get("name", ""), tac, status)
rows = list(csv.DictReader(open(csv_path, encoding="utf-8-sig")))
cols = ["technique_id", "attack_name", "attack_tactics", "status", "label_tactics", "datasets", "scenarios", "rows"]
with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    for r in rows:
        name, tac, st = info.get(r["technique_id"], ("", "", "not found"))
        w.writerow({"technique_id": r["technique_id"], "attack_name": name, "attack_tactics": tac, "status": st,
                    "label_tactics": r.get("label_tactics") or r.get("tactics", ""), "datasets": r["datasets"],
                    "scenarios": r["scenarios"], "rows": r["rows"]})
bad = [r["technique_id"] for r in rows if info.get(r["technique_id"], ("", "", "not found"))[2] != "ok"]
print("기법", len(rows), "개 처리. 확인 필요:", ", ".join(bad) if bad else "없음")
