#!/usr/bin/env python3
"""
2024 m. Seimo rinkimų 5 regionų kontrafakto skaičiavimas.

Įvestys tame pačiame kataloge:
  2024-minor-district.csv
  2024-votes.csv
  2024-parties.csv

Pasirinktinai:
  oficialus VRK "Apylinkės" CSV. Jei pateikiamas --vrk-apylinkes,
  pilnas apylinkė -> savivaldybė laukas jungiamas pagal
  (apygardos nr., apylinkės nr., normalizuotas apylinkės pavadinimas).

Regionų vietos: Hare kvota + didžiausios liekanos pagal registruotus rinkėjus.
Partijų vietos: D'Hondt kiekviename regione.
Pagrindinis variantas: be nacionalinio 5 % barjero.
Jautrumas: nacionalinis 5 % filtras.
Diaspora į 5 regionus nepriskiriama.
"""
import argparse, csv, math, re, unicodedata
from collections import defaultdict
from pathlib import Path

REGION_NAME = {
    "VIL":"Vilniaus miesto",
    "EAST":"Rytų Lietuvos",
    "CP":"Centrinės–Pietų Lietuvos",
    "WEST":"Vakarų Lietuvos",
    "NORTH":"Šiaurės Lietuvos",
    "DIASP":"Pasaulio lietuvių",
}

def norm(s):
    s = unicodedata.normalize("NFD", s or "")
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    return re.sub(r"[^0-9a-zA-Z]+", " ", s).lower().strip()

BASE = {}
for i in range(1,11): BASE[i]="VIL"
for i in range(12,15): BASE[i]="VIL"
for i in range(15,22): BASE[i]="CP"
for i in range(22,26): BASE[i]="WEST"
for i in range(26,30): BASE[i]="NORTH"
BASE.update({
  30:"CP",31:"WEST",32:"WEST",33:"NORTH",34:"WEST",35:"WEST",36:"WEST",37:"WEST",38:"WEST",
  40:"WEST",42:"CP",43:"CP",44:"NORTH",45:"NORTH",46:"NORTH",47:"NORTH",48:"NORTH",
  51:"EAST",52:"EAST",53:"EAST",54:"CP",55:"EAST",56:"EAST",57:"EAST",58:"EAST",
  60:"CP",61:"EAST",62:"WEST",63:"CP",64:"CP",65:"CP",66:"CP",67:"CP",68:"CP",69:"CP",70:"CP",71:"DIASP"
})

CROSS = {
  11:("EAST", ["Baltosios Vokės","Pagirių 1-oji","Keturiasdešimties Totorių","Valčiūnų","Mažųjų Lygainių","Juodšilių","Pagirių 2-oji"], "VIL"),
  39:("NORTH",["Senamiesčio","V. Kudirkos","Respublikos","Ramučių","Agluonų","Akmenės 1-oji","Alkiškių","Daubiškių","Kairiškių","Gulbinų","Kivylių","Kruopių","Pavenčio","Papilės","Luokavos","Sablauskių","Ventos","Naujamiesčio"],"WEST"),
  41:("NORTH",["Butkiškės","Dubėnų","Gailių","Janaučių","Junkilų","Karklėnų","Centro","A. Mackevičiaus","Kalno","Kolainių","Kražių","Kukečių","Liolių","Lupikų","Maironių","Pakėvio","Pakražančio","Pašilės","Pavėžupio","Petrališkės","Stulgių","Šaltenių","Šaukėnų","Užvenčio","Vaiguvos","Valpainių","Verpenos","Vidsodžio","Žalpių"],"WEST"),
  49:("NORTH",["Raguvos","Šilų","Miežiškių","Nevėžio","Velžio","Liūdynės","Katinų","Vadoklių","Jotainių"],"EAST"),
  50:("EAST",["Antalieptės","Antazavės","Šniukštų","Baibių","Degučių","Avilių","Imbrado","Suvieko","Dimitriškių","Magučių","Štadvilių","Dusetų","Zarasų rytų","Zarasų vakarų","Zarasų šiaurės"],"NORTH"),
  59:("EAST",["Draugystės","Saulės","Sodų","Versmės","Beižionių","Gilučių","Jagėlonių","Kietaviškių"],"CP"),
}
CROSS = {k:(a,{norm(x) for x in b},c) for k,(a,b,c) in CROSS.items()}

def station_region(row):
    major = int(row["major_id"])
    if major in BASE:
        return BASE[major]
    special, names, other = CROSS[major]
    return special if norm(row["minor_name"]) in names else other

def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def hamilton(reg_counts, seats):
    total=sum(reg_counts.values())
    q={r:reg_counts[r]*seats/total for r in reg_counts}
    out={r:math.floor(q[r]) for r in q}
    left=seats-sum(out.values())
    for r in sorted(q, key=lambda r:(q[r]-math.floor(q[r]), reg_counts[r], r), reverse=True)[:left]:
        out[r]+=1
    return out, q

def dhondt(votes, seats, eligible=None):
    ids=[p for p in votes if eligible is None or p in eligible]
    won={p:0 for p in ids}
    for _ in range(seats):
        p=max(ids, key=lambda x:(votes[x]/(won[x]+1), votes[x], -int(x) if str(x).isdigit() else 0))
        won[p]+=1
    return won

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--dir",default=".")
    ap.add_argument("--vrk-apylinkes",default=None)
    args=ap.parse_args()
    d=Path(args.dir)
    minors=read_csv(d/"2024-minor-district.csv")
    votes=read_csv(d/"2024-votes.csv")
    parties=read_csv(d/"2024-parties.csv")
    pnames={p["org_id"]:p["org_name"] for p in parties}

    # Optional full municipality join from official VRK open-data export.
    mun={}
    if args.vrk_apylinkes:
        rows=read_csv(args.vrk_apylinkes)
        for r in rows:
            date=(r.get("rink_turo_data") or "")[:10]
            if date and date!="2024-10-13": continue
            major=r.get("rink_turo_apyg_nr") or r.get("apyg_nr") or r.get("apygardos_nr")
            minor=r.get("apyl_nr")
            name=r.get("apyl_pavad")
            sav=r.get("sav_pavadinimas")
            if major and minor and name and sav:
                mun[(str(int(float(major))),str(int(float(minor))),norm(name))]=sav

    by_gid={}
    reg_stat=defaultdict(lambda: {"stations":0,"registered":0,"list_votes":0})
    out_st=[]
    for r in minors:
        rk=station_region(r)
        by_gid[r["minor_gid"]]=rk
        reg_stat[rk]["stations"]+=1
        reg_stat[rk]["registered"]+=int(r["registered_voters"])
        reg_stat[rk]["list_votes"]+=int(r["votes"])
        sav=mun.get((str(int(r["major_id"])),str(int(r["minor_id"])),norm(r["minor_name"]))) if mun else ""
        out_st.append([r["minor_gid"],r["major_id"],r["minor_id"],r["minor_name"],sav,REGION_NAME[rk],r["registered_voters"],r["votes"]])

    rv=defaultdict(lambda: defaultdict(int))
    for v in votes:
        rv[by_gid[v["minor_gid"]]][v["org_id"]]+=int(v["votes"])

    national=defaultdict(int)
    for rk in rv:
        for pid,v in rv[rk].items(): national[pid]+=v

    official = {
      "3":240503,"13":224026,"12":186305,"11":114792,"14":95868,"8":87374,"16":56379,
      "17":48288,"2":35726,"5":32813,"9":27362,"6":23547,"4":21002,"1":17218,"10":9367
    }
    assert sum(national.values())==1220570
    assert dict(national)==official, "Partijų nacionalinė kontrolė nesutampa."

    territorial=["VIL","EAST","CP","WEST","NORTH"]
    reg_counts={r:reg_stat[r]["registered"] for r in territorial}
    assert sum(reg_counts.values())==2331973

    national_total=sum(national.values())
    eligible5={p for p,v in national.items() if v/national_total>=0.05}

    with open(d/"out_station_region.csv","w",encoding="utf-8-sig",newline="") as f:
        w=csv.writer(f); w.writerow(["minor_gid","major_id","minor_id","minor_name","savivaldybe","regionas","registered_voters","list_votes"]); w.writerows(out_st)

    with open(d/"out_region_party_votes.csv","w",encoding="utf-8-sig",newline="") as f:
        w=csv.writer(f); w.writerow(["regionas","org_id","party","votes"])
        for r in territorial:
            for pid,v in sorted(rv[r].items(), key=lambda x:-x[1]):
                w.writerow([REGION_NAME[r],pid,pnames[pid],v])

    for M in (50,55,60):
        alloc,q=hamilton(reg_counts,M)
        for threshold,elig in [("no_threshold",None),("national_5pct",eligible5)]:
            rows=[]
            totals=defaultdict(int)
            for r in territorial:
                won=dhondt(rv[r],alloc[r],elig)
                for pid,s in won.items():
                    totals[pid]+=s
                    if s: rows.append([M,threshold,REGION_NAME[r],alloc[r],pid,pnames[pid],s])
            with open(d/f"out_seats_{M}_{threshold}.csv","w",encoding="utf-8-sig",newline="") as f:
                w=csv.writer(f); w.writerow(["regional_seats","threshold","region","region_seats","org_id","party","party_seats"]); w.writerows(rows)

        print(M, {REGION_NAME[r]:alloc[r] for r in territorial})

    print("PASS: national party votes =",sum(national.values()))
    print("PASS: territorial registered voters =",sum(reg_counts.values()))
    print("NOTE: diaspora kept outside 5-region denominator.")

if __name__=="__main__":
    main()