from unittest import TestCase
from optimizer.optimizer import ServiceOptimizer

class ServiceOptimizerTest(TestCase):
    def test_cpu(self):
        optimizer = ServiceOptimizer(None, None)
        test_cases = {
            ('low cpu', 25.0, 1024, 0, 256),
            ('extremely low cpu', 20, 1024, 0, 0),
            ('no cpu', 0.0, 4096, 0, 0),
            ('extremely high cpu', 100.0, 4096, 0, 4096),
            ('small over-reserved cpu', 7.0, 4096, 300, 300),
            ('small under-reserved cpu', 8.0, 4096, 300, 300),
        }

        for test_case in test_cases:
            msg, utilization, instance_cpu_capacity, cpu_shares, expected_cpu_shares = test_case
            new_cpu_shares = optimizer.recommend_cpu(utilization, instance_cpu_capacity, cpu_shares, 0.1, 0.1, True, 256)

            self.assertEquals(expected_cpu_shares, new_cpu_shares, 'cpu shares %s != %s %s' % (expected_cpu_shares, new_cpu_shares, msg))

    def test_memory(self):
        optimizer = ServiceOptimizer(None, None)
        test_cases = {
            ('extremely low memory', 1.0, 64, 64, 4, 4),
            ('under reserved memory', 200.0, 64, 64, 160, 160),
            ('large over-reserved memory', 50.0, 1000, 1000, 640, 640),
            ('small over-reserved memory', 91.0, 80, 80, 80, 80),
            ('small under-reserved memory', 109.0, 80, 80, 112, 112),
            ('diff hard/soft memory', 109.0, 160, 80, 112, 112),
        }

        for test_case in test_cases:
            msg, utilization, hard_limit, soft_limit, expected_hard_limit, expected_soft_limit = test_case
            new_limit = optimizer.recommend_memory(utilization, hard_limit, soft_limit, 0.25, True)

            self.assertEquals(expected_soft_limit, new_limit, 'soft limit %s != %s %s' % (expected_soft_limit, new_limit, msg))
            self.assertEquals(expected_hard_limit, new_limit, 'hard limit %s != %s %s' % (expected_hard_limit, new_limit, msg))
