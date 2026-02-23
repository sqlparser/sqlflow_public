### Handle the dataflow chain

Every relation in the SQL is picked up by the tool, and connected together to show the whole dataflow chain.
Sometimes, we only need to see the end to end relation and ignore all the intermediate relations.

If we need to convert a fully chained dataflow to an `end to end` dataflow, we may consider the following rules:

1. A single dataflow chain with the mixed relation types: fdd and fdr.

   ```
   A -> fdd -> B -> fdr -> C -> fdd -> D
   ```
   the rule is: if any `fdr` relation appears in the chain, the relation from `A -> D` will be consider as type of `fdr`, otherwise, the final relation is `fdd` for the end to end relation of `A -> D`.
2. If there are multiple chains from  `A -> D`

   ```
   A -> fdd -> B1 -> fdr -> C1 -> fdd -> D
   A -> fdd -> B2 -> fdr -> C1 -> fdd -> D
   A -> fdd -> B3 -> fdd -> C3 -> fdd -> D
   ```
   The final relation should choose the `fdd` chain if any.
