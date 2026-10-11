"""No public-email, price, signature or past-send assumption may bypass the restart hold."""
import copy
import json
import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / 'tools'
sys.path.insert(0, str(TOOLS))
from outreach_policy import load_policy, send_blocks, validate_email, ROOT
from suppression import load_registry


class SendPolicyTests(unittest.TestCase):
    def setUp(self):
        self.policy = copy.deepcopy(load_policy())
        self.registry = {'version': 1, 'entries': [], 'blocked_countries': {
            'US': {'reason': 'user-exclusion', 'blocked_on': '2026-10-11'},
            'CA': {'reason': 'user-exclusion', 'blocked_on': '2026-10-11'},
        }}
        self.row = {
            'id': 'test-only', 'country': 'GB', 'business': 'Fixture Bakery',
            'package': 'baguette', 'contact_verified': 'hello@fixture.example',
            'contact_source_verified': 'yes', 'contact_source_url': 'https://fixture.example/contact',
            'contact_purpose': 'general-business', 'legal_basis': 'corporate-subscriber',
            'recipient_entity_type': 'corporate', 'legal_evidence_url': 'https://registry.example/fixture',
            'legal_status': 'reviewed', 'legal_reviewed_on': '2026-10-11',
            'privacy_information_ready': 'yes', 'offer_state': 'approved-for-send',
        }

    def make_reviewed_fixture(self):
        self.policy['send_paused'] = False
        self.policy['storage']['privacy_storage_reviewed'] = True
        self.policy['sender'].update({
            'legal_identity_verified': True, 'legal_review_status': 'reviewed',
            'legal_review_reference': 'TEST fixture only, not a real review',
            'tax_review_status': 'reviewed', 'tax_review_reference': 'TEST fixture only',
            'payment_route_verified': True,
        })

    def test_global_pause_and_unverified_sender_cannot_be_bypassed(self):
        blocks = send_blocks(self.row, self.policy, self.registry)
        self.assertIn('campaign sending is paused', blocks)
        self.assertTrue(any('sender' in b for b in blocks))
        self.assertTrue(any('tax' in b for b in blocks))

    def test_unknown_uk_entity_is_not_a_corporate_subscriber(self):
        self.make_reviewed_fixture()
        self.row['recipient_entity_type'] = 'unknown'
        self.row['legal_evidence_url'] = ''
        self.assertTrue(any('corporate' in b for b in send_blocks(self.row, self.policy, self.registry)))

    def test_purpose_restricted_mailbox_is_not_a_vendor_inbox(self):
        self.make_reviewed_fixture()
        for purpose in ('hiring-only', 'merchandise-preorders-only', 'wholesale-orders-only', 'unknown'):
            self.row['contact_purpose'] = purpose
            self.assertTrue(any('purpose' in b for b in send_blocks(self.row, self.policy, self.registry)))

    def test_excluded_country_stays_blocked_even_with_consent(self):
        self.make_reviewed_fixture()
        for country in ('US', 'CA'):
            self.row.update({'country': country, 'legal_basis': 'explicit-consent', 'consent_evidence': 'TEST only'})
            self.assertTrue(any('exclud' in b or 'suppression' in b for b in send_blocks(self.row, self.policy, self.registry)))

    def test_previous_contact_requires_separate_follow_up_approval(self):
        self.make_reviewed_fixture()
        self.row['already_contacted_at'] = '2026-10-11'
        self.assertTrue(any('previous recipient' in b for b in send_blocks(self.row, self.policy, self.registry)))
        self.assertTrue(any('previous recipient' in b for b in send_blocks(self.row, self.policy, self.registry, True)))
        self.row['follow_up_approved'] = 'yes'
        self.assertEqual(send_blocks(self.row, self.policy, self.registry, True), [])

    def test_spanish_public_email_is_not_consent(self):
        self.make_reviewed_fixture()
        self.row.update({'country': 'ES', 'legal_basis': 'corporate-subscriber'})
        self.assertTrue(send_blocks(self.row, self.policy, self.registry))
        self.row.update({'legal_basis': 'explicit-consent', 'consent_evidence': ''})
        self.assertTrue(any('consent' in b for b in send_blocks(self.row, self.policy, self.registry)))

    @unittest.skipUnless((ROOT / 'sales/EMAIL-REWRITES.json').exists(), 'Private rewrite data must be restored from Drive')
    def test_generated_letters_are_bounded_location_free_and_not_sent(self):
        data = json.loads((ROOT / 'sales/EMAIL-REWRITES.json').read_text(encoding='utf-8'))
        self.assertEqual(len(data['messages']), 25)
        for message in data['messages']:
            with self.subTest(id=message['id']):
                self.assertFalse(message['sent'])
                self.assertFalse(message['send_ready'])
                self.assertTrue(message['review_only'])
                validate_email(message['subject'], message['body'])
                expected = self.policy['packages'][message['package']]['price_eur']
                self.assertEqual(message['planned_quote_eur'], expected)
                if message['contact_purpose'] not in {'general-business', 'owner-business', 'vendor-proposals'}:
                    self.assertIsNone(message['unapproved_recipient'])
        sample = data['messages'][0]
        for forbidden in ('Homs, Syria', 'UK-based', 'no VAT', '100% legal'):
            with self.assertRaises(ValueError):
                validate_email(sample['subject'], sample['body'] + '\n' + forbidden)

    def test_site_prices_and_scope_match_policy(self):
        site = json.loads((ROOT / 'src/data/site.json').read_text(encoding='utf-8'))
        for package in site['packages']:
            expected = self.policy['packages'][package['id']]
            self.assertEqual(package['price'], expected['price_eur'])
            self.assertEqual(package['days'], expected['days'])
            self.assertEqual(package['recurring'], 0)
            if package['id'] != 'licence':
                self.assertEqual(package['languages'], 1)
        self.assertEqual([o['id'] for o in site['options']], ['care'])
        self.assertEqual(site['options'][0]['price'], 25)
        self.assertFalse(site['studio']['phone'])
        self.assertFalse(site['studio']['whatsapp'])
        self.assertEqual(site['studio']['email'], self.policy['sender']['reply_to'])

    @unittest.skipUnless((ROOT / 'sales/prospects-2026.csv').exists(), 'Private source data must be restored from Drive')
    def test_current_dataset_and_gates_have_no_excluded_markets_or_hidden_care(self):
        import csv
        with (ROOT / 'sales/prospects-2026.csv').open(newline='', encoding='utf-8') as fh:
            rows = list(csv.DictReader(fh))
        registry = load_registry()
        self.assertEqual(len(rows), 104)
        for row in rows:
            self.assertNotIn(row['country'], ('US', 'CA'))
            self.assertEqual(int(row['care_eur_per_month']), 0)
            self.assertEqual(int(row['first_year_value_eur']), int(row['quote_eur']))
            self.assertTrue(send_blocks(row, self.policy, registry))
        with (ROOT / 'sales/SENT-RECORD.csv').open(newline='', encoding='utf-8') as fh:
            self.assertEqual(list(csv.DictReader(fh)), [])


if __name__ == '__main__':
    unittest.main()
