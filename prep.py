import csv, gzip, json, math, sys
S='/tmp/claude-1000/-home-sheheryar/50155157-b2da-43c4-8172-51c4d575fbeb/scratchpad/'
G={'Alp':'α','Bet':'β','Gam':'γ','Del':'δ','Eps':'ε','Zet':'ζ','Eta':'η','The':'θ','Iot':'ι','Kap':'κ','Lam':'λ','Mu':'μ','Nu':'ν','Xi':'ξ','Omi':'ο','Pi':'π','Rho':'ρ','Sig':'σ','Tau':'τ','Ups':'υ','Phi':'φ','Chi':'χ','Psi':'ψ','Ome':'ω'}
SUP={'1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹'}
names=json.load(open(S+'celdata/starnames.json'))
rows=[]
seen=set()
bayers=set()
for r in csv.DictReader(gzip.open(S+'hyg/f.gz','rt')):
    if r['id']=='0': continue
    m=float(r['mag'])
    if m>6.0: continue
    b=r['bayer']
    if b:
        bayers.add(b)
        parts=b.split('-'); g=G.get(parts[0],parts[0])
        if len(parts)>1: g+=''.join(SUP.get(c,c) for c in parts[1])
        b=g
    hip=int(r['hip']) if r['hip'] else 0
    nm=r['proper']
    if not nm and hip and str(hip) in names: nm=names[str(hip)].get('name','')
    d=float(r['dist']); d=-1 if d>=10000 else round(d,2)
    k=977792.0
    vx,vy,vz=[round(float(r[c])*k,1) for c in ('vx','vy','vz')]
    if d<0: vx=vy=vz=0
    ci=r['ci']; ci=round(float(ci),2) if ci else 0.6
    rows.append([round(float(r['ra']),5),round(float(r['dec']),4),round(m,2),ci,d,vx,vy,vz,round(float(r['absmag']),2),r['spect'],nm,b,r['flam'],r['con'],hip,int(r['comp'] or 1)])
rows.sort(key=lambda x:x[2])
print(len(rows),file=sys.stderr)
print(sorted(bayers - set(k for k in bayers if k.split('-')[0] in G)),file=sys.stderr)
# constellation lines -> star indices
import bisect
def vec(ra_deg,dec):
    a=math.radians(ra_deg);d=math.radians(dec);return (math.cos(d)*math.cos(a),math.cos(d)*math.sin(a),math.sin(d))
V=[vec(r[0]*15,r[1]) for r in rows]
lines=json.load(open(S+'celdata/constellations.lines.json'))
cons=json.load(open(S+'celdata/constellations.json'))
info={f['id']:[f['properties']['name'],f['properties']['gen']] for f in cons['features']}
L={}
miss=0
for f in lines['features']:
    segs=[]
    for seg in f['geometry']['coordinates']:
        idx=[]
        for lon,lat in seg:
            v=vec(lon,lat);best=-1;bd=-2
            for i,w in enumerate(V):
                dd=v[0]*w[0]+v[1]*w[1]+v[2]*w[2]
                if dd>bd: bd=dd;best=i
            if bd<math.cos(math.radians(0.3)): miss+=1
            idx.append(best)
        segs.append(idx)
    L[f['id']]=segs
print('miss',miss,file=sys.stderr)
json.dump({'s':rows,'l':L,'c':info},open(S+'build/data.json','w'),ensure_ascii=False,separators=(',',':'))
