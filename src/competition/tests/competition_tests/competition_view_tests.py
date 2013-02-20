from competition.tests.utils import FancyTestCase
from competition.tests.factories import CompetitionFactory


class CompetitionTestListView(FancyTestCase):
    """Test listing all competition objects"""

    def setUp(self):
        for _ in range(0, 73):
            CompetitionFactory.create()

    def test_pagination_first_page(self):
        """Make sure we're paginating the first page properly"""
        response = self.client.rget('competition_list')
        objects = response.context['competitions']
        paginator = response.context['paginator']
        page = response.context['page_obj']
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(10, len(objects))
        self.assertEqual(73, paginator.count)
        self.assertEqual(8, paginator.num_pages)
        self.assertEqual(1, page.number)
        self.assertFalse(page.has_previous())
        self.assertTrue(page.has_next())

    def test_pagination_mid_page(self):
        """Make sure we're paginating another page properly"""
        response = self.client.rget('competition_list', data={'page': '3'})
        objects = response.context['competitions']
        page = response.context['page_obj']
        self.assertEqual(10, len(objects))
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(3, page.number)
        self.assertTrue(page.has_previous())
        self.assertTrue(page.has_next())

    def test_sorted_by_start_time(self):
        """Make sure competitions are sorted properly"""
        response = self.client.rget('competition_list')
        competitions = response.context['competitions']
        for i in range(len(competitions) - 1):
            self.assertGreater(competitions[i].start_time,
                               competitions[i + 1].start_time)
