import torch,torch.nn as nn,networkx as nx
from motifwl.wl import Mode,_adjacency_sets,_directed_edges,_square_witnesses
def struct(G,mode):
 G=nx.convert_node_labels_to_integers(G);adj=_adjacency_sets(G);de=_directed_edges(G)
 idx={e:i for i,e in enumerate(de)};m=len(de)
 li=[[] for _ in range(m)];ri=[[] for _ in range(m)];tri=[];sq=[]
 for e in de:
  u,v=e;p=idx[e]
  for x in adj[u]:li[p].append(idx[(u,x)])
  for z in adj[v]:ri[p].append(idx[(v,z)])
  for y in (adj[u]&adj[v]):tri.append((p,idx[(u,y)],idx[(v,y)]))
  for y,w in _square_witnesses(adj,u,v,simple=mode.simple_squares):sq.append((p,idx[(u,y)],idx[(v,w)],idx[(y,w)]))
 return dict(m=m,li=li,ri=ri,tri=torch.tensor(tri,dtype=torch.long).reshape(-1,3),sq=torch.tensor(sq,dtype=torch.long).reshape(-1,4))
def agg(src,index,dim,m,d):
 o=torch.zeros(m,d,device=src.device)
 if index.numel():o.index_add_(0,index,src)
 return o
class Layer(nn.Module):
 def __init__(s,d,mode):
  super().__init__();s.mode=mode;k=3+(1 if mode.tri else 0)+(1 if mode.square1 else 0)+(2 if mode.square2 else 0)
  s.up=nn.Sequential(nn.Linear(k*d,2*d),nn.ReLU(),nn.Linear(2*d,d))
  if mode.tri:s.ft=nn.Sequential(nn.Linear(2*d,d),nn.ReLU(),nn.Linear(d,d))
  if mode.square1:s.f1=nn.Sequential(nn.Linear(3*d,d),nn.ReLU(),nn.Linear(d,d))
  if mode.square2:s.f2a=nn.Sequential(nn.Linear(2*d,d),nn.ReLU(),nn.Linear(d,d));s.f2b=nn.Sequential(nn.Linear(d,d),nn.ReLU(),nn.Linear(d,d))
 def forward(s,h,st):
  m=st['m'];d=h.size(1);L=agg(h[sum(st['li'],[])] if any(st['li']) else h[:0],torch.tensor([i for i,l in enumerate(st['li']) for _ in l],dtype=torch.long),0,m,d)
  R=agg(h[sum(st['ri'],[])] if any(st['ri']) else h[:0],torch.tensor([i for i,l in enumerate(st['ri']) for _ in l],dtype=torch.long),0,m,d)
  parts=[h,L,R]
  if s.mode.tri:
   t=st['tri'];msg=s.ft(torch.cat([h[t[:,1]],h[t[:,2]]],-1)) if t.numel() else torch.zeros(0,d)
   parts.append(agg(msg,t[:,0] if t.numel() else torch.zeros(0,dtype=torch.long),0,m,d))
  if s.mode.square1:
   q=st['sq'];msg=s.f1(torch.cat([h[q[:,1]],h[q[:,2]],h[q[:,3]]],-1)) if q.numel() else torch.zeros(0,d)
   parts.append(agg(msg,q[:,0] if q.numel() else torch.zeros(0,dtype=torch.long),0,m,d))
  if s.mode.square2:
   q=st['sq']
   na=s.f2a(torch.cat([h[q[:,1]],h[q[:,2]]],-1)) if q.numel() else torch.zeros(0,d)
   op=s.f2b(h[q[:,3]]) if q.numel() else torch.zeros(0,d)
   parts.append(agg(na,q[:,0] if q.numel() else torch.zeros(0,dtype=torch.long),0,m,d))
   parts.append(agg(op,q[:,0] if q.numel() else torch.zeros(0,dtype=torch.long),0,m,d))
  return h+s.up(torch.cat(parts,-1))
class EdgeMotifGNN(nn.Module):
 def __init__(s,d=32,layers=4,mode='tri_square1',out=1):
  super().__init__();s.mode=Mode.parse(mode);s.d=d
  s.emb=nn.Parameter(torch.randn(d)*.1)
  s.ls=nn.ModuleList([Layer(d,s.mode) for _ in range(layers)])
  s.rd=nn.Sequential(nn.Linear(d,d),nn.ReLU(),nn.Linear(d,out))
 def embed(s,G):
  st=struct(G,s.mode);h=s.emb.unsqueeze(0).repeat(st['m'],1)
  for l in s.ls:h=l(h,st)
  return h.sum(0)
 def forward(s,G):return s.rd(s.embed(G))
