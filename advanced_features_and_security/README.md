# Permissions & Groups

Model: `bookshelf.Book` defines custom permissions:
- `can_view`
- `can_create`
- `can_edit`
- `can_delete`

Groups:
- **Viewers** → `can_view`
- **Editors** → `can_view`, `can_create`, `can_edit`
- **Admins**  → `can_view`, `can_create`, `can_edit`, `can_delete`

Views (in `LibraryProject/bookshelf/views.py`) enforce permissions using
`@permission_required(...)`, including `book_list` for viewing.
