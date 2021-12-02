1. создаем 2-х пользователей
>>> from news.models import *
>>> u1= User.objects.create_user(username='Nikolay')
>>> u1
<User: Nikolay>
>>> u2= User.objects.create_user(username='Anton')
>>> u2
<User: Anton>


2. создаем 2-х авторов
>>> Author.objects.create(authorUser=u1)
>>> author1 = Author.objects.get(id=1)
<Author: Author object (1)>
>>> Author.objects.create(authorUser=u2)
>>> author2 = Author.objects.get(id=2)
<Author: Author object (2)>
>>> author1.authorUser
<User: Nikolay>
>>> author2.authorUser
<User: Anton>


3. создаем 4 категории статей (постов)
>>> Category.objects.create(name='Auto')
<Category: Category object (1)>
>>> Category.objects.create(name='World')
<Category: Category object (
>>> Category.objects.create(name='Weather')
<Category: Category object (3)>
>>> Category.objects.create(name='The Science')
<Category: Category object (4)>


4. создаем 2 статьи и 1 новость
>>> Post.objects.create(author=author1, categoryType='NW', title='News Auto', text='News Auto bla bla bla')
<Post: Post object (1)>
>>> Post(id=1).categoryType
'AR'
>>> Post.objects.create(author=author2, categoryType='NW', title='The Science', text='The Science  blo blo blo')
<Post: Post object (2)>
>>> Post.objects.get(id=2).title
'IT - good rabora'
>>> Post.objects.create(author=author1, categoryType='AR', title='World', text='In World pam pam pararam')
<Post: Post object (3)>
>>> Post.objects.get(id=3).text
'People  bly bly bly'
>>> Post.objects.all().values('text')
<QuerySet [{'text': 'News Auto bla bla bla'}, {'text': 'The Science  blo blo blo'}, {'text': 'In World pam pam pararam'}]>
>>> Post.objects.all().values('title')
<QuerySet [{'title': 'News Auto'}, {'title': 'The Science'}, {'title': 'World'}]>


5. присваиваем категории для наших статей
>>> Post.objects.get(id=1).postCategory.add(Category.objects.get(id=1))
>>> Post.objects.get(id=1).postCategory.add(Category.objects.get(id=2))
>>> Post.objects.get(id=2).postCategory.add(Category.objects.get(id=3))
>>> Post.objects.get(id=3).postCategory.add(Category.objects.get(id=4))


6. создаем комментарии к статьям (к первой статье 2 коммента от разных авторов)
>>> Comment.objects.create(commentPost=Post.objects.get(id=1), commentUser=Author.objects.get(id=1).authorUser, text='Best Auto')
<Comment: Comment object (1)>
>>> Comment.objects.create(commentPost=Post.objects.get(id=1), commentUser=Author.objects.get(id=2).authorUser, text='No! Auto hlam')
<Comment: Comment object (2)>
>>> Comment.objects.create(commentPost=Post.objects.get(id=2), commentUser=Author.objects.get(id=1).authorUser, text='The Science no stoping')
<Comment: Comment object (3)>
>>> Comment.objects.create(commentPost=Post.objects.get(id=3), commentUser=Author.objects.get(id=2).authorUser, text='The world is poorly understood')
<Comment: Comment object (4)>


7. создаем лайки и дизлайки к нашим статьям и комментам
>>> Comment.objects.get(id=1).like()
>>> Comment.objects.get(id=1).like()
>>> Comment.objects.get(id=1).rating
2
>>> Comment.objects.get(id=1).like()
>>> Comment.objects.get(id=1).like()
>>> Comment.objects.get(id=1).like()
>>> Comment.objects.get(id=1).dislike()
>>> Comment.objects.get(id=1).dislike()
>>> Comment.objects.get(id=1).like()
>>> Comment.objects.get(id=1).like()
>>> Comment.objects.get(id=2).like()
>>> Comment.objects.get(id=2).like()
>>> Comment.objects.get(id=2).like()
>>> Comment.objects.get(id=2).like()
>>> Comment.objects.get(id=2).dislike()
>>> Comment.objects.get(id=2).dislike()
>>> Comment.objects.get(id=3).like()
>>> Comment.objects.get(id=3).like()
>>> Comment.objects.get(id=3).like()
>>> Comment.objects.get(id=3).like()
>>> Comment.objects.get(id=3).rating
4
>>> Post.objects.get(id=1).like()
>>> Post.objects.get(id=1).like()
>>> Post.objects.get(id=1).like()
>>> Post.objects.get(id=1).dislike()
>>> Post.objects.get(id=2).dislike()
>>> Post.objects.get(id=2).like()
>>> Post.objects.get(id=2).like()
>>> Post.objects.get(id=1).rating
2
>>> Post.objects.get(id=2).rating
1


8. обновляем рейтинги авторов
>>> Author.objects.get(id=1)
<Author: Author object (1)>
>>> Author.objects.get(id=1).update_rating()
>>> Author.objects.get(id=1).ratingAuthor
15
>>> Post.objects.get(id=1).like()
>>> Author.objects.get(id=1).update_rating()
>>> Author.objects.get(id=1).ratingAuthor
18
>>> Author.objects.get(id=2)
<Author: Author object (2)>
>>> Author.objects.get(id=2).update_rating()
>>> Author.objects.get(id=2).ratingAuthor
5



9. получаем username и рейтинг лучшего пользователя
>>> Author.objects.all().order_by('-ratingAuthor')[:1]
<QuerySet [<Author: Author object (1)>]>
>>> Author.objects.all().order_by('-ratingAuthor').values('authorUser','ratingAuthor')[:1]
<QuerySet [{'authorUser': 1, 'ratingAuthor': 18}]>


10. выводим дату добавления, username автора, рейтинг, заголовок лучшей статьи, основываясь на лайках
>>> Post.objects.all().order_by('-rating').values('dateCreation', 'author', 'rating', 'title', 'text')[:1]
<QuerySet [{'dateCreation': datetime.datetime(2021, 12, 2, 13, 55, 50, 349180, tzinfo=<UTC>), 'author': 1, 'rating': 3, 'title': 'News Auto', 'text': 'News Auto bla bla bla'}]>
10.1 превьюшка данной статьи
>>> Post.objects.all().order_by('-rating')[0].preview()
'News Auto bla bla bla...'


11. выводим все комменты к лучшей статье (из п10) (дата, пользователь, рейтинг, текст)
получаем id лучшего поста (п10)
>>> Post.objects.all().order_by('-rating')[0].id
1
формируем запрос
>>> Comment.objects.filter(commentPost=Post.objects.get(id=Post.objects.all().order_by('-rating')[0].id)).values('dateCreation', 'commentUser', 'rating', 'text')
<QuerySet [{'dateCreation': datetime.datetime(2021, 12, 2, 14, 46, 50, 30342, tzinfo=<UTC>), 'commentUser': 1, 'rating': 5, 'text': 'Best Auto'}, {'dateCreation': datetime.datetime(2021, 12, 2, 14, 48, 14, 663354, tzinfo=<UTC>), 'commentUser': 2, 'rating': 2, 'text': 'No! Auto hlam'}]>
