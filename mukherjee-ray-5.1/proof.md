# No coefficientwise dominant connected zero forcing tree for large order

This proves the quantified nonexistence assertion in Conjecture 5.1 of
Sanjay Mukherjee and Papi Ray, *On the connected zero forcing polynomial of
finite trees*, [arXiv:2611.10985v1](https://arxiv.org/html/2611.10985v1#S5.Thmtheorem1)
(7 November 2026). An explicit sufficient threshold is

\[
N(p)=2p^3+1.
\]

The numbered conjecture also contains an informal sentence about growth in
the number of incomparable maximal elements. Section 5 proves a precise
version: that number is at least \(\max\{2,\lfloor p/3\rfloor\}\) once
\(n\ge2p^3+\lfloor p/3\rfloor\). This lower bound tends to infinity with \(p\);
it does not assert monotonicity of the exact number of maximal elements.

## Definitions and theorem

A tree is a finite, simple, connected, undirected, acyclic graph. Its leaves are
its degree-one vertices. Starting with a set of colored vertices, the zero
forcing rule allows a colored vertex having exactly one uncolored neighbor to
color that neighbor. A connected zero forcing set is an initial set that
induces a connected subgraph and can eventually color the entire tree.

Write

\[
F_T(x)=\sum_{k=0}^n c_k(T)x^k,
\]

where \(c_k(T)\) counts the connected zero forcing sets of size \(k\).
Thus \(F_T(1)\) is their total number. The paper's order \(T\ge T'\) means
\(c_k(T)\ge c_k(T')\) for every \(k\).

**Theorem.** If \(p\ge5\) and \(n\ge2p^3+1\), no tree with \(n\) vertices and
\(p\) leaves dominates every other tree with those same parameters.

This is stronger than the stated absence of a unique dominant tree: there is
no dominant tree at all.

## 1. The subtree every connected zero forcing set must contain

Call a vertex of degree at least three a branch vertex. Because \(p\ge5\), at
least one branch vertex exists: a finite tree with maximum degree at most two
is a path, and a nontrivial path has two leaves.

Let \(K\) be the minimal subtree containing all branch vertices; if there is
only one branch vertex, \(K\) consists of that vertex. Put \(s=|V(K)|\).

Every connected zero forcing set \(S\) contains every branch vertex. To see
this, suppose a branch vertex \(v\) is absent from \(S\). Since \(S\) is
connected, it lies in one component of \(T-v\). At least two other components
of \(T-v\) are initially entirely uncolored. Before \(v\) is colored no force
can enter either component, since each is connected to the rest of the tree
only through \(v\). After \(v\) is colored, both components still have
uncolored neighbors of \(v\). Neither component can receive its first force:
that force would have to come from \(v\), which has at least two uncolored
neighbors. Hence they remain uncolored, a contradiction.

As \(S\) contains all branch vertices and is connected, it contains the unique
path between every pair of them. It therefore contains \(K\).

Every component outside \(K\) attaches to \(K\) by exactly one edge. Otherwise
there would be a cycle. It contains no branch vertex, so it is a path attached
at an endpoint. Its other endpoint is a leaf of \(T\). Conversely every leaf
lies outside \(K\): leaves cannot be branch vertices or interior points of
paths between branch vertices. Thus there are exactly \(p\) such pendant
paths. Let their positive lengths, counting vertices outside \(K\), be
\(d_1,\ldots,d_p\). Then

\[
\sum_{i=1}^p d_i=n-s.
\]

A connected set containing \(K\) meets each pendant path in a prefix, starting
at its attachment vertex, of length \(0,1,\ldots,d_i\). Consequently

\[
F_T(1)\le\prod_{i=1}^p(d_i+1).
\tag{1}
\]

This is an upper bound because some prefix choices need not be forcing sets.

## 2. A uniform upper bound for trees with at least two branch vertices

Such a tree has \(s\ge2\). The arithmetic-geometric mean inequality applied
to the \(p\) positive numbers \(d_i+1\) in (1) gives

\[
F_T(1)\le\left(\frac{n-s+p}{p}\right)^p
\le\left(\frac{n+p-2}{p}\right)^p.
\tag{2}
\]

## 3. A balanced subdivided star beats that upper bound

Write

\[
n-1=pq+r,\qquad 0\le r<p.
\]

Our hypothesis implies \(q\ge2p^2\). Let \(B\) be the tree consisting of one
central vertex with \(p-r\) pendant paths of length \(q\) and \(r\) pendant
paths of length \(q+1\). It has \(n\) vertices and \(p\) leaves.

For any subdivided star with positive arm lengths \(b_1,\ldots,b_p\), every
connected forcing set contains the center and a prefix of each arm. At most
one prefix may be empty. If two are empty the center can never start either
arm. Conversely, with at most one empty prefix, the center can start that arm
if necessary, and the colored prefixes can force outward along all arms.
Hence its total number of connected forcing sets is exactly

\[
\prod_i b_i+\sum_i\prod_{j\ne i}b_j.
\tag{3}
\]

For \(B\), the product in (3) is
\(q^{p-r}(q+1)^r\ge q^p+r q^{p-1}\), by the binomial expansion.
Each of the \(p\) remaining products is at least \(q^{p-1}\). Therefore

\[
F_B(1)\ge q^p+(p+r)q^{p-1}.
\tag{4}
\]

Set \(a=(p+r-1)/p\). Then \(0<a<2\), and the upper bound (2) is

\[
\left(\frac{n+p-2}{p}\right)^p
=(q+a)^p
=q^p+(p+r-1)q^{p-1}+R,
\]

where

\[
R=\sum_{j=2}^p\binom pj a^j q^{p-j}.
\]

For every \(2\le j\le p\), the factorial formula gives

\[
\binom pj
=\frac{p(p-1)(p-2)\cdots(p-j+1)}{j!}
\le\frac{p(p-1)p^{j-2}}2.
\]

Using \(a<2\), \(q\ge2p^2>2p\), and a convergent geometric series, we get

\[
\begin{aligned}
R
&<2p(p-1)q^{p-2}\sum_{j=2}^p(2p/q)^{j-2}\\
&<\frac{2p(p-1)q^{p-2}}{1-2p/q}\\
&=\frac{2p(p-1)}{q-2p}\,q^{p-1}\\
&\le q^{p-1}.
\end{aligned}
\]

The last inequality follows from
\(q-2p\ge2p^2-2p=2p(p-1)\). Combining this strict bound with (4),

\[
F_B(1)>\left(\frac{n+p-2}{p}\right)^p.
\tag{5}
\]

Equations (2) and (5) show that \(B\) has more connected zero forcing sets in
total than **every** tree with at least two branch vertices.

If a tree dominated every other tree coefficientwise, it would in particular
have total count at least \(F_B(1)\). It must therefore have exactly one branch
vertex, and hence be a subdivided star.

## 4. One coefficient excludes every subdivided star

In a subdivided star with \(p\) arms, a connected forcing set must contain the
center and at least one vertex on each of at least \(p-1\) arms. A set of size
exactly \(p\) therefore consists of the center and the first vertex on all but
one arm. Every such choice is a forcing set, by the argument proving (3).
There are exactly \(p\) choices, so

\[
c_p(T)=p\qquad\text{for every subdivided star }T.
\tag{6}
\]

Now construct \(D\) with two adjacent vertices \(u,v\), with two pendant paths
at \(u\) and \(p-2\) pendant paths at \(v\). Give all paths positive lengths
summing to \(n-2\): explicitly, one length can be \(n-p-1\), and the other
\(p-1\) lengths can be one. This is possible since \(n\ge p+2\).
Both hubs have degree at least three; there are \(n\) vertices and \(p\) leaves.

Every connected forcing set contains \(u,v\). At either hub at most one
attached path can have an empty prefix, since two empty paths at that hub
cannot ever receive their first force. Thus a forcing set must include at
least one first vertex among the two paths at \(u\), and at least \(p-3\)
first vertices among the \(p-2\) paths at \(v\). This already uses
\(2+1+(p-3)=p\) vertices.

A forcing set of size exactly \(p\) must therefore omit exactly one path at
each hub and include just the first vertex of every other path. Conversely,
every such choice forces the whole tree: each hub can color the first vertex
of its one empty path, and all paths then force outward. The independent
omission choices give

\[
c_p(D)=2(p-2)>p\qquad(p\ge5).
\tag{7}
\]

By (6) and (7), no subdivided star dominates \(D\). Section 3 already excluded
every other tree from dominating \(B\). No tree dominates all trees with the
same \(n,p\), proving the theorem. \(\square\)

## 5. A quantitative version of the growth assertion

For every \(p\ge5\) and \(n\ge2p^3+\lfloor p/3\rfloor\), there are at least

\[
\max\{2,\lfloor p/3\rfloor\}
\]

pairwise incomparable maximal connected zero forcing polynomials, realized
by trees with \(n\) vertices and \(p\) leaves. Here maximal means that no
different polynomial in this family dominates it coefficientwise.

We first prove two additional elementary counting facts.

**The coefficient at \(x^p\).** For an arbitrary tree let \(K\) and \(s\)
be as in Section 1. Suppose exactly \(t\) vertices of \(K\) have pendant
paths attached, with positive numbers of attached paths
\(k_1,\ldots,k_t\), summing to \(p\). Every connected forcing set contains
\(K\). At each attachment vertex at most one pendant path can have an empty
prefix: two empty paths would prevent either from receiving its first force.
Conversely, if at most one prefix is empty at each attachment vertex, that
vertex can immediately start its empty path (all its neighbors in \(K\)
are already colored), and every nonempty prefix can force outward. Thus these
are exactly the valid prefix choices.

The smallest possible size of such a set is consequently

\[
s+\sum_{i=1}^t(k_i-1)=s+p-t.
\]

It is achieved by omitting one path at each attachment vertex and taking
exactly the first vertex of every other path. There are \(\prod_i k_i\)
such sets. Since \(t\le s\), it follows that

\[
c_p(T)=
\begin{cases}
0,&t<s,\\
\prod_{i=1}^s k_i,&t=s.
\end{cases}
\tag{8}
\]

**Products of integer parts.** Let \(M(p,c)\) denote the largest product of
\(c\) positive integers with sum \(p\). A maximizing tuple is balanced:
if two entries \(a,b\) satisfy \(a\ge b+2\), replacing them by \(a-1,b+1\)
increases their product by \(a-b-1>0\). Repeating this adjustment terminates,
for example because the sum of squares decreases. Therefore the entries of
a maximizing tuple differ by at most one, and if \(p=ch+r\), \(0\le r<c\),

\[
M(p,c)=h^{c-r}(h+1)^r.
\tag{9}
\]

For \(1\le c<\lfloor p/3\rfloor\), we have

\[
M(p,c+1)>M(p,c).
\tag{10}
\]

Indeed, \(p\ge3(c+1)\), so every entry of the balanced maximizing \(c\)-tuple
is at least three. If an entry \(a\ge5\) occurs, replace it by \(2,a-2\).
The sum is unchanged, the number of entries increases by one, and the factor
\(a\) becomes \(2(a-2)>a\). Otherwise all entries are three or four.
Writing their sum as \(3c+f\), where \(f\) is the number of fours, yields
\(f\ge3\). Replace three fours by four threes: the sum remains twelve, the
number of entries increases by one, and the factor \(64\) becomes \(81\).
In either case a \((c+1)\)-tuple has product greater than \(M(p,c)\), proving
(10).

Put \(m=\lfloor p/3\rfloor\). For each \(1\le c\le m\), construct a tree
\(B_c\) as follows. Take a path of \(c\) vertices as its stem (a single
vertex if \(c=1\)). Distribute \(p\) pendant paths among those vertices in
balanced positive group sizes \(k_1,\ldots,k_c\) attaining \(M(p,c)\).
All group sizes are at least three, because \(p\ge3c\). Hence each stem
vertex is a branch vertex, and the selected path is exactly the minimal
subtree containing all branch vertices. Finally make all \(p\) pendant path
lengths balanced, with sum \(n-c\).

Equation (8) gives

\[
c_p(B_c)=M(p,c).
\tag{11}
\]

If a tree \(T\) has stem size \(s<c\), equations (8)--(10) imply
\(c_p(T)\le M(p,s)<M(p,c)\), so \(T\) cannot dominate \(B_c\).

If a tree \(T\) has stem size \(s>c\), equation (1) and AM--GM give

\[
F_T(1)\le\left(\frac{n+p-c-1}{p}\right)^p.
\tag{12}
\]

Write \(n-c=pq+r\), \(0\le r<p\). Since \(n\ge2p^3+m\) and \(c\le m\),
we have \(q\ge2p^2\). Among the connected forcing sets of \(B_c\) are all
prefix choices with no empty path and all choices with exactly one empty
path globally. Counting just these choices, as in (3)--(4), gives

\[
F_{B_c}(1)\ge q^p+(p+r)q^{p-1}.
\]

The right side of (12) is \((q+(p+r-1)/p)^p\), so the identical binomial
remainder estimate from Section 3 proves \(F_{B_c}(1)>F_T(1)\).
Thus \(T\) cannot dominate \(B_c\) in this case either.

We have proved that **every tree dominating \(B_c\) must have stem size
exactly \(c\)**.

There are finitely many trees on \(n\) vertices, hence finitely many
polynomials under consideration. Starting with the polynomial of \(B_c\),
repeatedly move to a strictly larger polynomial whenever possible. Finiteness
ensures that this procedure terminates at a maximal polynomial \(Q_c\)
dominating \(B_c\). Any tree representing \(Q_c\) has stem size \(c\).
For \(c\ne d\), the polynomials \(Q_c,Q_d\) cannot be equal: a representative
of a common polynomial would dominate both \(B_c\) and \(B_d\) and thus have
two different stem sizes. They are also incomparable, since both are maximal
and distinct. This supplies \(m\) pairwise incomparable maximal polynomials.

The main theorem supplies at least two for all \(p\ge5\). To justify this
last inference explicitly, if a finite partially ordered set had only one
maximal element, extending any element upward by strict steps would reach
that same maximal element, making it greatest. We proved that there is no
greatest polynomial. There must therefore be at least two maximal elements.
Combining the two lower bounds proves the growth theorem. \(\square\)

## Computational verification and scope

The proof above covers all integers \(p\ge5\) and \(n\ge2p^3+1\); it does not
infer a universal claim from a finite sample. Its bounds are deliberately
nonoptimal. Only exact integer or rational arithmetic is used in the scripts.

- `exact_check.py` checks the displayed threshold inequality, its intermediate
  estimates, and a concrete \(p=5,n=251\) illustration using integer products
  and cleared denominators.
- `independent_check.py` independently enumerates connected zero forcing sets
  by the literal coloring rule and compares them with the prefix description
  on all non-path unlabeled trees of orders 4 through 10. It also checks all
  residue classes at the proposed threshold for \(5\le p\le100\), and (10)
  for \(6\le p\le500\).
- `proof_check.md` and `independent_tree_review.md` record separate reviews.
- `research_catalogues.md` records the prior-resolution search. Only v1 was
  listed. Searches in both requested catalogues found a resolution of this
  paper's separate Problem 5.3, not Conjecture 5.1. Dedicated citation-index
  endpoints were unavailable, so the novelty search is bounded rather than
  an exhaustive guarantee.

The paper motivates the conjecture with computations and examples for five
leaves (orders 9–13) and eight leaves (including orders 13 and 17), described
in Examples 4.17 and 4.19. It does not report a general exhaustive range over
all leaf counts. Section 5 supplies an unbounded quantitative lower bound
for the informal growth statement, without claiming monotonicity of the
exact number of maximal elements.
