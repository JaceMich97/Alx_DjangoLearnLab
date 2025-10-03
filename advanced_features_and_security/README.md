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

Views protected in `LibraryProject/bookshelf/views.py` with:
`@permission_required('bookshelf.can_view', ...)`,
`@permission_required('bookshelf.can_create', ...)`,
`@permission_required('bookshelf.can_edit', ...)`,
`@permission_required('bookshelf.can_delete', ...)`.

Setup (via Admin):
1. Create groups **Viewers**, **Editors**, **Admins**.
2. Assign the permissions above to each group.
3. Add users to the appropriate group(s).
