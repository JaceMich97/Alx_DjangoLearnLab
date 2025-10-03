# Permissions & Groups (advanced_features_and_security)

Model protected: `bookshelf.Book`

Custom permissions defined in `bookshelf/models.py` (Meta.permissions):
- `can_view`
- `can_create`
- `can_edit`
- `can_delete`

Groups to create in Django Admin and their permissions:
- **Viewers** → `can_view`
- **Editors** → `can_view`, `can_create`, `can_edit`
- **Admins**  → `can_view`, `can_create`, `can_edit`, `can_delete`

Views enforce permissions in `LibraryProject/bookshelf/views.py`
using `@permission_required(...)`, including the exact function:
- `book_list` (requires `bookshelf.can_view`)
- plus create/edit/delete views requiring `can_create`, `can_edit`, `can_delete`.

Assign users to groups via Admin to activate access control.
