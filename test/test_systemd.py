#!/usr/bin/env python3
import unittest
from unittest import mock
from unittest.mock import MagicMock, patch, PropertyMock

import systemd_unit

class testSystemd(unittest.TestCase):

    def setUp(self):
        systemd_unit.subprocess.check_output = MagicMock(return_value=True)
        self.unit = systemd_unit.Unit('foo')

    def testBasicCalls(self):
        self.unit.reload()
        self.unit.restart()
        self.unit.stop()
        self.unit.enable()
        self.unit.disable()

    def testRemove(self):
        with patch('os.path.exists', MagicMock(return_value=True)) as fake_path_exists, \
             patch.object(systemd_unit.Unit, 'stop') as fake_stop, \
             patch.object(systemd_unit.Unit, 'disable') as fake_disable, \
             patch('os.remove') as fake_os_remove, \
             patch.object(systemd_unit.Unit, 'reload') as fake_reload:
            self.unit.remove()
            fake_path_exists.assert_called_with(self.unit.service_file_path)
            self.assertTrue(fake_stop.called)
            self.assertTrue(fake_disable.called)
            fake_os_remove.assert_called_with(self.unit.service_file_path)
            self.assertTrue(fake_reload.called)

        with patch('os.path.exists', MagicMock(return_value=False)) as fake_path_exists, \
             patch.object(systemd_unit.Unit, 'stop') as fake_stop, \
             patch.object(systemd_unit.Unit, 'disable') as fake_disable, \
             patch('os.remove') as fake_os_remove, \
             patch.object(systemd_unit.Unit, 'reload') as fake_reload:
            self.unit.remove()
            fake_path_exists.assert_called_with(self.unit.service_file_path)
            self.assertFalse(fake_stop.called)
            self.assertFalse(fake_disable.called)
            fake_os_remove.assert_called_with(self.unit.service_file_path)
            self.assertTrue(fake_reload.called)

    def testCreateServiceFile(self):
        with patch('builtins.open', mock.mock_open(), create=True) as fake_open:
            self.unit.create_service_file()
            fake_open.assert_called_once_with(self.unit.service_file_path, 'w')

    @patch('systemd_unit.Unit.content', new_callable=PropertyMock)
    @patch.object(systemd_unit.Unit, 'create_service_file')
    def testEnsure(self, fake_create_service_file, fake_set_content):
        self.unit.ensure()
        self.assertFalse(fake_set_content.called)
        self.assertTrue(fake_create_service_file.called)

        self.unit.ensure(content='qwe')
        self.assertTrue(fake_set_content.called)
        self.assertTrue(fake_create_service_file.called)
