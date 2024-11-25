import os
import django
from datetime import date
from random import randint, choice

# 设置 Django 环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BookStoreBackend.settings")
django.setup()

# 导入模型
from user.models import User, Address
from category.models import Category, SubCategory
from product.models import Author, Publisher, Book
from cart.models import Cart

def create_test_data():
    # 创建多个用户
    for i in range(5):
        user = User(
            account=f"user{i+1}",
            avatar=f"user_avatars/user{i+1}.jpg",
            birthday=date(1990 + i, 1, 1 + i),
            city_code=f"1000{i+1}",
            gender="male" if i % 2 == 0 else "female",
            mobile=f"12345678{i+1}",
            nickname=f"User{i+1}",
            profession="Engineer" if i % 2 == 0 else "Artist",
            province_code=f"10{i+1}",
            token=f"token{i+1}"
        )
        user.save()

        # 每个用户创建一个收货地址
        address = Address(
            user=user,
            address=f"{i+1}23 Street, City{i+1}",
            address_tags="Home" if i % 2 == 0 else "Office",
            city_code=f"1000{i+1}",
            contact=f"12345678{i+1}",
            county_code=f"200{i+1}",
            full_location=f"{i+1}23 Street, City{i+1}, State{i+1}",
            postal_code=f"1234{i+1}",
            province_code=f"10{i+1}",
            receiver=f"Receiver{i+1}",
            is_default=True if i == 0 else False
        )
        address.save()

    # 创建多个一级分类和二级分类
    categories = []
    subcategories = []
    for i in range(3):
        category = Category(
            name=f"Category{i+1}",
            picture=f"category_pictures/category{i+1}.jpg"
        )
        category.save()
        categories.append(category)

        # 每个一级分类下创建多个二级分类
        for j in range(2):
            subcategory = SubCategory(
                name=f"SubCategory{i+1}-{j+1}",
                picture=f"subcategory_pictures/subcategory{i+1}_{j+1}.jpg",
                parent=category,
                sale_properties={"genre": f"genre{j+1}", "age_group": "adult" if j % 2 == 0 else "child"}
            )
            subcategory.save()
            subcategories.append(subcategory)

    # 创建多个作者和出版商
    authors = []
    publishers = []
    for i in range(5):
        author = Author(
            name=f"Author{i+1}",
            desc=f"Famous author{i+1}",
            picture=f"author_pictures/author{i+1}.jpg",
            place=f"Country{i+1}"
        )
        author.save()
        authors.append(author)

        publisher = Publisher(
            name=f"Publisher{i+1}",
            logo=f"publisher_logos/publisher{i+1}.jpg",
            desc=f"Top publisher{i+1}",
            picture=f"publisher_pictures/publisher{i+1}.jpg",
            place=f"City{i+1}"
        )
        publisher.save()
        publishers.append(publisher)

    # 创建多个书籍数据
    books = []
    for i in range(10):
        book = Book(
            ISBN=f"123-4567890{i+1}",
            name=f"Book{i+1}",
            desc=f"This is a description of book{i+1}",
            discount=randint(5, 20),
            old_price=randint(10, 100),
            inventory=randint(50, 200),
            publisher=choice(publishers),
            subcategory=choice(subcategories),
            collect_count=randint(0, 50),
            sales_count=randint(0, 100),
            comment_count=randint(0, 30),
            main_pictures=[f"main_pictures/book{i+1}.jpg"]
        )
        book.save()

        # 添加多个作者到每本书
        book.authors.add(*[choice(authors) for _ in range(randint(1, 3))])
        book.save()
        books.append(book)

    # 创建多个购物车数据
    for i in range(5):
        cart = Cart(
            user=User.objects.get(account=f"user{i+1}"),
            count=randint(1, 5),
            original_price=randint(10, 100),
            current_price=randint(5, 80),
            picture=f"cart_pictures/cart{i+1}.jpg",
            post_fee=randint(1, 10),
            stock=randint(20, 100)
        )
        cart.save()

        # 每个购物车添加多个书籍
        cart.books.add(*[choice(books) for _ in range(randint(1, 3))])
        cart.save()

    print("批量测试数据已成功保存到数据库。")

if __name__ == "__main__":
    create_test_data()
