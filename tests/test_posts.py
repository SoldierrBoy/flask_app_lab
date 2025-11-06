import unittest
from app import create_app, db
from app.posts.models import Post, PostCategory
from datetime import datetime


class PostCRUDTestCase(unittest.TestCase):

    def setUp(self):

        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):

        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def _create_dummy_post(self, title="Dummy Post", content="Dummy content"):

        post = Post(
            title=title,
            content=content,
            category=PostCategory.TECH,
            author="TestUser"
        )
        db.session.add(post)
        db.session.commit()
        return post

    def test_us01_create_post(self):

        response = self.client.post('/post/create', data={
            'title': 'My First Post',
            'content': 'This is TDD!',
            'category': 'tech',
            'publish_date': '2025-01-01T10:00',
            'is_active': True
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Post My First Post has been created!", response.data)


        post = db.session.scalar(db.select(Post).where(Post.title == 'My First Post'))
        self.assertIsNotNone(post)
        self.assertEqual(post.content, 'This is TDD!')

    def test_us02_list_posts(self):

        self._create_dummy_post(title="Test Post 123")

        response = self.client.get('/post/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Post 123', response.data)

    def test_us03_view_post_detail(self):

        post = self._create_dummy_post(content="Full detailed content")

        response = self.client.get(f'/post/{post.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Full detailed content', response.data)
        self.assertIn(b'Edit Post', response.data)

    def test_us04_update_post(self):

        post = self._create_dummy_post()

        response = self.client.post(f'/post/{post.id}/update', data={
            'title': 'Updated Title',
            'content': 'Updated Content',
            'category': 'other',
            'publish_date': post.posted.strftime('%Y-%m-%dT%H:%M')
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Post Updated Title has been updated!", response.data)


        updated_post = db.get_or_404(Post, post.id)
        self.assertEqual(updated_post.title, 'Updated Title')
        self.assertEqual(updated_post.category, PostCategory.OTHER)

    def test_us05_delete_post(self):

        post = self._create_dummy_post(title="Post to Delete")
        post_id = post.id


        response = self.client.post(f'/post/{post_id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Post Post to Delete has been deleted.", response.data)


        deleted_post = db.session.get(Post, post_id)
        self.assertIsNone(deleted_post)

    def test_us06_404_not_found(self):

        response = self.client.get('/post/9999')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Oops! Page Not Found', response.data)