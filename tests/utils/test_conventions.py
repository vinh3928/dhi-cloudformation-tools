import unittest
from cfn.utils import conventions

class TestName(unittest.TestCase):

    def test_should_return_name(self):
        # inputs
        parameters = {
            'Environment': 'someEnvironment',
            'Brand': 'someBrand',
            'Application': 'someApplication',
        }
        # when
        result = conventions.generate_name(parameters)
        # assertions
        self.assertEqual(result, f"{parameters['Environment']}-{parameters['Brand']}-{parameters['Application']}")


class TestValidateParameters(unittest.TestCase):

    def test_should_return_true_with_valid_parameters(self):
        # inputs
        parameters = {
            'Environment': 'someEnvironment',
            'Brand': 'someBrand',
            'Application': 'someApplication',
            'Owner': 'someOwner'
        }
        # when
        result = conventions.validate_parameters(parameters)
        # assertions
        self.assertTrue(result)

    def test_should_return_false_with_missing_environment_in_parameters(self):
        # inputs
        parameters = {
            'Brand': 'someBrand',
            'Application': 'someApplication',
            'Owner': 'someOwner'
        }
        # when
        result = conventions.validate_parameters(parameters)
        # assertions
        self.assertFalse(result)

    def test_should_return_false_with_missing_brand_in_parameters(self):
        # inputs
        parameters = {
            'Environment': 'someEnvironment',
            'Application': 'someApplication',
            'Owner': 'someOwner'
        }
        # when
        result = conventions.validate_parameters(parameters)
        # assertions
        self.assertFalse(result)

    def test_should_return_false_with_missing_application_in_parameters(self):
        # inputs
        parameters = {
            'Environment': 'someEnvironment',
            'Brand': 'someBrand',
            'Owner': 'someOwner'
        }
        # when
        result = conventions.validate_parameters(parameters)
        # assertions
        self.assertFalse(result)

    def test_should_return_false_with_missing_owner_in_parameters(self):
        # inputs
        parameters = {
            'Environment': 'someEnvironment',
            'Brand': 'someBrand',
            'Application': 'someApplication'
        }
        # when
        result = conventions.validate_parameters(parameters)
        # assertions
        self.assertFalse(result)


class TestMergeTag(unittest.TestCase):

    def test_should_return_tag_value_if_the_value_follows_the_convention(self):
        # inputs
        tag_name = 'someTag'
        tags = {
            tag_name:'someValue'
        }
        desired_value = 'someValue'
        # when
        result = conventions.merge_tag(tags, tag_name, desired_value)
        # assertions
        # should not warn logs warning
        self.assertTrue(result)

    def test_should_return_tag_value_if_tag_not_set(self):
        # inputs
        tag_name = 'someTag'
        tags = {}
        desired_value = 'someValue'
        # when
        result = conventions.merge_tag(tags, tag_name, desired_value)
        # assertions
        # should not warn logs warning
        self.assertTrue(result)

    def test_should_return_tag_value_and_log_warning_if_value_does_not_follow_convention(self):
        # inputs
        tag_name = 'someTag'
        tags = {
            tag_name:'randomValue'
        }
        desired_value = 'someValue'
        # when
        result = conventions.merge_tag(tags, tag_name, desired_value)
        # assertions
        # should warn logs warning
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
