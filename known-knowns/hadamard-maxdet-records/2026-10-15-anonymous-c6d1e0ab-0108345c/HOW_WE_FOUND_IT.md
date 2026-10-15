# How we found it (contributor text, unverified)

This condenses the original agent run's own account. The claim rests only on the object in `object/` and the checker in `verify-it-yourself/`.

- **Idea.** For n = h + 1, where h is a Hadamard order, add a border to a Hadamard matrix H of order h. The determinant is then h^(h/2) (1 + s/h), where s is the excess reached by choosing the signs of the border. So a large excess gives a large determinant.
- **Core.** The Paley construction from the prime 107 gives H of order 108. The same run used Paley cores for order 104 and a Williamson core for order 116.
- **Search.** A compiled iterated local search with basin hopping (`how-we-built-it/maxdet_search.c`) maximized the excess over sign vectors. It reached s = 1056 for order 108. The run then applied what it calls bordered Sherman-Morrison rank-one determinant polishing.
