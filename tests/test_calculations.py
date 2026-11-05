import unittest
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from calculations import price,loop,tickets
class TestLab(unittest.TestCase):
    def test_call1(self):self.assertAlmostEqual(price(12400,0,0,1850),.0433)
    def test_call2(self):self.assertAlmostEqual(price(900,0,11500,1850),.0226)
    def test_call3(self):self.assertAlmostEqual(price(900,11500,0,1850),.04905)
    def test_monthly(self):self.assertAlmostEqual((price(12400,0,0,1850)-price(900,0,11500,1850))*10000,207)
    def test_context(self):self.assertEqual(900+11500,12400)
    def test_20_turns(self):self.assertEqual(loop(20)["input"],445000)
    def test_30_turns(self):self.assertEqual(loop(30)["input"],892500)
    def test_20_cost(self):self.assertAlmostEqual(loop(20)["total_usd"],.97)
    def test_30_cost(self):self.assertAlmostEqual(loop(30)["total_usd"],1.905)
    def test_5k_file(self):self.assertAlmostEqual(loop(30,5000)["total_usd"]-loop(30)["total_usd"],.3)
    def test_tickets_a(self):self.assertAlmostEqual(tickets(.004,.55)["total_usd"],410.8)
    def test_tickets_b(self):self.assertAlmostEqual(tickets(.011,.92)["total_usd"],24.68)
    def test_api_spend(self):self.assertAlmostEqual(tickets(.011,.92)["api_usd"],11.88)
    def test_human_escalations(self):self.assertAlmostEqual(tickets(.004,.55)["human_tickets"],202.5)
if __name__=="__main__":unittest.main()
