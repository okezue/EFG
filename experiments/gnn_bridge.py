import torch,networkx as nx
from motifgnn.model import EdgeMotifGNN
from motifwl.wl import canonical_edge_motif_signature as csig
from motifwl.parity import private_triangle_parity_pair
torch.manual_seed(0)
def U(a,b):return nx.disjoint_union(a,b)
def pairs():
 yield "C3+C3 vs C6",U(nx.cycle_graph(3),nx.cycle_graph(3)),nx.cycle_graph(6)
 yield "C4+C4 vs C8",U(nx.cycle_graph(4),nx.cycle_graph(4)),nx.cycle_graph(8)
 yield "C5+C5 vs C10",U(nx.cycle_graph(5),nx.cycle_graph(5)),nx.cycle_graph(10)
 g0,g1=private_triangle_parity_pair(d=1);yield "parity80 (G0 vs G1)",g0,g1
MODES=["tri","square1","square2","tri_square1","tri_square2"]
def main():
 print(f"{'pair':24}{'mode':14}{'discrete_sep':14}{'rel_diff':12}{'neural_sep':12}match")
 ok=tot=0
 for name,G,H in pairs():
  for m in MODES:
   mdl=EdgeMotifGNN(d=32,layers=4,mode=m).double().eval()
   with torch.no_grad():
    eG,eH=mdl.embed(G),mdl.embed(H)
    rel=((eG-eH).norm()/(eG.norm()+eH.norm()+1e-30)).item()
   ds=csig(G,m)!=csig(H,m);ns=rel>1e-9;tot+=1;ok+=ds==ns
   print(f"{name:24}{m:14}{str(ds):14}{rel:<12.2e}{str(ns):12}{'OK' if ds==ns else 'MISMATCH'}")
 print(f"\nneural matches discrete refinement on {ok}/{tot} (pair,mode) cases (float64, rel threshold 1e-9)")
if __name__=="__main__":main()
