---main page route
/catalogue (and '/')

method: showCatalogue()

---show a category
/catalogue/<int:category_id>
/catalogue/<int:category_id>/items

method: showCategory()

---edit a category
/catalogue/<int:category_id>/edit

method: editCategory()

---delete a category (only if you own it)
/catalogue/<int:category_id>/delete

---show a specific item
/catalogue/<int:category_id>/<int:item_id>

method: showItem()

---edit a specific item (if you own it)
/catalogue/<int:category_id>/<int:item_id>/edit

method: editItem()

---delete a specific item (if you own it)
/catalogue/<int:category_id>/<int:item_id>/delete

deleteItem()

---JSON endpoint
catalogue.json
