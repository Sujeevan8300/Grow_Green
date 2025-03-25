from flask import Blueprint, render_template, flash, send_from_directory, redirect
from flask_login import login_required, current_user
from .forms import ShopItemsForm, OrderForm, CategoryForm

from werkzeug.utils import secure_filename
from .models import Product, Order, Customer, Category
from . import db
import os


admin = Blueprint('admin', __name__)


@admin.route('/media/<path:filename>')
def get_image(filename):
    return send_from_directory('../media', filename)


@admin.route('/add-shop-items', methods=['GET', 'POST'])
@login_required
def add_shop_items():
    if current_user.id == 1:
        form = ShopItemsForm()
        
        # Pass available categories to the form
        form.category_id.choices = [(category.id, category.name) for category in Category.query.all()]
        
        if form.validate_on_submit():
            product_name = form.product_name.data
            current_price = form.current_price.data
            previous_price = form.previous_price.data
            in_stock = form.in_stock.data
            flash_sale = form.flash_sale.data
            category_id = form.category_id.data  # Get selected category

            file = form.product_picture.data
            file_name = secure_filename(file.filename)
            file_path = f'./media/{file_name}'
            file.save(file_path)

            new_shop_item = Product()
            new_shop_item.product_name = product_name
            new_shop_item.current_price = current_price
            new_shop_item.previous_price = previous_price
            new_shop_item.in_stock = in_stock
            new_shop_item.flash_sale = flash_sale
            new_shop_item.product_picture = file_path
            new_shop_item.category_id = category_id  # Assign category to the product

            try:
                db.session.add(new_shop_item)
                db.session.commit()
                flash(f'{product_name} added successfully!')
                return render_template('add-shop-items.html', form=form)
            except Exception as e:
                flash('Error adding product!')
                print(e)

        return render_template('add-shop-items.html', form=form)
    
    return render_template('404.html')




@admin.route('/shop-items', methods=['GET', 'POST'])
@login_required
def shop_items():
    if current_user.id == 1:
        items = Product.query.order_by(Product.date_added).all()
        return render_template('shop_items.html', items=items)
    return render_template('404.html')



@admin.route('/update-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def update_item(item_id):
    if current_user.id == 1:
        form = ShopItemsForm()

        item_to_update = Product.query.get(item_id)

        # Set form fields with current product values
        form.product_name.render_kw = {'placeholder': item_to_update.product_name}
        form.previous_price.render_kw = {'placeholder': item_to_update.previous_price}
        form.current_price.render_kw = {'placeholder': item_to_update.current_price}
        form.in_stock.render_kw = {'placeholder': item_to_update.in_stock}
        form.flash_sale.render_kw = {'placeholder': item_to_update.flash_sale}

        # Fetch categories to populate the category dropdown
        categories = Category.query.all()
        form.category_id.choices = [(category.id, category.name) for category in categories]

        if form.validate_on_submit():
            product_name = form.product_name.data
            current_price = form.current_price.data
            previous_price = form.previous_price.data
            in_stock = form.in_stock.data
            flash_sale = form.flash_sale.data
            category_id = form.category_id.data

            file = form.product_picture.data

            if file:
                file_name = secure_filename(file.filename)
                file_path = f'./media/{file_name}'
                file.save(file_path)

                try:
                    Product.query.filter_by(id=item_id).update(dict(
                        product_name=product_name,
                        current_price=current_price,
                        previous_price=previous_price,
                        in_stock=in_stock,
                        flash_sale=flash_sale,
                        product_picture=file_path,
                        category_id=category_id
                    ))

                    db.session.commit()
                    flash(f'{product_name} updated successfully')
                    return redirect('/shop-items')
                except Exception as e:
                    flash('Item not updated!')

        return render_template('update_item.html', form=form)

    return render_template('404.html')





@admin.route('/delete-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def delete_item(item_id):
    if current_user.id == 1:
        try:
            item_to_delete = Product.query.get(item_id)
            
            # Remove the associated product picture from the file system
            if item_to_delete.product_picture:
                try:
                    os.remove(item_to_delete.product_picture)
                except Exception as e:
                    print(f"Error deleting image file: {e}")

            # Delete the product from the database
            db.session.delete(item_to_delete)
            db.session.commit()

            flash(f'Item "{item_to_delete.product_name}" deleted successfully!')
            return redirect('/shop-items')
        except Exception as e:
            flash('Error: Item not deleted!')
            print('Item not deleted', e)
            return redirect('/shop-items')

    return render_template('404.html')


@admin.route('/view-orders')
@login_required
def order_view():
    if current_user.id == 1:
        orders = Order.query.all()
        return render_template('view_orders.html', orders=orders)
    return render_template('404.html')



@admin.route('/update-order/<int:order_id>', methods=['GET', 'POST'])
@login_required
def update_order(order_id):
    if current_user.id == 1:
        form = OrderForm()

        order = Order.query.get(order_id)

        if form.validate_on_submit():
            status = form.order_status.data
            order.status = status

            try:
                db.session.commit()
                flash(f'Order {order_id} Updated successfully')
                return redirect('/view-orders')
            except Exception as e:
                print(e)
                flash(f'Order {order_id} not updated')
                return redirect('/view-orders')

        return render_template('order_update.html', form=form)

    return render_template('404.html')


@admin.route('/customers')
@login_required
def display_customers():
    if current_user.id == 1:
        customers = Customer.query.all()
        return render_template('customers.html', customers=customers)
    return render_template('404.html')



@admin.route('/admin-page')
@login_required
def admin_page():
    if current_user.id == 1:
        return render_template('admin.html')
    return render_template('404.html')



@admin.route('/categories', methods=['GET', 'POST'])
@login_required
def manage_categories():
    if current_user.id == 1:
        form = CategoryForm()
        categories = Category.query.order_by(Category.date_added).all()

        if form.validate_on_submit():
            name = form.name.data
            description = form.description.data

            new_category = Category(name=name, description=description)

            try:
                db.session.add(new_category)
                db.session.commit()
                flash(f'Category "{name}" added successfully!')
                return redirect('/categories')
            except Exception as e:
                flash('Error adding category!')
                print(e)

        return render_template('categories.html', form=form, categories=categories)
    return render_template('404.html')



@admin.route('/update-category/<int:category_id>', methods=['GET', 'POST'])
@login_required
def update_category(category_id):
    if current_user.id == 1:
        category = Category.query.get_or_404(category_id)
        form = CategoryForm(obj=category)

        if form.validate_on_submit():
            category.name = form.name.data
            category.description = form.description.data

            try:
                db.session.commit()
                flash(f'Category "{category.name}" updated successfully!')
                return redirect('/categories')
            except Exception as e:
                flash('Error updating category!')
                print(e)

        return render_template('update_category.html', form=form)
    return render_template('404.html')


@admin.route('/delete-category/<int:category_id>', methods=['GET', 'POST'])
@login_required
def delete_category(category_id):
    if current_user.id == 1:
        category = Category.query.get_or_404(category_id)
        try:
            db.session.delete(category)
            db.session.commit()
            flash(f'Category "{category.name}" deleted successfully!')
            return redirect('/categories')
        except Exception as e:
            flash('Error deleting category!')
            print(e)
        return redirect('/categories')
    return render_template('404.html')


@admin.route('/delete-customer/<int:customer_id>', methods=['POST'])
@login_required
def delete_customer(customer_id):
    if current_user.id == 1:  # Only the admin can delete customers
        customer_to_delete = Customer.query.get_or_404(customer_id)

        try:
            db.session.delete(customer_to_delete)
            db.session.commit()
            flash(f'Customer "{customer_to_delete.username}" deleted successfully!')
        except Exception as e:
            flash('Error deleting customer!')
            print(e)

        return redirect('/customers')  # Redirect back to the customer list

    return render_template('404.html')




