from django.test import TestCase, Client
from django.urls import reverse
from apps.accounts.models import CustomUser
from apps.proposals.models import BookProposal

class ProposalTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = CustomUser.objects.create_user(
            username='student1', email='student1@example.com', password='password123', role='student'
        )
        self.librarian = CustomUser.objects.create_user(
            username='lib1', email='lib1@example.com', password='password123', role='librarian'
        )
        self.p1 = BookProposal.objects.create(
            user=self.student, title='Clean Code', author_name='Robert Martin', isbn='9780132350884', reason='Học tập'
        )
        self.p2 = BookProposal.objects.create(
            user=self.student, title='Clean Code 2', author_name='Robert Martin', isbn='9780132350884', reason='Tham khảo'
        )

    def test_proposal_creation_mandatory_isbn(self):
        """Happy case & Edge case: Đảm bảo đề xuất được tạo với ISBN bắt buộc."""
        self.assertEqual(self.p1.isbn, '9780132350884')
        self.assertEqual(BookProposal.objects.filter(isbn='9780132350884').count(), 2)

    def test_mass_approve_proposals_by_isbn(self):
        """Happy case: Phê duyệt đồng loạt (Mass Approve) tất cả yêu cầu cùng ISBN."""
        self.client.login(username='lib1@example.com', password='password123')
        url = reverse('proposals:review_proposal_action', args=[self.p1.pk])
        response = self.client.post(url, {'action': 'approved', 'admin_notes': 'Đã duyệt mua'})
        self.assertEqual(response.status_code, 302)
        
        self.p1.refresh_from_db()
        self.p2.refresh_from_db()
        self.assertEqual(self.p1.status, 'approved')
        self.assertEqual(self.p2.status, 'approved')
