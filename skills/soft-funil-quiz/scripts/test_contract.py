#!/usr/bin/env python3
"""Independent contract rejection tests; no owner data or external requests."""
import copy,json,unittest
from pathlib import Path
from validate_quiz import validate,safe_url
BASE=Path(__file__).resolve().parent.parent
class Contract(unittest.TestCase):
 def setUp(self):self.c=json.loads((BASE/'examples/organizacao-checkout.json').read_text())
 def test_examples(self):
  for p in (BASE/'examples').glob('*.json'):self.assertEqual(validate(json.loads(p.read_text())),[],p.name)
 def test_tie_missing(self):self.c['tieOrder']=[];self.assertTrue(validate(self.c))
 def test_unknown_profile(self):self.c['steps'][0]['options'][0]['scores']={'inexistente':1};self.assertTrue(validate(self.c))
 def test_future_condition(self):self.c['steps'][0]['when']={'question':'futura','op':'eq','value':'x'};self.assertTrue(validate(self.c))
 def test_backend_not_implemented(self):self.c['capture']['mode']='remote';self.assertTrue(validate(self.c))
 def test_unsafe_destinations(self):
  for u in ['javascript:alert(1)','//example.com/x','../private','https://user:secret@example.com/x','data:text/html,x','http://example.com']:self.assertFalse(safe_url(u),u)
 def test_allowed_destinations(self):
  for u in ['destinos/checkout.html','https://example.invalid/checkout']:self.assertTrue(safe_url(u),u)
 def test_meeting_requires_eligibility(self):self.c['route']='meeting';self.assertTrue(validate(self.c))
if __name__=='__main__':unittest.main()
