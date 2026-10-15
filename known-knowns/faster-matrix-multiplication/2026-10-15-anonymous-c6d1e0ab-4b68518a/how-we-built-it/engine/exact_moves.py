"""Explicit exact absorption constraints, replayed independently of a proposer."""
from fractions import Fraction

def absorb_constraints(sa, terms, basis, zero_terms):
    """Choose the unique linear absorption map zeroing a full independent set.

    `basis` contains verified exact relations sum_t lambda_t U_t tensor V_t=0.
    Only raw term indices are supplied by the proposer; all coefficients of the
    move are recomputed over Q from this basis and the actual input W factors.
    """
    k=len(basis)
    if not k or len(zero_terms)!=k or len(set(zero_terms))!=k:
        raise ValueError('need one distinct constraint per exact kernel dimension')
    if any(type(t) is not int or not 0<=t<len(terms) for t in zero_terms):
        raise ValueError('invalid raw term index')
    rays=[[vector.get(t,Fraction(0)) for vector in basis] for t in zero_terms]
    if sa.exact_left_nullspace([{j:x for j,x in enumerate(ray) if x} for ray in rays]):
        raise ValueError('selected exact constraints are dependent')
    rhs=[{a:-x for a,x in sorted(terms[t][2].items())} for t in zero_terms]
    Z=sa._solve_rays(rays,rhs,k)
    support=sorted(set().union(*(set(vector) for vector in basis)))
    result=list(terms);killed=set()
    for t in support:
        U,V,W=terms[t];changed=dict(W)
        for j,vector in enumerate(basis):
            coefficient=vector.get(t,0)
            if coefficient:
                for a,z in Z[j].items():
                    value=changed.get(a,0)+coefficient*z
                    if value:changed[a]=value
                    else:changed.pop(a,None)
        if changed:result[t]=(U,V,changed)
        else:result[t]=None;killed.add(t)
    if not set(zero_terms)<=killed:raise ValueError('exact selected constraints did not vanish')
    return [term for term in result if term is not None],len(killed)
