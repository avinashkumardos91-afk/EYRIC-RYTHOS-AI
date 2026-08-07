import unittest

from app.core.agent import Agent


class WorkflowTests(unittest.TestCase):
    def test_security_workflow_generates_protection_plan(self):
        agent = Agent(state_dir='data')
        result = agent.execute_workflow('website_protection', {'url': 'https://example.com'})

        self.assertEqual(result['workflow'], 'website_protection')
        self.assertIn('protective_actions', result)
        self.assertTrue(result['protective_actions'])

    def test_repo_guard_workflow_sets_monitoring_plan(self):
        agent = Agent(state_dir='data')
        result = agent.execute_workflow('repo_guard', {'repo': 'example/repo'})

        self.assertEqual(result['workflow'], 'repo_guard')
        self.assertIn('monitoring_plan', result)

    def test_self_protection_and_public_guard_are_available(self):
        agent = Agent(state_dir='data')
        self_protection = agent.self_protect()
        public_guard = agent.public_guard_status()

        self.assertEqual(self_protection['status'], 'ok')
        self.assertEqual(public_guard['mode'], 'public_ready')


if __name__ == '__main__':
    unittest.main()
