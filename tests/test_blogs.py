import unittest

from app.api.v1.blog.actions import Blogs

CREATE_SAMPLE_BLOG = {
    ""
}


class TestBlogs(unittest.TestCase):

    def test_create(self):
        Blogs().create()


if __name__ == '__main__':
    unittest.main()
