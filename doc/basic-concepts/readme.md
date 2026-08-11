The basic concepts and elements of the data lineage

This section explains the fundamental lineage concepts captured by SQLFlow. Each SQL sample first documents the current legacy dlineage output and then shows how the same proven semantics are represented by the Static Lineage Projection Contract (SLPC) v0.2.

> [!IMPORTANT]
> Sections titled <span style="color:#8250df">**SLPC v0.2 representation**</span> use a purple heading and
> callout so they are easy to distinguish from legacy output. SLPC separates canonical `Endpoint`/`Fact`
> semantics from per-statement `Occurrence` evidence, typed operations and relationships, and
> `IntermediateGraph` explain details. The former experimental replacement model has been retired from these docs.
> The callouts describe the contract-correct target representation. A producer or legacy adapter that lacks
> authoritative evidence must use Candidate, Diagnostic, loss accounting, or partial completeness; it must
> not fabricate the illustrated canonical record.

Common shorthand used in the callouts:

| Shorthand | Contract meaning |
|---|---|
| `VALUE + DIRECT` | `Fact(axis=VALUE, role=DIRECT)`; a value passes through unchanged |
| `VALUE + TRANSFORM` | `Fact(axis=VALUE, role=TRANSFORM)`; an expression changes or combines values |
| `VALUE + AGGREGATE` | `Fact(axis=VALUE, role=AGGREGATE)`; an aggregate produces the target value |
| `ROW + FILTER` | `Fact(axis=ROW, role=FILTER)`; a predicate determines row presence |
| `ROW + JOIN` | `Fact(axis=ROW, role=JOIN)`; a join key/predicate shapes joined rows |
| Candidate/Diagnostic | semantics or identity are incomplete and are reported without guessing |

### Concepts
- [1. Introduction to Data Lineage](./01-introduction.md)
- [2. Direct Data Flow](./02-direct-dataflow.md)
- [3. Indirect Dataflow and Pseudo Columns](./03-indirect-dataflow-and-pseudo-column.md)
- [4. Functions](./04-functions.md)
- [5. Dataflow Chain](./05-dataflow-chain.md)
- [6. Temporary Result Set](./06-temporary-resultset-table.md)
- [7. Joins](./07-join-relation.md)
- [8. Transforms](./08-transforms.md)
- [9. Constants and Variables](./09-constant-and-variables.md)
- [10. ER Diagrams](./10-er-diagram.md)
