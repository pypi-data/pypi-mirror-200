import os

from django.test import TestCase

from ipam.models import VRF

from netdoc.utils import test_prepare
from netdoc.models import Discoverable

TEST_DIRECTORY= os.path.dirname(os.path.realpath(__file__))

class QuestionModelTests(TestCase):
    def setUp(self):
        """Clean previous data and load lab-specific content."""
        test_prepare(TEST_DIRECTORY)


    def test_discoverables(self):
        discoverable_qs = Discoverable.objects.all()
        self.assertEquals(len(discoverable_qs), 2)

        sw1_discoverable_o = Discoverable.objects.get(device__name="SW1")
        sw2_discoverable_o = Discoverable.objects.get(device__name="SW2")
        self.assertEquals(sw1_discoverable_o.mode, sw2_discoverable_o.mode)
        self.assertEquals(sw1_discoverable_o.site.pk, sw2_discoverable_o.site.pk)
        self.assertEquals(sw1_discoverable_o.credential.pk, sw2_discoverable_o.credential.pk)

    def test_vrfs(self):
        vrf_qs = VRF.objects.all()
        self.assertEquals(len(vrf_qs), 3)

        blue_vrf_o = VRF.objects.get(name="blue")
        self.assertIs(blue_vrf_o.rd, None)

        management_vrf_o = VRF.objects.get(name="management")
        self.assertIs(management_vrf_o.rd, None)

        red_vrf_o = VRF.objects.get(name="red")
        self.assertIs(red_vrf_o.rd, None)
