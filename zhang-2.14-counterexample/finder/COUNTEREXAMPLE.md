# Counterexample to Zhang's Conjecture 2.14

The pair of layer sizes **(165,165)** disproves the interlacing clause of
Conjecture 2.14 in Jiahao Zhang, *Characteristic Chow Polynomials of
Layered-Permutation Intervals*, [arXiv:2610.33037v1](https://arxiv.org/html/2610.33037v1),
submitted 15 October 2026. No minimality is claimed.

## Object and exact certificate

Use the paper's gamma polynomials, defined by

\[
H_{(a,b)}(t)=(1+t)^{a+b-1}
\Gamma_{a,b}\!\left(\frac{t}{(1+t)^2}\right).
\]

The underlying poset is the interval of compositions below `(a,b)` in
generalized subword order. For the counterexample it consists of the empty
composition, all one-part compositions `(i)` with `1<=i<=165`, and all
two-part compositions `(i,j)` with `1<=i,j<=165`. Equivalently, its host
permutation is the direct sum of two decreasing permutations of length 165.

Set

\[
p(s)=\Gamma_{165,164}(s),\qquad
g(s)=\Gamma_{165,165}(s)-\Gamma_{165,164}(s),\qquad
W(s)=p(s)g'(s)-p'(s)g(s).
\]

Both polynomials have degree 164. The complete integer coefficient vectors,
in ascending order, are stored in `counterexample.json`. Exact computation
gives

\[
\boxed{W(0)=164>0,\qquad -5621<W(-5/101)<-5620<0.}
\]

This is a certificate for failure of interlacing. It does not require a
claim about the individual real-rootedness of either polynomial. Their
coefficients are nonnegative, so coefficient negativity is not the
obstruction used here.

## Why this disproves weak interlacing

We prove the needed elementary fact, including the paper's convention
that equal-degree interlacing can have either orientation.

Suppose equal-degree real polynomials `p,g` have strictly alternating real
zeros. Write the zeros of `p` as `alpha_1<...<alpha_d`. Polynomial division
and partial fractions give

\[
\frac{g(s)}{p(s)}=c+\sum_{i=1}^d\frac{r_i}{s-\alpha_i},
\qquad r_i=\frac{g(\alpha_i)}{p'(\alpha_i)}.
\]

As `i` increases, both `g(alpha_i)` and `p'(alpha_i)` alternate in sign.
Hence all nonzero residues `r_i` have the same sign. Differentiation yields

\[
\frac{W(s)}{p(s)^2}
=-\sum_{i=1}^d\frac{r_i}{(s-\alpha_i)^2}.
\]

Thus `W` has one sign away from the roots of `p`, and continuity gives the
same weak sign at those roots.

For weakly alternating roots, fix an alternating ordering of the combined
root lists, including multiplicities. Perturb these ordered roots to
strictly increasing real numbers in that order, while keeping the leading
coefficients fixed. The resulting strictly interlacing pairs converge
coefficientwise to `p,g`. The sign just proved is identical for every
perturbation, since the orientation and leading coefficients are fixed.
Their Wronskians converge pointwise to `W`, so `W` also has one weak sign.

The two opposite signs in the displayed certificate contradict this
necessary condition. Consequently `Gamma_(165,164)` and `Delta_(165,165)`
do not weakly interlace. The pair `(165,165)` satisfies the conjecture's
positive-integer hypothesis and is not its excluded pair `(1,1)`.

## Two independent exact computations

Run with Python 3.12; only the standard library is required:

```sh
python3.12 verify_gamma_counterexample.py
python3.12 independent_wronskian_verify.py
```

The first program uses the two-dimensional gamma recurrence from
Proposition 2.11, differentiated formally and evaluated with integer
denominator scaling. It asserts both signs and the strict integer bounds.

The second program constructs the complete polynomial coefficient vectors
from the diagonal generating function of Theorem 2.13, independently of
the two-dimensional recurrence. For clarity, its exact construction is
as follows. Put

\[
D_n(s)=\sum_{j=0}^n\binom nj^2s^j,\qquad G_n(s)=\Gamma_{n,n}(s).
\]

The generating-function multiplier is

\[
\frac{(1-Z)(1-sZ)}{1-Z+sZ^2}.
\]

Multiplying by its denominator and comparing coefficients gives

\[
G_0=G_1=1,\qquad
G_n=G_{n-1}-sG_{n-2}+D_n-(1+s)D_{n-1}+sD_{n-2}.
\]

Let `f_0=f_1=1` and `f_n=f_(n-1)-s*f_(n-2)`. The diagonal defect identity
and reversal symmetry give

\[
\Gamma_{n,n-1}
=\frac{G_n-(s-1)G_{n-1}+sf_{n-1}}2.
\]

The program checks that every coefficient is even before dividing. It then
forms the two formal derivatives and evaluates all four polynomials by
integer Horner arithmetic. If `N` is its stored Wronskian numerator, then

\[
W(-5/101)=N/101^{327},\qquad
-5621\cdot101^{327}<N<-5620\cdot101^{327}.
\]

As an additional convention check, `gamma_terminal_verify.py` directly
enumerated terminal chains in all 64 principal intervals with both parts
at most eight, converted the Chow polynomials to gamma coefficients, and
agreed with the two-dimensional recurrence in every case. The full
coefficient vectors at the final counterexample also agree between the
two-dimensional recurrence and the diagonal construction.

## Published evidence and resolution search

The paragraph following Conjecture 2.14 reports exact coefficient
generation with numerical root tests for `1<=a,b<=16`; it separately
reports diagonal Sturm tests through 24, including rational root isolation.

On 25 November 2026 the [arXiv version history](https://arxiv.org/abs/2610.33037)
listed only v1. Searches by title, arXiv identifier, and conjecture name,
and searches of the public
[trureturing catalogue](https://www.trureturing.org/conjectures) and
[solved-conjectures catalogue](https://github.com/1337isnot1337/solved-conjectures),
found no resolution. Citation-service endpoints were inaccessible, so the
novelty search is not exhaustive. `catalogues.md` records that limitation.
