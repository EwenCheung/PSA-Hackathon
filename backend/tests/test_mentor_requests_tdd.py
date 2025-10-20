"""
Test-Driven Development tests for Mentor Request System.

This file demonstrates TDD principles for the mentor request functionality.
Following the principle: Write tests first, then implement to make tests pass.
"""
import pytest
import sqlite3
from unittest.mock import Mock

from app.core.db import init_db
from app.services.mentor_match_request_service import MentorMatchingService
from app.data.repositories.mentor_match_request import MentorMatchRequestRepository
from app.data.repositories.employee import EmployeeRepository


class TestMentorRequestSystemTDD:
    """TDD tests for mentor request system."""
    
    def setup_method(self):
        """Set up test database and services."""
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        init_db(self.conn)
        
        # Seed test data
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO employees (id, name, role, department_id, level, position_level, points_current, hire_date)
            VALUES 
            ('TEST001', 'Junior Dev', 'Software Engineer', 'DEPT001', 'Junior', 2, 100, '2023-01-01'),
            ('TEST002', 'Senior Dev', 'Senior Engineer', 'DEPT001', 'Senior', 4, 500, '2020-01-01')
        """)
        self.conn.commit()
        
        self.service = MentorMatchingService(self.conn)

    def test_create_request_success(self):
        """Test: Successfully create a mentor request."""
        # Given: A junior employee wants mentorship from a senior employee
        mentee_id = "TEST001"
        mentor_id = "TEST002" 
        message = "I want to improve my coding skills"
        goals = ["Python", "Architecture"]
        
        # When: Creating a mentor request
        result = self.service.create_request(mentee_id, mentor_id, message, goals)
        
        # Then: Request should be created successfully
        assert result["status"] == "pending"
        assert result["menteeId"] == mentee_id
        assert result["mentorId"] == mentor_id
        assert result["message"] == message
        assert result["goals"] == goals
        assert "requestId" in result

    def test_create_request_fails_for_same_position_level(self):
        """Test: Cannot request mentorship from same/lower position level."""
        # Given: Two employees with same position level
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO employees (id, name, role, department_id, level, position_level, points_current, hire_date)
            VALUES ('TEST003', 'Another Junior', 'Developer', 'DEPT001', 'Junior', 2, 100, '2023-01-01')
        """)
        self.conn.commit()
        
        # When/Then: Requesting mentorship should fail
        with pytest.raises(ValueError, match="higher position level"):
            self.service.create_request("TEST001", "TEST003", "message", ["goal"])

    def test_prevent_duplicate_pending_requests(self):
        """Test: Cannot create duplicate pending requests."""
        # Given: An existing pending request
        self.service.create_request("TEST001", "TEST002", "message", ["goal"])
        
        # When/Then: Creating another request should fail
        with pytest.raises(ValueError, match="pending mentorship request"):
            self.service.create_request("TEST001", "TEST002", "another message", ["goal"])

    def test_soft_delete_functionality(self):
        """Test: Soft delete marks request as deleted."""
        # Given: A pending request
        request = self.service.create_request("TEST001", "TEST002", "message", ["goal"])
        request_id = int(request["requestId"].replace("REQ", ""))
        
        # When: Deleting the request
        self.service.delete_request(request_id, "TEST001")
        
        # Then: Request should be marked as deleted, not removed
        active_requests = self.service.list_requests(mentee_id="TEST001")
        all_requests = self.service.list_requests(mentee_id="TEST001", include_deleted=True)
        
        assert len(active_requests) == 0  # Filtered out
        assert len(all_requests) == 1     # Still exists
        assert all_requests[0]["status"] == "deleted"

    def test_can_create_new_request_after_deletion(self):
        """Test: Can create new request after deleting previous one."""
        # Given: A deleted request
        request = self.service.create_request("TEST001", "TEST002", "message", ["goal"])
        request_id = int(request["requestId"].replace("REQ", ""))
        self.service.delete_request(request_id, "TEST001")
        
        # When: Creating a new request
        new_request = self.service.create_request("TEST001", "TEST002", "new message", ["new goal"])
        
        # Then: New request should be created successfully
        assert new_request["status"] == "pending"
        assert new_request["message"] == "new message"

    def test_accept_request_creates_mentorship_pair(self):
        """Test: Accepting request creates active mentorship."""
        # Given: A pending request
        request = self.service.create_request("TEST001", "TEST002", "message", ["goal"])
        request_id = int(request["requestId"].replace("REQ", ""))
        
        # When: Accepting the request
        accepted = self.service.update_request_status(request_id, "accepted")
        
        # Then: Request status should be accepted and mentorship pair created
        assert accepted["status"] == "accepted"
        
        pairs = self.service.list_pairs(mentee_id="TEST001")
        assert len(pairs) == 1
        assert pairs[0]["menteeId"] == "TEST001"
        assert pairs[0]["mentorId"] == "TEST002"

    def test_cannot_delete_accepted_request(self):
        """Test: Cannot delete accepted requests."""
        # Given: An accepted request
        request = self.service.create_request("TEST001", "TEST002", "message", ["goal"])
        request_id = int(request["requestId"].replace("REQ", ""))
        self.service.update_request_status(request_id, "accepted")
        
        # When/Then: Trying to delete should fail
        with pytest.raises(ValueError, match="Accepted requests cannot be deleted"):
            self.service.delete_request(request_id, "TEST001")

    def test_mentee_can_only_delete_own_requests(self):
        """Test: Mentees can only delete their own requests."""
        # Given: A request from one mentee
        request = self.service.create_request("TEST001", "TEST002", "message", ["goal"])
        request_id = int(request["requestId"].replace("REQ", ""))
        
        # When/Then: Another employee trying to delete should fail
        with pytest.raises(ValueError, match="only modify your own"):
            self.service.delete_request(request_id, "TEST002")  # Wrong employee

    def teardown_method(self):
        """Clean up test database."""
        self.conn.close()


# Additional integration test
def test_complete_mentor_workflow():
    """Integration test for complete mentor request workflow."""
    # This would test the entire workflow from creation to acceptance
    # Following TDD principles: define the complete behavior first
    pass


if __name__ == "__main__":
    # Run tests with: python -m pytest tests/test_mentor_requests_tdd.py -v
    print("TDD Tests for Mentor Request System")
    print("Run with: pytest tests/test_mentor_requests_tdd.py -v")