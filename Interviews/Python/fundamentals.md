| Feature         | List                                                                   | Tuple                                                              |
| --------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **Mutability**  | **Mutable** — you can change, add, remove elements after creation      | **Immutable** — once created, you cannot change elements           |
| **Syntax**      | Square brackets: `[1, 2, 3]`                                           | Parentheses (usually): `(1, 2, 3)`                                 |
| **Performance** | Slightly slower due to mutability overhead                             | Faster and more memory efficient                                   |
| **Use cases**   | When you need a collection that can change                             | When data should remain constant and hashable (e.g., as dict keys) |
| **Methods**     | Many list methods: `.append()`, `.remove()`, `.pop()`, `.sort()`, etc. | Very few methods, mainly `.count()`, `.index()`                    |
| **Hashability** | Not hashable (cannot be dict keys or set elements)                     | Hashable if all elements are hashable (can be dict keys)           |

