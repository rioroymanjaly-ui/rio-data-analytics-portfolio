import unittest
from operations import generate,validate,summarize,sql_scorecard

class TestOperations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=generate()
        cls.metrics=summarize(cls.rows)
    def test_deterministic(self):
        self.assertEqual(generate(10),generate(10))
    def test_row_count(self):
        self.assertEqual(len(self.rows),1800)
    def test_unique_ids(self):
        self.assertEqual(len({r["order_id"] for r in self.rows}),1800)
    def test_valid_rows(self):
        self.assertTrue(validate(self.rows))
    def test_duplicate_detection(self):
        with self.assertRaises(ValueError):
            validate(self.rows[:1]*2)
    def test_invalid_cost(self):
        x=dict(self.rows[0]);x["actual_cost_eur"]=-1
        with self.assertRaises(ValueError):
            validate([x])
    def test_kpi_reconciliation(self):
        self.assertEqual(self.metrics["late_orders"],sum(r["actual_days"]>r["promised_days"] for r in self.rows))
    def test_sql_groups(self):
        self.assertEqual(len(sql_scorecard(self.rows)),6)

if __name__=="__main__":unittest.main()
