import random
import numpy as np


def get_rand_alphas(K):
    return sorted([random.random() for _ in range(K)], reverse=True)

def get_rand_values(n):
    return sorted([random.random()*10 for _ in range(n)], reverse=True)

def get_rand_bids(values,truthful=True, min_underbid=0.75, max_overbid=1.05):
    if truthful:
        return values
    new_range=max_overbid-min_underbid
    return [(random.random()*new_range+min_underbid) * v for v in values]

def get_rand_bidders():
    return random.randint(1,99)
    
def get_rand_items():
    return np.random.poisson(5)+1

def check_get_rand_bidders():
    li=[0 for _ in range(100)]
    for i in range(1000):
        li[get_rand_bidders()]+=1
    print(li)
    
def check_get_rand_item():
    li=[0 for _ in range(100)]
    for i in range(1000):
        li[get_rand_items()]+=1
    print(li)

def prepare_auction(debug=False):
    items=get_rand_items()
    n=get_rand_bidders()
    if debug:
        items=3
        n=10
    m=min(n,items)
    alphas=[round(r,2) for r in (get_rand_alphas(items))]
    values=[round(r,2) for r in (get_rand_values(n))]
    
    return items,n,m,alphas,values

def  conduct_auctions(items,n,m,alphas,values, debug=False):
    fpa=FPA(items,n,m,alphas,values,debug)
    spa=SPA(items,n,m,alphas,values,debug)
    vcg=VCG(items,n,m,alphas,values,debug)
    return fpa,spa,vcg
def print_all(n,items,alphas,values,bids,argsorted,winning_prices,revenue):
    print("n",n)
    print("items",items)
    print("alphas",alphas)
    print("values",values)
    print("bids",bids)
    print("argsorted",argsorted[:items])
    print("winningprices",winning_prices)
    print("revenue",revenue)
        
def FPA(items,n,m,alphas,values, debug=False):
    bids=get_rand_bids(values,truthful=False)
    argsorted=list(np.argsort(bids)[::-1])
    winning_prices=[bids[x]*alphas[i] for i,x in enumerate(argsorted[:m])]
    revenue=sum(winning_prices)
    if debug:
        print("\nFPA:")
        print_all(n,items,alphas,values,bids,argsorted,winning_prices,revenue)
    utilities=[alphas[i]*values[argsorted[i]]-winning_prices[i] for i in range(m)]
    return utilities
    
def SPA(items,n,m,alphas,values, debug=True):
    bids=get_rand_bids(values,truthful=True)
    argsorted=list(np.argsort(bids)[::-1])
    bids.append(0)
    winning_prices=[bids[x+1]*alphas[i] for i,x in enumerate(argsorted[:m])]
    revenue=sum(winning_prices)
    if debug:
        print("\nSPA:")
        print_all(n,items,alphas,values,bids,argsorted,winning_prices,revenue)
    utilities=[alphas[i]*values[argsorted[i]]-winning_prices[i] for i in range(m)]
    return utilities
    ...
def VCG(items,n,m,alphas,values, debug=False):
    bids=get_rand_bids(values,truthful=True)
    argsorted=list(np.argsort(bids)[::-1])
    alphas.append(0)
    #winning price is calculated inductively, from last to first
    winning_prices=[0 for _ in range(m+1)]
    for i in range(m-1,-1,-1):
        winning_prices[i]+=winning_prices[i+1]
        winning_prices[i]+=bids[argsorted[i]+1]*(alphas[i]-alphas[i+1])
    revenue=sum(winning_prices)
    if debug:
        print("\nVCG:")
        print_all(n,items,alphas,values,bids,argsorted,winning_prices,revenue)
    utilities=[alphas[i]*values[argsorted[i]]-winning_prices[i] for i in range(m)]
    return utilities
    ...
    
def main(debug=False):
    items,n,m,alphas,values=prepare_auction(debug=debug)
    fpa,spa,vcg=conduct_auctions(items,n,m,alphas,values,True)
    print()
    print("Utilities")
    print(fpa)
    print(spa)
    print(vcg)


np.random.seed(0)
random.seed(0)
main(debug=True)
